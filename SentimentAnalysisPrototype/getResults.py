import argparse
import sys
import pandas as pd
from MyWidget import MyWidget
from PySide6.QtCore import QDateTime, QTimeZone
from PySide6.QtWidgets import QApplication 
class getResults(object):
    """description of class"""

   
    def read_data(self,fname):
        # Read the CSV content
        df = pd.read_csv(fname)
        # Remove wrong magnitudes

        dates = df["date"].apply(lambda x: self.date(x))
        sentiment= df["scale"]

        # My local timezone

        # Get timestamp transformed to our timezone

        return dates, sentiment
  
    def date(self,utc):
        ##BUG HHERE
            utc_fmt = "MM-dd-yyyy"
            timezone = QTimeZone(b"Australia/Sydney")

            new_date = QDateTime().fromString(utc, utc_fmt)
            return new_date    