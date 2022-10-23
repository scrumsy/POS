from kivy.app import App
from kivy.uix.boxlayout import BoxLayout 
from kivy.lang import Builder

import mysql.connector
import hashlib


Builder.load_file('signin/signin.kv')

class SigninWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
            
    def validate_user(self):
        # Connect to the database 
        self.mydb = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='password',
            database='gotogro'
        )
        self.mycursor = self.mydb.cursor()
        

        username = self.ids.username_field.text
        password = self.ids.pwd_field.text
        info = self.ids.info

        self.ids.username_field.text = ''
        self.ids.pwd_field.text = ''


        
        #condition checker to validate the username and password 
        if username == '' or password == '':
            info.text = '[color=#FF0000]username and/or password required[/color]'
        else:
            sql = 'Select * From employees Where user_name = %s'
            value = [username]
            self.mycursor.execute(sql, value)
            user = self.mycursor.fetchall() 

            #Check to see if a user was returned from the database
            if user == []:
                info.text = '[color=FF0000]User not found[/color]'

            #If user was returned then check to see if the password is correct    
            else:
                password = hashlib.sha256(password.encode()).hexdigest()
                    
                                
                #If password is correct then redirect the user to its designation page(Admin or Normal Staff)
                if password == user[0][4]:
                    des = user[0][5]
                    info.text = ''
                    self.parent.parent.parent.ids.scrn_system.children[0].ids.loggedin_user.text = username
                    if des == 'Manager':
                        self.parent.parent.current = 'scrn_admin'
                    else:
                        self.parent.parent.current = 'scrn_system'
                #If password is wrong then throw error message
                else:

                    info.text = '[color=FF0000]Invalid Username or Password[/color]'
    def home(self):
        self.parent.parent.current = 'scrn_home'

class SigninApp(App):
    def build(self):
        return SigninWindow()

if __name__=="__main__":
    sa = SigninApp()
    sa.run()