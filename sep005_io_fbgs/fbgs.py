import os
import warnings
import datetime
from pathlib import Path
from typing import Union

import numpy as np
import pandas as pd
from pytz import utc


class FBG(object):

    def __init__(self, channels:list, error_status=None):
        """
        Initialize a FBG reader object
        """
        self.channels = channels # SEP005 compliant channel objects
        self.error_status = None



    @classmethod
    def from_df(cls, df:pd.DataFrame, mode='engineering_units', dt_format='%Y-%m-%dT%H:%M:%S%z', qa:bool=True):
        """
        Import FBGS data from a dataframe

        """
        if mode == 'engineering_units' or mode == 'eu':
            pass # do Nothing
        elif mode == 'wavelength' or mode == 'wl':
            raise NotImplementedError(f'Data model (wavelength/wl) is not implemented')
        else:
            raise NotImplementedError(f'Data mode {mode} is not a valid option')

        if 'Error status' in df.columns:
            error_status = df['Error status']
        else:
            error_status = None

        timestamp = datetime.datetime.strptime(df['Date'][0], dt_format)

        # FBGS data sometimes has a bad timestamping, e.g. only to second precision.
        dt_e = datetime.datetime.strptime(df['Date'].iloc[-1], dt_format).replace(microsecond=0) \
                + datetime.timedelta(seconds=1) # Floor to the second then add 1
        duration = (dt_e-timestamp).total_seconds()  # Due to the rounding to second precision this
        fs = round(len(df)/duration, 2) # Assumption: Sampling frequency is defined up to 2 decimal points



        if duration*fs != len(df):
            warnings.warn(
                f'QA: Inconsistent number of samples found ({len(df)}) for estimated sampling frequency of {fs},'
                f' set qa to False if you want to still consider this file.',
                UserWarning
            )
            if qa:
                # Failed QA: Returning empty
                return cls(channels=[], error_status=error_status)



        # Convert timestamp to UTC
        timestamp = timestamp.astimezone(utc)

        channels = []
        for c in df.columns:
            if c not in ['Date','Time', 'Linenumber', 'Error status']:
                channel = {
                    'group': 'fbgs',
                    'name': c,
                    'data': df[c].to_numpy(),
                    'start_timestamp': str(timestamp),
                    'fs': fs,
                    'unit_str':''
                }
                channels.append(channel)

        return cls(channels=channels, error_status=error_status)


def read_fbgs(path: Union[str, Path], qa:bool = True) -> list:
    """
    Primary function to read fbgs files based on path

    qa : Quality assurance applied, rejecting files with a bad length. When set to False this check is skipped

    """
    if not os.path.isfile(path):
        warnings.warn('FAILED IMPORT: No FBGS file at: ' + path, UserWarning)
        signals = []
        return signals

    df = _open_fbgs_file(path, sep='\t')
    fbg = FBG.from_df(df, qa=qa)

    return fbg.channels

def _open_fbgs_file(path: Union[str, Path], **kwargs) -> pd.DataFrame:
    df = pd.read_csv(path, **kwargs)
    return df