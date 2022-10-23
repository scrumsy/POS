from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.uix.modalview import ModalView
from kivy.uix.button import Button 


import re
import mysql.connector
from datetime import datetime

Builder.load_file('system/system.kv')

class Notify(ModalView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.size_hint = (.7,.7)

class SystemWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.mydb = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='password',
            database='gotogro'
        )
        self.mycursor = self.mydb.cursor()

        self.notify = Notify()

        self.cart = []
        self.qty = []
        self.ptotal = 0.00
        self.member_code = ''
        self.discount = 1
    
    def logout(self):
        self.parent.parent.current = 'scrn_si'
      
    #Function for updating the sales list when item is added to cart
    def update_purchases(self):
            pcode = self.ids.code_input.text
            iqty = self.ids.qty_input.text
            self.product_container = self.ids.products
            values = [pcode]

            self.mycursor.execute('Select * FROM products Where product_code =%s', values)
            target_code = self.mycursor.fetchall()

            #if no product code or incorrect code is entered then the system will do nothing 
            if target_code == []:
                pass
            else:
                #Condition checker to identify what item has been selected and add its details to the cart
                self.details = BoxLayout(size_hint_y = None,height=30, pos_hint={'top':1})
                self.product_container.add_widget(self.details)

                if iqty != '':
                    qty = Label(text=iqty, size_hint_x=.1, color=(.78,.27,.89,1))
                else:
                    qty = Label(text='1', size_hint_x=.1, color=(.78,.27,.89,1))
                code = Label(text=pcode, size_hint_x=.3, color=(.78,.27,.89,1) )
                name = Label(text=str(target_code[0][2]), size_hint_x=.3, color=(.78,.27,.89,1) )
                price = Label(text=str(target_code[0][3]), size_hint_x=.1, color=(.78,.27,.89,1) )
                total_format = float(qty.text) * float(price.text)
                total_format = round(total_format, 2)
                total = Label(text=str(total_format), size_hint_x=.2, color=(.78,.27,.89,1) )
        
                self.details.add_widget(qty)
                self.details.add_widget(code)
                self.details.add_widget(name)
                self.details.add_widget(price)
                self.details.add_widget(total)

                #update Preview
                #product name
                pname=name.text
                #Product Price
                pprice=float(price.text)
                #Quantity of product to purchase
                pqty= qty.text
                
                self.ptotal += float(total.text) *self.discount
                self.ptotal = round(self.ptotal,2)
                

                #Formating for the total price for Receipt
                purchase_total = '`\n\nTotal\t\t\t\t\t\t' + str(self.ptotal)
                if self.discount is not 1:
                    purchase_total = '`\n\nTotal\t\t\t\t\t\t' + str(self.ptotal) + '\n*Discount is being Applied*'
                self.ids.cur_product.text = pname
                self.ids.cur_price.text = str(pprice)
                self.preview = self.ids.receipt_preview
                prev_text = self.preview.text
                _prev = prev_text.find('`')
                if _prev>0:
                    prev_text = prev_text[:_prev]

                ptarget = -1

                for i,c in enumerate(self.cart):
                    if c == pcode:
                        ptarget = i

                if ptarget >= 0:
                    pqty = self.qty[ptarget]+int(qty.text)
                    self.qty[ptarget] = pqty
                    expr='%s\t\tx\d\t'%(pname)
                    rexpr = pname+'\t\tx'+str(pqty)+'\t'
                    print("This should be pqty:")
                    print(pqty)
                    new_text = re.sub(expr,rexpr,prev_text)
                    self.preview.text = new_text + purchase_total
                    print(new_text + purchase_total)
                else:
                    self.cart.append(pcode)
                    self.qty.append(int(qty.text))
                    new_preview = '\n'.join([prev_text, pname+'\t\tx'+str(pqty)+'\t\t'+str(pprice), purchase_total])
                    self.preview.text = new_preview
                    print(new_preview)

                self.ids.qty_input.text = str(pqty)
                self.ids.code_input.text = str(target_code[0][1])
                self.ids.pname_input.text = str(target_code[0][2])
                self.ids.price_input.text = str(target_code[0][3])
                total_format = float(pqty) * float(pprice)
                total_format = round(total_format, 2)
                self.ids.total_input.text = str(total_format)

               

    def create_sale(self):
        scode =  self.ids.sale_code.text
        mcode = self.ids.member_code.text


        if scode =='':
            self.notify.add_widget(Label(text='[color=#FF0000][b]Sales Code Required[/b][/color]', markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch,2)
        elif mcode == '':
            self.notify.add_widget(Label(text='[color=#FF0000][b]Member Code Required[/b][/color]', markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch,2)
        elif self.cart == []:
            self.notify.add_widget(Label(text='[color=#FF0000][b]Products are required[/b][/color]', markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch,2)
        else:
            #insert each item bought by the member into the sales database
            while self.cart != []:
                pcode = self.cart.pop()
                qty = self.qty.pop()
                sql = 'INSERT INTO sales(sale_code, member_code, product_code, quantity, date) VALUES(%s,%s,%s,%s,%s)'
                values = [scode,mcode,pcode,qty,datetime.now()]

                self.mycursor.execute(sql,values)
                self.mydb.commit()
        

            #clear all input fields and reset values for next sale 
            self.reset_sale()

   #when the button is clicked the field to enter code of item to remove will be displayed 
   #look at admin.py for example 
    def remove_item_field(self):
        target = self.ids.sys_fields
        target.clear_widgets()
        crud_item = TextInput(hint_text='Item Code')
        crud_submit = Button(text='Remove', size_hint_x=None, width=100, on_release=lambda x:
        self.remove_item(crud_item.text))

        target.add_widget(crud_item)
        target.add_widget(crud_submit)

    # implement remove item function 
    # remove the item from the cart 
    # wont be able to remove the widget from the display but the acctual functionality will work 
    def remove_item(self, item):
        remove = self.cart.index(item)
        print("Item is:")
        print(item)
        print("Index of item is:")
        print(remove)

        print("List before removal:")
        print(self.cart)
        print(self.qty)

        del self.cart[remove]
        del self.qty[remove]

        print("List after removal:")
        print(self.cart)
        print(self.qty)
    
    def reset_sale(self):
        #clear all input fields and reset values for next sale 
        self.ids.sale_code.text = ''
        self.ids.member_code.text = ''
        self.ids.qty_input.text = ''
        self.ids.code_input.text = ''
        self.ids.pname_input.text = ''
        self.ids.price_input.text = ''
        self.ids.total_input.text = ''

        self.details.clear_widgets()
        self.product_container.clear_widgets()
        self.preview.text = 'GotoGro\n 10 Hawthron Road\n Tel: 1300 555 333\n Receipt No: \n Date: \n\n'
        self.ids.cur_product.text = 'No Current Product'
        self.ids.cur_price.text = 'Price'

        self.cart = []
        self.qty = []
        self.ptotal = 0.00


        
    def apply_discount(self):
        #depnding on the code entered discount the total amount of the sale 
        if self.ids.discount.text == '30OFF':
            self.ptotal = self.ptotal * 0.7
            self.discount = 0.7
        elif self.ids.discount.text == '20OFF':
            self.ptotal = self.ptotal * 0.8
            self.discount = 0.8
        elif self.ids.discount.text == '10OFF':
            self.ptotal = self.ptotal * 0.9
            self.discount = 0.9

        print("Discount is being applied")
        print("New total is:")
        print(self.ptotal)
        print("New Discount is:")
        print(self.discount)



    def killswitch(self,dtx):
        self.notify.dismiss()
        self.notify.clear_widgets()
               

class SystemApp(App):
    def build(self):
        return SystemWindow()

if __name__=="__main__":
    oa = SystemApp()
    oa.run()