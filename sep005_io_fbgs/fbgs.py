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
        self.channels = channels
        self.error_status = None



    @classmethod
    def from_df(cls, df:pd.DataFrame, mode='engineering_units', dt_format='%Y-%m-%dT%H:%M:%S%z'):
        """

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
        for idx, row in df.iterrows():
            timestamp_i = datetime.datetime.strptime(row['Date'], dt_format)
            if timestamp_i > timestamp:
                fs = idx/(timestamp_i-timestamp).total_seconds()
                break

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


def read_fbgs(path: Union[str, Path]) -> list:
    """
    Primary function to read fbgs files based on path


    """
    if not os.path.isfile(path):
        warnings.warn('FAILED IMPORT: No FBGS file at: ' + path, UserWarning)
        signals = []
        return signals

    df = _open_fbgs_file(path, sep='\t')
    fbg = FBG.from_df(df)

    return fbg.channels

def _open_fbgs_file(path: Union[str, Path], **kwargs) -> pd.DataFrame:
    df = pd.read_csv(path, **kwargs)
    return df