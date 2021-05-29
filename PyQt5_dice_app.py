from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from mainwindow import Ui_MainWindow
from aboutdialog import Ui_aboutDialog
from rpg_tools.PyDiceroll import roll
import sys

class aboutDialog(QDialog, Ui_aboutDialog):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.Drawer | Qt.WindowStaysOnTopHint)
        self.setupUi(self)
        self.aboutOKButton.clicked.connect(self.acceptOKButtonClicked)
        
    def acceptOKButtonClicked(self):
        self.close()

class DiceWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        self.diceCount.valueChanged.connect(self.diceCount_changed)
        
        self.diceType.addItem('D4')
        self.diceType.addItem('D6')
        self.diceType.addItem('D8')
        self.diceType.addItem('D10')
        self.diceType.addItem('D12')
        self.diceType.addItem('D20')
        self.diceType.addItem('D30')
        self.diceType.addItem('D66')
        self.diceType.addItem('D100')
        self.dice_type = 'D6'
        self.diceType.setCurrentIndex(1)
        self.diceType.currentIndexChanged.connect(self.diceType_changed)
        
        self.diceDM.valueChanged.connect(self.diceDM_changed)
        
        self.rollButton.clicked.connect(self.rollButton_clicked)
        self.actionRoll_Dice.triggered.connect(self.rollButton_clicked)
        
        self.clearButton.clicked.connect(self.clearButton_clicked)
        self.actionClear_All.triggered.connect(self.clearButton_clicked)
        
        self.actionAbout_Dice_Roll.triggered.connect(self.actionAbout_triggered)
        self.popAboutDialog=aboutDialog()
        
        self.quitButton.clicked.connect(self.quitButton_clicked)
        self.actionQuit.triggered.connect(self.quitButton_clicked)
        
        self.dice_to_roll = ''
        
    def diceCount_changed(self):
        if self.diceCount.value() > 1:
            if self.diceType.currentIndex() > 2:
                self.diceType.setCurrentIndex(2)
        self.diceDM.setValue(0)
        self.diceRoll.setText('')
        
    def diceType_changed(self):
        die_types = ['D4', 'D6', 'D8', 'D10', 'D12', 'D20', 'D30', 'D66', 'D100']
        self.dice_type = die_types[self.diceType.currentIndex()]
        if self.diceType.currentIndex() > 2:
            self.diceCount.setValue(1)
            self.countLabel.setEnabled(0)
            self.diceCount.setEnabled(0)
        self.diceRoll.setText('')
        self.diceDM.setValue(0)
        if self.diceType.currentIndex() == 7:
            self.dmLabel.setEnabled(0)
            self.diceDM.setEnabled(0)
        if self.diceType.currentIndex() < 3:
            self.countLabel.setEnabled(1)
            self.diceCount.setEnabled(1)
        if self.diceType.currentIndex() != 7:
            self.dmLabel.setEnabled(1)
            self.diceDM.setEnabled(1)
            
    def diceDM_changed(self):
        if self.diceType.currentIndex() == 7:
            self.diceDM.setValue(0)
        self.diceRoll.setText('')
    
    def rollButton_clicked(self):
        if self.diceDM.value() >= 0:
            math_op = '+'
        else:
            math_op = ''
        if self.diceType.currentIndex() > 2:
            self.dice_to_roll = ''
        else:
            self.dice_to_roll = str(self.diceCount.value())
        self.dice_to_roll += self.dice_type
        if self.diceType.currentIndex() != 7:
            self.dice_to_roll += math_op + str(self.diceDM.value())
        self.diceRoll.setText(str(roll(self.dice_to_roll)))
        print(self.dice_to_roll, '=', self.diceRoll.text())
        
    def clearButton_clicked(self):
        self.countLabel.setEnabled(1)
        self.diceCount.setEnabled(1)
        self.dmLabel.setEnabled(1)
        self.diceDM.setEnabled(1)
        self.diceCount.setValue(1)
        self.diceDM.setValue(0)
        self.diceRoll.setText('')
        
    def actionAbout_triggered(self):
        self.popAboutDialog.show()
    
    def quitButton_clicked(self):
        self.close()
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Use print(QStyleFactory.keys()) to find a setStyle you like, instead of 'Fusion'

    app.setStyle('Fusion')
    
    darkPalette = QPalette()
    darkPalette.setColor(QPalette.Window, QColor(53, 53, 53))
    darkPalette.setColor(QPalette.WindowText, Qt.white)
    darkPalette.setColor(QPalette.Disabled, QPalette.WindowText, QColor(127, 127, 127))
    darkPalette.setColor(QPalette.Base, QColor(42, 42, 42))
    darkPalette.setColor(QPalette.AlternateBase, QColor(66, 66, 66))
    darkPalette.setColor(QPalette.ToolTipBase, Qt.white)
    darkPalette.setColor(QPalette.ToolTipText, Qt.white)
    darkPalette.setColor(QPalette.Text, Qt.white)
    darkPalette.setColor(QPalette.Disabled, QPalette.Text, QColor(127, 127, 127))
    darkPalette.setColor(QPalette.Dark, QColor(35, 35, 35))
    darkPalette.setColor(QPalette.Shadow, QColor(20, 20, 20))
    darkPalette.setColor(QPalette.Button, QColor(53, 53, 53))
    darkPalette.setColor(QPalette.ButtonText, Qt.white)
    darkPalette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(127, 127, 127))
    darkPalette.setColor(QPalette.BrightText, Qt.red)
    darkPalette.setColor(QPalette.Link, QColor(42, 130, 218))
    darkPalette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    darkPalette.setColor(QPalette.Disabled, QPalette.Highlight, QColor(80, 80, 80))
    darkPalette.setColor(QPalette.HighlightedText, Qt.white)
    darkPalette.setColor(QPalette.Disabled, QPalette.HighlightedText, QColor(127, 127, 127))
    
    MainApp = DiceWindow()
    MainApp.show()
    
    app.setPalette(darkPalette)
    
    app.exec_()
