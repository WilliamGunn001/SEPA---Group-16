from PySide6.QtCore import QDateTime, Qt
from PySide6.QtGui import QPainter,QPen
from PySide6.QtWidgets import (QWidget, QHeaderView, QHBoxLayout,QVBoxLayout, QTableView,
                               QSizePolicy)
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QDateTimeAxis, QValueAxis,QPieSeries, QBarSeries, QBarSet,QBarCategoryAxis

from CustomTableModel import CustomTableModel
import time


class MyWidget(QWidget):
    def __init__(self, data):
        QWidget.__init__(self)

        # Getting the Model
          # Getting the Model
        self.model = CustomTableModel(data)

        # Creating a QTableView
        self.table_view = QTableView()
        self.table_view.setModel(self.model)

        # Creating QChart
        self.chart = QChart()
        self.chart.setAnimationOptions(QChart.AllAnimations)
        self.add_series("Sentiment (Column 1)", [0, 1])
         # Creating QChart pie
        self.chart1 = QChart()
        self.chart1.setAnimationOptions(QChart.AllAnimations)
        self.add_pie_series()
           # Creating QChart pie
        self.chart2 = QChart()
        self.chart2.setAnimationOptions(QChart.AllAnimations)
        self.add_bar_series()
        # Creating QChartView
        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)
        self.chart_view1 = QChartView(self.chart1)
        self.chart_view1.setRenderHint(QPainter.Antialiasing)
        self.chart_view2 = QChartView(self.chart2)
        self.chart_view2.setRenderHint(QPainter.Antialiasing)
        # QWidget Layout
        
        self.main_layout = QHBoxLayout()
        self.sub_layout = QVBoxLayout()
        self.sub_sub_layout=QHBoxLayout()
        size = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        ## Left layout
        size.setHorizontalStretch(1)
        self.table_view.setSizePolicy(size)
        self.main_layout.addWidget(self.table_view)

        ## Right Layout
        size.setVerticalStretch(7)
        self.chart_view.setSizePolicy(size)
        self.sub_layout.addWidget(self.chart_view)
        ## Right Layout
        size.setHorizontalStretch(3)
        self.chart_view1.setSizePolicy(size)
      #  self.chart_view2.setSizePolicy(size)
        self.sub_sub_layout.addWidget(self.chart_view1)
       # self.sub_sub_layout.addWidget(self.chart_view2)

        self.sub_layout.addLayout(self.sub_sub_layout,5)
        # Set the layout to the QWidget
        size.setHorizontalStretch(4)
        self.main_layout.addLayout(self.sub_layout,4)
        self.setLayout(self.main_layout)
    def add_bar_series(self):

        self.set_0 = QBarSet("common Words")
        
        self.set_0.append([9,7,5,6,8,4])
   

        self.series = QBarSeries()
        self.series.append(self.set_0)
  
        self.chart2.addSeries(self.series)
        self.chart2.setTitle("Simple barchart example")
        self.categories=["a","b","c","d","e","f"]
        self.axis_x = QBarCategoryAxis()
        self.axis_x.append(self.categories)
        self.chart2.addAxis(self.axis_x, Qt.AlignBottom)
        self.series.attachAxis(self.axis_x)

        self.axis_y = QValueAxis()
        self.axis_y.setRange(0, 15)
        self.chart2.addAxis(self.axis_y, Qt.AlignLeft)
        self.series.attachAxis(self.axis_y)

        self.chart2.legend().setVisible(False)
        self.chart2.legend().setAlignment(Qt.AlignBottom)

        self._chart_view2 = QChartView(self.chart2)
        self._chart_view2.setRenderHint(QPainter.Antialiasing)

    def add_pie_series(self):
        self.series = QPieSeries()
        p=0
        n=0
        m=0
        for i in range(self.model.rowCount()):
        # Getting the data
            t = float(self.model.index(i, 1).data())
            if t>3 :
                p=p+1
            elif t<3:
                n=n+1
            else:
                m=m+1

        self.series.append('Positive', p)
        self.series.append('Negative', n)
        self.series.append('Neutral', m)
    

        self.slice = self.series.slices()[1]
        self.slice.setBrush(Qt.red)
        
        self.slice = self.series.slices()[0]
        self.slice.setBrush(Qt.green)
        self.chart1.addSeries(self.series)
        self.chart1.setTitle('Overall Sentiment')
        self.chart1.legend()

        self._chart_view1 = QChartView(self.chart)
        self._chart_view1.setRenderHint(QPainter.Antialiasing)

    def add_series(self, name, columns):
        # Create QLineSeries
        self.series = QLineSeries()
        self.series.setName(name)

        # Filling QLineSeries
        for i in range(self.model.rowCount()):
            # Getting the data
            t = self.model.index(i, 0).data()
            date_fmt = "dd-MM-yyyy hh:mm:ss.zzz"
            t=t+" 00:00:00.000"
          
            x =float( QDateTime().fromString(t, date_fmt).toMSecsSinceEpoch())
            y = float(self.model.index(i, 1).data())

            if x > 0 and y > 0:
                self.series.append(x, y)
        
        self.chart.addSeries(self.series)
        
        # Setting X-axis
        self.axis_x = QDateTimeAxis()
        self.axis_x.setTickCount(5)

        self.axis_x.setFormat("dd-MM-yyyy")
        self.axis_x.setTitleText("Date")
        
        self.chart.addAxis(self.axis_x, Qt.AlignBottom)
        self.series.attachAxis(self.axis_x)
        # Setting Y-axis
        self.axis_y = QValueAxis()
        self.axis_y.setRange(0,5)
        self.axis_y.setTickCount(5)
        self.axis_y.setLabelFormat("%.2f")
        self.axis_y.setTitleText("Sentiment")
        self.chart.addAxis(self.axis_y, Qt.AlignLeft)
        self.series.attachAxis(self.axis_y)

        # Getting the color from the QChart to use it on the QTableView
        color_name = self.series.pen().color().name()
        self.model.color = f"{color_name}"
