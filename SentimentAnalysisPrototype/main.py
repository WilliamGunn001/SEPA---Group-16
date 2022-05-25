from UI import Main
from PySide6 import QtWidgets
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QLineEdit, QLabel, QPushButton, QBoxLayout, QVBoxLayout, QHBoxLayout, QWidget, QComboBox, QRadioButton, QTextEdit, QSpinBox
import sys
import os
from datetime import datetime, timedelta
from PySide6.QtCore import Qt

def main():
    app = QApplication(sys.argv)
    win = Main()
    while True:
        win.show()
        win.update()
        sys.exit(app.exec())
    
        
if __name__ == "__main__":
    main()
