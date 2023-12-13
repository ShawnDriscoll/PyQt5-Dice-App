from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from mainwindow import Ui_MainWindow
from aboutdialog import Ui_aboutDialog
from rpg_tools.pydice import roll
import sys

die_types = ['D4', 'D6', 'D8', 'D10', 'D12', 'D20', 'D30', 'D66', 'D100']

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
        
        for i in range(len(die_types)):
            self.diceType.addItem(die_types[i])
            
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
        
        self.rollInput.returnPressed.connect(self.manual_roll)
        
        self.dice_to_roll = ''
        
    def diceCount_changed(self):
        '''
        Clear die modifier and last roll result
        '''
        self.diceDM.setValue(0)
        self.diceRoll.setText('')
        self.rollInput.clear()
        
    def diceType_changed(self):
        '''
        Enable/disable the dice count and die modifier fields
        depending on the dice type chosen.
        
        And clear fields as needed.
        '''
        self.dice_type = die_types[self.diceType.currentIndex()]
        if self.diceType.currentIndex() <= 4:
            self.countLabel.setEnabled(1)
            self.diceCount.setEnabled(1)
            self.dmLabel.setEnabled(1)
            self.diceDM.setEnabled(1)
        if self.diceType.currentIndex() >= 5 and self.diceType.currentIndex() <= 6 or self.diceType.currentIndex() >= 8:
            self.diceCount.setValue(1)
            self.countLabel.setEnabled(0)
            self.diceCount.setEnabled(0)
            self.dmLabel.setEnabled(1)
            self.diceDM.setEnabled(1)
        if self.diceType.currentIndex() == 7:
            self.diceCount.setValue(1)
            self.countLabel.setEnabled(0)
            self.diceCount.setEnabled(0)
            self.dmLabel.setEnabled(0)
            self.diceDM.setEnabled(0)
        self.diceDM.setValue(0)
        self.diceRoll.setText('')
        self.rollInput.clear()
            
    def diceDM_changed(self):
        '''
        Clear last roll result if die modifier is changed
        '''
        self.diceRoll.setText('')
        self.rollInput.clear()
    
    def rollButton_clicked(self):
        '''
        Roll button was clicked.
        Construct the string argument needed for roll().
        '''
        if self.diceDM.value() >= 0:
            math_op = '+'
        else:
            math_op = ''
        if self.diceType.currentIndex() > 4:
            self.dice_to_roll = ''
        else:
            self.dice_to_roll = str(self.diceCount.value())
        self.dice_to_roll += self.dice_type
        if self.diceType.currentIndex() != 7:
            self.dice_to_roll += math_op + str(self.diceDM.value())
        self.diceRoll.setText(str(roll(self.dice_to_roll)))
        self.rollBrowser.append(self.dice_to_roll + ' = ' + self.diceRoll.text())
        self.rollInput.clear()
    
    def manual_roll(self):
        '''
        A roll was inputed manually
        '''
        dice_entered = self.rollInput.text()
        roll_returned = roll(dice_entered)
        
        # Was the roll a valid one?
        if roll_returned == -9999:
            returned_line = dice_entered + ' = ' + '<span style=" color:#ff0000;">' + str(roll_returned) + '</span>'
        else:
            returned_line = dice_entered + ' = ' + str(roll_returned)
            
        # Display the roll result inside the text browser
        self.rollBrowser.append(returned_line)
        
    def clearButton_clicked(self):
        '''
        Clear/reset all fields
        '''
        self.diceCount.setValue(1)
        self.diceDM.setValue(0)
        self.diceRoll.setText('')
        self.rollInput.clear()
        self.rollBrowser.clear()
        
    def actionAbout_triggered(self):
        '''
        Display the About window
        '''
        self.popAboutDialog.show()
    
    def quitButton_clicked(self):
        '''
        Exit this app
        '''
        self.close()
        
    def activate(self, reason):
        if reason == QSystemTrayIcon.Trigger:  # systray icon clicked.
            if self.isVisible():
                self.hide()
            else:
                self.show()
    
    def display_app(self, reason):
        self.show()
    
    def hide_app(self, reason):
        self.hide()
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(True) # set to False for app to remain persistent
    
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
    
    # Create the systray icon
    icon = QIcon(":/icons/die_icon.ico")
    
    # Create the systray
    tray = QSystemTrayIcon()
    tray.setIcon(icon)
    tray.setVisible(True)
    
    # Create the systray menu
    menu = QMenu()
    
    showApp = QAction("Show App")
    showApp.triggered.connect(MainApp.display_app)
    menu.addAction(showApp)
    
    hideApp = QAction("Hide App")
    hideApp.triggered.connect(MainApp.hide_app)
    menu.addAction(hideApp)

    quit = QAction("Exit")
    quit.triggered.connect(app.quit)
    menu.addAction(quit)
    
    tray.setToolTip("Dice Roll")
    
    # Add the menu to the tray
    tray.setContextMenu(menu)
    tray.activated.connect(MainApp.activate)
    
    app.exec_()
