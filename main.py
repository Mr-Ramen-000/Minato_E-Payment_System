import os
from tkinter import messagebox, filedialog
import random
import datetime
import mysql.connector as mysql
from tkinter import *
from PIL import Image, ImageTk
import cv2

def database():
    global host
    global user
    global psw

    host = 'localhost'
    user = 'root'
    psw = ''

    try:
        db = mysql.connect(host=host, user=user, password=psw)
        dbcursor = db.cursor()
        dbcursor.execute('CREATE DATABASE cromwell')
        db.commit()
        db.close()

        account_db = mysql.connect(host=host, user=user, password=psw, database='cromwell')
        cursor = account_db.cursor()
        cursor.execute('CREATE TABLE account(id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(30), password VARCHAR(120), firstname VARCHAR(126), lastname VARCHAR(126), phone_number VARCHAR(126), balance INT(11) DEFAULT 0, profile_pic MEDIUMBLOB NULL)')
        cursor.execute('CREATE TABLE history(id INT(11), username VARCHAR(30), date VARCHAR(120), time VARCHAR(126), transaction VARCHAR(126), amount INT(15), status VARCHAR(126), reference VARCHAR(13))')
        account_db.commit()
        account_db.close()

    except:
        pass

database()

def splash_screen():
    global sp_screen

    sp_screen = Tk()
    sp_w = 543
    sp_h = 390         
    screen_w = sp_screen.winfo_screenwidth()
    screen_h = sp_screen.winfo_screenheight()
    x = (screen_w / 2) - (sp_w / 2)
    y = (screen_h / 2) - (sp_h / 2)

    sp_screen.geometry(f'{int(sp_w)}x{int(sp_h)}+{int(x)}+{int(y)}')
    sp_screen.wm_attributes('-transparentcolor', '#003145')
    sp_screen.overrideredirect(1)

    bg_image = PhotoImage(file='Images/Splash_screen.png')

    splash_bg = Label(sp_screen, bg='#003145', image=bg_image).pack()
    sp_screen.after(4000, main_window)
    sp_screen.mainloop()

def signup_db():
    global user
    global login
    user = signup_username.get()
    pws = signup_password.get()
    f_name = first_name.get()
    l_name = last_name.get()
    phone = phone_number.get()
    exist = False

    try:
        existing_account = mysql.connect(host='localhost', user='root', password='', database='cromwell')
        cursor = existing_account.cursor()
        cursor.execute('SELECT username from account')
        result = cursor.fetchall()
        for r in result:
            if r[0] == user:
                exist = True
            else:
                pass

        if exist:
            s_error_msg.config(text='Username already exist')
        else:
            s_error_msg.config(text='')
            try:
                login = False
                value = f'{user}', f'{pws}', f'{f_name.title()}', f'{l_name.title()}', f'{phone}'
                cursor.execute('INSERT INTO account(username, password, firstname, lastname, phone_number) VALUES (%s, %s, %s, %s, %s)', value)
                existing_account.commit()
                window.after(1000, account_created)
            except:
                pass
    except Exception as e:
        error = messagebox.showerror('Connection Error', e)

def login_db():
    global login
    global user
        
    user = username.get()
    psw = password.get()
    exist = False

    try:
        existing_account = mysql.connect(host='localhost', user='root', password='', database='cromwell')
        cursor = existing_account.cursor()
        cursor.execute('SELECT username from account')
        result = cursor.fetchall()
        for r in result:
            if r[0] == user:
                exist = True
            else:
                pass
        if not exist:
            error_msg.config(text='Username doesn\'t exist')
            error_msg.place_configure(x=200)

        else:
            try:
                cursor.execute(f'SELECT * from account where username="{user}"')
                result = cursor.fetchall()
                if user == result[0][1] and psw == result[0][2]:
                    login = True
                    error_msg.config(text='')
                    window.after(1000, home)

                else:
                    error_msg.config(text='Username and Password not match')
                    error_msg.place_configure(x=160)
            except:
                pass
        existing_account.close()
    except Exception as e:
        error = messagebox.showerror('Connection Error', e)

def account_created():
    global success
    main_frame.destroy()
    success = Label(window, bd=0, image=new_account)
    success.place(x=0, y=0)
    window.after(3000, home)

def main_window():
    global window
    global new_account

    try:
        sp_screen.destroy()
    except:
        pass

    try:
        window = Tk()
        window.title('Minato')
        window.state('zoomed')

        width = 1366
        height = 768

        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        window.geometry(f'{screen_width}x{screen_height}+{x}+{y}')

        window.resizable(height=False, width=False)
    except:
        pass

    # Images
    w_bg_image = PhotoImage(file='Images/window_bg.png')
    text_image = PhotoImage(file='Images/Text.png')
    new_account = PhotoImage(file='Images/account_created.png')

    login_bg = PhotoImage(file='Images/login_bg.png')
    entry_bg = PhotoImage(file='Images/entry_bg.png')
    btn_bg = PhotoImage(file='Images/Btn_image.png')
    btn_press = PhotoImage(file='Images/Btn_press_image.png')

    signup_bg = (PhotoImage(file='Images/signup_bg.png'))
    signup_entry_bg = PhotoImage(file='Images/singup_tbox.png')
    signup_btn = PhotoImage(file='Images/signup_btn.png')
    signup_press = PhotoImage(file='Images/signup_btn_press.png')
    signup_blank_entry = PhotoImage(file='Images/singup_tbox_blank.png')

    def on_focus_in(event):
        if event.widget == window:
            window.focus()

    # submit btn animation.
    def press(event):
        try:
            submit.config(image=btn_press)
        except:
            signup_submit.config(image=signup_press)

    def release(event):
        try:
            submit.config(image=btn_bg)
        except:
            signup_submit.config(image=signup_btn)

    # login placeholder
    def user_ph(event):
        try:
            if username.get() == 'Username  ':
                username.config(fg='black')
                username.delete(0, END)
        except:
            if signup_username.get() == 'Username  ':
                signup_username.config(fg='black')
                signup_username.delete(0, END)
                usn_bg.config(image=signup_entry_bg)

    def pass_ph(event):
        try:
            if password.get() == 'Password  ':
                password.config(fg='black', show='*')
                password.delete(0, END)
        except:
            if signup_password.get() == 'Password  ':
                signup_password.config(fg='black', show='*')
                signup_password.delete(0, END)
                psw_bg.config(image=signup_entry_bg)

    def check_user_input(event):
        try:
            if username.get() == '':
                username.insert(0, 'Username  ')
                username.config(fg='grey')
        except:
            if signup_username.get() == '':
                signup_username.insert(0, 'Username  ')
                signup_username.config(fg='grey')
                usn_bg.config(image=signup_blank_entry)

    def check_pass_input(event):
        try:
            if password.get() == '':
                password.insert(0, 'Password  ')
                password.config(fg='grey', show='')
        except:
            if signup_password.get() == '':
                signup_password.insert(0, 'Password  ')
                signup_password.config(fg='grey', show='')
                psw_bg.config(image=signup_blank_entry)

    def l_submit():
        window.focus()
        if username.get() == '' or username.get() == 'Username  ' or password.get() == '' or password.get() == 'Password  ':
            error_msg.config(text='Enter username and password')
            error_msg.place_configure(x=180)
        else:
            login_db()

    # Login frame
    def login():
        global username
        global password
        global submit
        global error_msg

        def login_clear():
            login_frame.destroy()
            signup()

        # Login Frame
        login_frame = Frame(main_frame, bg='#1d3c45')
        login_frame.pack(side=RIGHT, padx=(70, 25), ipadx=200, ipady=40)

        w_login = Label(login_frame, bg='#1d3c45', image=login_bg)
        w_login.place(x=0, y=0)

        # Username Password Entry Background.
        user_frame = Frame(login_frame, bg='#fff1e1')
        user_frame.pack(pady=(110, 0), ipadx=30, ipady=18)
        pass_frame = Frame(login_frame, bg='#fff1e1')
        pass_frame.pack(ipadx=30, ipady=18)

        user_bg = Label(user_frame, image=entry_bg, bg='#fff1e1')
        user_bg.place(x=0, y=0)
        pass_bg = Label(pass_frame, image=entry_bg, bg='#fff1e1')
        pass_bg.place(x=0, y=0)

        # Username Password Entry.
        username = Entry(user_frame, bd=0, fg='grey', width=23, font='Times 25')
        username.insert(0, 'Username  ')
        username.pack(pady=(25, 0))

        password = Entry(pass_frame, bd=0, fg='grey', width=23, font='Times 25')
        password.insert(0, 'Password  ')
        password.pack(pady=(25, 0))

        error_msg = Label(login_frame, font='Times 12', fg='red', bg='#fff1e1', text='')
        error_msg.place(x=180, y=300)

        # Submit button and sign up button.
        submit = Button(login_frame, bd=0, bg='#fff1e1', image=btn_bg, cursor='hand2', activebackground='#fff1e1', command=l_submit)
        submit.pack(pady=(20, 10))

        sign_up = Button(login_frame, text='Create account', bg='#fff1e1', fg='blue', font='Times 12', bd=0,
                         activebackground='#fff1e1', command=login_clear)
        sign_up.pack()

        # Binds
        username.bind('<FocusIn>', user_ph)
        password.bind('<FocusIn>', pass_ph)

        username.bind('<FocusOut>', check_user_input)
        password.bind('<FocusOut>', check_pass_input)

        submit.bind('<ButtonPress>', press)
        submit.bind('<ButtonRelease>', release)

    # Signup placeholder
    def f_name(event):
        global widget
        widget = 'Firstname'
        window.bind('<Key>', char_only)
        if first_name.get() == 'Firstname  ':
            first_name.config(fg='black')
            first_name.delete(0, END)
            fn_bg.config(image=signup_entry_bg)

    def l_name(event):
        global widget
        widget = 'Lastname'
        window.bind('<Key>', char_only)
        if last_name.get() == 'Lastname  ':
            last_name.config(fg='black')
            last_name.delete(0, END)
            ln_bg.config(image=signup_entry_bg)

    def phone(event):
        window.bind('<Key>', int_only)
        if phone_number.get() == 'Phone number  ':
            phone_number.config(fg='black')
            phone_number.delete(0, END)
            ph_bg.config(image=signup_entry_bg)

    def check_fn_input(event):
        global widget
        widget = ''
        window.unbind('<Key>')
        if first_name.get() == '':
            first_name.insert(0, 'Firstname  ')
            first_name.config(fg='grey')
            fn_bg.config(image=signup_blank_entry)

    def check_ln_input(event):
        global widget
        widget = ''
        window.unbind('<Key>')
        if last_name.get() == '':
            last_name.insert(0, 'Lastname  ')
            last_name.config(fg='grey')
            ln_bg.config(image=signup_blank_entry)

    def check_ph_input(event):
        window.unbind('<Key>')
        if phone_number.get() == '':
            phone_number.insert(0, 'Phone number  ')
            phone_number.config(fg='grey')
            ph_bg.config(image=signup_blank_entry)

    def blank_fill():

        window.focus()

        if first_name.get() == '' or first_name.get() == 'Firstname  ':
            first_name.delete(0, END)
            first_name.insert(0, 'Firstname  ')
            first_name.config(fg='grey')
            fn_bg.config(image=signup_blank_entry)

        if last_name.get() == '' or last_name.get() == 'Lastname  ':
            last_name.delete(0, END)
            last_name.insert(0, 'Lastname  ')
            last_name.config(fg='grey')
            ln_bg.config(image=signup_blank_entry)

        if phone_number.get() == '' or phone_number.get() == 'Phone number  ':
            phone_number.delete(0, END)
            phone_number.insert(0, 'Phone number  ')
            phone_number.config(fg='grey')
            ph_bg.config(image=signup_blank_entry)

        if signup_username.get() == '' or signup_username.get() == 'Username  ':
            signup_username.delete(0, END)
            signup_username.insert(0, 'Username  ')
            signup_username.config(fg='grey')
            usn_bg.config(image=signup_blank_entry)

        if signup_password.get() == '' or signup_password.get() == 'Password  ':
            signup_password.delete(0, END)
            signup_password.insert(0, 'Password  ')
            signup_password.config(fg='grey', show='')
            psw_bg.config(image=signup_blank_entry)

    def s_submit():
        window.unbind('<Key>')
        if first_name.get() == '' or first_name.get() == 'Firstname  ' or last_name.get() == '' or last_name.get() == 'Lastname  ' or \
                phone_number.get() == '' or phone_number.get() == 'Phone number  ' or signup_username.get() == '' or signup_username.get() == 'Username  ' or \
                signup_password.get() == '' or signup_password.get() == 'Password  ':
            blank_fill()
            s_error_msg.config(text='Fill the empty Textbox!')
        else:
            s_error_msg.config(text='')
            signup_db()

    def int_only(event):
        try:
            original = phone_number.get()
            new = ''

            for c in original:
                c = ord(c)
                if 48 <= c <= 57:
                    new += chr(c)
                else:
                    pass

            phone_number.delete(0, END)
            phone_number.insert(0, new)

            if len(new) > 11:
                phone_number.delete(len(phone_number.get())-1)
            else:
                pass
        except:
            pass

    def char_only(event):
        try:
            if widget == 'Firstname':
                entry = first_name
            elif widget == 'Lastname':
                entry = last_name

            text_original = entry.get()
            new = ''

            for char in text_original:
                char = ord(char)
                if 65 <= char <= 90 or 97 <= char <= 122 or char == 32:
                    new += chr(char)
                else:
                    pass

            entry.delete(0, END)
            entry.insert(0, new)
        except:
            pass

    # Signup frame
    def signup():
        # Entry var
        global signup_username
        global signup_password
        global first_name
        global last_name
        global phone_number

        # Entry bg var
        global usn_bg
        global psw_bg
        global fn_bg
        global ln_bg
        global ph_bg

        # Submit var
        global signup_submit
        global s_error_msg

        def signup_clear():
            signup_frame.destroy()
            login()

        # Signup Frame
        signup_frame = Frame(main_frame, bg='#1d3c45')
        signup_frame.pack(side=RIGHT, pady=(50, 0), padx=(90, 18), ipadx=200, ipady=40)

        w_signup = Label(signup_frame, bg='#1d3c45', image=signup_bg)
        w_signup.place(x=0, y=0)

        # Signup Entry Background.
        fn_frame = Frame(signup_frame, bg='#fff1e1')
        fn_frame.pack(pady=(110, 0), padx=(0, 20), ipadx=20, ipady=10)

        ln_frame = Frame(signup_frame, bg='#fff1e1')
        ln_frame.pack(ipadx=20, ipady=10, pady=(10, 0), padx=(0, 20))

        ph_frame = Frame(signup_frame, bg='#fff1e1')
        ph_frame.pack(ipadx=20, ipady=10, pady=(10, 0), padx=(0, 20))

        usn_frame = Frame(signup_frame, bg='#fff1e1')
        usn_frame.pack(ipadx=20, ipady=10, pady=(10, 0), padx=(0, 20))

        psw_frame = Frame(signup_frame, bg='#fff1e1')
        psw_frame.pack(ipadx=20, ipady=18, pady=(10, 0), padx=(0, 20))

        fn_bg = Label(fn_frame, image=signup_entry_bg, bg='#fff1e1')
        fn_bg.place(x=0, y=0)
        ln_bg = Label(ln_frame, image=signup_entry_bg, bg='#fff1e1')
        ln_bg.place(x=0, y=0)
        ph_bg = Label(ph_frame, image=signup_entry_bg, bg='#fff1e1')
        ph_bg.place(x=0, y=0)
        usn_bg = Label(usn_frame, image=signup_entry_bg, bg='#fff1e1')
        usn_bg.place(x=0, y=0)
        psw_bg = Label(psw_frame, image=signup_entry_bg, bg='#fff1e1')
        psw_bg.place(x=0, y=0)

        # Signup Entry.
        first_name = Entry(fn_frame, bd=0, fg='grey', width=32, font='Times 16')
        first_name.insert(0, 'Firstname  ')
        first_name.pack(pady=(14, 0))

        last_name = Entry(ln_frame, bd=0, fg='grey', width=32, font='Times 16')
        last_name.insert(0, 'Lastname  ')
        last_name.pack(pady=(14, 0))

        phone_number = Entry(ph_frame, bd=0, fg='grey', width=32, font='Times 16')
        phone_number.insert(0, 'Phone number  ')
        phone_number.pack(pady=(14, 0))

        signup_username = Entry(usn_frame, bd=0, fg='grey', width=32, font='Times 16')
        signup_username.insert(0, 'Username  ')
        signup_username.pack(pady=(14, 0))

        signup_password = Entry(psw_frame, bd=0, fg='grey', width=32, font='Times 16')
        signup_password.insert(0, 'Password  ')
        signup_password.pack(pady=(14, 0))

        s_error_msg = Label(signup_frame, font='Times 12', fg='red', bg='#fff1e1', text='')
        s_error_msg.place(x=188, y=448)

        # Submit button and sign up button.
        signup_submit = Button(signup_frame, bd=0, bg='#fff1e1', image=signup_btn, cursor='hand2',
                               activebackground='#fff1e1', command=s_submit)
        signup_submit.pack(pady=(15, 0), padx=(0, 15))

        sign_up = Button(signup_frame, text='I have already account', bg='#fff1e1', fg='blue', font='Times 12', bd=0,
                         activebackground='#fff1e1', command=signup_clear)
        sign_up.pack(padx=(0, 15))

        # binds
        first_name.bind('<FocusIn>', f_name)
        last_name.bind('<FocusIn>', l_name)
        phone_number.bind('<FocusIn>', phone)
        signup_username.bind('<FocusIn>', user_ph)
        signup_password.bind('<FocusIn>', pass_ph)

        signup_username.bind('<FocusOut>', check_user_input)
        signup_password.bind('<FocusOut>', check_pass_input)
        first_name.bind('<FocusOut>', check_fn_input)
        last_name.bind('<FocusOut>', check_ln_input)
        phone_number.bind('<FocusOut>', check_ph_input)

        signup_submit.bind('<ButtonPress>', press)
        signup_submit.bind('<ButtonRelease>', release)

    global main_frame
    # Main window frame
    main_frame = Frame(window)
    main_frame.pack(ipady=170)

    # Main window background.
    w_bg = Label(main_frame, image=w_bg_image, bd=0)
    w_bg.place(x=0, y=0)

    # Window frames and background
    text_frame = Frame(main_frame)
    text_frame.pack(side=LEFT, padx=(190, 130), pady=(0, 100))

    w_text = Label(text_frame, bg='#fff1e1', image=text_image)
    w_text.pack()
    login()

    window.bind("<FocusIn>", on_focus_in)

    window.mainloop()

def home():

    if not login:
        success.destroy()
    elif login:
        main_frame.destroy()

    home_bg_image = PhotoImage(file='Images/home_bg.png')
    tab_btn_image = PhotoImage(file='Images/tab_btn.png')
    cash_in = PhotoImage(file='Images/cash_in.png')
    cash_out = PhotoImage(file='Images/cash_out.png')
    go_btn_image = PhotoImage(file='Images/go_btn.png')
    cancel_btn_image = PhotoImage(file='Images/cancel_btn.png')
    php_sign_image = PhotoImage(file='Images/php_sign.png')
    balance_image = PhotoImage(file='Images/balance.png')
    cash_in_image = PhotoImage(file='Images/cash_in_btn.png')
    cash_out_image = PhotoImage(file='Images/cash_out_btn.png')

    payment_image = PhotoImage(file='Images/payment_bg.png')
    electric_image = PhotoImage(file='Images/payment_electric_btn.png')
    electric_form_image = PhotoImage(file='Images/electric.png')
    water_image = PhotoImage(file='Images/payment_water_btn.png')
    water_form_image = PhotoImage(file='Images/water.png')
    internet_image = PhotoImage(file='Images/payment_internet_btn.png')
    internet_form_image = PhotoImage(file='Images/internet.png')

    history_table = PhotoImage(file='Images/history_table.png')
    nav_bg_image = PhotoImage(file='Images/nav_bg.png')
    success_trans_image = PhotoImage(file='Images/success_trans.png')
    details_bg_image = PhotoImage(file='Images/act_details.png')
    ok_btn_image = PhotoImage(file='Images/ok_btn.png')

    account_bg_image = PhotoImage(file='Images/account_bg.png')
    signup_entry_bg = PhotoImage(file='Images/singup_tbox.png')
    b_save_btn = PhotoImage(file='Images/save.png')
    b_cancel_btn = PhotoImage(file='Images/b_cancel_btn.png')
    take_image = PhotoImage(file='Images/take_image.png')
    upload_image = PhotoImage(file='Images/upload_image.png')

    capture = PhotoImage(file='Images/cam_take.png')
    re_take = PhotoImage(file='Images/take_again.png')
    cam_save = PhotoImage(file='Images/cam_save.png')
    cam_cancel = PhotoImage(file='Images/cam_cancel.png')

    def temp_profile():
        global temp_profile_img
        temp_profile_img = Image.open("Images/Profile_pic/temp_image.png")
        temp_profile_img = temp_profile_img.resize((190, 165))
        temp_profile_img = ImageTk.PhotoImage(temp_profile_img)

    def int_only(event):
        try:
            original = amount.get()
            new = ''

            for c in original:
                c = ord(c)
                if 48 <= c <= 57:
                    new += chr(c)
                else:
                    pass

            amount.delete(0, END)
            amount.insert(0, new)

            if len(new) > 5:
                amount.delete(len(amount.get()) - 1)
            else:
                pass
        except:
            pass

    def my_account():
        global id_number
        global username
        global password
        global phone_number
        global firstname
        global lastname
        global balance
        global user
        global profile_img
        global w
        global h

        def binary_To_file(path):
            with open('Images/Profile_pic/profile.png', 'wb') as file:
                file.write(path)
                file.close()

        account = mysql.connect(host='localhost', user='root', password='', database='cromwell')
        cursor = account.cursor()

        cursor.execute(f'SELECT * from account where username="{user}"')
        result = cursor.fetchall()

        id_number = result[0][0]
        username = result[0][1]
        password = result[0][2]
        firstname = result[0][3]
        lastname = result[0][4]
        phone_number = result[0][5]
        balance = result[0][6]

        if str(result[0][7]) != 'None':
            binary_To_file(result[0][7])
            profile_img = Image.open("Images/Profile_pic/profile.png")
            profile_img = profile_img.resize((190, 165))
            profile_img = ImageTk.PhotoImage(profile_img)
            w, h = 70, 90
        else:
            w, h = 110, 90
            profile_img = PhotoImage(file='Images/temp.png')

        account.commit()
        account.close()

    def history_db():
        i = 1

        now = datetime.datetime.today()
        date = now.date().strftime('%b %d, %Y')
        time = now.time().strftime('%I:%M %p')

        history_number = mysql.connect(host='localhost', user='root', password='', database='cromwell')
        cursor = history_number.cursor()

        cursor.execute('SELECT username from history')
        result = cursor.fetchall()
        for r in result:
            if r[0] == user:
                i += 1

        def random_ref():
            global reference
            global exist_ref

            exist_ref = False
            reference = random.randint(1000000000000, 9999999999999)
            cursor.execute('SELECT reference from history')
            result = cursor.fetchall()
            for r in result:
                if r == reference:
                    exist_ref = True

        random_ref()

        if exist_ref:
            random_ref()

        else:
            history_number.close()

            if i <= 5:
                history_db = mysql.connect(host='localhost', user='root', password='', database='cromwell')
                cursor = history_db.cursor()
                data = i, f'{user}', f'{date}', f'{time}', f'{transaction_act}', f'{value}', f'{status}', f'{reference}'
                cursor.execute(
                    'INSERT INTO history(id, username, date, time, transaction, amount, status, reference) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
                    data)
                history_db.commit()
                history_db.close()
            else:
                old_h_num = []

                history_db = mysql.connect(host='localhost', user='root', password='', database='cromwell')
                cursor = history_db.cursor()
                cursor.execute(f'SELECT * from history where username="{user}"')
                result = cursor.fetchall()

                for h_num in result:
                    old_h_num.append(h_num[0])

                old = min(old_h_num)
                latest = max(old_h_num)

                cursor.execute(
                    f'UPDATE history SET id={latest + 1}, date="{date}", time="{time}", transaction="{transaction_act}", amount={value}, status="{status}" WHERE id={old} AND username="{user}"')
                history_db.commit()
                history_db.close()

    def success_transaction():
        global status
        global success_trans

        status = 'Success'

        window.unbind('<Key>')

        if trans == 'home':
            back = home_page
        elif trans == 'payment':
            back = payment_page

        history_db()

        success_trans = Label(home_bg_frame, bg='#fff1e1', image=success_trans_image)
        success_trans.place(x=510, y=200)
        window.after(3000, back)

    def home_page():
        global home_frame
        global bal_amount_frame

        my_account()

        try:
            nav_frame.destroy()
            home_top_btn.place_configure(x=924, y=0)
            window.unbind('<Button-1>')
        except:
            pass
        try:
            activity_frame.destroy()
        except:
            pass
        try:
            details_frame.destroy()
        except:
            pass
        try:
            payment_frame.destroy()
        except:
            pass
        try:
            success_trans.destroy()
        except:
            pass
        try:
            form_frame.destroy()
        except:
            pass
        try:
            account_frame.destroy()
        except:
            pass
        try:
            about_frame.destroy()
        except:
            pass
        try:
            cap.release()
            camera_frame.destroy()
        except:
            pass
        try:
            os.remove('Images/Profile_pic/temp_image.png')
        except:
            pass

        def cash_in_out(btn):
            global amount
            global cash_in_frame

            home_frame.destroy()
            bal_amount_frame.destroy()

            def amount_in(event):
                window.bind('<Key>', int_only)

            def amount_out(event):
                window.unbind('<Key>')

            def go():
                global value

                value = amount.get()
                success = False
                window.focus()
                try:
                    account = mysql.connect(host='localhost', user='root', password='', database='cromwell')
                    cursor = account.cursor()

                    if btn == 'cash_in':
                        if value == '' or int(value) == 0:
                            error_msg.config(text='Enter cash-in amount')
                            error_msg.place_configure(x=200, y=395)

                        elif int(value) > 10000:
                            error_msg.config(text='Can\'t cash-in more than 10,000')
                            error_msg.place_configure(x=165, y=395)

                        elif int(value) < 0:
                            error_msg.config(text='Transaction Error')
                            error_msg.place_configure(x=215, y=395)

                        else:
                            error_msg.config(text='')
                            cursor.execute(f'UPDATE account SET balance=balance + {value} WHERE id={id_number}')
                            success = True

                    elif btn == 'cash_out':
                        if value == '' or int(value) == 0:
                            error_msg.config(text='Enter cash-Out amount')
                            error_msg.place_configure(x=195, y=395)

                        elif int(value) > int(balance):
                            error_msg.config(text='You don\'t have enough balance')
                            error_msg.place_configure(x=163, y=395)

                        elif int(value) > 10000:
                            error_msg.config(text='Can\'t cash-out more than 10,000')
                            error_msg.place_configure(x=160, y=395)

                        elif int(value) < 0:
                            error_msg.config(text='Transaction Error')
                            error_msg.place_configure(x=215, y=395)

                        else:
                            error_msg.config(text='')
                            cursor.execute(f'UPDATE account SET balance=balance - {value} WHERE id={id_number}')
                            success = True
                except:
                    pass

                if success:
                    global trans
                    global transaction_act

                    if btn == 'cash_in':
                        transaction_act = 'Cash-In'
                    elif btn == 'cash_out':
                        transaction_act = 'Cash-Out'

                    trans = 'home'
                    account.commit()
                    cash_in_frame.destroy()
                    success_transaction()
                account.close()

            def cancel():
                window.unbind('<Key>')
                cash_in_frame.destroy()
                home_page()

            def amount_number(event):
                new_bal.config(state=NORMAL)
                new_bal.delete(0, END)

                if btn == 'cash_in':
                    try:
                        value = amount.get()
                        new_bal_result = balance + int(value)
                        new_bal.insert(0, new_bal_result)
                    except:
                        new_bal.delete(0, END)
                        pass

                elif btn == 'cash_out':
                    try:
                        value = amount.get()
                        new_bal_result = balance - int(value)
                        new_bal.insert(0, new_bal_result)
                    except:
                        new_bal.delete(0, END)
                        pass

                new_bal.config(state=DISABLED)

            cash_in_frame = Frame(window, bg='#fff1e1')
            cash_in_frame.pack(pady=(110, 0))

            cash_in_bg = Label(cash_in_frame, bg='#fff1e1')
            cash_in_bg.place(x=0, y=0)

            if btn == 'cash_in':
                cash_in_bg.config(image=cash_in)
            elif btn == 'cash_out':
                cash_in_bg.config(image=cash_out)

            my_bal = Entry(cash_in_frame, bd=0, width=16, font='lucida 19 bold')
            my_bal.pack(padx=(272, 60), pady=(174, 0))
            amount = Entry(cash_in_frame, bd=0, fg='#1d3545', bg='#fff1e1', width=16, font='lucida 19 bold')
            amount.pack(padx=(272, 60), pady=(50, 0))
            new_bal = Entry(cash_in_frame, bd=0, bg='#fff1e1', width=16, font='lucida 19 bold')
            new_bal.pack(padx=(272, 60), pady=(49, 0))

            error_msg = Label(cash_in_frame, bg='#fff1e1', fg='red', font='lucida 13', text='')
            error_msg.place(x=0, y=0)

            go_btn = Button(cash_in_frame, activebackground='#fff1e1', bd=0, bg='#fff1e1', image=go_btn_image,
                            command=go)
            go_btn.pack(side=LEFT, padx=(100, 0), pady=(70, 80))
            cancel_btn = Button(cash_in_frame, activebackground='#fff1e1', bd=0, bg='#fff1e1', image=cancel_btn_image,
                                command=cancel)
            cancel_btn.pack(side=RIGHT, padx=(0, 100), pady=(70, 80))

            my_bal.insert(0, balance)
            my_bal.config(disabledforeground='#1d3545', disabledbackground='#fff1e1', state=DISABLED)
            new_bal.config(disabledforeground='#1d3545', disabledbackground='#fff1e1', state=DISABLED)

            amount.focus_set()
            amount.bind('<FocusIn>', amount_in)
            amount.bind('<FocusOut>', amount_out)
            amount.bind('<KeyRelease>', amount_number)

        home_btn.config(disabledforeground='#1d3545', bg='#fff1e1', state=DISABLED)
        pay_btn.config(bg='#1d3545', fg='#fff1e1', state=NORMAL)
        act_btn.config(bg='#1d3545', fg='#fff1e1', state=NORMAL)

        home_frame = Frame(window, bg='#fff1e1')
        home_frame.place(x=434, y=245, width=510, height=280)

        balance_bg = Label(home_frame, bd=0, bg='#fff1e1', image=balance_image)
        balance_bg.place(x=0, y=0)

        bal_amount_frame = Frame(window, bg='#fff1e1', width=900, height=100)
        bal_amount_frame.pack(pady=(303, 0))

        php_sign = Label(bal_amount_frame, bd=0, bg='#fff1e1', image=php_sign_image)
        php_sign.grid(row=0, column=0, padx=5)

        b_amount = Label(bal_amount_frame, bd=0, bg='#fff1e1', fg='#1d3545', font='default 35 bold', text=balance)
        b_amount.grid(row=0, column=1, padx=(0, 18), pady=(5, 0))

        cash_in_btn = Button(home_frame, activebackground='#fff1e1', bd=0, bg='#fff1e1', image=cash_in_image,
                             command=lambda: cash_in_out('cash_in'))
        cash_in_btn.place(x=80, y=180)

        cash_out_btn = Button(home_frame, activebackground='#fff1e1', bd=0, bg='#fff1e1', image=cash_out_image,
                              command=lambda: cash_in_out('cash_out'))
        cash_out_btn.place(x=280, y=180)

    def payment_page():
        global form_frame
        global payment_frame

        window.unbind('<Key>')

        pay_btn.config(disabledforeground='#1d3545', bg='#fff1e1', state=DISABLED)

        home_btn.config(bg='#1d3545', fg='#fff1e1', state=NORMAL)
        act_btn.config(bg='#1d3545', fg='#fff1e1', state=NORMAL)

        try:
            nav_frame.destroy()
            home_top_btn.place_configure(x=924, y=0)
            window.unbind('<Button-1>')
        except:
            pass
        try:
            details_frame.destroy()
        except:
            pass
        try:
            home_frame.destroy()
            bal_amount_frame.destroy()
        except:
            pass
        try:
            activity_frame.destroy()
        except:
            pass
        try:
            cash_in_frame.destroy()
        except:
            pass
        try:
            success_trans.destroy()
        except:
            pass
        try:
            account_frame.destroy()
        except:
            pass
        try:
            about_frame.destroy()
        except:
            pass
        try:
            cap.release()
            camera_frame.destroy()
        except:
            pass
        try:
            os.remove('Images/Profile_pic/temp_image.png')
        except:
            pass

        def payment_forms(pay):
            payment_frame.destroy()

            def int_only(event):
                try:
                    i = 0

                    if entry == 'account':
                        i = 17
                        e = account_num
                    elif entry == 'amount':
                        i = 5
                        e = amount
                    elif entry == 'mobile':
                        i = 11
                        e = mobile

                    original = e.get()
                    new = ''

                    for c in original:
                        c = ord(c)
                        if 48 <= c <= 57:
                            new += chr(c)
                        else:
                            pass

                    e.delete(0, END)
                    e.insert(0, new)

                    if len(new) > i:
                        e.delete(len(e.get()) - 1)
                    else:
                        pass
                except:
                    pass

            def focus_num(event):
                global entry
                entry = 'account'
                window.bind('<Key>', int_only)

            def focus_amount(event):
                global entry
                entry = 'amount'
                window.bind('<Key>', int_only)

            def focus_mobile(event):
                global entry
                entry = 'mobile'
                window.bind('<Key>', int_only)

            def new_balance(event):
                new_bal.config(state=NORMAL)
                new_bal.delete(0, END)

                try:
                    value = amount.get()
                    new_bal_result = balance - int(value)
                    new_bal.insert(0, new_bal_result)
                except:
                    new_bal.delete(0, END)
                    pass

                new_bal.config(state=DISABLED)

            def go():
                global amount
                global value

                entry = ''
                window.focus()
                window.unbind('<Key>')

                value = amount.get()
                value1 = account_num.get()
                value2 = mobile.get()

                success = False
                window.focus()

                try:
                    if value == '' or value1 == '' or value2 == '':
                        error_msg.config(text='Fill the blank text box')
                        error_msg.place_configure(x=375, y=410)

                    else:
                        account = mysql.connect(host='localhost', user='root', password='', database='cromwell')
                        cursor = account.cursor()

                        if int(value) > int(balance):
                            error_msg.config(text='You don\'t have enough balance')
                            error_msg.place_configure(x=330, y=410)

                        elif int(value) < 0:
                            error_msg.config(text='Transaction Error')
                            error_msg.place_configure(x=380, y=410)

                        else:
                            error_msg.config(text='')
                            cursor.execute(f'UPDATE account SET balance=balance - {value} WHERE id={id_number}')
                            success = True

                        if success:
                            global trans
                            global transaction_act

                            if pay == 'Electric':
                                transaction_act = 'Electric payment'
                            elif pay == 'Water':
                                transaction_act = 'Water payment'
                            elif pay == 'Internet':
                                transaction_act = 'Internet payment'

                            trans = 'payment'
                            account.commit()
                            form_frame.destroy()
                            success_transaction()
                            account.close()
                except:
                    pass

            def cancel():
                entry = ''
                window.unbind('<Key>')
                form_frame.destroy()
                payment_page()

            if pay == 'Electric':
                image = electric_form_image
            if pay == 'Water':
                image = water_form_image
            if pay == 'Internet':
                image = internet_form_image

            global amount
            global form_frame

            form_frame = Frame(window, bg='#fff1e1')
            form_frame.pack(pady=(120, 0))

            form_bg = Label(form_frame, bg='#fff1e1', image=image)
            form_bg.place(x=0, y=0)

            account_num = Entry(form_frame, bd=0, fg='#1d3545', bg='#fff1e1', width=18, font='lucida 19 bold')
            account_num.pack(padx=(417, 180), pady=(151, 33))
            amount = Entry(form_frame, bd=0, fg='#1d3545', bg='#fff1e1', width=18, font='lucida 19 bold')
            amount.pack(padx=(417, 180), pady=(0, 35))
            mobile = Entry(form_frame, bd=0, fg='#1d3545', bg='#fff1e1', width=18, font='lucida 19 bold')
            mobile.pack(padx=(417, 180), pady=(0, 40))
            new_bal = Entry(form_frame, state=DISABLED, bd=0, fg='#1d3545', bg='#fff1e1', width=18,
                            font='lucida 19 bold')
            new_bal.pack(padx=(417, 180), pady=(0, 60))

            new_bal.config(disabledforeground='#1d3545', disabledbackground='#fff1e1', state=DISABLED)

            error_msg = Label(form_frame, bg='#fff1e1', fg='red', font='lucida 13', text='')
            error_msg.place(x=0, y=0)

            btn_frame = Frame(form_frame, bg='#fff1e1')
            btn_frame.pack(pady=(0, 75))

            go_btn = Button(btn_frame, activebackground='#fff1e1', bd=0, bg='#fff1e1', image=go_btn_image, command=go)
            go_btn.pack(side=LEFT, padx=50)
            cancel_btn = Button(btn_frame, activebackground='#fff1e1', bd=0, bg='#fff1e1', image=cancel_btn_image,
                                command=cancel)
            cancel_btn.pack(side=RIGHT)

            account_num.bind('<FocusIn>', focus_num)
            amount.bind('<FocusIn>', focus_amount)
            mobile.bind('<FocusIn>', focus_mobile)

            amount.bind('<KeyRelease>', new_balance)

        payment_frame = Frame(window, bg='#fff1e1')
        payment_frame.pack(pady=(220, 0))

        payment_bg = Label(payment_frame, bg='#fff1e1', image=payment_image)
        payment_bg.place(x=0, y=0)

        payment_btn_frame = Frame(payment_frame, bg='#fff1e1')
        payment_btn_frame.pack(pady=(105, 80), padx=160)

        electric_btn = Button(payment_btn_frame, activebackground='#fff1e1', bd=0, bg='#fff1e1', image=electric_image,
                              command=lambda: payment_forms('Electric'))
        electric_btn.grid(row=0, column=0)

        water_btn = Button(payment_btn_frame, activebackground='#fff1e1', bd=0, bg='#fff1e1', image=water_image,
                           command=lambda: payment_forms('Water'))
        water_btn.grid(row=0, column=1, padx=130)

        internet_btn = Button(payment_btn_frame, activebackground='#fff1e1', bd=0, bg='#fff1e1', image=internet_image,
                              command=lambda: payment_forms('Internet'))
        internet_btn.grid(row=0, column=2)

    def activity_page():
        global activity_frame

        window.unbind('<Key>')

        act_btn.config(disabledforeground='#1d3545', bg='#fff1e1', state=DISABLED)

        home_btn.config(bg='#1d3545', fg='#fff1e1', state=NORMAL)
        pay_btn.config(bg='#1d3545', fg='#fff1e1', state=NORMAL)

        try:
            nav_frame.destroy()
            home_top_btn.place_configure(x=924, y=0)
            window.unbind('<Button-1>')
        except:
            pass
        try:
            home_frame.destroy()
            bal_amount_frame.destroy()
        except:
            pass
        try:
            payment_frame.destroy()
        except:
            pass
        try:
            cash_in_frame.destroy()
        except:
            pass
        try:
            success_trans.destroy()
        except:
            pass
        try:
            form_frame.destroy()
        except:
            pass
        try:
            account_frame.destroy()
        except:
            pass
        try:
            about_frame.destroy()
        except:
            pass
        try:
            cap.release()
            camera_frame.destroy()
        except:
            pass
        try:
            os.remove('Images/Profile_pic/temp_image.png')
        except:
            pass

        def history_data():
            global result
            history_list = []

            history_db = mysql.connect(host='localhost', user='root', password='', database='cromwell')
            cursor = history_db.cursor()
            cursor.execute(f'SELECT * from history where username="{user}"')
            result = cursor.fetchall()

            history_db.commit()
            history_db.close()

            result.sort(reverse=True)

            try:
                data = result[0]

                date1.config(state=NORMAL)
                time1.config(state=NORMAL)
                transaction1.config(state=NORMAL)
                status1.config(state=NORMAL)

                date1.delete(0, END)
                time1.delete(0, END)
                transaction1.delete(0, END)
                status1.delete(0, END)

                date1.insert(0, result[0][2])
                time1.insert(0, result[0][3])
                transaction1.insert(0, result[0][4])
                status1.insert(0, result[0][6])

                details1.grid(row=1, column=2, padx=(0, 10))

                date1.config(state=DISABLED)
                time1.config(state=DISABLED)
                transaction1.config(state=DISABLED)
                status1.config(state=DISABLED)
            except:
                pass

            try:
                data = result[1]

                date2.config(state=NORMAL)
                time2.config(state=NORMAL)
                transaction2.config(state=NORMAL)
                status2.config(state=NORMAL)

                date2.delete(0, END)
                time2.delete(0, END)
                transaction2.delete(0, END)
                status2.delete(0, END)

                date2.insert(0, result[1][2])
                time2.insert(0, result[1][3])
                transaction2.insert(0, result[1][4])
                status2.insert(0, result[1][6])

                details2.grid(row=3, column=2, padx=(0, 10))

                date2.config(state=DISABLED)
                time2.config(state=DISABLED)
                transaction2.config(state=DISABLED)
                status2.config(state=DISABLED)
            except:
                pass

            try:
                data = result[2]

                date3.config(state=NORMAL)
                time3.config(state=NORMAL)
                transaction3.config(state=NORMAL)
                status3.config(state=NORMAL)

                date3.delete(0, END)
                time3.delete(0, END)
                transaction3.delete(0, END)
                status3.delete(0, END)

                date3.insert(0, result[2][2])
                time3.insert(0, result[2][3])
                transaction3.insert(0, result[2][4])
                status3.insert(0, result[2][6])

                details3.grid(row=5, column=2, padx=(0, 10))

                date3.config(state=DISABLED)
                time3.config(state=DISABLED)
                transaction3.config(state=DISABLED)
                status3.config(state=DISABLED)
            except:
                pass

            try:
                data = result[3]

                date4.config(state=NORMAL)
                time4.config(state=NORMAL)
                transaction4.config(state=NORMAL)
                status4.config(state=NORMAL)

                date4.delete(0, END)
                time4.delete(0, END)
                transaction4.delete(0, END)
                status4.delete(0, END)

                date4.insert(0, result[3][2])
                time4.insert(0, result[3][3])
                transaction4.insert(0, result[3][4])
                status4.insert(0, result[3][6])

                details4.grid(row=7, column=2, padx=(0, 10))

                date4.config(state=DISABLED)
                time4.config(state=DISABLED)
                transaction4.config(state=DISABLED)
                status4.config(state=DISABLED)
            except:
                pass

            try:
                data = result[4]

                date5.config(state=NORMAL)
                time5.config(state=NORMAL)
                transaction5.config(state=NORMAL)
                status5.config(state=NORMAL)

                date5.delete(0, END)
                time5.delete(0, END)
                transaction5.delete(0, END)
                status5.delete(0, END)

                date5.insert(0, result[4][2])
                time5.insert(0, result[4][3])
                transaction5.insert(0, result[4][4])
                status5.insert(0, result[4][6])

                details5.grid(row=9, column=2, padx=(0, 10), pady=(0, 40))

                date5.config(state=DISABLED)
                time5.config(state=DISABLED)
                transaction5.config(state=DISABLED)
                status5.config(state=DISABLED)
            except:
                pass

        def ok():
            details_frame.destroy()
            activity_page()

        def details(btn):
            global details_frame
            activity_frame.destroy()

            def set_text_newline(s):
                h_details.insert(END, s + '\n\n')

            details_frame = Frame(window)
            details_frame.pack(pady=(160, 0))

            d_bg = Label(details_frame, bg='#fff1e1', image=details_bg_image)
            d_bg.place(x=0, y=0)

            h_details = Text(details_frame, bd=0, bg='#fff1e1', fg='#1d3545', font='times 18', height=10, width=45)
            h_details.pack(padx=(35, 65), pady=(80, 0))

            ok_btn = Button(details_frame, activebackground='#fff1e1', bd=0, bg='#fff1e1', image=ok_btn_image, command=ok)
            ok_btn.pack(pady=(10, 50))

            if btn == 1:
                d_date = result[0][2]
                d_time = result[0][3]
                d_trans = result[0][4]
                d_amount = result[0][5]
                d_stat = result[0][6]
                d_ref = result[0][7]

            elif btn == 2:
                d_date = result[1][2]
                d_time = result[1][3]
                d_trans = result[1][4]
                d_amount = result[1][5]
                d_stat = result[1][6]
                d_ref = result[1][7]

            elif btn == 3:
                d_date = result[2][2]
                d_time = result[2][3]
                d_trans = result[2][4]
                d_amount = result[2][5]
                d_stat = result[2][6]
                d_ref = result[2][7]

            elif btn == 4:
                d_date = result[3][2]
                d_time = result[3][3]
                d_trans = result[3][4]
                d_amount = result[3][5]
                d_stat = result[3][6]
                d_ref = result[3][7]

            elif btn == 5:
                d_date = result[4][2]
                d_time = result[4][3]
                d_trans = result[4][4]
                d_amount = result[4][5]
                d_stat = result[4][6]
                d_ref = result[4][7]

            if d_trans == 'Cash-In':
                trans_from = 'Bank'
                trans_to = 'Minato E-payment'
                op = ''

            elif d_trans == 'Cash-Out':
                trans_from = 'Minato E-payment'
                trans_to = 'Bank'
                op = '-'

            elif d_trans == 'Electric payment':
                trans_from = 'Minato E-payment'
                trans_to = 'Electric company'
                op = '-'

            elif d_trans == 'Water payment':
                trans_from = 'Minato E-payment'
                trans_to = 'Water company'
                op = '-'

            elif d_trans == 'Internet payment':
                trans_from = 'Minato E-payment'
                trans_to = 'Internet company'
                op = '-'

            set_text_newline(f'Transaction: {d_trans}')
            set_text_newline(f'Transfer from {trans_from} to {trans_to}')
            set_text_newline(f'Date & Time: {d_date} {d_time}')
            set_text_newline(f'Amount: {op}{d_amount}')
            h_details.insert(END, f'Reference Number: {d_ref}')

            h_details.config(state=DISABLED)

        activity_frame = Frame(window, bg='#fff1e1')
        activity_frame.pack(pady=(130, 0))

        activity_table = Label(activity_frame, bg='#fff1e1', image=history_table)
        activity_table.place(x=0, y=0)

        date1 = Entry(activity_frame, bd=0, bg='#fff1e1', font='lucida 15 bold', width=25, justify=CENTER)
        date1.grid(row=0, column=0, padx=(15, 0), pady=(95, 0))
        time1 = Entry(activity_frame, bd=0, bg='#fff1e1', font='lucida 15 bold', width=25, justify=CENTER)
        time1.grid(row=1, column=0, padx=(15, 0))
        transaction1 = Entry(activity_frame, bd=0, bg='#fff1e1', font='lucida 18 bold', width=31, justify=CENTER)
        transaction1.grid(row=0, column=1, rowspan=2, padx=12, pady=(95, 0))
        status1 = Entry(activity_frame, bd=0, bg='#fff1e1', font='lucida 15 bold', width=26, justify=CENTER)
        status1.grid(row=0, column=2, padx=(0, 10), pady=(95, 0))
        details1 = Button(activity_frame, activebackground='#fff1e1', fg='blue', bd=0, text='Details', bg='#fff1e1', font='lucida 11 bold', width=5,
                          justify=CENTER, command=lambda: details(1))

        date1.config(disabledforeground='#1d3545', disabledbackground='#fff1e1', state=DISABLED)
        time1.config(disabledforeground='#1d3545', disabledbackground='#fff1e1', state=DISABLED)
        transaction1.config(disabledforeground='#1d3545', disabledbackground='#fff1e1', state=DISABLED)
        status1.config(disabledforeground='#1d3545', disabledbackground='#fff1e1', state=DISABLED)

        date2 = Entry(activity_frame, bd=0, bg='#fff1e1', font='lucida 15 bold', width=25, justify=CENTER)
        date2.grid(row=2, column=0, padx=(15, 0), pady=(35, 0))
        time2 = Entry(activity_frame, bd=0, bg='#fff1e1', font='lucida 15 bold', width=25, justify=CENTER)
        time2.grid(row=3, column=0, padx=(15, 0))
        transaction2 = Entry(activity_frame, bd=0, bg='#fff1e1', font='lucida 18 bold', width=31, justify=CENTER)
        transaction2.grid(row=2, column=1, rowspan=2, padx=12, pady=(35, 0))
        status2 = Entry(activity_frame, bd=0, bg='#fff1e1', font='lucida 15 bold', width=26, justify=CENTER)
        status2.grid(row=2, column=2, padx=(0, 10), pady=(35, 0))
        details2 = Button(activity_frame, activebackground='#fff1e1', fg='blue', bd=0, text='Details', bg='#fff1e1', font='lucida 11 bold', width=5,
                          justify=CENTER, command=lambda: details(2))

        date2.config(disabledforeground='#1d3545', disabledbackground='#fff1e1', state=DISABLED)
        time2.config(disabledforeground='#1d3545', disabledbackground='#fff1e1', state=DISABLED)
        transaction2.config(disabledforeground='#1d3545', disabledbackground='#fff1e1', state=DISABLED)
        status2.config(disabledforeground='#1d3545', disabledbackground='#fff1e1', state=DISABLED)

        date3 = Entry(activity_frame, bd=0, bg='#fff1e1', font='lucida 15 bold', width=25, justify=CENTER)
        date3.grid(row=4, column=0, padx=(15, 0), pady=(38, 0))
        time3 = Entry(activity_frame, bd=0, bg='#fff1e1', font='lucida 15 bold', width=25, justify=CENTER)
        time3.grid(row=5, column=0, padx=(15, 0))
        transaction3 = Entry(activity_frame, bd=0, bg='#fff1e1', font='lucida 18 bold', width=31, justify=CENTER)
        transaction3.grid(row=4, column=1, rowspan=2, padx=12, pady=(38, 0))
        status3 = Entry(activity_frame, bd=0, bg='#fff1e1', font='lucida 15 bold', width=26, justify=CENTER)
        status3.grid(row=4, column=2, padx=(0, 10), pady=(38, 0))
        details3 = Button(activity_frame, activebackground='#fff1e1', fg='blue', bd=0, text='Details', bg='#fff1e1', font='lucida 11 bold', width=5,
                          justify=CENTER, command=lambda: details(3))

        date3.config(disabledforeground='#1d3545', disabledbackground='#fff1e1', state=DISABLED)
        time3.config(disabledforeground='#1d3545', disabledbackground='#fff1e1', state=DISABLED)
        transaction3.config(disabledforeground='#1d3545', disabledbackground='#fff1e1', state=DISABLED)
        status3.config(disabledforeground='#1d3545', disabledbackground='#fff1e1', state=DISABLED)

        date4 = Entry(activity_frame, bd=0, bg='#fff1e1', font='lucida 15 bold', width=25, justify=CENTER)
        date4.grid(row=6, column=0, padx=(15, 0), pady=(38, 0))
        time4 = Entry(activity_frame, bd=0, bg='#fff1e1', font='lucida 15 bold', width=25, justify=CENTER)
        time4.grid(row=7, column=0, padx=(15, 0))
        transaction4 = Entry(activity_frame, bd=0, bg='#fff1e1', font='lucida 18 bold', width=31, justify=CENTER)
        transaction4.grid(row=6, column=1, rowspan=2, padx=12, pady=(38, 0))
        status4 = Entry(activity_frame, bd=0, bg='#fff1e1', font='lucida 15 bold', width=26, justify=CENTER)
        status4.grid(row=6, column=2, padx=(0, 10), pady=(38, 0))
        details4 = Button(activity_frame, activebackground='#fff1e1', fg='blue', bd=0, text='Details', bg='#fff1e1', font='lucida 11 bold', width=5,
                          justify=CENTER, command=lambda: details(4))

        date4.config(disabledforeground='#1d3545', disabledbackground='#fff1e1', state=DISABLED)
        time4.config(disabledforeground='#1d3545', disabledbackground='#fff1e1', state=DISABLED)
        transaction4.config(disabledforeground='#1d3545', disabledbackground='#fff1e1', state=DISABLED)
        status4.config(disabledforeground='#1d3545', disabledbackground='#fff1e1', state=DISABLED)

        date5 = Entry(activity_frame, bd=0, bg='#fff1e1', font='lucida 15 bold', width=24, justify=CENTER)
        date5.grid(row=8, column=0, padx=(15, 0), pady=(46, 0))
        time5 = Entry(activity_frame, bd=0, bg='#fff1e1', font='lucida 15 bold', width=24, justify=CENTER)
        time5.grid(row=9, column=0, padx=(15, 0), pady=(0, 40))
        transaction5 = Entry(activity_frame, bd=0, bg='#fff1e1', font='lucida 18 bold', width=31, justify=CENTER)
        transaction5.grid(row=8, column=1, rowspan=2, padx=12, pady=(46, 40))
        status5 = Entry(activity_frame, bd=0, bg='#fff1e1', font='lucida 15 bold', width=26, justify=CENTER)
        status5.grid(row=8, column=2, padx=(0, 10), pady=(46, 0))
        details5 = Button(activity_frame, activebackground='#fff1e1', fg='blue', bd=0, text='Details', bg='#fff1e1', font='lucida 11 bold', width=5,
                          justify=CENTER, command=lambda: details(5))

        date5.config(disabledforeground='#1d3545', disabledbackground='#fff1e1', state=DISABLED)
        time5.config(disabledforeground='#1d3545', disabledbackground='#fff1e1', state=DISABLED)
        transaction5.config(disabledforeground='#1d3545', disabledbackground='#fff1e1', state=DISABLED)
        status5.config(disabledforeground='#1d3545', disabledbackground='#fff1e1', state=DISABLED)

        history_data()

    def account_status():
        global account_frame

        try:
            nav_frame.destroy()
            home_top_btn.place_configure(x=924, y=0)
            window.unbind('<Button-1>')
        except:
            pass
        try:
            home_frame.destroy()
            bal_amount_frame.destroy()
        except:
            pass
        try:
            activity_frame.destroy()
        except:
            pass
        try:
            details_frame.destroy()
        except:
            pass
        try:
            payment_frame.destroy()
        except:
            pass
        try:
            cash_in_frame.destroy()
        except:
            pass
        try:
            success_trans.destroy()
        except:
            pass
        try:
            form_frame.destroy()
        except:
            pass
        try:
            account_frame.destroy()
        except:
            pass
        try:
            about_frame.destroy()
        except:
            pass
        try:
            cap.release()
            camera_frame.destroy()
        except:
            pass
        try:
            os.remove('Images/Profile_pic/temp_image.png')
        except:
            pass

        def save(btn):
            if btn == 'basic info':
                fn = b_firstname.get()
                ln = b_lastname.get()

                if b_firstname.get() == firstname and b_lastname.get() == lastname and b_mobile.get() == phone_number:
                    print('asd')
                    pass

                elif b_firstname.get() == '' or b_lastname.get() == '' or b_mobile.get() == '':
                    error_msg = messagebox.showerror('Saving Error', 'Empty text field')
                    basic_info.destroy()
                    basic_information()
                else:
                    try:
                        conn = mysql.connect(host='localhost', username='root', password='', database='cromwell')
                        my_cursor = conn.cursor()
                        my_cursor.execute('UPDATE account SET firstname=%s, lastname=%s, phone_number=%s WHERE id=%s',
                                          (fn.title(), ln.title(), b_mobile.get(), id_number))

                        confirmation_msg = messagebox.askyesno('Confirmation', 'Do you want to update information')
                        if confirmation_msg > 0:
                            conn.commit()
                            confirmation_msg = messagebox.showinfo('Information', 'Update Successfully')
                            basic_info.destroy()
                            conn.close()
                        basic_information()

                        my_account()
                    except:
                        pass

            elif btn == 'security':
                if s_old_password.get() == '' and s_new_pass.get() == '' and s_re_pass.get() == '':
                    pass

                elif s_old_password.get() == '' or s_new_pass.get() == '' or s_re_pass.get() == '':
                    error_msg = messagebox.showerror('Saving Error', 'Empty field')
                    security_info.destroy()
                    security()

                elif s_old_password.get() != password:
                    error_msg = messagebox.showerror('Saving Error', 'Old password not match')

                elif s_new_pass.get() != s_re_pass.get():
                    error_msg = messagebox.showerror('Saving Error', 'New password not match')

                else:
                    try:
                        conn = mysql.connect(host='localhost', username='root', password='', database='cromwell')
                        my_cursor = conn.cursor()
                        my_cursor.execute('UPDATE account SET password=%s WHERE id=%s', (s_new_pass.get(), id_number))

                        confirmation_msg = messagebox.askyesno('Confirmation', 'Do you want to change your password')
                        if confirmation_msg > 0:
                            conn.commit()
                            confirmation_msg = messagebox.showinfo('Information', 'Update Successfully')
                            security_info.destroy()
                            security()
                            conn.close()

                        my_account()
                    except:
                        pass

        def cancel():
            try:
                os.remove('Images/Profile_pic/temp_image.png')
            except:
                pass
            account_frame.destroy()
            home_page()

        def basic_information():
            global basic_info
            global b_firstname
            global b_lastname
            global b_mobile

            try:
                cap.release()
                camera_frame.destroy()
            except:
                pass
            try:
                security_info.destroy()
            except:
                pass
            try:
                profile_pic_frame.destroy()
            except:
                pass
            try:
                os.remove('Images/Profile_pic/temp_image.png')
            except:
                pass

            my_account()

            basic_btn.config(disabledforeground='#1d3545', bg='#fff1e1', state=DISABLED)

            home_btn.config(bg='#1d3545', fg='#fff1e1', state=NORMAL)
            act_btn.config(bg='#1d3545', fg='#fff1e1', state=NORMAL)
            pay_btn.config(bg='#1d3545', fg='#fff1e1', state=NORMAL)

            security_btn.config(bg='#1d3545', fg='#fff1e1', state=NORMAL)
            profile_btn.config(bg='#1d3545', fg='#fff1e1', state=NORMAL)

            basic_info = Frame(account_frame, bg='#1d3545')
            basic_info.pack(padx=160, side=RIGHT)

            b_fname = Frame(basic_info, bg='#1d3545')
            b_fname.pack()

            b_lname = Frame(basic_info, bg='#1d3545')
            b_lname.pack(pady=20)

            b_phone = Frame(basic_info, bg='#1d3545')
            b_phone.pack()

            b_fn_bg = Label(b_fname, image=signup_entry_bg, bg='#1d3545')
            b_fn_bg.place(x=108, y=0)

            b_ln_bg = Label(b_lname, image=signup_entry_bg, bg='#1d3545')
            b_ln_bg.place(x=104, y=0)

            b_mobile_bg = Label(b_phone, image=signup_entry_bg, bg='#1d3545')
            b_mobile_bg.place(x=140, y=0)

            fname = Label(b_fname, text='First Name:', fg='#fff1e1', bg='#1d3545', font='times 16')
            fname.pack(padx=(0, 5), side=LEFT)

            b_firstname = Entry(b_fname, bd=0, fg='#1d3545', width=32, font='Times 16')
            b_firstname.pack(padx=(17, 18), pady=14, side=RIGHT)

            lname = Label(b_lname, text='Last Name:', fg='#fff1e1', bg='#1d3545', font='times 16')
            lname.pack(padx=(0, 5), side=LEFT)

            b_lastname = Entry(b_lname, bd=0, fg='#1d3545', width=32, font='Times 16')
            b_lastname.pack(padx=(17, 18), pady=14)

            mobile = Label(b_phone, text='Phone Number:', fg='#fff1e1', bg='#1d3545', font='times 16')
            mobile.pack(padx=(0, 5), side=LEFT)

            b_mobile = Entry(b_phone, bd=0, fg='#1d3545', width=32, font='Times 16')
            b_mobile.pack(padx=(17, 48), pady=14)

            b_btn_frame = Frame(basic_info, bg='#1d3545')
            b_btn_frame.pack(padx=(40, 0), pady=(45, 0))

            b_firstname.insert(0, firstname)
            b_lastname.insert(0, lastname)
            b_mobile.insert(0, phone_number)

            b_save = Button(b_btn_frame, activebackground='#1d3545', bd=0, image=b_save_btn, bg='#1d3545', command=lambda: save('basic info'))
            b_save.pack(padx=(0, 40), side=LEFT)

            b_cancel = Button(b_btn_frame, activebackground='#1d3545', bd=0, image=b_cancel_btn, bg='#1d3545', command=cancel)
            b_cancel.pack(side=RIGHT)

        def security():
            global security_info
            global s_old_password
            global s_new_pass
            global s_re_pass

            security_btn.config(disabledforeground='#1d3545', bg='#fff1e1', state=DISABLED)

            basic_btn.config(bg='#1d3545', fg='#fff1e1', state=NORMAL)
            profile_btn.config(bg='#1d3545', fg='#fff1e1', state=NORMAL)

            try:
                basic_info.destroy()
            except:
                pass
            try:
                profile_pic_frame.destroy()
            except:
                pass
            try:
                cap.release()
                camera_frame.destroy()
            except:
                pass
            try:
                os.remove('Images/Profile_pic/temp_image.png')
            except:
                pass

            security_info = Frame(account_frame, bg='#1d3545')
            security_info.pack(padx=150, side=RIGHT)

            old_pass = Frame(security_info, bg='#1d3545')
            old_pass.pack()

            new_pass = Frame(security_info, bg='#1d3545')
            new_pass.pack(pady=20)

            repeat_pass = Frame(security_info, bg='#1d3545')
            repeat_pass.pack()

            b_old_pass = Label(old_pass, image=signup_entry_bg, bg='#1d3545')
            b_old_pass.place(x=128, y=0)

            b_new_pass = Label(new_pass, image=signup_entry_bg, bg='#1d3545')
            b_new_pass.place(x=135, y=0)

            b_re_pass = Label(repeat_pass, image=signup_entry_bg, bg='#1d3545')
            b_re_pass.place(x=153, y=0)

            old_password = Label(old_pass, text='Old Password:', fg='#fff1e1', bg='#1d3545', font='times 16')
            old_password.pack(padx=(0, 5), side=LEFT)

            s_old_password = Entry(old_pass, show='*', bd=0, fg='#1d3545', width=32, font='Times 16')
            s_old_password.pack(padx=(17, 18), pady=14, side=RIGHT)

            new_password = Label(new_pass, text='New Password:', fg='#fff1e1', bg='#1d3545', font='times 16')
            new_password.pack(padx=(0, 5), side=LEFT)

            s_new_pass = Entry(new_pass, show='*', bd=0, fg='#1d3545', width=32, font='Times 16')
            s_new_pass.pack(padx=(17, 24), pady=14)

            s_re_pass = Label(repeat_pass, text='Repeat Password:', fg='#fff1e1', bg='#1d3545', font='times 16')
            s_re_pass.pack(padx=(0, 5), side=LEFT)

            s_re_pass = Entry(repeat_pass, show='*', bd=0, fg='#1d3545', width=32, font='Times 16')
            s_re_pass.pack(padx=(17, 37), pady=14)

            b_btn_frame = Frame(security_info, bg='#1d3545')
            b_btn_frame.pack(padx=(55, 0), pady=(45, 0))

            b_save = Button(b_btn_frame, activebackground='#1d3545', bd=0, image=b_save_btn, bg='#1d3545', command=lambda: save('security'))
            b_save.pack(padx=(0, 40), side=LEFT)

            b_cancel = Button(b_btn_frame, activebackground='#1d3545', bd=0, image=b_cancel_btn, bg='#1d3545', command=cancel)
            b_cancel.pack(side=RIGHT)

        def profile_pic():
            global profile_pic_frame

            profile_btn.config(disabledforeground='#1d3545', bg='#fff1e1', state=DISABLED)

            basic_btn.config(bg='#1d3545', fg='#fff1e1', state=NORMAL)
            security_btn.config(bg='#1d3545', fg='#fff1e1', state=NORMAL)

            try:
                cap.release()
                camera_frame.destroy()
            except:
                pass
            try:
                basic_info.destroy()
            except:
                pass
            try:
                security_info.destroy()
            except:
                pass

            def camera(btn):
                global camera_frame

                def cancel():
                    camera_frame.destroy()
                    profile_pic()

                def cam_save_pic():
                    image = Image.fromarray(rgb)
                    image.save('Images/Profile_pic/profile.png')

                    profile_pic_path = 'Images/Profile_pic/profile.png'

                    def convert_To_binary(path):
                        with open(profile_pic_path, 'rb') as file:
                            binary_data = file.read()
                        return binary_data

                    try:
                        conn = mysql.connect(host='localhost', username='root', password='', database='cromwell')
                        cursor = conn.cursor()

                        query = 'UPDATE account SET profile_pic = %s WHERE id = %s'
                        value = convert_To_binary(profile_pic_path), id_number
                        cursor.execute(query, value)
                        update = 'success'
                        conn.commit()
                    except:
                        pass

                    try:
                        if update == 'success':
                            os.remove('Images/Profile_pic/profile.png')
                            my_account()
                            profile_pic_frame.destroy()
                            profile_pic()
                            confirmation_msg = messagebox.showinfo('Information', 'Image save successfully')
                    except:
                        pass

                def take_copy(im):
                    cam_btn_frame.destroy()
                    cap.release()

                    copy = im.copy()
                    copy = cv2.resize(copy, (350, 300))
                    rgb = cv2.cvtColor(copy, cv2.COLOR_BGR2RGB)
                    image = Image.fromarray(copy)
                    img_tk = ImageTk.PhotoImage(image)
                    cam.configure(image=img_tk)
                    cam.image = img_tk

                    camera_frame.pack_configure(padx=230)

                    cam_btn_frame1 = Frame(camera_frame, bg='#1d3545')
                    cam_btn_frame1.pack(pady=(30, 50))

                    re_take_shot = Button(cam_btn_frame1, activebackground='#1d3545', image=re_take, bd=0, bg='#1d3545',command=lambda: camera('cam'))
                    re_take_shot.pack(side=LEFT)

                    save_shot = Button(cam_btn_frame1, activebackground='#1d3545', image=cam_save, bd=0, bg='#1d3545', command=cam_save_pic)
                    save_shot.pack(padx=30, side=LEFT)

                    cancel_cam_btn = Button(cam_btn_frame1, activebackground='#1d3545', image=cam_cancel, bd=0, bg='#1d3545', command=cancel)
                    cancel_cam_btn.pack(side=RIGHT)

                def select_img():
                    global rgb

                    _, img = cap.read()
                    try:
                        img = cv2.resize(img, (350, 300))
                        img = cv2.circle(img, (175, 150), 200, (69, 53, 29), 100)
                        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                        image = Image.fromarray(rgb)
                        img_tk = ImageTk.PhotoImage(image)
                        cam.configure(image=img_tk)
                        cam.image = img_tk
                        cam.after(10, select_img)
                    except:
                        pass

                if btn == 'cam':
                    try:
                        test_cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
                        _, img = test_cam.read()
                        if _:
                            cam_conn = True
                        else:
                            cam_conn = False
                        test_cam.release()
                    except:
                        pass

                    try:
                        global cap

                        profile_pic_frame.destroy()

                        camera_frame = Frame(account_frame, bg='#1d3545')
                        camera_frame.pack(padx=269, side=RIGHT)

                        cam = Label(camera_frame, bg='#1d3545')
                        cam.pack()
                        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
                    except:
                        pass

                    if cam_conn:
                        cam_btn_frame = Frame(camera_frame, bg='#1d3545')
                        cam_btn_frame.pack(pady=(30, 50))

                        take_shot = Button(cam_btn_frame, activebackground='#1d3545', image=capture, bd=0, bg='#1d3545',
                                           command=lambda: take_copy(rgb))
                        take_shot.pack(padx=(0, 30), side=LEFT)

                        cancel_cam_btn = Button(cam_btn_frame, activebackground='#1d3545', image=cam_cancel, bd=0, bg='#1d3545', command=cancel)
                        cancel_cam_btn.pack(side=RIGHT)

                        select_img()

                    else:
                        cam.config(text='Camera Error...', font='arial 40 bold', fg='#fff1e1', bg='#1d3545')
                        camera_frame.pack_configure(padx=230)
                        error_msg = messagebox.showerror('Camera Error', 'Camera Connection problem')
                        camera_frame.destroy()
                        profile_pic_frame.destroy()
                        profile_pic()

                elif btn == 'upload':
                    try:
                        img_filepath = filedialog.askopenfilename(title='Select a Image',
                                                                  filetype=[('JPEG (*.JPEG)', '.jpeg'),
                                                                            ('PNG (*.PNG)', '.png')])

                        img = cv2.imread(img_filepath)
                        img = cv2.resize(img, (350, 300))
                        img = cv2.circle(img, (175, 150), 200, (69, 53, 29), 100)

                        cv2.imwrite('Images/Profile_pic/temp_image.png', img)

                        temp_profile()

                        profile_pic_image.config(image=temp_profile_img)
                    except:
                        pass

            def upload_save():
                profile_pic_path = 'Images/Profile_pic/temp_image.png'

                def convert_To_binary(path):
                    with open(profile_pic_path, 'rb') as file:
                        binary_data = file.read()
                    return binary_data

                try:
                    conn = mysql.connect(host='localhost', username='root', password='', database='cromwell')
                    cursor = conn.cursor()

                    query = 'UPDATE account SET profile_pic = %s WHERE id = %s'
                    value = convert_To_binary(profile_pic_path), id_number
                    cursor.execute(query, value)
                    update = 'success'
                    conn.commit()
                except:
                    pass

                try:
                    if update == 'success':
                        os.remove('Images/Profile_pic/temp_image.png')
                        my_account()
                        profile_pic_frame.destroy()
                        profile_pic()
                        confirmation_msg = messagebox.showinfo('Information', 'Image save successfully')
                except:
                    pass

            profile_pic_frame = Frame(account_frame, bg='#1d3545')
            profile_pic_frame.pack(padx=225, side=RIGHT)

            image_btn_frame = Frame(profile_pic_frame, bg='#1d3545')
            image_btn_frame.pack()

            image_frame = Frame(image_btn_frame, bg='#1d3545')
            image_frame.pack(side=LEFT)

            btn_image_frame = Frame(image_btn_frame, bg='#1d3545')
            btn_image_frame.pack(side=RIGHT)

            profile_pic_image = Label(image_frame, bg='#1d3545', image=profile_img)
            profile_pic_image.pack(padx=20)

            take_image_btn = Button(btn_image_frame, activebackground='#1d3545', bd=0, bg='#1d3545', image=take_image,
                                    command=lambda: camera('cam'))
            take_image_btn.pack(pady=15)

            upload_image_btn = Button(btn_image_frame, activebackground='#1d3545', bd=0, bg='#1d3545', image=upload_image, command=lambda: camera('upload'))
            upload_image_btn.pack()

            b_btn_frame = Frame(profile_pic_frame, bg='#1d3545')
            b_btn_frame.pack(padx=(55, 0), pady=(90, 20))

            b_save = Button(b_btn_frame, activebackground='#1d3545', bd=0, image=b_save_btn, bg='#1d3545', command=upload_save)
            b_save.pack(padx=(0, 40), side=LEFT)

            b_cancel = Button(b_btn_frame, activebackground='#1d3545', bd=0, image=b_cancel_btn, bg='#1d3545', command=cancel)
            b_cancel.pack(side=RIGHT)

        account_frame = Frame(window, bg='#fff1e1')
        account_frame.place(x=145, y=100)

        account_bg = Label(account_frame, bg='#fff1e1', image=account_bg_image)
        account_bg.place(x=0, y=0)

        btn_frame = Frame(account_frame, bg='#1d3545')
        btn_frame.pack(padx=7, pady=(160, 212), side=LEFT)

        basic_btn = Button(btn_frame, bd=0, bg='#1d3545', fg='#fff1e1', height=2, width=17, font='times 18',
                           text='        Basic Info', anchor=W, command=basic_information)
        basic_btn.pack(anchor=W)

        security_btn = Button(btn_frame, bd=0, bg='#1d3545', fg='#fff1e1', height=2, width=17, font='times 18',
                              text='        Security', anchor=W, command=security)
        security_btn.pack(pady=10, anchor=W)

        profile_btn = Button(btn_frame, bd=0, bg='#1d3545', fg='#fff1e1', height=2, width=17, font='times 18',
                             text='        Profile pic', anchor=W, command=profile_pic)
        profile_btn.pack(anchor=W)

        basic_information()

    def about_system():
        global about_frame

        try:
            nav_frame.destroy()
            home_top_btn.place_configure(x=924, y=0)
            window.unbind('<Button-1>')
        except:
            pass
        try:
            home_frame.destroy()
            bal_amount_frame.destroy()
        except:
            pass
        try:
            payment_frame.destroy()
        except:
            pass
        try:
            cash_in_frame.destroy()
        except:
            pass
        try:
            success_trans.destroy()
        except:
            pass
        try:
            form_frame.destroy()
        except:
            pass
        try:
            account_frame.destroy()
        except:
            pass
        try:
            about_frame.destroy()
        except:
            pass
        try:
            activity_frame.destroy()
        except:
            pass
        try:
            details_frame.destroy()
        except:
            pass
        try:
            cap.release()
            camera_frame.destroy()
        except:
            pass
        try:
            os.remove('Images/Profile_pic/temp_image.png')
        except:
            pass

        def ok():
            about_frame.destroy()
            home_page()

        def set_text_newline(s):
            h_details.insert(END, s)

        home_btn.config(bg='#1d3545', fg='#fff1e1', state=NORMAL)
        act_btn.config(bg='#1d3545', fg='#fff1e1', state=NORMAL)
        pay_btn.config(bg='#1d3545', fg='#fff1e1', state=NORMAL)

        about_frame = Frame(window)
        about_frame.pack(pady=(160, 0))

        d_bg = Label(about_frame, bg='#fff1e1', image=details_bg_image)
        d_bg.place(x=0, y=0)

        h_details = Text(about_frame, bd=0, bg='#fff1e1', fg='#1d3545', font='times 18', height=9, width=45)
        h_details.pack(padx=(35, 65), pady=(90, 0))

        ok_btn = Button(about_frame, activebackground='#fff1e1', bd=0, bg='#fff1e1', image=ok_btn_image, command=ok)
        ok_btn.pack(pady=(10, 60))

        set_text_newline('In simple terms, Minato is “e-money” that allows you to\n')
        set_text_newline('pay bills, cash-in or cash-out money with the use of\n')
        set_text_newline('your pc or laptop\n\n')
        set_text_newline('Through a “mobile wallet,” you get to do all these\n')
        set_text_newline('transactions anytime and anywhere without the need to withdraw money. Compare that to carrying cash in your pocket which has a higher risk of getting lost or stolen.')

        h_details.config(state=DISABLED)

    def navigation_bar():
        global nav_frame

        window.focus()

        def clear_nav(event):
            nav_frame.destroy()
            home_top_btn.place_configure(x=924, y=0)
            window.unbind('<Button-1>')

        def mouse_in_nav(event):
            window.unbind('<Button-1>')

        def mouse_out_nav(event):
            window.bind('<Button-1>', clear_nav)

        def sig_out():
            nav_frame.destroy()
            home_top_btn.place_configure(x=924, y=0)
            confirmation_msg = messagebox.askyesno('Confirmation', 'Do you want to sign-out')

            if confirmation_msg > 0:
                try:
                    os.remove('Images/Profile_pic/profile.png')
                except:
                    pass
                try:
                    os.remove('Images/Profile_pic/temp_image.png')
                except:
                    pass
                window.destroy()
                main_window()

        home_top_btn.place_configure(x=671, y=0)

        nav_frame = Frame(window, bg='#1d3545', width=500, height=750)
        nav_frame.place(x=1015, y=0)

        nav_bg = Label(nav_frame, bg='#1d3545', image=nav_bg_image)
        nav_bg.place(x=0, y=0)

        nav_image = Label(nav_frame, bg='#1d3545', image=profile_img)
        nav_image.pack(padx=(w, h), pady=(90, 15))

        nav_name = Label(nav_frame, bg='#1d3545', fg='#fff1e1', font='times 20', text=f'{firstname} {lastname}')
        nav_name.pack(pady=(0, 90))

        account = Button(nav_frame, bd=0, bg='#1d3545', fg='#fff1e1', font='times 18', text='Account', height=2,
                         width=25, activebackground='#fff1e1', activeforeground='#1d3545', command=account_status)
        account.pack()

        about = Button(nav_frame, bd=0, bg='#1d3545', fg='#fff1e1', font='times 18', text='About', height=2, width=25,
                       activebackground='#fff1e1', activeforeground='#1d3545', command=about_system)
        about.pack(pady=(0, 110))

        about = Button(nav_frame, bd=0, bg='#1d3545', fg='#fff1e1', font='times 15', text='Sign out',
                       activebackground='#fff1e1', activeforeground='#1d3545', command=sig_out)
        about.pack(pady=(0, 100))

        home_top_btn.bind('<Enter>', mouse_in_nav)
        home_top_btn.bind('<Leave>', mouse_out_nav)
        nav_frame.bind('<Enter>', mouse_in_nav)
        nav_frame.bind('<Leave>', mouse_out_nav)

    home_bg_frame = Frame(window, width=1400, height=800)
    home_bg_frame.place(x=0, y=0)

    home_bg = Label(home_bg_frame, bd=0, image=home_bg_image)
    home_bg.place(x=0, y=0)

    home_top_btn = Frame(window, bg='#1d3545', width=450, height=88)
    home_top_btn.place(x=924, y=0)

    nav_btn = Button(home_top_btn, bd=0, bg='#1d3545', image=tab_btn_image, activebackground='#1d3545',
                     command=navigation_bar)
    nav_btn.place(x=370, y=25)

    act_frame = Frame(home_top_btn)
    act_frame.place(x=230, y=0)

    pay_frame = Frame(home_top_btn)
    pay_frame.place(x=110, y=0)

    home_btn_frame = Frame(home_top_btn)
    home_btn_frame.place(x=1, y=0)

    act_btn = Button(act_frame, bd=0, fg='#fff1e1', font='times 18', bg='#1d3545', text='Activity',
                     activebackground='#fff1e1', command=activity_page)
    act_btn.pack(ipady=23, ipadx=10)

    pay_btn = Button(pay_frame, bd=0, fg='#fff1e1', font='times 18', bg='#1d3545', text='Payment',
                     activebackground='#fff1e1', command=payment_page)
    pay_btn.pack(ipady=23, ipadx=10)

    home_btn = Button(home_btn_frame, bd=0, fg='#1d3545', font='times 18', bg='#fff1e1', text='Home',
                      activebackground='#fff1e1', command=home_page)
    home_btn.pack(ipady=23, ipadx=18)

    home_page()

    def close():
        try:
            os.remove('Images/Profile_pic/profile.png')
        except:
            pass
        try:
            os.remove('Images/Profile_pic/temp_image.png')
        except:
            pass
        window.destroy()

    window.protocol('WM_DELETE_WINDOW', close)

    window.mainloop()

splash_screen()
