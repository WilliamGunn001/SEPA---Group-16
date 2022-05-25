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
    def __init__(self):
        pass
    def date(self, utc):
        d=utc[0:10]
        utc_fmt = "yyyy-MM-dd"

        new_date = QDateTime().fromString(d, utc_fmt)
        tes=new_date.toString()
        return new_date    


   
    def read_data(self, fname):
        # Read the CSV content
        df = pd.read_csv(fname)
        # Remove wrong magnitudes
        df['date'] = df['date'].str[:10]
        df= df.groupby('date', as_index=False).mean()
        dates = df["date"].apply(lambda x: self.date(x))
        sentiment=df["scale"].apply(lambda x: round(x,3))
        # My local timezone

        # Get timestamp transformed to our timezone

        return dates, sentiment