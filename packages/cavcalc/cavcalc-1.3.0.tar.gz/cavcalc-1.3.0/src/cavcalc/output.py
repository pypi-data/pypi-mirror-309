"""
The output objects which store the results from any call to :func:`.calculate`.
"""

import abc
import pickle
from typing import Sequence as _Sequence, Union as _Union

from . import Q_
from .errors import CavCalcError
from ._exiters import (
    bug as _bug,
    quit_print as _quit_print,
)
from .parameters import (
    ArgParameter,
    TargetParameter,
    ParameterCategory,
    ParameterType,
)


def load(file: str):
    """Load a :class:`.SingleOutput` or :class:`.MultiOutput` instance
    from a "pickled" binary file.

    Parameters
    ----------
    file : str
        The name (and path if it isn't in the current working directory)
        of the file to open.

    Returns
    -------
    output : :class:`.SingleOutput` | :class:`.MultiOutput`
        The cavcalc output instance.

    Raises
    ------
    cce : :class:`.CavCalcError`
        If the type of the loaded object is not :class:`.SingleOutput`
        or :class:`.MultiOutput`.
    """
    with open(file, "rb") as f:
        output = pickle.load(f)
        if not isinstance(output, (SingleOutput, MultiOutput)):
            raise CavCalcError(f"Unrecognised serialized object in {file}")

    return output


def _param_str_gen(params: _Sequence[_Union[ArgParameter, TargetParameter]]):
    return (f"{'' if getattr(p, 'was_used', True) else '[UNUSED] '}{p}" for p in params)


class BaseOutput(abc.ABC):
    """Abstract base class for output objects. Both :class:`.SingleOutput` and
    :class:`.MultiOutput` derive from this type."""

    category_order = (
        ParameterCategory.Frequency,
        ParameterCategory.Power,
        ParameterCategory.Distance,
        ParameterCategory.Curvature,
        ParameterCategory.BeamRadius,
        ParameterCategory.Stability,
        ParameterCategory.Phase,
        ParameterCategory.Angle,
        ParameterCategory.Wave,
    )

    def __init__(self, phys_args: tuple[ArgParameter]):
        self.__given = phys_args

    def __str__(self) -> str:
        s = "Given:\n\t"
        for category in self.category_order:
            if args := tuple(filter(lambda p: p.category == category, self.__given)):
                s += "\n\t".join(_param_str_gen(sorted(args, key=lambda a: a.ptype.value)))
                s += "\n\n\t"

        return s.strip() + "\n\n"

    @property
    def given(self) -> dict[str, ArgParameter]:
        """A dictionary of the given parameter names with their corresponding
        :class:`.ArgParameter` values."""
        return {arg_p.name: arg_p for arg_p in self.__given}

    def print(self, **kwargs):
        """Prints a string representation of the output, in an identical style to the CLI.

        Parameters
        ----------
        kwargs : Keyword Arguments
            Optional arguments to pass to Python ``print`` function.
        """
        print(str(self), **kwargs)

    def save(self, file: str):
        """Saves the output object to the specified ``file``, in a binary
        serialised Python object format (via ``pickle``).

        Parameters
        ----------
        file : str
            The file name (and path if saving to a location outside of the current
            working directory) to save this output instance to.
        """
        with open(file, "wb") as f:
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)


class SingleOutput(BaseOutput):
    """Storage and manipulation of a single target parameter computed via :func:`.calculate`."""

    def __init__(self, target: TargetParameter, phys_args: tuple[ArgParameter]):
        super().__init__(phys_args)
        self.__target = target

    def __str__(self) -> str:
        return super().__str__() + "Computed:\n\t" + "".join(_param_str_gen((self.result,)))

    @property
    def name(self):
        """A short-hand for ``out.result.name``."""
        return self.__target.name

    @property
    def result(self):
        """The result itself as a :class:`.TargetParameter` instance.

        .. hint::

            Use ``result.value`` to get the ``pint.Quantity`` object, ``result.value.m``
            to obtain the numerical value, and ``result.value.u`` to retrieve the units
            of this result.
        """
        return self.__target

    def convert(self, units: str):
        """Attempts to convert the result quantity, in-place, to the
        specified units.

        .. warning::

            This method converts the actual quantity held by this output. If you
            do not want to modify this object, then instead do::

                q = out.result.to(units)

            to get a new quantity object, ``q``, in the given units.

        Parameters
        ----------
        units : str
            The units to convert to, as a string or ``cavcalc.ureg.<units>`` object.
        """
        self.__target = TargetParameter(self.result.name, self.result.value.to(units))

    def plot(
        self,
        xlim: _Union[str, _Sequence[float]] = "auto",
        ylim: _Union[str, _Sequence[float]] = "auto",
        zlim: _Union[str, _Sequence[float]] = "auto",
        filename: str = None,
        logx: bool = False,
        logy: bool = False,
        logz: bool = False,
        cmap: str = None,
        show: bool = True,
        fig=None,
        **kwargs,
    ):
        """Plots the result against the given array-like argument dependencies (if any).

        If only one of the given arguments to the :func:`.calculate` call was array-like,
        then this will plot a standard line plot. Otherwise an image plot, via
        :func:`matplotlib.pyplot.imshow`, will be produced.

        Parameters
        ----------
        xlim : str | Iterable[float], optional; default = "auto"
            The limits of the x-axis. Defaults to ``"auto"`` such that matplotlib
            determines these automatically. This can be set to ``"data"`` so that
            the exact limits of the x-axis data are used. An iterable of length
            two can be used to manually override the x-axis limits; these will
            simply be forwarded to :func:`matplotlib.pyplot.xlim`.

        ylim : str | Iterable[float], optional; default = "auto"
            The limits of the y-axis. Defaults to ``"auto"`` such that matplotlib
            determines these automatically. This can be set to ``"data"`` so that
            the exact limits of the y-axis data are used. An iterable of length
            two can be used to manually override the y-axis limits; these will
            simply be forwarded to :func:`matplotlib.pyplot.ylim`.

        zlim : str | Iterable[float], optional; default = "auto"
            The limits of the color-bar scale for image plots. Ignored if
            this is a line plot.

        filename : str, optional; default = None
            A filename to save the figure to.

        logx : bool, optional; default = False
            Whether to use a log-scale on the x-axis. Ignored if this is an image plot.

        logy : bool, optional; default = False
            Whether to use a log-scale on the y-axis. Ignored if this is an image plot.

        logz : bool, optional; default = False
            Whether to use a log normalisation of the image plot Z data. Ignored if
            this is a line plot.

        cmap : str | :class:`matplotlib.colors.ListedColormap`, optional; default = None
            Name, or instance, of the colormap to use for image plots. If not given,
            the colormap will default to the relevant ``matplotlib.rcParams`` value.
            Ignored if this is a line plot.

        show : bool, optional; default = False
            Shows the resulting figure, via :func:`matplotlib.pyplot.show`, if true.

        fig : :class:`matplotlib.figure.Figure`, optional; default = None
            An optional pre-existing figure object to draw on. If not given, then a new
            figure is created and used.

        kwargs : Keyword arguments
            Optional keyword arguments to pass to the relevant matplotlib plot or imshow
            call(s).

        Returns
        -------
        fig : :class:`matplotlib.figure.Figure`
            The matplotlib Figure object.

        Raises
        ------
        cce : :class:`.CavCalcError`
            If the value of :attr:`.SingleOutput.result` is not array-like (i.e. no
            dependencies of the target parameter were array-like, when making the
            :func:`.calculate` call).
        """
        if not self.__target.is_array:
            _quit_print(
                f"Value of target '{self.__target.name}' is not array-like! Did "
                "you forget to set one of the dependent arguments to an array?"
            )

        given = self.given.values()
        xs = tuple(sorted(filter(lambda p: p.is_array, given), key=lambda p: (p.axis, p.index)))
        num_x_arrays = len(xs)
        if not num_x_arrays:
            _bug(
                f"Somehow none of the given args, ({', '.join(self.given.keys())}), "
                f"are array-like, but the target value, {self.__target.name}, is!"
            )

        plotting_dims = max(len(x.value.m.shape) for x in xs)
        if plotting_dims > 2:
            _quit_print(f"Cannot plot results over {plotting_dims} dimensions!")

        import matplotlib.pyplot as plt

        make_subplots = False
        if fig is None:
            fig = plt.figure()
        else:
            if fig.axes:
                plt.sca(fig.axes[0])
            else:
                make_subplots = True

        def _make_label(p: ArgParameter):
            return p.description + (f" [{p.value.units:~}]" if not p.is_unitless else "")

        # The non-array arguments specified
        if fixed := tuple(filter(lambda p: p.is_scalar and p.was_used, given)):
            fixed_params_str = "with: " + ", ".join(f"{p.symbol_str} = {p.value:~}" for p in fixed)
        else:
            fixed_params_str = ""

        if plotting_dims == 1 or num_x_arrays == 1:
            if num_x_arrays > 2:
                _quit_print("Plots with more than two x-axes are not supported.")

            if num_x_arrays == 1:
                (x,) = xs
            else:
                x, x2 = xs
            y = self.__target

            # This typically occurs when plotting a MultiOutput, where a target was computed
            # over a mesh-grid but only depended on one of the grid parameters. So here we
            # just grab the first row of the data and plot that; as all rows should be equal.
            # TODO (sjr) Might be better to do this more automatically in MultiOutput, via some
            #            reduce_grid method which gets applied to any target where above is true.
            if plotting_dims > 1:
                x = ArgParameter(x.name, Q_(x.value.m[0], x.value.units), axis=x.axis)
                y = TargetParameter(y.name, Q_(y.value.m[0], y.value.units))

            if make_subplots:
                plt.sca(fig.subplots())

            plot_func = plt.plot
            if logx and logy:
                plot_func = plt.loglog
            elif logx:
                plot_func = plt.semilogx
            elif logy:
                plot_func = plt.semilogy

            if num_x_arrays == 1:
                label = f"{y.symbol_str}({x.symbol_str}) " + fixed_params_str
            else:
                label = f"{y.symbol_str}({{{x.symbol_str}, {x2.symbol_str}}}) " + fixed_params_str

            try:
                plot_func(x.value.m.T, y.value.m.T, label=label, **kwargs)
            except Exception as ex:
                _quit_print(str(ex))

            if isinstance(xlim, str):
                if xlim.casefold() == "data":
                    plt.xlim(x.value.m.min(), x.value.m.max())
            else:
                if xlim:
                    plt.xlim(*xlim)
            if isinstance(ylim, str):
                if ylim.casefold() == "data":
                    plt.ylim(y.value.m.min(), y.value.m.max())
            else:
                if ylim:
                    plt.ylim(*ylim)

            plt.legend()

            if num_x_arrays > 1:
                ax1 = plt.gca()

                ax2 = plt.twiny()
                plot_func2 = ax2.plot
                if logx and logy:
                    plot_func2 = ax2.loglog
                elif logx:
                    plot_func2 = ax2.semilogx
                elif logy:
                    plot_func2 = ax2.semilogy

                # "Plot" it again over x2 to get the auto limits for this variable,
                # but don't actually draw it this time as it will be the same curve
                plot_func2(x2.value.m.T, y.value.m.T, alpha=0)
                ax2.set_xlabel(_make_label(x2))

                # Reset current state to first axes
                plt.sca(ax1)

        else:
            if num_x_arrays > 2:
                _quit_print("Image plots with multiple x-axes are not supported.")

            import matplotlib

            x, y = xs
            z = self.__target

            try:
                cmap = matplotlib.colormaps.get_cmap(cmap)
            except Exception as ex:
                _quit_print(str(ex))

            extent = [x.value.m.min(), x.value.m.max(), y.value.m.min(), y.value.m.max()]

            if logz:
                if not zlim or isinstance(zlim, str):
                    norm = plt.cm.colors.LogNorm()
                else:
                    vmin, vmax = zlim
                    if vmin <= 0:
                        vmin = None

                    norm = plt.cm.colors.LogNorm(vmin, vmax)
            else:
                if zlim and not isinstance(zlim, str):
                    norm = plt.cm.colors.Normalize(*zlim)
                else:
                    norm = None

            title = f"{z.symbol_str}({x.symbol_str}, {y.symbol_str}) " + fixed_params_str

            shape = z.value.m.shape
            if len(shape) == 2:
                if make_subplots:
                    plt.sca(fig.subplots())

                try:
                    surf = plt.imshow(
                        z.value.m.T,
                        cmap=cmap,
                        extent=extent,
                        norm=norm,
                        origin="lower",
                        aspect="auto",
                        **kwargs,
                    )
                except Exception as ex:
                    _quit_print(str(ex))

                plt.colorbar(surf, label=_make_label(z), fraction=0.046, pad=0.04)
                plt.title(title)

            elif len(shape) == 3:
                n_dual, N1, N2 = shape
                if n_dual != 2:
                    _bug(
                        f"The shape of target '{z.name}' should be (2, {N1}, {N2}) "
                        f"but got a shape of {shape} instead!"
                    )

                ax1 = fig.add_subplot(121)
                ax2 = fig.add_subplot(122)
                plt.sca(ax1)

                z1, z2 = z.value.m
                try:
                    surf1 = ax1.imshow(
                        z1.T,
                        cmap=cmap,
                        extent=extent,
                        norm=norm,
                        origin="lower",
                        aspect="auto",
                        **kwargs,
                    )
                except Exception as ex:
                    _quit_print(str(ex))

                plt.colorbar(surf1, ax=ax1, label=_make_label(z), fraction=0.09, pad=0.04)

                ax1.set_xlabel(_make_label(x))
                ax1.set_ylabel(_make_label(y))
                ax1.set_title(title)

                plt.sca(ax2)
                surf2 = ax2.imshow(
                    z2.T,
                    cmap=cmap,
                    extent=extent,
                    norm=norm,
                    origin="lower",
                    aspect="auto",
                    **kwargs,
                )

                plt.colorbar(surf2, ax=ax2, label=_make_label(z), fraction=0.09, pad=0.04)

                ax2.set_title(title)

                fig.tight_layout()

            else:
                _bug(
                    f"Dimensions, {shape}, of target '{z.name}' are incompatible "
                    "with image plotting!"
                )

        plt.xlabel(_make_label(x))
        plt.ylabel(_make_label(y))

        if filename:
            fig.savefig(filename)

        if show:
            plt.show()

        return fig


class MultiOutput(BaseOutput):
    """Storage and manipulation of multiple target parameters computed via :func:`.calculate`.

    Use :meth:`.MultiOutput.as_singles` to easily construct :class:`.SingleOutput` instances
    from a multi-output object.
    """

    def __init__(
        self, targets: dict[TargetParameter, tuple[ParameterType]], phys_args: tuple[ArgParameter]
    ):
        super().__init__(phys_args)
        self.__targets = targets

    def __getitem__(self, key: _Union[str, ParameterType, ParameterCategory]):
        if isinstance(key, str):
            try:
                return next((tgt_p for tgt_p in self.__targets if tgt_p.name == key))
            except StopIteration:
                raise CavCalcError(f"No target of name '{key}' exists in the output.")

        if isinstance(key, ParameterType):
            try:
                return next((tgt_p for tgt_p in self.__targets if tgt_p.ptype == key))
            except StopIteration:
                raise CavCalcError(f"No target of parameter type '{key}' exists in the output.")

        if isinstance(key, ParameterCategory):
            targets = tuple(filter(lambda t: t.category == key, self.__targets))
            if not targets:
                raise CavCalcError(f"No targets of parameter category '{key}' exist in the output.")

            return targets

        raise TypeError(
            f"Expected key-type of str, ParameterType or ParameterCategory, but got {type(key)}"
        )

    def __str__(self) -> str:
        s = "Computed:\n\t"
        for category in self.category_order:
            if targets := self.get(category):
                s += "\n\t".join(_param_str_gen(sorted(targets, key=lambda t: t.ptype.value)))
                s += "\n\n\t"

        return super().__str__() + s.strip()

    @property
    def results(self):
        """A dictionary of results, mapping the names of the target parameters to their values (as
        ``pint.Quantity`` instances)."""
        return {tgt_p.name: tgt_p for tgt_p in self.__targets}

    def as_single(self, ptype: _Union[str, ParameterType]) -> SingleOutput:
        """A :class:`.SingleOutput` instance constructed, from this multi-output,
        for a single desired parameter type.

        Parameters
        ----------
        ptype : str | :class:`.ParameterType`
            The parameter type.

        Returns
        -------
        single : :class:`.SingleOutput`
            The single output object for the desired parameter type.
        """
        singles = self.as_singles(ptype)
        return tuple(singles.values())[0]

    def as_singles(self, *args) -> dict[ParameterType, SingleOutput]:
        """A dictionary of :class:`.SingleOutput` instances, for given
        :class:`.ParameterType` objects, constructed from this multi-output.

        To retrieve single output objects for all target parameters in
        this multi-output, simply give no args when calling this method.

        Parameters
        ----------
        args : tuple[str | :class:`.ParameterType`]
            Parameter names or types as positional arguments. These will form the
            keys of the returned dictionary. If none are given then all target
            parameter types are used.

        Returns
        -------
        singles : dict[str | :class:`.ParameterType`, :class:`.SingleOutput`]
            The single outputs constructed for each desired parameter.
        """
        if not args:
            args = tuple(tgt_p.ptype for tgt_p in self.__targets)

        singles = {}
        for arg in args:
            if not isinstance(arg, (str, ParameterType)):
                raise CavCalcError(
                    "All arguments to as_singles must be strings or ParameterType instances."
                )

            target = next(
                (tgt_p for tgt_p in self.__targets if (tgt_p.ptype == arg or tgt_p.name == arg)),
                None,
            )
            if target is None:
                raise CavCalcError(f"No target of type '{arg}' in the output.")

            func_params = self.__targets.get(target)
            if not func_params:
                _bug(f"No function parameters for target parameter of type '{arg}'")

            phys_args = tuple(arg_p for arg_p in self.given.values() if arg_p.ptype in func_params)
            singles[arg] = SingleOutput(target, phys_args)

        return singles

    def get(self, key: _Union[str, ParameterType, ParameterCategory], default=None):
        """Retrieve a target result, or a collection of these, using a suitable key.

        If ``key`` is a string or a :class:`.ParameterType` then the corresponding target parameter
        will be returned if it exists, ``default`` is returned otherwise.

        Alternatively, ``key`` can be a :class:`.ParameterCategory`. In this case all the target
        parameters belonging to this category will be returned, or ``default`` if no targets of
        this category are present in the output.

        Parameters
        ----------
        key : str | :class:`.ParameterType` | :class:`.ParameterCategory`
            The key of the target(s) to retrieve. See above for options.

        default : Any | NoneType, optional
            The default value to return if no target(s) corresponding to ``key`` could be found.

        Returns
        -------
        target : :class:`.TargetParameter` | tuple[:class:`.TargetParameter`] | Any
            The target, or tuple of targets if ``key`` was a :class:`.ParameterCategory`, or ``default``
            if no target(s) could be obtained from the given ``key``.
        """
        try:
            return self[key]
        except CavCalcError:
            return default

    def plot(self, filename: str = None, show: bool = True, **kwargs):
        """Plots all the outputs which have array-like target parameters.

        See :meth:`.SingleOutput.plot` for plotting options, the ``**kwargs`` here
        will be forwarded to this method for each target parameter.

        Parameters
        ----------
        show : bool, optional; default = False
            Shows the resulting figure, via :func:`matplotlib.pyplot.show`, if true.

        Returns
        -------
        figures : dict[:class:`.ParameterType`, :class:`matplotlib.figure.Figure`]
            A dictionary of the parameter types mapping to their respective figure objects.
        """
        import matplotlib.pyplot as plt

        singles = self.as_singles(*(tgt_p.ptype for tgt_p in self.__targets if tgt_p.is_array))
        figures = {}
        for ptype, out in singles.items():
            if filename:
                try:
                    filename_single, ext = filename.split(".")
                except ValueError:
                    filename_single = filename
                    ext = ""

                filename_single = f"{filename_single}_{out.name}" + (f".{ext}" if ext else ext)
            else:
                filename_single = None

            fig = out.plot(filename=filename_single, show=False, **kwargs)
            figures[ptype] = fig

        if show and figures:
            plt.show()

        return figures
