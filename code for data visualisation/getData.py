import argparse
import sys
import pandas as pd
from MyWidget import MyWidget
from PySide6.QtCore import QDateTime, QTimeZone

from Window import Window
from PySide6.QtWidgets import QApplication 
def date(utc):
        d=utc[0:10]
        utc_fmt = "yyyy-MM-dd"

        new_date = QDateTime().fromString(d, utc_fmt)
        tes=new_date.toString()
        return new_date    
class getData(object):
    """description of class"""

   
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
   
    if __name__ == "__main__":
      #  options = argparse.ArgumentParser()
        #options.add_argument("-f", "--file", type=str, required=True)
       # args = options.parse_args()
        data = read_data("output.csv")

        # Qt Application
        app = QApplication(sys.argv)

        widget = MyWidget(data)
        window = Window(widget)
        window.show()

        sys.exit(app.exec())

