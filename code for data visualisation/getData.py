import argparse
import sys
import pandas as pd
from MyWidget import MyWidget
from PySide6.QtCore import QDateTime, QTimeZone

from Window import Window
from PySide6.QtWidgets import QApplication 
def date(utc):
        utc_fmt = "MM-dd-yyyy"
        timezone = QTimeZone(b"Australia/Sydney")

        new_date = QDateTime().fromString(utc, utc_fmt)
        return new_date    
class getData(object):
    """description of class"""

   
    def read_data(fname):
        # Read the CSV content
        df = pd.read_csv(fname)
        # Remove wrong magnitudes

        dates = df["Date"].apply(lambda x: date(x))
        sentiment= df["Sentiment_Score"]

        # My local timezone

        # Get timestamp transformed to our timezone

        return dates, sentiment
   
    if __name__ == "__main__":
        options = argparse.ArgumentParser()
        options.add_argument("-f", "--file", type=str, required=True)
        args = options.parse_args()
        data = read_data(args.file)

        # Qt Application
        app = QApplication(sys.argv)

        widget = MyWidget(data)
        window = Window(widget)
        window.show()

        sys.exit(app.exec())

