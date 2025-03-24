import sqlite3
import bcrypt
# from PyQt6 import QtCore, QtWidgets
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QPushButton, QTableWidgetItem, QMessageBox
import re
    

import sqlite3

# Create the database and table if they don't exist
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# Users Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fullname TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)""")

# Messages Table (Fixed UNIQUE constraints)
# cursor.execute("""DROP TABLE messages""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    msg TEXT NOT NULL,
    msgSubject TEXT NOT NULL,
    senderMail TEXT NOT NULL,
    ReceiverMail TEXT NOT NULL,
    status TEXT NOT NULL,
    date TEXT NOT NULL,
    tag TEXT NOT NULL,
    FOREIGN KEY(senderMail) REFERENCES users(email),
    FOREIGN KEY(ReceiverMail) REFERENCES users(email)
)""")

# Spam Strings Table (Fixed Syntax Error)
cursor.execute("""
CREATE TABLE IF NOT EXISTS spamstring (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL
)""")

conn.commit()
conn.close()



class Ui_home(object):
    def navigate_to_login_from_home(self, homePage):
        """Navigate back to the login page."""
        self.login_ui = Ui_loginPage()
        self.login_ui.setupUi(homePage)
    def navigate_to_sender_from_home(self, homePage):
        """Navigate back to the login page."""
        self.login_ui = Ui_sender()
        self.login_ui.setupUi(homePage)

        
           

    def setupUi(self, homePage):
        homePage.setObjectName("WELCOME")
        homePage.resize(800, 600)
        homePage.setMaximumSize(QtCore.QSize(1080, 1024))
        homePage.setStyleSheet("background-color: rgb(255, 255, 255);")
        homePage.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QtWidgets.QWidget(parent=homePage)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 20, 751, 161))
        self.label.setStyleSheet("color: rgb(0, 0, 0);\n"
"font: 75 18pt \"Calibri\";\n"
"textAlign: center\n"
"")
        self.label.setScaledContents(False)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(200, 200, 411, 151))
        self.label_2.setStyleSheet("\n"
"font: 75 18pt \"Calibri\";")
        self.label_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.start = QtWidgets.QPushButton(parent=self.centralwidget)
        self.start.setGeometry(QtCore.QRect(250, 370, 131, 41))
        self.start.setStyleSheet("\n"
"\n"
"QPushButton {\n"
"    background-color: #4CAF50;\n"
"    color: white;\n"
"    border-radius: 10px;\n"
"    padding: 5px 10px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #45a049;\n"
"}\n"
"")
        self.start.setObjectName("start")
        self.start.clicked.connect(lambda: self.navigate_to_login_from_home(homePage))
        self.MODEL_TEST = QtWidgets.QPushButton(parent=self.centralwidget)
        self.MODEL_TEST.setGeometry(QtCore.QRect(450, 370, 131, 41))
        self.MODEL_TEST.setStyleSheet("\n"
"\n"
"QPushButton {\n"
"    background-color:#000;\n"
"    color: white;\n"
"    border-radius: 10px;\n"
"    padding: 5px 10px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #45a049;\n"
"}\n"
"")
        self.MODEL_TEST.setObjectName("MODEL_TEST")
        self.MODEL_TEST.clicked.connect(lambda: self.navigate_to_sender_from_home(homePage))
        homePage.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=homePage)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        homePage.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=homePage)
        self.statusbar.setObjectName("statusbar")
        homePage.setStatusBar(self.statusbar)

        self.retranslateUi(homePage)
        QtCore.QMetaObject.connectSlotsByName(homePage)

    def retranslateUi(self, homePage):
        _translate = QtCore.QCoreApplication.translate
        homePage.setWindowTitle(_translate("homePage", "HOME"))
        self.label.setText(_translate("homePage", " ENSEMBLE MODEL FOR EMAIL FILTERING AND CLASSIFICATION "))
        self.label_2.setText(_translate("homePage", "BY\n"
"Fadiran Peter Opeyemi\n"
"Full Stack developer\n"
""))
        self.start.setAccessibleName(_translate("homePage", "startbtn"))
        self.start.setText(_translate("homePage", "START"))
        self.MODEL_TEST.setAccessibleName(_translate("homePage", "MODELTEST"))
        self.MODEL_TEST.setText(_translate("homePage", "SEND MESSAGE"))


class Ui_loginPage(object):
    def handleLogin(self,loginPage):
        """Handle login with database and hashed passwords."""
        email = self.email.text()
        password = self.password.text()

        # Connect to the SQLite database
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        # Query user credentials
        cursor.execute("SELECT fullname,password FROM users WHERE email = ?", (email,))
        result = cursor.fetchone()
        conn.close()

        if result:
            fullname, stored_password = result
            if bcrypt.checkpw(password.encode(), stored_password.encode()):
                ###go to dashboard
                self.dashboard_ui = Ui_DASHBOARD()
                self.dashboard_ui.setupUi(loginPage,email,fullname)
                
                
            else:
                QMessageBox.warning(None, "Login Failed", "Invalid email or password.")
        else:
            QMessageBox.warning(None, "Login Failed", "User does not exist.")

    def setupUi(self, loginPage):
        loginPage.setObjectName("loginPage")
        loginPage.resize(800, 600)
        loginPage.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.centralwidget = QtWidgets.QWidget(parent=loginPage)
        self.centralwidget.setObjectName("centralwidget")

        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setGeometry(QtCore.QRect(280, 110, 261, 81))
        self.label.setStyleSheet("color: rgb(0, 0, 0); font: 75 18pt 'Calibri';")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("label")

        self.loginBtn = QtWidgets.QPushButton(parent=self.centralwidget)
        self.loginBtn.setGeometry(QtCore.QRect(220, 330, 381, 41))
        self.loginBtn.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 10px;")
        self.loginBtn.setObjectName("loginBtn")
        self.loginBtn.setText("LOGIN")
        self.loginBtn.clicked.connect(lambda:self.handleLogin(loginPage))

        self.email = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.email.setGeometry(QtCore.QRect(220, 210, 381, 41))
        self.email.setStyleSheet("border: 2px solid #4CAF50; border-radius: 5px; background-color: #f9f9f9; padding: 5px;")
        self.email.setPlaceholderText("Enter Your Email")

        self.password = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.password.setGeometry(QtCore.QRect(220, 270, 381, 41))
        self.password.setStyleSheet("border: 2px solid #4CAF50; border-radius: 5px; background-color: #f9f9f9; padding: 5px;")
        self.password.setPlaceholderText("Enter Your Password")

        self.create_account = QtWidgets.QPushButton(parent=self.centralwidget)
        self.create_account.setGeometry(QtCore.QRect(340, 390, 161, 41))
        self.create_account.setStyleSheet("background-color: #000; color: white; border-radius: 10px;")
        self.create_account.setObjectName("create_accountBtn")
        self.create_account.setText("CREATE AN ACCOUNT")
        self.create_account.clicked.connect(lambda: self.navigate_to_signup(loginPage))

        loginPage.setCentralWidget(self.centralwidget)
        self.retranslateUi(loginPage)

    def retranslateUi(self, loginPage):
        _translate = QtCore.QCoreApplication.translate
        loginPage.setWindowTitle(_translate("loginPage", "LOGIN"))
        self.label.setText(_translate("loginPage", "LOGIN"))

    def navigate_to_signup(self, loginPage):
        """Navigate to the signup page."""
        self.signup_ui = Ui_signupPage()
        self.signup_ui.setupUi(loginPage)

#/////////////////////////////////################################################################################################SIGNUPPAGE
class Ui_signupPage(object):
     def navigate_to_login(self, signupPage):
        """Navigate back to the login page."""
        self.login_ui = Ui_loginPage()
        self.login_ui.setupUi(signupPage)

     def handleCreateAccount(self):
        fullname = self.fullname.text()
        email = self.email.text()
        password = self.password.text()

        # Basic input validation
        if not fullname or not email or not password:
                QMessageBox.warning(None, "Input Error", "Please fill in all fields.")
                return

        # Validate email format
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
                QMessageBox.warning(None, "Invalid Email", "Please enter a valid email address.")
                return

        # Hash the password
        try:
                hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        except Exception as e:
                QMessageBox.critical(None, "Error", f"Password hashing failed: {e}")
                return

        try:
                # Connect to the SQLite database
                conn = sqlite3.connect("users.db")
                cursor = conn.cursor()

                # Check if the email already exists
                cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
                if cursor.fetchone():
                        QMessageBox.warning(None, "Email Exists", "This email is already registered.")
                else:
                # Insert the new user into the database
                        cursor.execute(
                        "INSERT INTO users (fullname, email, password) VALUES (?, ?, ?)",
                        (fullname, email, hashed_password)
                )
                conn.commit()
                QMessageBox.information(None, "Account Created", "Your account has been created successfully!")

        except sqlite3.Error as e:
                QMessageBox.critical(None, "Database Error", f"An error occurred: {e}")

        finally:
                conn.close()

     def setupUi(self, signupPage):
        signupPage.setObjectName("signupPage")
        signupPage.resize(800, 600)
        signupPage.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.centralwidget = QtWidgets.QWidget(parent=signupPage)
        self.centralwidget.setObjectName("centralwidget")

        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setGeometry(QtCore.QRect(270, 110, 261, 81))
        self.label.setStyleSheet("color: rgb(0, 0, 0); font: 75 18pt 'Calibri';")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("label")

        self.fullname = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.fullname.setGeometry(QtCore.QRect(220, 210, 381, 41))
        self.fullname.setStyleSheet("border: 2px solid #4CAF50; border-radius: 5px; background-color: #f9f9f9; padding: 5px;")
        self.fullname.setPlaceholderText("Enter Your Fullname")

        self.email = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.email.setGeometry(QtCore.QRect(220, 260, 381, 41))
        self.email.setStyleSheet("border: 2px solid #4CAF50; border-radius: 5px; background-color: #f9f9f9; padding: 5px;")
        self.email.setPlaceholderText("Enter Your Mail Address")

        self.password = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.password.setGeometry(QtCore.QRect(220, 310, 381, 41))
        self.password.setStyleSheet("border: 2px solid #4CAF50; border-radius: 5px; background-color: #f9f9f9; padding: 5px;")
        self.password.setPlaceholderText("Enter Your Password")

        self.create_account_2 = QtWidgets.QPushButton(parent=self.centralwidget)
        self.create_account_2.setGeometry(QtCore.QRect(230, 370, 371, 41))
        self.create_account_2.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 10px;")
        self.create_account_2.setObjectName("create_accountBtn_2")
        self.create_account_2.setText("CREATE ACCOUNT")
        self.create_account_2.clicked.connect(self.handleCreateAccount)  # Handle account creation

        self.login = QtWidgets.QPushButton(parent=self.centralwidget)
        self.login.setGeometry(QtCore.QRect(340, 420, 131, 41))
        self.login.setStyleSheet("background-color: #000; color: white; border-radius: 10px;")
        self.login.setObjectName("loginBtn")
        self.login.setText("LOGIN")
        self.login.clicked.connect(lambda: self.navigate_to_login(signupPage))
        signupPage.setCentralWidget(self.centralwidget)
        self.retranslateUi(signupPage)

     def retranslateUi(self, signupPage):
        _translate = QtCore.QCoreApplication.translate
        signupPage.setWindowTitle(_translate("signupPage", "SIGN UP"))
        self.label.setText(_translate("signupPage", "CREATE AN ACCOUNT"))


##############################################################################################SENDER PAGE

class Ui_sender(object):
    def handleSendMessage(self):
        subject = self.subject.text()
        senderMail = self.sender_mail.text()
        ReceiverMail = self.receiver_mail.text()
        Message = self.message.toPlainText()

        # Basic input validation
        if not subject or not senderMail or not ReceiverMail or not Message:
                QMessageBox.warning(None, "Input Error", "Please provide all fields.")
                return
        try:
                # Connect to the SQLite database
                conn = sqlite3.connect("users.db")
                cursor = conn.cursor()

                # Fetch spam strings from the database
                cursor.execute("SELECT text FROM spamstring")
                spam_strings = [row[0] for row in cursor.fetchall()]

                # Check if message contains any spam string
                tag = "spam" if any(spam_str.lower() in Message.lower() for spam_str in spam_strings) else "primary"

                # Insert the new message into the database with the determined tag
                cursor.execute(
                "INSERT INTO messages (msg, msgSubject, senderMail, ReceiverMail, status, date, tag) "
                "VALUES (?, ?, ?,?, 'unread', datetime('now'), ?)",
                (Message,subject, senderMail, ReceiverMail, tag)
                )

                conn.commit()
                QMessageBox.information(None, "Message Sent", "Your message has been sent successfully!")

        except sqlite3.Error as e:
                QMessageBox.critical(None, "Database Error", f"An error occurred: {e}")

        finally:
                conn.close()

    def navigate_to_home_from_sender(self, senderPage):
        """Navigate back to the login page."""
        self.home_ui = Ui_home()
        self.home_ui.setupUi(senderPage)
    def setupUi(self, senderPage):
        senderPage.setObjectName("senderPage")
        senderPage.resize(800, 600)
        senderPage.setMaximumSize(QtCore.QSize(1080, 1024))
        senderPage.setStyleSheet("background-color: rgb(255, 255, 255);")
        senderPage.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QtWidgets.QWidget(parent=senderPage)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 20, 751, 50))
        self.label.setStyleSheet("color: rgb(0, 0, 0);\n"
"font: 75 18pt \"Calibri\";\n"
"textAlign: center\n"
"")
        self.label.setScaledContents(False)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.start = QtWidgets.QPushButton(parent=self.centralwidget)
        self.start.setGeometry(QtCore.QRect(210, 450, 131, 41))
        self.start.setStyleSheet("\n"
"\n"
"QPushButton {\n"
"    background-color: #4CAF50;\n"
"    color: white;\n"
"    border-radius: 10px;\n"
"    padding: 5px 10px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #45a049;\n"
"}\n"
"")
        self.start.setObjectName("start")
        self.start.clicked.connect(lambda: self.handleSendMessage())
        self.subject = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.subject.setGeometry(QtCore.QRect(170, 90, 491, 40))
        self.subject.setStyleSheet("QLineEdit {\n"
"    border: 2px solid #4CAF50;\n"
"    border-radius: 5px;\n"
"    padding: 5px;\n"
"    background-color: #f9f9f9;\n"
"    color: #333333;\n"
"}")
        self.subject.setObjectName("subject")
        self.sender_mail = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.sender_mail.setGeometry(QtCore.QRect(170, 140, 491, 40))
        self.sender_mail.setStyleSheet("QLineEdit {\n"
"    border: 2px solid #4CAF50;\n"
"    border-radius: 5px;\n"
"    padding: 5px;\n"
"    background-color: #f9f9f9;\n"
"    color: #333333;\n"
"}")
        self.sender_mail.setObjectName("sender_mail")
        self.receiver_mail = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.receiver_mail.setGeometry(QtCore.QRect(170, 190, 491, 40))
        self.receiver_mail.setStyleSheet("QLineEdit {\n"
"    border: 2px solid #4CAF50;\n"
"    border-radius: 5px;\n"
"    padding: 5px;\n"
"    background-color: #f9f9f9;\n"
"    color: #333333;\n"
"}")
        self.receiver_mail.setObjectName("receiver_mail")
        self.message = QtWidgets.QPlainTextEdit(parent=self.centralwidget)
        self.message.setGeometry(QtCore.QRect(170, 270, 490, 150))
        self.message.setStyleSheet("QPlainTextEdit {\n"
"    border: 2px solid #4CAF50;\n"
"    border-radius: 5px;\n"
"    padding: 5px;\n"
"    background-color: #f9f9f9;\n"
"    color: #333333;\n"
"}")
        self.message = QtWidgets.QPlainTextEdit(parent=self.centralwidget)
        self.message.setGeometry(QtCore.QRect(170, 270, 490, 150))
        self.message.setStyleSheet("QPlainTextEdit {\n"
"    border: 2px solid #4CAF50;\n"
"    border-radius: 5px;\n"
"    padding: 5px;\n"
"    background-color: #f9f9f9;\n"
"    color: #333333;\n"
"}")
        self.message.setObjectName("message")
#         self.train_model = QtWidgets.QPushButton(parent=self.centralwidget)
#         self.train_model.setGeometry(QtCore.QRect(460, 450, 131, 41))
#         self.train_model.setStyleSheet("\n"
# "\n"
# "QPushButton {\n"
# "    background-color: #000;\n"
# "    color: white;\n"
# "    border-radius: 10px;\n"
# "    padding: 5px 10px;\n"
# "}\n"
# "QPushButton:hover {\n"
# "    background-color: #45a049;\n"
# "}\n"
# "")
        # self.train_model.setObjectName("train_model")
        self.BACKBTN = QtWidgets.QPushButton(parent=self.centralwidget)
        self.BACKBTN.setGeometry(QtCore.QRect(50, 20, 131, 41))
        self.BACKBTN.setStyleSheet("\n"
"\n"
"QPushButton {\n"
"    background-color: RED;\n"
"    color: white;\n"
"    border-radius: 10px;\n"
"    padding: 5px 10px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #45a049;\n"
"}\n"
"")
        self.BACKBTN.setObjectName("BACKBTN")
        self.BACKBTN.clicked.connect(lambda: self.navigate_to_home_from_sender(senderPage))
        senderPage.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(parent=senderPage)
        self.statusbar.setObjectName("statusbar")
        senderPage.setStatusBar(self.statusbar)

        self.retranslateUi(senderPage)
        QtCore.QMetaObject.connectSlotsByName(senderPage)

    def retranslateUi(self, senderPage):
        _translate = QtCore.QCoreApplication.translate
        senderPage.setWindowTitle(_translate("senderPage", "send message"))
        self.label.setText(_translate("senderPage", "SEND MAIL MESSAGE"))
        self.start.setAccessibleName(_translate("senderPage", "startbtn"))
        self.start.setText(_translate("senderPage", "SEND MESSAGE"))
        self.sender_mail.setPlaceholderText(_translate("senderPage", "From"))
        self.receiver_mail.setPlaceholderText(_translate("senderPage", "To"))
        self.subject.setPlaceholderText(_translate("senderPage", "Subject"))
        self.message.setPlaceholderText(_translate("senderPage", "Compose Email"))
        # self.train_model.setAccessibleName(_translate("senderPage", "trainbtn"))
        # self.train_model.setText(_translate("senderPage", "TRAIN MODEL"))
        self.BACKBTN.setAccessibleName(_translate("senderPage", "BACKBTN"))
        self.BACKBTN.setText(_translate("senderPage", "BACK"))
 
 
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    homePage = QtWidgets.QMainWindow()
    ui = Ui_home()
    ui.setupUi(homePage)
    homePage.show()
    sys.exit(app.exec())
