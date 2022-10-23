from kivy.app import App
from kivy.uix.boxlayout import BoxLayout


from admin.admin import AdminWindow
from signin.signin import SigninWindow
from system.system import SystemWindow
from home.home import HomeWindow

class MainWindow(BoxLayout):
    #creating widgets of the Different windows
    # to be displayed  
    signin_widget = SigninWindow()
    system_widget = SystemWindow()
    admin_widget = AdminWindow()
    home_widget = HomeWindow()


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #assigning each widget to its own screen 
        self.ids.scrn_home.add_widget(self.home_widget)
        self.ids.scrn_si.add_widget(self.signin_widget)
        self.ids.scrn_system.add_widget(self.system_widget)
        self.ids.scrn_admin.add_widget(self.admin_widget)

class MainApp(App):
    def build(self):
        return MainWindow()

if __name__ == '__main__':
    MainApp().run()