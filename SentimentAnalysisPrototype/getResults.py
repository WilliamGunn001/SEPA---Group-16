import argparse
import sys
import pandas as pd
from MyWidget import MyWidget
from PySide6.QtCore import QDateTime, QTimeZone
from PySide6.QtWidgets import QApplication 
from datetime import datetime
from dateutil.parser import parse
from dateutil.tz import gettz

class getResults(object):
    """description of class"""

    def date(utc):
        d=utc[0:10]
        utc_fmt = "yyyy-MM-dd"

        new_date = QDateTime().fromString(d, utc_fmt)
        tes=new_date.toString()
        return new_date    


   
    def read_data(fname):
        # Read the CSV content
        df = pd.read_csv(fname)
        # Remove wrong magnitudes
        df['date'] = df['date'].str[:10]
        df= df.groupby('date', as_index=False).mean()
        dates = df["date"].apply(lambda x: date(x))
        sentiment=df["scale"]
        # My local timezone

        # Get timestamp transformed to our timezone

        return dates, sentiment