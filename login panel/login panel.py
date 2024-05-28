import PyQt5 as qt
from PyQt5 import QtCore, uic 
import PyQt5.QtWidgets as qtw 
from PyQt5.QtWidgets import QWidget , QDesktopWidget, QApplication, QVBoxLayout
from PyQt5 import QtCore, QtGui, QtWidgets 
from PyQt5.QtCore import Qt, QPoint , QTimer
from screeninfo import get_monitors
import re , hashlib, random, sys
import mysql.connector
#============================================================= 
#open data base
mydB = mysql.connector.connect(  host="localhost",
    user="root",
    password="afyo250012",
    database="mydatabase")
mycursor = mydB.cursor()
# mycursor.execute("CREATE TABLE users (user_id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), email VARCHAR(255), password VARCHAR(20))")
#============================================================= 

def login_check(x):

        mycursor.execute(f"select name from users where name = %s", (x,))
        result = mycursor.fetchone()
        
        if result == None:
            return False
        else:
            return True

def is_valid_email(Email):

    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, Email)

def is_name_exist(x):
    
    mycursor.execute(f"select name from users where name = %s", (x,))
    result = mycursor.fetchone()
    
    if result == None:
        return False
    else:
        return True
    
def is_email_exist(x):
    
    mycursor.execute(f"select email from users where email = %s", (x,))
    result = mycursor.fetchone()
    
    if result == None:
        return False
    else:
        return True
#============================================================= 

        
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(r'D:\programming\python\programs\projects\green system\ui\main\main.ui', self)



class login_screen(qtw.QWidget):
    login_successful = QtCore.pyqtSignal()
    def __init__ (self):
        super().__init__()
        uic.loadUi(r'D:\programming\python\programs\projects\green system\ui\login\login.ui', self)
        
        self.login_button.clicked.connect(self.login)
        self.open_register_button.clicked.connect(self.open_register_screen)
        self.login_title.setGraphicsEffect(qtw.QGraphicsDropShadowEffect(blurRadius=25, xOffset=0, yOffset=0, color=QtGui.QColor(234, 221, 186,100)))
        self.login_button.setGraphicsEffect(qtw.QGraphicsDropShadowEffect(blurRadius=25, xOffset=0, yOffset=0, color=QtGui.QColor(234, 221, 186,100)))
        self.setWindowTitle("Green System")
        
    def open_register_screen(self):
        
        login_widgets.setCurrentIndex(login_widgets.currentIndex()+1)
        self.name_input.setText("")
        self.password_input.setText("")
        
    def login(self):
        
        password = self.password_input.text()
        name_input = self.name_input.text()

        if login_check(name_input) == True:
        
            mycursor.execute(f'select password from users where name = %s', (name_input,)) 
            result = mycursor.fetchone()[0]
            if hashlib.md5(password.encode()).hexdigest() == result:
                
                print(f'hi {name_input}')
                self.login_successful.emit()
                login_widgets.close()
            
            else:
                
                if password == "":
                    
                    self.password_input.setStyleSheet('background-color: rgba(0, 0, 0, 0); border:none; border-bottom:2px solid rgb(230, 0, 4); color: rgba(255, 255, 255, 230); padding-bottom:7px;')
                    QTimer.singleShot(3000, lambda : login.password_input.setStyleSheet('background-color: rgba(0, 0, 0, 0);border:none;border-bottom:2px solid rgb(255, 189, 167);color: rgba(255, 255, 255, 230);padding-bottom:7px;'))
            
                else:
                        
                    self.password_input.setStyleSheet('background-color: rgba(0, 0, 0, 0); border:none; border-bottom:2px solid rgb(230, 0, 4); color: rgba(255, 255, 255, 230); padding-bottom:7px;')
                    self.password_input.setPlaceholderText('      Wrong Password')
                    self.password_input.setText("")
                    QTimer.singleShot(3000, lambda : login.password_input.setStyleSheet('background-color: rgba(0, 0, 0, 0);border:none;border-bottom:2px solid rgb(255, 189, 167);color: rgba(255, 255, 255, 230);padding-bottom:7px;'))
                    QTimer.singleShot(3000, lambda : login.password_input.setPlaceholderText('            Password'))

        else:
            
            if name_input == '' or password == '':
                
                if name_input == '' :
                    
                    self.name_input.setStyleSheet('background-color: rgba(0, 0, 0, 0); border:none; border-bottom:2px solid rgb(230, 0, 4); color: rgba(255, 255, 255, 230); padding-bottom:7px;')
                    QTimer.singleShot(3000, lambda : login.name_input.setStyleSheet('background-color: rgba(0, 0, 0, 0);border:none;border-bottom:2px solid rgb(255, 189, 167);color: rgba(255, 255, 255, 230);padding-bottom:7px;'))
                
                if password == '' :
                    
                    self.password_input.setStyleSheet('background-color: rgba(0, 0, 0, 0); border:none; border-bottom:2px solid rgb(230, 0, 4); color: rgba(255, 255, 255, 230); padding-bottom:7px;')
                    QTimer.singleShot(3000, lambda : login.password_input.setStyleSheet('background-color: rgba(0, 0, 0, 0);border:none;border-bottom:2px solid rgb(255, 189, 167);color: rgba(255, 255, 255, 230);padding-bottom:7px;'))
            
            else:
                        
                self.name_input.setPlaceholderText('        User Not Found')        
                self.name_input.setStyleSheet('background-color: rgba(0, 0, 0, 0); border:none; border-bottom:2px solid rgb(230, 0, 4); color: rgba(255, 255, 255, 230); padding-bottom:7px;')
                self.name_input.setText("")
                self.password_input.setText("")
                QTimer.singleShot(3000, lambda : login.name_input.setStyleSheet('background-color: rgba(0, 0, 0, 0);border:none;border-bottom:2px solid rgb(255, 189, 167);color: rgba(255, 255, 255, 230);padding-bottom:7px;'))
                QTimer.singleShot(3000, lambda : login.name_input.setPlaceholderText('           User Name'))
                
    #=============================================================       
    #make the window move
    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()


    def mouseMoveEvent(self, event):
        self.move(self.pos() + event.globalPos() - self.dragPos )
        self.dragPos = event.globalPos()
        event.accept()
    #=============================================================



class register_screen(qtw.QDialog):
    
    def __init__(self):
        super().__init__()
        uic.loadUi(r'D:\programming\python\programs\projects\green system\ui\login\register.ui', self)
        
        self.back.clicked.connect(self.back_to_login)
        self.register_button.clicked.connect(self.add_data)
        
        self.register_title.setGraphicsEffect(qtw.QGraphicsDropShadowEffect(blurRadius=25, xOffset=0, yOffset=0, color=QtGui.QColor(234, 221, 186,100)))
        self.register_button.setGraphicsEffect(qtw.QGraphicsDropShadowEffect(blurRadius=25, xOffset=0, yOffset=0, color=QtGui.QColor(234, 221, 186,100)))

    def add_data(self):

        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()
        email = self.email_input.text()
        name = self.name_input.text()
        
        if (email == '') or (name == '') or (password == '') or ( is_valid_email(email) == None ) :
            
            if email == '' :            
                
                self.email_input.setStyleSheet('background-color: rgba(0, 0, 0, 0); border:none; border-bottom:2px solid rgb(230, 0, 4); color: rgba(255, 255, 255, 230); padding-bottom:7px;')
                QTimer.singleShot(3000, lambda : register.email_input.setStyleSheet('background-color: rgba(0, 0, 0, 0);border:none;border-bottom:2px solid rgb(255, 189, 167);color: rgba(255, 255, 255, 230);padding-bottom:7px;'))

            else:
                
                if ( is_valid_email(email) == None ):
                    
                    self.email_input.setText("")
                    self.email_input.setPlaceholderText('          Invalid Mail')        
                    self.email_input.setStyleSheet('background-color: rgba(0, 0, 0, 0); border:none; border-bottom:2px solid rgb(230, 0, 4); color: rgba(255, 255, 255, 230); padding-bottom:7px;')
                    QTimer.singleShot(3000, lambda : register.email_input.setStyleSheet('background-color: rgba(0, 0, 0, 0);border:none;border-bottom:2px solid rgb(255, 189, 167);color: rgba(255, 255, 255, 230);padding-bottom:7px;'))
                    QTimer.singleShot(3000, lambda : register.email_input.setPlaceholderText('               Email'))                   
                    
                
            if name == '' :
                    
                self.name_input.setStyleSheet('background-color: rgba(0, 0, 0, 0); border:none; border-bottom:2px solid rgb(230, 0, 4); color: rgba(255, 255, 255, 230); padding-bottom:7px;')
                QTimer.singleShot(3000, lambda : register.name_input.setStyleSheet('background-color: rgba(0, 0, 0, 0);border:none;border-bottom:2px solid rgb(255, 189, 167);color: rgba(255, 255, 255, 230);padding-bottom:7px;'))
                    
            if password == '' :
                        
                self.password_input.setStyleSheet('background-color: rgba(0, 0, 0, 0); border:none; border-bottom:2px solid rgb(230, 0, 4); color: rgba(255, 255, 255, 230); padding-bottom:7px;')
                QTimer.singleShot(3000, lambda : register.password_input.setStyleSheet('background-color: rgba(0, 0, 0, 0);border:none;border-bottom:2px solid rgb(255, 189, 167);color: rgba(255, 255, 255, 230);padding-bottom:7px;'))
        
        else:
            
            if (is_name_exist(name) == True) or (is_email_exist(email) == True):
                
                if is_email_exist(email) == True :
                    
                    self.email_input.setPlaceholderText('         Already Exist')        
                    self.email_input.setStyleSheet('background-color: rgba(0, 0, 0, 0); border:none; border-bottom:2px solid rgb(230, 0, 4); color: rgba(255, 255, 255, 230); padding-bottom:7px;')
                    self.email_input.setText("")
                    QTimer.singleShot(3000, lambda : register.email_input.setStyleSheet('background-color: rgba(0, 0, 0, 0);border:none;border-bottom:2px solid rgb(255, 189, 167);color: rgba(255, 255, 255, 230);padding-bottom:7px;'))
                    QTimer.singleShot(3000, lambda : register.email_input.setPlaceholderText('               Email'))    
                        
                if is_name_exist(name) == True :
                    
                    self.name_input.setPlaceholderText('         Already exist')        
                    self.name_input.setStyleSheet('background-color: rgba(0, 0, 0, 0); border:none; border-bottom:2px solid rgb(230, 0, 4); color: rgba(255, 255, 255, 230); padding-bottom:7px;')
                    self.name_input.setText("")
                    QTimer.singleShot(3000, lambda : register.name_input.setStyleSheet('background-color: rgba(0, 0, 0, 0);border:none;border-bottom:2px solid rgb(255, 189, 167);color: rgba(255, 255, 255, 230);padding-bottom:7px;'))
                    QTimer.singleShot(3000, lambda : register.name_input.setPlaceholderText('           User Name'))                       


            else:    
                
                if (password == confirm_password) and (password != ''):

                    mycursor.execute(f"insert into users (name, email, password) values (%s, %s, %s)", (name, email, hashlib.md5(password.encode()).hexdigest()))
                    mydB.commit()
                    self.back_to_login()


                else:

                    self.confirm_password_input.setStyleSheet('background-color: rgba(0, 0, 0, 0); border:none; border-bottom:2px solid rgb(230, 0, 4); color: rgba(255, 255, 255, 230); padding-bottom:7px;')
                    self.confirm_password_input.setPlaceholderText('Password Doesn\'t Match')
                    self.confirm_password_input.setText("")
                    QTimer.singleShot(3000, lambda : register.confirm_password_input.setStyleSheet('background-color: rgba(0, 0, 0, 0);border:none;border-bottom:2px solid rgb(255, 189, 167);color: rgba(255, 255, 255, 230);padding-bottom:7px;'))
                    QTimer.singleShot(3000, lambda : register.confirm_password_input.setPlaceholderText('      Confirm Password'))
    
    def back_to_login(self):
        
        login_widgets.setCurrentIndex(login_widgets.currentIndex()-1)
        
        self.password_input.setText("")
        self.confirm_password_input.setText("")
        self.name_input.setText("")
        self.email_input.setText("")
        
    #=============================================================       
    #make the window move
    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()


    def mouseMoveEvent(self, event):
        self.move(self.pos() + event.globalPos() - self.dragPos )
        self.dragPos = event.globalPos()
        event.accept()
    #=============================================================


#===================================================================
#get screen info
def get_screen_resolution():
    monitors = get_monitors()
    
    resolutions = []
    for monitor in monitors:
        resolutions.append((monitor.width, monitor.height))
    
    return resolutions
s_r = get_screen_resolution()
screen_width = s_r[0][0]
screen_height = s_r[0][1]
wtp = (screen_width-280)//2
htp = (screen_height-400)//2
#===================================================================

if __name__ == "__main__":
    
    app = qtw.QApplication(sys.argv)
#===================================
    #identify and run the windows
    login = login_screen()
    register = register_screen()
    main = MainWindow()
#===================================

#===============================================================
    # login and register panel
    login_widgets = QtWidgets.QStackedWidget()
    login_widgets.addWidget(login)
    login_widgets.addWidget(register)
    login_widgets.setWindowFlags(QtCore.Qt.FramelessWindowHint)
    login_widgets.setAttribute(QtCore.Qt.WA_TranslucentBackground)
    login_widgets.setGeometry(wtp, htp,screen_width, screen_height)
    login_widgets.show()
#===============================================================
    layout = QVBoxLayout()
    layout.addWidget(login_widgets)
#===============================================================
    # start the main window after login
    login.login_successful.connect(main.showMaximized)
#===============================================================
    sys.exit(app.exec_())
