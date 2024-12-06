import pandas as pd
import numpy as np
from otpsy import mathematics


def threshold_iqr(
    df: pd.DataFrame,
    column_to_test: str,
    distance: float | int
) -> float:
    """ IQR outlier method

    This function allow the user to have the low threshold
    and the high threshold with the "IQR" outliers method
    with a specific distance.

    Parameters
    ------------
        df: pd.DataFrame
            The dataframe used
        column_to_test: str | list | int | pd.Series
            The name of the colum of interest
        distance: float | int
            The distance used to calculate threshold
    """
    # calculate the interquartile range and the median
    ret = {}
    for column in column_to_test:
        q1, q3 = df[column].quantile([0.25, 0.75])
        iqr = q3-q1

        med = np.nanmedian(df[column])

        # threshold
        low_threshold = round(med - (distance * iqr), 3)
        high_threshold = round(med + (distance * iqr), 3)

        ret[column] = (low_threshold, high_threshold)

    # avoid having a dictionnary for one column
    if len(column_to_test) == 1:
        return ret[column_to_test[0]][0], ret[column_to_test[0]][1]
    else:
        return ret


def threshold_sd(
    df: pd.DataFrame,
    column_to_test: str,
    distance: float | int
) -> float:
    """ SD outlier method

    This function allow the user to have the low threshold
    and the high threshold with the "SD" outliers method
    with a specific distance.

    Parameters
    ------------
        df: pd.DataFrame
            The dataframe used
        column_to_test: str | list | int | pd.Series
            The name of the colum of interest
        distance: float | int
            The distance used to calculate threshold
    """
    # calculate the interquartile range and the median
    ret = {}
    for column in column_to_test:
        sd = np.nanstd(df[column])
        # Pareil que IQR
        moy = np.nanmean(df[column])
        # définition des bornes
        low_threshold = round(moy - distance * sd, 3)
        high_threshold = round(moy + distance * sd, 3)

        ret[column] = (low_threshold, high_threshold)

    # avoid having a dictionnary for one column
    if len(column_to_test) == 1:
        return ret[column_to_test[0]][0], ret[column_to_test[0]][1]
    else:
        return ret


def threshold_mad(
    df: pd.DataFrame,
    column_to_test: str,
    distance: float | int,
    b: float | int
) -> float:
    """ MAD detection method

    This function allow the user to have the low threshold
    and the high threshold with the "MAD" outliers method
    with a specific distance.

    Parameters
    ------------
        df: pd.DataFrame
            The dataframe used
        column_to_test: str | list | int | pd.Series
            The name of the colum of interest
        distance: float | int
            The distance used to calculate threshold
    """
    ret = {}
    for column in column_to_test:
        med = np.nanmedian(df[column])
        mad = mathematics.compute_mad(df, column, med, b)

        # threshold
        low_threshold = med - (distance * mad)
        high_threshold = med + (distance * mad)

        ret[column] = (low_threshold, high_threshold)
    # avoid having a dictionnary for one column
    if len(column_to_test) == 1:
        return ret[column_to_test[0]][0], ret[column_to_test[0]][1]
    else:
        return ret


def threshold_tukey(
    df: pd.DataFrame,
    column_to_test: str,
    distance: float | int
) -> float:
    """ Tukey detection method

    This function allow the user to have the low threshold
    and the high threshold with the "Tukey" outliers method
    with a specific distance.

    Parameters
    ------------
        df: pd.DataFrame
            The dataframe used
        column_to_test: str | list | int | pd.Series
            The name of the colum of interest
        distance: float | int
            The distance used to calculate threshold
    """
    ret = {}
    for column in column_to_test:
        q1, q3 = df[column].quantile([0.25, 0.75])
        iqr = q3-q1

        low_threshold = q1 - distance*iqr
        high_threshold = q3 + distance*iqr
        ret[column] = (low_threshold, high_threshold)

    # avoid having a dictionnary for one column
    if len(column_to_test) == 1:
        return ret[column_to_test[0]][0], ret[column_to_test[0]][1]
    else:
        return ret


def threshold_sn(
    df: pd.DataFrame,
    column_to_test: str,
    distance: float | int
) -> float:
    """ Sn detection method

    This function allow the user to have the low threshold
    and the high threshold with the "Sn" outliers method
    with a specific distance.

    Parameters
    ------------
        df: pd.DataFrame
            The dataframe used
        column_to_test: str | list | int | pd.Series
            The name of the colum of interest
        distance: float | int
            The distance used to calculate threshold
    """
    ret = {}
    for column in column_to_test:
        Sn, all_median = mathematics.S_n(df, column)

        threshold = Sn * distance

        ret[column] = (threshold, all_median)

    # avoid having a dictionnary for one column
    if len(column_to_test) == 1:
        return ret[column_to_test[0]][0], ret[column_to_test[0]][1]
    else:
        return ret


def threshold_prctile(
    df: pd.DataFrame,
    column_to_test: str,
    distance: float | int
) -> tuple:
    """ Percentile detection method

    This function allow the user to have the low threshold
    and the high threshold with the "Percentile" outliers method
    with a specific distance. It flagged values above the value of 
    the percentile (lambda) and below (100 - lambda). Thus, if you
    input 90, values above the 90 percentile and below the 10 (100-90)
    will be flag as outliers.

    Parameters
    ------------
        df: pd.DataFrame
            The dataframe used
        column_to_test: str | list | int | pd.Series
            The name of the colum of interest
        distance: float | int
            The distance used to calculate threshold
    """
    if distance >= 100 or distance <= 50:
        raise ValueError("Distance needs to be above 50"
                         " and below 100. Check documentation for more"
                         " information about percentile computation.")
    ret = {}
    for column in column_to_test:
        # threshold computation
        low_threshold = np.nanpercentile(df[column], 100- distance)
        high_threshold = np.nanpercentile(df[column], distance)
        ret[column] = (low_threshold, high_threshold)

    # avoid having a dictionnary for one column
    if len(column_to_test) == 1:
        return ret[column_to_test[0]][0], ret[column_to_test[0]][1]
    else:
        return ret


def threshold_identical(
    df: pd.DataFrame,
    column_to_test: str,
) -> pd.Series:
    """ Identical detection method

    This function allow the user to have the low threshold
    and the high threshold with the "Identical" outliers method.

    Parameters
    ------------
        df: pd.DataFrame
            The dataframe used
        column_to_test: str | list | int | pd.Series
            The name of the colum of interest
    """
    ret = {}
    # get the maximal frequency of the item
    all_max_frequency = df[column_to_test].apply(
        lambda x: x.value_counts(), axis=1).max(axis=1)
    ret = all_max_frequency.div(len(column_to_test))

    return ret
