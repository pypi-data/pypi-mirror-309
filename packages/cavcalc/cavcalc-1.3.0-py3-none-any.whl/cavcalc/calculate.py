"""
A module holding the primary function for interacting with ``cavcalc``
via the API.
"""

import numpy as np
import os as _os
from tempfile import NamedTemporaryFile as _NTF
from typing import Union as _Union, Sequence as _Sequence

from . import _SESSION, Q_
from .errors import CavCalcError
from ._handler import make_handler as _make_handler
from .parameters import ArgParameter, Parameter, ParameterType, valid_arguments, valid_targets
from .parameters.tools import get_name


def calculate(
    target: _Union[str, ParameterType] = None,
    meshes: _Union[bool, str, _Sequence[_Union[str, _Sequence[str]]]] = None,
    **kwargs,
):
    """Calculates a target parameter from an arbitrary number of physical arguments.

    If no `target` is specified then the default behaviour is to calculate all computable
    parameters from the given arguments.

    .. dropdown:: Valid targets and keyword arguments
        :icon: info
        :color: primary
        :animate: fade-in-slide-down

        You can also refer to the :ref:`param_ref` for a convenient overview of
        the information below.

        .. rubric:: Targets

        .. jupyter-execute::
            :hide-code:

            import cavcalc.parameters as ccp
            import pandas as pd

            table_styles = [
                {'selector': "th.col_heading", "props": 'text-align: center'},
                {"selector": "td", "props": "padding: 10px; text-align: center"},
                {
                    "selector": "th",
                    "props": "padding-left: 60px; padding-right: 60px; background-color: grey; text-align: center"
                },
                {"selector": "tr", "props": "border: solid; border-width: 0.5px 0"},
            ]

            pd.DataFrame(
                [
                    (p.name, p.description) for p in sorted(
                        (ccp.TargetParameter(name) for name in ccp.valid_targets),
                        key=lambda p: (p.category.value, p.ptype.value)
                    )
                ],
                columns=["Target", "Description"]
            ).style.hide().set_table_styles(table_styles)

        .. rubric:: Keyword arguments

        .. jupyter-execute::
            :hide-code:

            pd.DataFrame(
                [
                    (p.name, p.description) for p in sorted(
                        (ccp.ArgParameter(name) for name in ccp.valid_arguments),
                        key=lambda p: (p.category.value, p.ptype.value)
                    )
                ],
                columns=["Argument", "Description"]
            ).style.hide().set_table_styles(table_styles)

        Each kwarg value can be specified as:

        * A single value, or an array of values. The units of this value will correspond to
          those of the associated parameter, or parameter category, in the config file being used.
        * A ``cavcalc.ureg.Quantity`` instance. See the Pint documentation for details on
          instantiating ``Quantity`` objects.
        * A :class:`.Parameter` object: i.e. an entry from an existing :class:`.BaseOutput` instance.
        * Or any value which can be converted into a ``Quantity`` instance; e.g. a string
          (such as ``"10cm"``) or a tuple (such as ``(310, "deg")``).

    Parameters
    ----------
    target : str | :class:`.ParameterType`, optional
        The target parameter to compute, can be specified as a string (see drop-down box above) or
        a constant of the enum :class:`.ParameterType`. Defaults to ``None`` so that the function
        computes all the parameters it can from the given inputs.

    meshes : str | bool | Sequence[str | Sequence[str]], optional
        Parameter combinations from which to construct mesh-grids. This argument can given in
        a number of different ways, e.g:

        * `meshes=True`: constructs mesh-grids from the array-like arguments in the order in which
          they are given to this function.
        * `meshes="g1,g2"`: makes mesh-grids from arguments `g1` and `g2`, respectively.
        * `meshes=["g1,g2", "R1,R2"]`: makes mesh-grids from `g1` and `g2`, respectively, and also
          makes mesh-grids from `R1` and `R2`, respectively.
        * `meshes=("L, R1, R2")`: makes mesh-grids from `L1`, `R1` and `R2`, respectively.

    **kwargs : Keyword Arguments
        See the drop-down box above for details.

    Returns
    -------
    out : :class:`.SingleOutput` | :class:`.MultiOutput`
        An output object containing the results; with methods for accessing, displaying, and plotting them. If
        a ``target`` was given, and was not ``None``, then this object will be a :class:`.SingleOutput` instance,
        otherwise it will be a :class:`.MultiOutput` object.

    Examples
    --------
    The following imports are used for the below examples:

    .. jupyter-execute::
        :hide-output:

        import cavcalc as cc
        import numpy as np

        # This configures the matplotlib rcParams for the session
        # to use the style-sheet provided by cavcalc
        cc.configure("cavcalc")

    .. jupyter-execute::
        :hide-code:
        :hide-output:

        import matplotlib.pyplot as plt
        plt.rcParams["figure.figsize"] = [12, 7.416]
        plt.rcParams["font.size"] = 13

    Compute and show all determined properties from the cavity length and round-trip Gouy phase:

    .. jupyter-execute::

        print(cc.calculate(L=1, gouy=300))

    Calculate, and plot, the beam radii on the cavity mirrors over a range of radii of curvature:

    .. jupyter-execute::

        cc.calculate("w", L="4km", Rc=np.linspace(2.1e3, 2.5e3, 300)).plot();

    Make an image plot of the round-trip Gouy phase calculated on a grid over the stability
    factors of the cavity mirrors:

    .. jupyter-execute::

        g_arr = np.linspace(-2, 2, 399)
        # Setting meshes=True here will construct mesh-grids from all array
        # parameters in the order that they are specified
        cc.calculate("gouy", meshes=True, g1=g_arr, g2=g_arr).plot(cmap="Spectral_r");

    Get the radius of curvature of the cavity mirrors given the beam radii on them:

    .. jupyter-execute::

        out = cc.calculate(L="3cm", w1="100um", w2="120um")

        # .value is the pint.Quantity object
        print(f"Rc1 = {out.get('Rc1').value.to('mm'):~}")
        print(f"Rc2 = {out.get('Rc2').value.to('mm'):~}")

    Compute the fractional transmission intensity over a grid of the mirror reflectivities:

    .. jupyter-execute::

        cc.calculate("Atrn", R1=np.linspace(0, 1, 250), R2="R1", meshes=True).plot(cmap="hot");

    Plot the radius of the beam at the waist position, as a function of the beam radii
    on the mirrors; whilst using :func:`.configure` to temporarily override the default
    units (loaded from the config files) for beam-size type parameters:

    .. jupyter-execute::

        w_arr = np.linspace(80, 150, 499)
        with cc.configure(beamsizes="um"):
            fig = cc.calculate("w0", L="3cm", meshes=True, w1=w_arr, w2=w_arr).plot(show=False)
            fig.subplots_adjust(wspace=0.25)
    """
    if target is not None:
        if not isinstance(target, ParameterType):
            if target not in valid_targets:
                raise CavCalcError(f"Unrecognised / invalid target '{target}'")
        else:
            target = get_name(target)
            if target not in valid_targets:
                raise CavCalcError(f"Invalid target '{target}'")
    else:
        target = "all"

    tmp_files = []
    command = [target]
    for arg, value in kwargs.items():
        if arg not in valid_arguments:
            raise CavCalcError(f"Unrecognised / invalid argument '{arg}'")

        if isinstance(value, str) and value in valid_arguments:  # parameter reference
            command.extend([f"-{arg}", value])
            continue

        if isinstance(value, Parameter):
            value = value.value
        elif isinstance(value, tuple):
            if len(value) != 2:
                raise CavCalcError(f"Expected tuple of length 2 for argument '{arg}'")
            value = Q_(*value)
        else:
            value = Q_(value)

        arg_param = ArgParameter(arg, value)

        command.append(arg_param.cli_form)
        units_str = str(arg_param.value.units)
        if arg_param.is_array:
            # If the array is irregularly spaced, then we need to save it to a
            # tmp file for loading later on in the parser (as the data-range
            # syntax only allows for linearly spaced array args).
            if np.any(np.abs(np.diff(arg_param.value.m, n=2)) > 1e-13):
                with _NTF(suffix=".npy", delete=False) as f:
                    np.save(f, arg_param.value.m)
                    command.append(f"{f.name} {arg_param.value.u}")
                    tmp_files.append(f.name)
            else:
                start = np.min(arg_param.value.m)
                stop = np.max(arg_param.value.m)
                size = arg_param.value.m.size

                command.append(f"{start} {stop} {size} {units_str}")
        else:
            command.append(f"({arg_param.value.m}){units_str}")

    if meshes:
        command.append("--mesh")
        command.append(_deduce_meshes(meshes))

    out = _make_handler(_SESSION.parse_args(command)).run()

    for tmp_f in tmp_files:
        if _os.path.isfile(tmp_f):
            _os.remove(tmp_f)

    return out


def _deduce_meshes(meshes):
    if isinstance(meshes, (str, bool)):
        return str(meshes)

    err_msg = "Could not deduce mesh parameters from specified meshes argument."
    if not hasattr(meshes, "__getitem__"):
        raise CavCalcError(err_msg + " Expected this argument to be iterable.")

    if all((isinstance(m, str) and "," not in m) for m in meshes):
        return ",".join(meshes)

    mesh_str = ""
    for m in meshes:
        if isinstance(m, str):
            if "," not in m:
                raise CavCalcError(
                    err_msg + " Either all strings in this sequence must correspond to "
                    "single parameter names, or each string must represent a combination "
                    "of parameters separated by commas."
                )

            mesh_str += m
        else:
            if not hasattr(m, "__getitem__"):
                raise CavCalcError(
                    err_msg + " Expected each item in this sequence to be a string of "
                    "parameter name combinations separated by commas, or an iterable "
                    "of parameter names."
                )

            mesh_str += ",".join(m)

        mesh_str += ";"

    return mesh_str
