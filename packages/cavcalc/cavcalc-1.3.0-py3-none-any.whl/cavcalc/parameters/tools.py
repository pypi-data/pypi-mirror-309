"""
Functions for retrieving information on parameters, typically provided via
both str and :class:`.ParameterType` arguments.
"""

from collections import defaultdict
from typing import Union as _Union

from . import ParameterType, ParameterCategory
from ._maps import (
    NAME_PTYPE_MAP as _NAME_PTYPE_MAP,
    PTYPE_NAME_MAP as _PTYPE_NAME_MAP,
    PTYPE_DESCR_MAP as _PTYPE_DESCR_MAP,
    PTYPE_CATEGORY_MAP as _PTYPE_CAT_MAP,
)

from ..errors import CavCalcError


def get_default_units(ptype: _Union[str, ParameterType]):
    """Get the default units, as a string, of the given parameter type.

    The default units value is obtained from the loaded config file(s); i.e.
    the first instance of the corresponding option in the load order: current
    working directory -> user config directory -> package install location.

    Parameters
    ----------
    ptype : str | :class:`.ParameterType`
        The name (as it appears in the config file for example), or :class:`.ParameterType`,
        of the parameter.

    Returns
    -------
    units : Optional[str]
        A string representing the units for the given parameter, or ``None``, if ``ptype``
        does not correspond to any valid option in any of the loaded config files.
    """
    from .. import _CONFIG

    if isinstance(ptype, ParameterType):
        ptype = _PTYPE_NAME_MAP[ptype]

    return _CONFIG["units"].get(ptype)


def get_name(ptype: ParameterType):
    """Obtain the name of a parameter from the :class:`.ParameterType` literal.

    Parameters
    ----------
    ptype : :class:`.ParameterType`
        The parameter type.

    Returns
    -------
    name : Optional[str]
        The name of the parameter, or ``None`` if ``ptype`` does not correspond to
        any parameter.
    """
    return _PTYPE_NAME_MAP.get(ptype)


def get_names(*args) -> tuple[str]:
    """Retrieve a tuple of the names of all the parameters exposed by cavcalc, or
    all the parameters in the categories given in ``args``.

    Parameters
    ----------
    args : Sequence[:class:`.ParameterCategory`]
        A sequence of :class:`.ParameterCategory` literals from which
        to obtain parameter names. If none given, then all parameter
        names will be returned.

    Returns
    -------
    names : tuple[str]
        The names of the parameters.
    """
    if not args:
        return tuple(_NAME_PTYPE_MAP.keys())

    if not all(isinstance(arg, ParameterCategory) for arg in args):
        raise CavCalcError("All args must be of type ParameterCategory.")

    cat_to_types = defaultdict(set)
    for ptype, cat in _PTYPE_CAT_MAP.items():
        cat_to_types[cat].add(ptype)

    ptypes = set()
    for arg in args:
        ptypes.update(cat_to_types[arg])

    return tuple(get_name(ptype) for ptype in ptypes)


def get_names_descriptions() -> dict[str, str]:
    """Get a dictionary of all the parameter names with a description of each of these.

    Returns
    -------
    details : dict[str, str]
        The names of all the parameters (keys), with their descriptions (values).
    """
    return {get_name(ptype): descr for ptype, descr in _PTYPE_DESCR_MAP.items()}


def get_type(name: str):
    """Get the :class:`.ParameterType` literal corresponding to the
    given name of the parameter.

    Parameters
    ----------
    name : str
        The name of the parameter.

    Returns
    -------
    ptype : Optional[:class:`.ParameterType`]
        The parameter type of the parameter, or ``None`` if ``name`` does not
        correspond to any parameter.
    """
    return _NAME_PTYPE_MAP.get(name)


# TODO (sjr) Get rid of below eventually, as should be able to specify any
#            parameter as an arg or target


def get_valid_arguments():
    """Get the names of all the parameters which can be used as arguments
    in a :func:`.calculate` / CLI call.

    Returns
    -------
    names : tuple[str]
        The valid argument parameter names.
    """
    non_arg_ptypes = (
        ParameterType.FINESSE,
        ParameterType.FSR,
        ParameterType.FWHM,
        ParameterType.MODESEP,
        ParameterType.POLE,
        ParameterType.RES_ENHANCE_INTERNAL,
        ParameterType.RES_ENHANCE_EXTERNAL,
        ParameterType.TRANSMISSION_INTENSITY_FRAC,
        ParameterType.WAISTPOS,
        ParameterType.WAISTSIZE,
    )
    return tuple(name for name in get_names() if get_type(name) not in non_arg_ptypes)


def get_valid_targets():
    """Get the names of all the parameters which can be specified as targets
    in a :func:`.calculate` / CLI call.

    Returns
    -------
    names : tuple[str]
        The valid target parameter names.
    """
    non_tgt_ptypes = (
        ParameterType.CAV_LENGTH,
        ParameterType.LOSS_M1,
        ParameterType.LOSS_M2,
    )
    return tuple(name for name in get_names() if get_type(name) not in non_tgt_ptypes)
