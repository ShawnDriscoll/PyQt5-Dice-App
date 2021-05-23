from PyQt5 import QtCore, QtGui, QtWidgets
from mainwindow import Ui_MainWindow
from aboutdialog import Ui_aboutDialog
from rpg_tools.PyDiceroll import roll
import sys

class aboutDialog(QtWidgets.QDialog, Ui_aboutDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setWindowFlags(QtCore.Qt.Drawer | QtCore.Qt.WindowStaysOnTopHint)
        self.setupUi(self)
        self.aboutOKButton.clicked.connect(self.acceptOKButtonClicked)
        
    def acceptOKButtonClicked(self):
        self.close()

class DiceWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
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
    app = QtWidgets.QApplication(sys.argv)
    
    # Use print(PyQt5.QtWidgets.QStyleFactory.keys()) to find a setStyle you like, instead of 'Fusion'
    
    app.setStyle('Fusion')
    MainApp = DiceWindow()
    MainApp.show()
    sys.exit(app.exec_())
    
    
        
        
        
        
        
        
        
        
        
        
        
        
            
            
            
            
            
                    
        
        