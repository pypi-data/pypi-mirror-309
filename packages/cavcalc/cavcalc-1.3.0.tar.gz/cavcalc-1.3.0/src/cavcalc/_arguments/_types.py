"""Functions to convert strings, passed as CLI arguments, to
appropriate quantities for these argument types."""

import numpy as np
import os
from pint.errors import UndefinedUnitError

from ._utils import _ReferencedQuantity
from .. import Q_, ureg
from .._exiters import quit_print
from ..parameters import valid_arguments


def _parse_data_range(*args):
    nargs = len(args)
    if nargs < 3 or nargs > 4:
        quit_print(
            f'Expected data range in format "<start> <stop> <num> [<units>]" ' f"but got: {args}"
        )

    if nargs == 3:
        start, stop, num = args
        units = ""
    else:
        start, stop, num, units = args

    for x in start, stop, num:
        xc = x.casefold()
        if "inf" in xc:
            quit_print("Encountered 'inf' in a data range. Values must be real and finite.")
        if "nan" in xc:
            quit_print("Encountered 'NaN' in a data range. Values must be real and finite.")

    try:
        start = float(start)
    except ValueError:
        quit_print(
            f"Could not convert data range start value '{start}' to a floating point number."
        )

    try:
        stop = float(stop)
    except ValueError:
        quit_print(f"Could not convert data range stop value '{stop}' to a floating point number.")

    try:
        num = int(num)
    except ValueError:
        quit_print(f"Could not convert data range num value '{num}' to an integer.")

    if num <= 0:
        quit_print(f"Number of points in data range must be a positive integer.")

    try:
        return Q_(np.linspace(start, stop, num), units)
    except UndefinedUnitError as ex:
        quit_print(str(ex))


def _parse_file(filename: str, units: str = None):
    try:
        if filename.casefold().endswith(".npy"):
            data = np.load(filename)
        else:  # load from text/csv file
            data = np.loadtxt(filename)
    except Exception as ex:
        quit_print(f"Unable to load file {filename}, error message: {ex}")

    if not np.issubdtype(data.dtype, np.number) or np.issubdtype(data.dtype, np.complex128):
        quit_print(f"Invalid data-type for parameter, expected real-valued numbers only.")

    return Q_(data, units)


def float_file_range_t(string: str):
    string = string.strip()

    # First check if it's a reference to another parameter...
    if string in valid_arguments:
        return _ReferencedQuantity(string)

    possible_file = True
    args = string.split()
    if (n_args := len(args)) > 1:
        if n_args > 2:  # ... parse range syntax into a linearly spaced array
            return _parse_data_range(*args)

        value, units = args
        try:
            ureg.Unit(units)
        except (UndefinedUnitError, ValueError) as ex:
            quit_print(f"Parsing units: {units}. " + str(ex))

        if os.path.isfile(value):
            return _parse_file(value, units)

        # if no file was specified then concatenate the value and
        # units into one string for easy conversion into Quantity
        string = value + units
        possible_file = False

    if possible_file and os.path.isfile(string):
        return _parse_file(string)

    try:
        return Q_(string)
    except UndefinedUnitError as ex:
        quit_print(str(ex))


def mesh_t(string: str):
    string = string.strip()

    if string.casefold() == "true":
        return True

    if string.casefold() == "false":
        return tuple()

    mesh_gen = (param_combo.split(",") for param_combo in string.split(";"))
    meshes = []
    params = []
    for param_combo in mesh_gen:
        if not param_combo or all(not s for s in param_combo):
            continue

        pnames = tuple(pname.strip() for pname in param_combo)
        for pname in pnames:
            if (num_occ := pnames.count(pname)) > 1:
                quit_print(
                    f"Parameter '{pname}' was given {num_occ} times in the mesh "
                    f"combination '{param_combo}'."
                )
            if pname in params:
                quit_print(
                    f"Parameter '{pname}' was already specified in a previous mesh "
                    "combination! Repeated parameter meshes are not currently supported."
                )
            params.append(pname)

        meshes.append(pnames)

    return tuple(meshes)


def limits_t(string: str):
    string = string.strip()

    if string.casefold() == "data":
        return string

    try:
        lo_s, hi_s = string.split()
    except ValueError:
        quit_print('Expected limits specified as "<low> <high>".')

    try:
        lo = None if lo_s == "None" else float(lo_s)
    except ValueError:
        quit_print(f"Lower limit: {lo_s} must be convertible to a number, or None.")

    try:
        hi = None if hi_s == "None" else float(hi_s)
    except ValueError:
        quit_print(f"Upper limit: {hi_s} must be convertible to a number, or None.")

    return lo, hi


def options_t(string: str):
    opts = string.strip().split(",")
    if any(":" not in x for x in opts):
        quit_print('Expected options argument in format "key1: value1, key2: value2"')

    return dict(map(lambda s: s.split(":"), map(lambda s: s.replace(" ", ""), opts)))
