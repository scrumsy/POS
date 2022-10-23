from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.modalview import ModalView
from kivy.clock import Clock
from kivy.uix.label import Label

from collections import OrderedDict

from testutils.datatable import DataTable
import mysql.connector
import hashlib
from datetime import datetime

import pandas as pd
import matplotlib.pyplot as plt
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg as FCK

Builder.load_file('admin/admin.kv')

class Notify(ModalView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.size_hint = (.7,.7)


class AdminWindow(BoxLayout):
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

        sql = 'SELECT * FROM products'
        self.mycursor.execute(sql)
        products = self.mycursor.fetchall()

        product_code = []
        product_name = []
        spinvals = []

        for product in products:
            product_code.append(product[1])
            name = product[2]
            if len(name) > 30:
                name = name[:30] + '...'
            product_name.append(name)

        for x in range(len(product_code)):
            line = ' | '.join([product_code[x], product_name[x]])
            spinvals.append(line)

        self.ids.target_product.values = spinvals

        #Display employees
        content = self.ids.scrn_contents
        employees = self.get_employees()
        usertable = DataTable(table=employees)
        content.add_widget(usertable)
    

        #Display Products
        product_scrn = self.ids.scrn_product_contents
        products = self.get_products()
        prod_table = DataTable(table=products)
        product_scrn.add_widget(prod_table)

        #Display Members
        member_scrn = self.ids.scrn_member_contents
        members = self.get_members()
        member_table = DataTable(table=members)
        member_scrn.add_widget(member_table)

        #Display Sales
        sale_scrn = self.ids.scrn_sale_contents
        sales = self.get_sales()
        sale_table = DataTable(table=sales)
        sale_scrn.add_widget(sale_table)
    
    def logout(self):
        self.parent.parent.current = 'scrn_si'


    #### Field inputs are defined here for Add,Update, Remove ####

    def add_employee_fields(self):
        target = self.ids.ops_fields
        target.clear_widgets()
        crud_first = TextInput(hint_text = 'First Name')
        crud_last = TextInput(hint_text = 'Last Name')
        crud_user = TextInput(hint_text = 'Username')
        crud_pwd = TextInput(hint_text = 'Password')
        crud_role = Spinner(text='Employee', values=['Employee','Manager'])
        crud_submit = Button(text='Add', size_hint_x=None, width=100, on_release=lambda x:
        self.add_employee(crud_first.text, crud_last.text, crud_user.text, crud_pwd.text, crud_role.text))
        target.add_widget(crud_first)
        target.add_widget(crud_last)
        target.add_widget(crud_user)
        target.add_widget(crud_pwd)
        target.add_widget(crud_role)
        target.add_widget(crud_submit)

    def add_member_fields(self):
        target = self.ids.ops_fields_m
        target.clear_widgets()
        crud_mcode = TextInput(hint_text = 'Member Code')
        crud_first = TextInput(hint_text = 'First Name')
        crud_last = TextInput(hint_text = 'Last Name')
        crud_email = TextInput(hint_text = 'Email')
        crud_number = TextInput(hint_text = "Phone Number")
        crud_submit = Button(text='Add', size_hint_x=None, width=100, on_release=lambda x:
        self.add_member(crud_mcode.text, crud_first.text, crud_last.text, crud_email.text, crud_number.text))
        target.add_widget(crud_mcode)
        target.add_widget(crud_first)
        target.add_widget(crud_last)
        target.add_widget(crud_email)
        target.add_widget(crud_number)
        target.add_widget(crud_submit)

    def add_product_fields(self):
        target = self.ids.ops_fields_p
        target.clear_widgets()

        crud_code = TextInput(hint_text="Product Code")
        crud_name = TextInput(hint_text="Product Name")
        crud_price = TextInput(hint_text="Product Price")
        crud_stock = TextInput(hint_text="Product In Stock")
        crud_sold = TextInput(hint_text="Product Sold")
        crud_order = TextInput(hint_text="Product Order")
        crud_purchase = TextInput(hint_text="Product Last Purchase")

        crud_submit = Button(text='Add', size_hint_x=None, width=100, on_release=lambda x:
        self.add_product(crud_code.text, crud_name.text,crud_price.text, crud_stock.text, 
        crud_sold.text, crud_order.text, crud_purchase.text))
        target.add_widget(crud_code)
        target.add_widget(crud_name)
        target.add_widget(crud_price)
        target.add_widget(crud_stock)
        target.add_widget(crud_sold)
        target.add_widget(crud_order)
        target.add_widget(crud_purchase)
        target.add_widget(crud_submit)

    def update_employee_fields(self):
        target = self.ids.ops_fields
        target.clear_widgets()
        crud_first = TextInput(hint_text = 'First Name')
        crud_last = TextInput(hint_text = 'Last Name')
        crud_user = TextInput(hint_text = 'Username')
        crud_pwd = TextInput(hint_text = 'Password')
        crud_role = Spinner(text='Employee', values=['Employee','Manager'])
        crud_submit = Button(text='Update', size_hint_x=None, width=100, on_release=lambda x:
        self.update_employee(crud_first.text, crud_last.text, crud_user.text, crud_pwd.text, crud_role.text))
        target.add_widget(crud_first)
        target.add_widget(crud_last)
        target.add_widget(crud_user)
        target.add_widget(crud_pwd)
        target.add_widget(crud_role)
        target.add_widget(crud_submit)

    def update_member_fields(self):
        target = self.ids.ops_fields_m
        target.clear_widgets()
        crud_mcode = TextInput(hint_text = 'Member Code')
        crud_first = TextInput(hint_text = 'First Name')
        crud_last = TextInput(hint_text = 'Last Name')
        crud_email = TextInput(hint_text = 'Email')
        crud_number = TextInput(hint_text = "Phone Number")
        crud_submit = Button(text='Update', size_hint_x=None, width=100, on_release=lambda x:
        self.update_member(crud_mcode.text, crud_first.text, crud_last.text, crud_email.text, crud_number.text))
        target.add_widget(crud_mcode)
        target.add_widget(crud_first)
        target.add_widget(crud_last)
        target.add_widget(crud_email)
        target.add_widget(crud_number)
        target.add_widget(crud_submit)

    def update_sale_fields(self):
        target = self.ids.ops_fields_s
        target.clear_widgets()
        crud_scode = TextInput(hint_text = 'Sale Code')
        crud_mcode = TextInput(hint_text = 'Member Code')
        crud_pcode = TextInput(hint_text = 'Product Code')
        crud_qty = TextInput(hint_text = 'Quantity')
        crud_date = TextInput(hint_text = "Date")
        crud_submit = Button(text='Update', size_hint_x=None, width=100, on_release=lambda x:
        self.update_sale(crud_scode.text, crud_mcode.text, crud_pcode.text, crud_qty.text, crud_date.text))
        target.add_widget(crud_scode)
        target.add_widget(crud_mcode)
        target.add_widget(crud_pcode)
        target.add_widget(crud_qty)
        target.add_widget(crud_date)
        target.add_widget(crud_submit)

    def update_product_fields(self):
        target = self.ids.ops_fields_p
        target.clear_widgets()

        crud_code = TextInput(hint_text="Product Code")
        crud_name = TextInput(hint_text="Product Name")
        crud_price = TextInput(hint_text="Product Price")
        crud_stock = TextInput(hint_text="Product In Stock")
        crud_sold = TextInput(hint_text="Product Sold")
        crud_order = TextInput(hint_text="Product Order")
        crud_purchase = TextInput(hint_text="Product Last Purchase")

        crud_submit = Button(text='Update', size_hint_x=None, width=100, on_release=lambda x:
        self.update_product(crud_code.text, crud_name.text, crud_price.text, crud_stock.text, 
        crud_sold.text, crud_order.text, crud_purchase.text))
        target.add_widget(crud_code)
        target.add_widget(crud_name)
        target.add_widget(crud_price)
        target.add_widget(crud_stock)
        target.add_widget(crud_sold)
        target.add_widget(crud_order)
        target.add_widget(crud_purchase)
        target.add_widget(crud_submit)  


    def remove_employee_fields(self):
        target = self.ids.ops_fields
        target.clear_widgets()
        crud_user = TextInput(hint_text='User Name')
        crud_submit = Button(text='Remove', size_hint_x=None, width=100, on_release=lambda x:
        self.remove_employee(crud_user.text))

        target.add_widget(crud_user)
        target.add_widget(crud_submit)

    def remove_product_fields(self):
        target = self.ids.ops_fields_p
        target.clear_widgets()
        crud_code = TextInput(hint_text='Product Code')
        crud_submit = Button(text='Remove', size_hint_x=None, width=100, on_release=lambda x:
        self.remove_product(crud_code.text))

        target.add_widget(crud_code)
        target.add_widget(crud_submit)

    def remove_sale_fields(self):
        target = self.ids.ops_fields_s
        target.clear_widgets()
        crud_code = TextInput(hint_text='Sale Code')
        crud_submit = Button(text='Remove', size_hint_x=None, width=100, on_release=lambda x:
        self.remove_sale(crud_code.text))

        target.add_widget(crud_code)
        target.add_widget(crud_submit)

    def remove_member_fields(self):
        target = self.ids.ops_fields_m
        target.clear_widgets()
        crud_code = TextInput(hint_text='Member Code')
        crud_submit = Button(text='Remove', size_hint_x=None, width=100, on_release=lambda x:
        self.remove_member(crud_code.text))

        target.add_widget(crud_code)
        target.add_widget(crud_submit)

    # Function to get the employees from the database and order them 
    # into a table format
    def get_employees(self):
        _employees = OrderedDict()
        _employees['first_names'] = {}
        _employees['last_names'] = {}
        _employees['user_names'] = {}
        _employees['passwords'] = {}
        _employees['role'] = {}


        first_names = []
        last_names = []
        user_names = []
        passwords = []
        role = []
        
        sql = 'SELECT * FROM employees'
        self.mycursor.execute(sql)
        employees = self.mycursor.fetchall()

        for employee in employees:
            first_names.append(employee[1])
            last_names.append(employee[2])
            user_names.append(employee[3])
            pwd = employee[4]
            if len(pwd) > 10:
                pwd = pwd[:10] + '...'
            passwords.append(pwd)
            role.append(employee[5])
        
        employees_length = len(first_names)
        idx = 0
        while idx < employees_length:
            _employees['first_names'][idx] = first_names[idx]
            _employees['last_names'][idx] = last_names[idx]
            _employees['user_names'][idx] = user_names[idx]
            _employees['passwords'][idx] = passwords[idx]
            _employees['role'][idx] = role[idx]

            idx += 1
        return _employees

    # Function to get the products from the database and order them 
    # into a table format
    def get_products(self):
        _prodcuts = OrderedDict()
        _prodcuts['product_code'] = {}
        _prodcuts['product_name'] = {}
        _prodcuts['product_price'] = {}
        _prodcuts['in_stock'] = {}
        _prodcuts['sold'] = {}
        _prodcuts['order'] = {}
        _prodcuts['last_purchase'] = {}

        product_code = []
        product_name = []
        product_price = []
        in_stock = []
        sold = []
        order = []
        last_purchase = []

        sql = 'SELECT * FROM products'
        self.mycursor.execute(sql)
        products = self.mycursor.fetchall()


        for product in products:
            product_code.append(product[1])
            name = product[2]
            if len(name) > 10:
                name = name[:10] + '...'
            product_name.append(name)
            product_price.append(product[3])
            in_stock.append(product[4])
            try:
                sold.append(product[5])
            except KeyError:
                sold.append('')
            try:
                order.append(product[6])
            except KeyError:
                order.append('')
            try:
                last_purchase.append(product[7])
            except KeyError:
                last_purchase.append('')
        # print(role)
        products_length = len(product_code)
        idx = 0
        while idx < products_length:
            _prodcuts['product_code'][idx] = product_code[idx]
            _prodcuts['product_name'][idx] = product_name[idx]
            _prodcuts['product_price'][idx] = product_price[idx]
            _prodcuts['in_stock'][idx] = in_stock[idx]
            _prodcuts['sold'][idx] = sold[idx]
            _prodcuts['order'][idx] = order[idx]
            _prodcuts['last_purchase'][idx] = last_purchase[idx]
           

            idx += 1
        
        return _prodcuts


    # Function to get the members from the database and order them 
    # into a table format
    def get_members(self):
        _members = OrderedDict()
        _members['member_code'] = {}
        _members['first_names'] = {}
        _members['last_names'] = {}      
        _members['email'] = {}
        _members['phone_number'] = {}


        member_code = []
        first_names = []
        last_names = []
        email = []
        phone_number = []
        
        sql = 'SELECT * FROM members'
        self.mycursor.execute(sql)
        members = self.mycursor.fetchall()

        for member in members:
            member_code.append(member[1])
            first_names.append(member[2])
            last_names.append(member[3])
            email.append(member[4])
            phone_number.append(member[5])
        
        members_length = len(first_names)
        idx = 0
        while idx < members_length:
            _members['member_code'][idx] = member_code[idx]
            _members['first_names'][idx] = first_names[idx]
            _members['last_names'][idx] = last_names[idx]
            _members['email'][idx] = email[idx]
            _members['phone_number'][idx] = phone_number[idx]

            idx += 1
        return _members

    # Function to get the Sales from the database and order them 
    # into a table format
    def get_sales(self):
        _sales = OrderedDict()
        _sales['sale_code'] = {}
        _sales['member_code'] = {}
        _sales['product_code'] = {}
        _sales['quantity'] = {}
        _sales['date'] = {}


        sale_code = []
        member_code = []
        product_code = []
        quantity = []
        date = []
        
        sql = 'SELECT * FROM sales'
        self.mycursor.execute(sql)
        sales = self.mycursor.fetchall()

        for sale in sales:
            sale_code.append(sale[1])
            member_code.append(sale[2])
            product_code.append(sale[3])
            quantity.append(sale[4])
            date.append(sale[5])
        
        sales_length = len(sale_code)
        idx = 0
        while idx < sales_length:
            _sales['sale_code'][idx] = sale_code[idx]
            _sales['member_code'][idx] = member_code[idx]
            _sales['product_code'][idx] = product_code[idx]
            _sales['quantity'][idx] = quantity[idx]
            _sales['date'][idx] = date[idx]

            idx += 1
        return _sales

    def killswitch(self,dtx):
        self.notify.dismiss()
        self.notify.clear_widgets()

    #### Functions are defined here for Add, Update, Remove ####

    def add_employee(self, first, last, user, pwd,role):
        content = self.ids.scrn_contents
        content.clear_widgets()
        pwd = hashlib.sha256(pwd.encode()).hexdigest()
        sql = 'INSERT INTO employees(first_name, last_name, user_name, password, role, date) VALUES(%s,%s,%s,%s,%s,%s)'
        values = [first,last,user,pwd,role,datetime.now()]
        
        if first == '' or last == '' or user == '' or pwd == '':
            self.notify.add_widget(Label(text='[color=#FF0000][b]All Fields Required[/b][/color]', markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch,2)
        else:           
            self.mycursor.execute(sql,values)
            self.mydb.commit()
        

        employees = self.get_employees()
        usertable = DataTable(table=employees)
        content.add_widget(usertable)


    def add_member(self,code, first, last, email, phone):
        content = self.ids.scrn_member_contents
        content.clear_widgets()

        sql = 'INSERT INTO members(member_code, first_name, last_name, email, phone_number, date) VALUES(%s,%s,%s,%s,%s,%s)'
        values = [code,first,last,email,phone,datetime.now()]
        
        if first == '' or last == '' or email == '' or phone == '' or code == '':
            self.notify.add_widget(Label(text='[color=#FF0000][b]All Fields Required[/b][/color]', markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch,2)
        else:    
            if code.isnumeric():       
                self.mycursor.execute(sql,values)
                self.mydb.commit()
            else:
                self.notify.add_widget(Label(text='[color=#FF0000][b]Member Code must be only numbers[/b][/color]', markup=True))
                self.notify.open()
                Clock.schedule_once(self.killswitch,2)
        

        members = self.get_members()
        usertable = DataTable(table=members)
        content.add_widget(usertable)


    def add_product(self, code, name, price, stock, sold, order,purchase):
        content = self.ids.scrn_product_contents
        content.clear_widgets()

        sql = 'INSERT INTO products(product_code, product_name, product_price, in_stock, sold, ordered, last_purchase) VALUES(%s,%s,%s,%s,%s,%s,%s)'
        values = [code,name,price,stock,sold,order,purchase]

        if code == '' or name == '' or price == '' or stock == '':
            self.notify.add_widget(Label(text='[color=#FF0000][b]All Fields Required[/b][/color]', markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch,2)
        else:
            if code.isnumeric():             
                self.mycursor.execute(sql,values)
                self.mydb.commit()
            else:
                self.notify.add_widget(Label(text='[color=#FF0000][b]Product Code must be only numbers[/b][/color]', markup=True))
                self.notify.open()
                Clock.schedule_once(self.killswitch,2)

        products = self.get_products()
        prod_table = DataTable(table=products)
        content.add_widget(prod_table)

    def update_member(self,code, first, last, email, phone):
        content = self.ids.scrn_member_contents
        content.clear_widgets()

        sql = 'Update members SET member_code=%s, first_name=%s, last_name=%s, email=%s, phone_number=%s WHERE member_code = %s' 
        values = [code,first,last,email,phone,code]
        
        if code == '':
            self.notify.add_widget(Label(text='[color=#FF0000][b]Member code is Required[/b][/color]', markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch,2)
        else:      
            sqlverify = 'Select * from members Where member_code = %s'
            value = [code]
            self.mycursor.execute(sqlverify, value)
            memberverify = self.mycursor.fetchall()

            if memberverify == []:
                self.notify.add_widget(Label(text='[color=#FF0000][b]Member is not found[/b][/color]', markup=True))
                self.notify.open()
                Clock.schedule_once(self.killswitch,2)
            else:
                for x in memberverify:                 
                    if code == '':
                        code = x[1]
                    if first == '':
                        first = x[2]
                    if last == '':
                        last = x[3]
                    if email == '':
                        email = x[4]
                    if phone == '':
                        phone = x[5]

                values = [code,first,last,email,phone,code]
                self.mycursor.execute(sql,values)
                self.mydb.commit()

        members = self.get_members()
        usertable = DataTable(table=members)
        content.add_widget(usertable)

    def update_sale(self,scode, mcode, pcode, qty, date):
        content = self.ids.scrn_sale_contents
        content.clear_widgets()

        sql = 'Update sales SET sale_code=%s, member_code=%s, product_code=%s, quantity=%s, date=%s WHERE sale_code = %s' 
        values = [scode,mcode,pcode,qty,date,scode]
        
        if scode == '':
            self.notify.add_widget(Label(text='[color=#FF0000][b]Sale code is Required[/b][/color]', markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch,2)
        else:      
            sqlverify = 'Select * from sales Where sale_code = %s'
            value = [scode]
            self.mycursor.execute(sqlverify, value)
            saleverify = self.mycursor.fetchall()

            if saleverify == []:
                self.notify.add_widget(Label(text='[color=#FF0000][b]Sale is not found[/b][/color]', markup=True))
                self.notify.open()
                Clock.schedule_once(self.killswitch,2)
            else:
                for x in saleverify:                 
                    if scode == '':
                        scode = x[1]
                    if mcode == '':
                        mcode = x[2]
                    if pcode == '':
                        pcode = x[3]
                    if qty == '':
                        qty = x[4]
                    if date == '':
                        date = x[5]

                values = [scode,mcode,pcode,qty,date,scode]
                self.mycursor.execute(sql,values)
                self.mydb.commit()

        sales = self.get_sales()
        salestable = DataTable(table=sales)
        content.add_widget(salestable)

    def update_employee(self, first, last, user, pwd,role):
        content = self.ids.scrn_contents
        content.clear_widgets()
        pwd = hashlib.sha256(pwd.encode()).hexdigest()
        sql = 'Update employees SET first_name=%s, last_name=%s, user_name=%s, password=%s, role=%s WHERE user_name = %s'
        values = [first,last,user,pwd,role,user]

        if user == '':
            self.notify.add_widget(Label(text='[color=#FF0000][b]Username is required to update[/b][/color]', markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch,2)
        else: 
            sqlverify = 'Select * from employees Where user_name = %s'
            value = [user]  
            self.mycursor.execute(sqlverify,value)     
            userverify = self.mycursor.fetchall()
            
            if userverify == []:
                self.notify.add_widget(Label(text='[color=#FF0000][b]Username is not found[/b][/color]', markup=True))
                self.notify.open()
                Clock.schedule_once(self.killswitch,2)
            else:
                for x in userverify:                 
                    if first == '':
                        first = x[1]
                    if last == '':
                        last = x[2]
                    if pwd == '':
                        pwd = x[4]
                    if role == '':
                        role = x[5]

                values = [first,last,user,pwd,role,user]
    
                self.mycursor.execute(sql,values)
                self.mydb.commit()
        
        employees = self.get_employees()
        usertable = DataTable(table=employees)
        content.add_widget(usertable)
    
    

    def update_product(self, code, name, price, stock, sold, order,purchase):
        content = self.ids.scrn_product_contents
        content.clear_widgets()

        sql = 'Update products SET product_code=%s, product_name=%s, product_price=%s, in_stock=%s, sold=%s, ordered=%s, last_purchase=%s WHERE product_code=%s'
        values = [code,name,price,stock,sold,order,purchase,code]

        if code == '':
            self.notify.add_widget(Label(text='[color=#FF0000][b]Product Code is required to update[/b][/color]', markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch,2)
        else:
            sqlverify = 'Select * from products Where product_code = %s'
            value = [code]  
            self.mycursor.execute(sqlverify,value)     
            productverify = self.mycursor.fetchall()
            
            if productverify == []:
                self.notify.add_widget(Label(text='[color=#FF0000][b]Product Code is not found[/b][/color]', markup=True))
                self.notify.open()
                Clock.schedule_once(self.killswitch,2)
            else:
                for x in productverify:                 
                    if code == '':
                        code = x[1]
                    if name == '':
                        name = x[2]
                    if price == '':
                        price = x[3]
                    if stock == '':
                        stock = x[4]
                    if sold == '':
                        sold = x[5]
                    if order == '':
                        order = x[6]
                    if purchase == '':
                        purchase = x[7]

                values = [code,name,price,stock,sold,order,purchase,code]
    
                self.mycursor.execute(sql,values)
                self.mydb.commit()
           

        products = self.get_products()
        prod_table = DataTable(table=products)
        content.add_widget(prod_table)

    def remove_employee(self,user):
        content = self.ids.scrn_contents
        content.clear_widgets()

        sql = 'DELETE FROM employees WHERE user_name = %s'
        values = [user]

        if user == '':
            self.notify.add_widget(Label(text='[color=#FF0000][b]Username is required to remove user[/b][/color]', markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch,2)
        else:
            sqlverify = 'Select * from employees Where user_name = %s'
            value = [user]  
            self.mycursor.execute(sqlverify,value)     
            userverify = self.mycursor.fetchall()
            
            if userverify == []:
                self.notify.add_widget(Label(text='[color=#FF0000][b]Username is not found[/b][/color]', markup=True))
                self.notify.open()
                Clock.schedule_once(self.killswitch,2)
            else:
                self.mycursor.execute(sql,values)
                self.mydb.commit()

        employees = self.get_employees()
        usertable = DataTable(table=employees)
        content.add_widget(usertable)

    def remove_product(self,code):
        content = self.ids.scrn_product_contents
        content.clear_widgets()

        sql = 'DELETE FROM products WHERE product_code = %s'
        values = [code]

        if code == '':
            self.notify.add_widget(Label(text='[color=#FF0000][b]Product Code is required to remove product[/b][/color]', markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch,2)
        else:
            sqlverify = 'Select * from products Where product_code = %s'
            value = [code]  
            self.mycursor.execute(sqlverify,value)     
            productverify = self.mycursor.fetchall()
            
            if productverify == []:
                self.notify.add_widget(Label(text='[color=#FF0000][b]Product Code is not found[/b][/color]', markup=True))
                self.notify.open()
                Clock.schedule_once(self.killswitch,2)
            else:
                self.mycursor.execute(sql,values)
                self.mydb.commit()

        products = self.get_products()
        prod_table = DataTable(table=products)
        content.add_widget(prod_table)
        
    def remove_member(self,code):
        content = self.ids.scrn_member_contents
        content.clear_widgets()

        sql = 'DELETE FROM members WHERE member_code = %s'
        values = [code]

        if code == '':
            self.notify.add_widget(Label(text='[color=#FF0000][b]Member Code is required to remove product[/b][/color]', markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch,2)
        else:
            sqlverify = 'Select * from members Where member_code = %s'
            value = [code]  
            self.mycursor.execute(sqlverify,value)     
            memberverify = self.mycursor.fetchall()
            
            if memberverify == []:
                self.notify.add_widget(Label(text='[color=#FF0000][b]Member Code is not found[/b][/color]', markup=True))
                self.notify.open()
                Clock.schedule_once(self.killswitch,2)
            else:
                self.mycursor.execute(sql,values)
                self.mydb.commit()

        members = self.get_products()
        member_table = DataTable(table=members)
        content.add_widget(member_table)

    def remove_sale(self,code):
        content = self.ids.scrn_sale_contents
        content.clear_widgets()

        sql = 'DELETE FROM sales WHERE sale_code = %s'
        values = [code]

        if code == '':
            self.notify.add_widget(Label(text='[color=#FF0000][b]Sale Code is required to remove sale[/b][/color]', markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch,2)
        else:
            sqlverify = 'Select * from sales Where sale_code = %s'
            value = [code]  
            self.mycursor.execute(sqlverify,value)     
            saleverify = self.mycursor.fetchall()
            
            if saleverify == []:
                self.notify.add_widget(Label(text='[color=#FF0000][b]Sale Code is not found[/b][/color]', markup=True))
                self.notify.open()
                Clock.schedule_once(self.killswitch,2)
            else:
                self.mycursor.execute(sql,values)
                self.mydb.commit()

        sales = self.get_sales()
        sale_table = DataTable(table=sales)
        content.add_widget(sale_table)


    def sale_report_fields(self):
        target = self.ids.ops_fields_s
        target.clear_widgets()
        start_date = TextInput(hint_text='Start Date')
        end_date = TextInput(hint_text='End Date')
        submit = Button(text='Create', size_hint_x=None, width=100, on_release=lambda x:
        self.sale_report(start_date.text, end_date.text))

        target.add_widget(start_date)
        target.add_widget(end_date)
        target.add_widget(submit)

    # Create CSV report 
    def sale_report(self,sdate,edate):
        sql = 'SELECT product_code, SUM(quantity) as quantity FROM sales WHERE date BETWEEN %s and %s Group By product_code,date'
        values = [sdate,edate]
        self.mycursor.execute(sql, values)

        #get file for csv 
        f = open(r'C:\Users\paaka\OneDrive\Documents\Github\repo\Python POS\admin\sales.csv', 'w')
        
        holder = self.mycursor.fetchall()
        colnames = [desc[0] for desc in self.mycursor.description]

        df = pd.DataFrame(holder)
        print(holder)
        #write to csv file 
        df.to_csv(f, index = False, header = colnames)

        #pop-up messsage
        self.notify.add_widget(Label(text='[color=#FF0000][b]Report has been created![/b][/color]', markup=True))
        self.notify.open()
        Clock.schedule_once(self.killswitch,2)



    # Function for changing between the different views in the admin dashboard
    def change_screen(self, instance):
            # depending on the name of the selected text view 
            # the corresponding page will be displayed
            if instance.text == 'Manage Products':
                self.ids.scrn_mngr.current = 'scrn_product_content'
            elif instance.text == 'Manage Employees':
                self.ids.scrn_mngr.current = 'scrn_content'
            elif instance.text == 'Manage Members':
                self.ids.scrn_mngr.current = 'scrn_member_content'
            elif instance.text == 'Manage Sales':
                self.ids.scrn_mngr.current = 'scrn_sale_content'
            else:
                self.ids.scrn_mngr.current = 'scrn_analysis'

    #function for displaying the data from a csv file onto a graph 
    def view_stats(self):
        plt.cla()

        #clear widgets so new graphs dont stack 
        self.ids.analysis_res.clear_widgets()
        target_product = self.ids.target_product.text
        target = target_product[:target_product.find(' | ')]
        name = target_product[target_product.find(' | '):]

        # read data from file location 
        df = pd.read_csv(r'C:\Users\paaka\OneDrive\Documents\Github\repo\Python POS\admin\sales.csv')
        purchases = []
        dates = []
        count = 0

        for x in range(len(df)):
            if str(df.product_code[x]) == target:
                purchases.append(df.quantity[x])
                dates.append(count)
                count += 1

        #create graph
        plt.bar(dates, purchases, color='pink', label=name)
        plt.ylabel('Total Purchases')
        plt.xlabel('day')

        #display graph
        self.ids.analysis_res.add_widget(FCK(plt.gcf()))


class AdminApp(App):
    def build(self):

        return AdminWindow()



if __name__=='__main__':
    AdminApp().run()

