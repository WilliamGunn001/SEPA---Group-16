from PySide6 import QtWidgets
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QLineEdit, QLabel, QPushButton, QBoxLayout, QVBoxLayout, QHBoxLayout, QWidget, QComboBox, QRadioButton, QTextEdit, QSpinBox
import sys
import os
from datetime import datetime, timedelta
from PySide6.QtCore import Qt


class Main(QMainWindow):
    def __init__(self):
        #Initializes window
        super(Main, self).__init__()

        #Embedded CSS Styling
        #Add group tag in widget constructor eg self.boldTextLbl = QLabel(self, objectName="bold")
        self.setStyleSheet("""
            QLabel#rowLbl {
                font-weight: bold;
                font-size:13px;
            }
            QLabel#warningLbl {
                font-weight: bold;
                font-size:14px;
                color:red;
                text-align:center;
            }
            QPushButton#submit {
                background-color: #0078d4;
                font-weight: bold;
                font-size:13px;
                padding: 12px 28px;
                border-radius: 5px;
            }
            QPushButton#submit:hover {
                color: white;
            }
        """)

        self.initUI()
        self.setWindowTitle("Sentiment Analysis")


    def initUI(self):
        #Creates all widgets
        #Included a widget to apply layout to
        widget = QWidget(self)

        self.nlpLbl = QLabel(self, objectName="rowLbl")
        self.nlpLbl.setText("Select NLP Model")
        self.nlpLbl.setMinimumSize(110, 40)

        self.nlpModel = QComboBox(self)
        self.nlpModel.addItems(["Nlptown", "Siebert", "Finiteautomata", "Cardiffnlp", "Seethal", "DaNLP"])

        self.fileLoadLbl = QLabel(self, objectName="rowLbl")
        self.fileLoadLbl.setText("Load Data From")
        self.fileLoadLbl.setMinimumSize(110, 40)

        self.fileLbl = QLabel(self)
        self.fileLbl.setText(".csv, .hsv, .xlsx, .xls")
        self.fileLbl.setMaximumWidth(250)

        self.fileBtn = QPushButton(self)
        self.fileBtn.setText("Select File")
        self.fileBtn.clicked.connect(self.getFile)
        self.fileBtn.setMinimumSize(110,30)

        self.timeLbl = QLabel(self, objectName="rowLbl")
        self.timeLbl.setText('Time Period')
        self.timeLbl.setMinimumSize(110, 40)

        self.timeText = QSpinBox(self)
        self.timeText.setMaximum(999)
        self.timeText.setMinimumWidth(140)
        self.timeText.setAlignment(Qt.AlignCenter)

        self.timePeriod = QComboBox(self)
        self.timePeriod.addItems(["Days", "Weeks", "Months", "Years"])
        self.timePeriod.setMinimumWidth(110)

        self.date1Lbl = QLabel(self, objectName="rowLbl")
        self.date1Lbl.setText('Date Range')
        self.date1Lbl.setMinimumSize(110, 40)

        self.date1Text = QLineEdit(self)
        #self.date1Text.resize(200, 30)
        self.date1Text.setInputMask("99/99/99;")
        self.date1Text.setText("01/01/22;")

        self.date2Lbl = QLabel(self)
        self.date2Lbl.setText('to')

        self.date2Text = QLineEdit(self)
        #self.date2Text.resize(200, 30)
        self.date2Text.setInputMask("99/99/99;")
        self.date2Text.setText("01/05/22;")

        self.filterLbl = QLabel(self, objectName="rowLbl")
        self.filterLbl.setText('Filter Words')
        self.filterLbl.setMinimumSize(110, 40)

        self.filterLblWhite = QLabel(self)
        self.filterLblWhite.setText('Include')

        self.filterLblBlack = QLabel(self)
        self.filterLblBlack.setText('Exclude')

        self.filterRadioWhite = QRadioButton(self)
        self.filterRadioWhite.setChecked(True)

        self.filterRadioBlack = QRadioButton(self)

        self.filterText = QTextEdit(self)
        self.filterText.setMaximumWidth(150)
        self.filterText.setPlaceholderText("Seperate, different, words, using, commas")

        self.warningLbl = QLabel(self, objectName="warningLbl")
        self.warningLbl.setText(" ")
        self.warningLbl.setMinimumSize(140, 50)
        self.warningLbl.setAlignment(Qt.AlignCenter)

        self.generateBtn = QPushButton(self, objectName="submit")
        self.generateBtn.setText("Generate")
        self.generateBtn.clicked.connect(self.generate)

        self.downloadBtn = QPushButton(self, objectName="submit")
        self.downloadBtn.setText("Download Results")
        #self.downloadBtn.clicked.connect()

        #Layout setup
        self.setCentralWidget(widget)
        self.vLayout = QVBoxLayout()

        #First row NLP
        self.row1 = QHBoxLayout()
        self.row1.addWidget(self.nlpLbl)
        self.row1.addWidget(self.nlpModel)
        self.row1.addStretch()

        #Second row file select
        self.row2 = QHBoxLayout()
        self.row2.addWidget(self.fileLoadLbl)
        self.row2.addWidget(self.fileBtn)
        self.row2.addWidget(self.fileLbl)
        self.row2.addStretch()

        #Third row time period
        self.row3 = QHBoxLayout()
        self.row3.addWidget(self.timeLbl)
        self.row3.addWidget(self.timeText)
        self.row3.addWidget(self.timePeriod)
        
        #Fourth row date range
        self.row4 = QHBoxLayout()
        self.row4.addWidget(self.date1Lbl)
        self.row4.addWidget(self.date1Text)
        self.row4.addWidget(self.date2Lbl)
        self.row4.addWidget(self.date2Text)

        #Fifth row filter
        self.row5 = QHBoxLayout()
        self.row5.addWidget(self.filterLbl)

        self.radio = QVBoxLayout()
        self.radio.addWidget(self.filterRadioWhite)
        self.radio.addWidget(self.filterRadioBlack)
        self.row5.addLayout(self.radio)

        self.radioLbls = QVBoxLayout()
        self.radioLbls.addWidget(self.filterLblWhite)
        self.radioLbls.addWidget(self.filterLblBlack)
        self.row5.addLayout(self.radioLbls)

        self.row5.addWidget(self.filterText)

        #Sixth row warning
        self.row6 = QHBoxLayout()
        self.row6.addWidget(self.warningLbl)

        #Seventh row buttons
        self.row7 = QHBoxLayout()
        self.row7.addWidget(self.generateBtn)
        self.row7.addStretch()
        self.row7.addWidget(self.downloadBtn)

        #Adding rows to column
        self.vLayout.addLayout(self.row1)
        self.vLayout.addLayout(self.row2)
        self.vLayout.addLayout(self.row3)
        self.vLayout.addLayout(self.row4)
        self.vLayout.addLayout(self.row5)
        self.vLayout.addLayout(self.row6)
        self.vLayout.addLayout(self.row7)


        widget.setLayout(self.vLayout)

    def getFile(self):
        fileFilter = 'Comma Seperated Values (*.csv);;Hash Seperated Values (*.hsv);; Excel File (*.xlsx, *xls)'
        #Filedeets is tuple. [0] is filename and [1] is file type
        self.fileDeets = QFileDialog.getOpenFileName(
            parent = self,
            caption = 'Select a Data Set',
            dir = os.getcwd(),
            filter = fileFilter,
            selectedFilter = 'Comma Seperated Values (*.csv)')
        self.fileLbl.setText(self.fileDeets[0])
        self.fileLbl.adjustSize()

    def generate(self):
        #If time needed, remove .date()
        #Gets the calender dates
        if self.timeText.text() == "0":
            fromDate = datetime.strptime(self.date1Text.text(), "%d/%m/%y").date()
            endDate = datetime.strptime(self.date2Text.text(), "%d/%m/%y").date()
        #Or converts time period to a date
        else:
            endDate = datetime.today().date()
            timeNum = int(self.timeText.text())
            if self.timePeriod.currentText() == "Days":
                dateGap = timedelta(days=timeNum)
            elif self.timePeriod.currentText() == "Weeks":
                dateGap = timedelta(weeks=timeNum)
            elif self.timePeriod.currentText() == "Months":
                timeNum  = timeNum*4
                dateGap = timedelta(weeks=timeNum)
            elif self.timePeriod.currentText() == "Years":
                timeNum  = timeNum*52
                dateGap = timedelta(weeks=timeNum)
            fromDate = (endDate - dateGap)
        try:
            #if startdate less than end date throw exception
            if endDate < fromDate:
                self.warningLbl.setText("The starting date cannot be later than the end date")
            #TODO: Data processing here? convert Include/Exclude to one variable, 
            #     Model (Can get text or index)  , File tuple    ,start date,end date, Include filter? (True/False)     , Exclude filter? (True/False)    , filter words          
            else:
                self.warningLbl.setText(" ")
                print(self.nlpModel.currentText(), self.fileDeets, fromDate, endDate, self.filterRadioWhite.isChecked(), self.filterRadioBlack.isChecked(),  self.filterText.toPlainText())
        except AttributeError:
            self.warningLbl.setText("Please select a dataset to use")
def window():
    app = QApplication(sys.argv)
    win = Main()

    win.show()
    sys.exit(app.exec())

window()
