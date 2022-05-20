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

   
    def read_data(self,fname):
        # Read the CSV content
        df = pd.read_csv(fname)
        # Remove wrong magnitudes

        # My local timezone
        local_tz = gettz()
        # Get timestamp transformed to our timezone
        dates = df["date"].apply(lambda x: self.date(x, local_tz))
        sentiment= df["scale"]

        return dates, sentiment
  
    def date(self,utc,local_tz):
        date = parse(utc)
        new_date = date.astimezone(local_tz)
        #print(new_date)
        
        return new_date