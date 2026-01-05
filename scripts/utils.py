"""
Utility functions for foraging data analysis.

These functions are used across multiple notebooks for data processing
and visualization of foraging behavior data.
"""

import numpy as np


def add_to_nxt_idx(lst):
    """
    Calculate cumulative sums that handle session resets.

    Given total time counts over a session as a list,
    if the next index is less than the current one,
    add the two and replace the next index.

    Parameters
    ----------
    lst : list
        List of values (typically times or counts)

    Returns
    -------
    list
        Cumulative values handling resets
    """
    max_so_far = lst[0]
    new_lst = []
    for x in lst:
        if x >= max_so_far:
            new_lst.append(x)
            max_so_far = x
        elif x < max_so_far:
            y = max_so_far + x
            new_lst.append(y)
            max_so_far = y
    return new_lst


def get_prt(lst):
    """
    Extract patch residence times from time series.

    Parameters
    ----------
    lst : list
        List of cumulative times

    Returns
    -------
    list
        List of time spent in each patch
    """
    max_so_far = lst[0]
    new_lst = []
    for x in lst:
        if x >= max_so_far:
            max_so_far = x
        elif x < max_so_far:
            new_lst.append(max_so_far)
            max_so_far = x
    new_lst.append(lst[-1])
    return new_lst


def split_lst_if_less_than(lst):
    """
    Split list into sublists when values decrease.

    Used to separate blocks/patches in foraging data.

    Parameters
    ----------
    lst : list
        List of values (typically patch numbers)

    Returns
    -------
    list of lists
        Sublists split at decreasing values
    """
    curr = lst[0]
    temp = []
    res = []
    for ele in lst:
        if ele < curr:
            res.append(temp)
            curr = ele
            temp = []
        else:
            curr = ele
        temp.append(ele)
    res.append(temp)
    return res


def get_ind_patch_times(lst):
    """
    Get individual patch times (alias for add_to_nxt_idx).

    Parameters
    ----------
    lst : list
        List of time values

    Returns
    -------
    list
        Processed time values
    """
    return add_to_nxt_idx(lst)


def create_bct_trials(lst):
    """
    Split berry count list into trials based on 0.0 separators.

    Parameters
    ----------
    lst : list
        List of berry counts with 0.0 indicating trial boundaries

    Returns
    -------
    list of lists
        Berry counts separated by trial
    """
    size = len(lst)
    idx_list = [idx + 1 for idx, val in enumerate(lst) if val == 0.0]
    res = [
        lst[i:j]
        for i, j in zip(
            [0] + idx_list,
            idx_list + ([size] if idx_list[-1] != size else [])
        )
    ]
    return res


def rmv_last_bush(list1):
    """
    Remove last list if it doesn't end with 0 (incomplete patch).

    Parameters
    ----------
    list1 : list of lists
        List of trial data

    Returns
    -------
    list of lists
        Cleaned list with incomplete patches removed
    """
    for idx, lst in enumerate(list1):
        if lst[-1] != 0:
            list1.pop(idx)
    return list1


def flatten(t):
    """
    Flatten a list of lists into a single list.

    Parameters
    ----------
    t : list of lists
        Nested list structure

    Returns
    -------
    list
        Flattened list
    """
    return [item for sublist in t for item in sublist]
