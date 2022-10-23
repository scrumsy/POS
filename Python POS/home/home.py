from kivy.app import App
from kivy.uix.boxlayout import BoxLayout 
from kivy.lang import Builder



Builder.load_file('home/home.kv')

class HomeWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def login(self):
         self.parent.parent.current = 'scrn_si'
            
  
class HomeApp(App):
    def build(self):
        return HomeWindow()

if __name__=="__main__":
    sa = HomeApp()
    sa.run()