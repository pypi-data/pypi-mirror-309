import gymnasium
import numpy as np


def initialize(base_class, arg, default_class, default_args):
    if arg is None:
        return default_class(**default_args)
    if isinstance(arg, type):
        raise Exception("Need initialization value")
    elif isinstance(arg, base_class):
        return arg
    elif type(arg) is str:
        raise Exception("Deprecated in version 3.0.0")
    elif type(arg) is dict:
        default_args.update(arg)
        return default_class(**default_args)


def state_dict_to_state_array(state_dict, state_array, state_names):
    """
    Mapping of a passed state dictionary to a fitting state array.

    This function is mainly used in the initialization phase to map a dictionary of passed state_name, state_value pairs
    to a numpy state array with the entries of the state_dict at the corresponding places of the state_names.

    Args:
        state_dict(dict): Dictionary containing pairs of state_name, state_values for the state_array
        state_array(iterable): Array into which the state_dict entries shall be passed
        state_names(list/ndarray(str)): List of the state names.
    """
    state_dict = dict((key.lower(), v) for key, v in state_dict.items())
    assert all(key in state_names for key in state_dict.keys()), f"A state name in {state_dict.keys()} is invalid."
    for ind, key in enumerate(state_names):
        try:
            state_array[ind] = state_dict[key]
        except KeyError:  # TODO
            pass


def set_state_array(input_values, state_names):
    """
    Setting of the input values to a valid state array with the shape of the physical systems state.

    The input values can be passed as dict with state_name: value pairs or as list  / ndarray. In the latter case the
    shape of the list has to fit the state_names shape and the list will just be returned as array. If a float is
    passed as input value, then this value will be set onto all positions of the state array equally.

    Args:
        input_values(dict(float) / list(float) / ndarray(float) / float): Values to be set onto the state array.
        state_names(list(str)): List containing the state names of the physical system.

    Returns:
        An initialized state array with all values passed in input values set onto the corresponding position in
        the state_names and zero otherwise.
    """

    if isinstance(input_values, dict):
        state_array = np.zeros_like(state_names, dtype=float)
        state_dict_to_state_array(input_values, state_array, state_names)
    elif isinstance(input_values, np.ndarray):
        assert len(input_values) == len(state_names)
        state_array = input_values
    elif isinstance(input_values, list):
        assert len(input_values) == len(state_names)
        state_array = np.array(input_values)
    elif isinstance(input_values, float) or isinstance(input_values, int):
        state_array = input_values * np.ones_like(state_names, dtype=float)
    else:
        raise Exception("Incorrect type for the input values.")
    return state_array


def update_parameter_dict(source_dict, update_dict, copy=True):
    """Merges two dictionaries (source and update) together.

    It is similar to pythons dict.update() method. Furthermore, it assures that all keys in the update dictionary are
    already present in the source dictionary. Otherwise a KeyError is thrown.

    Arguments:
          source_dict(dict): Source dictionary to be updated.
          update_dict(dict): The new dictionary with the entries to update the source dict.
          copy(bool): Flag, if the source dictionary shall be copied before updating. (Default True)
    Returns:
        dict: The updated source dictionary.
    Exceptions:
        KeyError: Thrown, if a key in the update dict is not available in the source dict.
    """
    source_keys = source_dict.keys()
    for key in update_dict.keys():
        if key not in source_keys:
            raise KeyError(f'Cannot update_dict the source_dict. The key "{key}" is not available.')
    new_dict = source_dict.copy() if copy else source_dict
    new_dict.update(update_dict)
    return new_dict


#: Short notation for the gymnasium.make call to avoid the necessary import of gym when making environments.
# make = gymnasium.make
