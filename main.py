import tkinter as tk, tkinter
from tkinter import messagebox as mb
from mysql.connector import connect
import random
import json
from PIL import Image, ImageTk, ImageDraw
import uuid
import tkinter.font as tkFont
import tkext as tkmisc
try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal
from datetime import date as _datetimedate
import datetime as dt
import os
from dotenv import load_dotenv
import sys
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import date
from dateutil.relativedelta import relativedelta

load_dotenv()


try:
    _pass = os.getenv("passtwo")
    mydb = connect(
        host="localhost",
        user="root",
        passwd=_pass,
        database="TRAINS")
except:
    try:
        _pass = os.getenv("passone")
        mydb = connect(
            host="localhost",
            user="root",
            passwd=_pass,
            database="TRAINS")
    except:
        print("Error Connecting to Database!")
        sys.exit()
db=mydb
cu = mydb.cursor()


class ticket:
    def __init__(self,
                 trainno:str,
                 fromst:str,
                 tost:str,
                 uid:str='0'
                 ):
        self.trainno = trainno
        self.uid = uid
        self.date = _datetimedate.today()
        self.fromst = fromst
        self.tost = tost

    def generate_ticket(self, 
                        get: Literal["create", "check"] = "create"):

        x = basic.getdatawhere(type="*", name="trst", where=f"number='{self.trainno}'")[0]
        path=x[1]
        ind = []
        cost=x[2]
        path=json.loads(path)
        for i in path:
            if self.fromst == i:
                ind.append([path.index(i), i])
            elif self.tost == i:
                if ind != []:
                    ind.append([path.index(i), i])
                else:
                    mb.showerror(title="Error", message="Invalid Stations Selected.")
        if len(ind) < 2:
            mb.showerror(title="Error", message="Invalid Stations Selected.")
            print(ind)
            return False
        actual = path[ind[0][0]:ind[1][0]+1]
        _iternary = {
            'trainno':self.trainno,
            'path':((ind[0][1], ind[1][1]), actual),
            'cost':cost
        }
        return _iternary
    def multigenerate(self,
                      dte, 
                      *args):
        """
        *Args:
            0: name
            1: age
            2: gender
        """
        n = len(args)
        x = basic.getdatawhere(type="*", name="trst", where=f"number='{self.trainno}'")[0]
        path = x[1]
        ind = []
        cost = x[2]
        if basic.getdatawhere("wallet", "userlogin", f"id={self.uid}")[0][0] < cost*n:
            mb.showerror(title="Error", message="Insufficient Balance!")
            return False
        path = json.loads(path)
        for i in path:
            if self.fromst == i:
                ind.append([path.index(i), i])
            elif self.tost == i:
                if ind!=[]:
                    ind.append([path.index(i), i])
                else:
                    mb.showerror(title="Error", text="Invalid Sections Selected")
        if len(ind) < 2:
            mb.showerror(title="Error", text="Invalid Sections Selected")
            print(ind)
            return False
        actual = path[ind[0][0]:ind[1][0]+1]
        ticd = 0
        for i in range(999999999):
            ticd = random.randint(100000000, 999999999)
            if basic.getdatawhere("tid", 'ticketiternary', f'tid={ticd}') == []:
                break
        _iternary = {
            'path':((ind[0][1], ind[1][1]), actual),
            }
        k=1
        for i in args:
            _iternary[f"{k}"] = {
                'uid':self.uid,
                'name':i[0],
                'age':i[1],
                'gender':i[2],
                'trainno':self.trainno,
                'cost':cost,
                }   
            k+=1 
        iternary=json.dumps(_iternary)
        dtx = str(date.isoformat(dte))
        cu.execute('insert into ticketiternary values (%s, %s, %s, %s, %s)', (self.uid, self.trainno, iternary,ticd, dtx))
        db.commit()
        data = basic.getdatawhere(type="*", name="userlogin", where=f'id="{self.uid}"')[0]
        cu.execute(f'update userlogin set wallet = {data[4] - (cost*n)} where id = "{self.uid}"')
        db.commit()
        return True
        
    def cancel_ticket(self, ticket_id):
        cu.execute(f'select * from ticketiternary where tid="{ticket_id}" and trainno="{self.trainno}"')
        data = cu.fetchall()
        cuid = basic.getdatawhere(type="id", name="userlogin", where=f"log='{hex(uuid.getnode())}'")[0][0]
        if data==[]:
            return False, mb.showerror(title="Error", message="No Data Found!")
        else:
            cost = basic.getdatawhere(type="cost", name="trst", where=f"number='{self.trainno}'")[0][0]
            cost = 0.3*cost
            resp = mb.askyesno(
                title="Confirm",
                message=f"""Are you sure you want to cancel this ticket?

Refund Amount: ₹{cost}

Note:  This can't be undone!"""
            )
            if resp:
                pass
            else:
                return False
            up = basic.getdatawhere("wallet", 'userlogin', f'id={cuid}')[0][0] + cost
            cu.execute(f'Update userlogin set wallet={up} where id={cuid}')
            cu.execute(f"delete from ticketiternary where uid={cuid}")
            db.commit()
            return True, mb.showinfo(title="Done!", message=f"Your ticket has been cancelled!\nRefund Amount: {cost}")
    
    def change_boarding(self, cur:str = None):
        data = basic.getdatawhere("iternary", "ticketiternary", f"uid={self.uid} and trainno={self.trainno}")
        if data == []:
            return False, mb.showerror(title="Error", message="Can't find ticket!")
        else:
            data=data[0][0]
            data=json.loads(data)
            _board=data['path']
            _board[0].pop(0)
            _board[0].insert(0, cur)
            x = basic.getdatawhere(type="*", name="trst", where=f"number='{self.trainno}'")[0]
            path=x[1]
            ind = []
            cost=x[2]
            path=json.loads(path)
            for i in path:
                if cur == i:
                    ind.append([path.index(i), i])
                elif self.tost == i:
                    if ind != []:
                        ind.append([path.index(i), i])
                    else:
                        mb.showerror(title="Error", message="Invalid Stations Selected")
            if len(ind) != 2 or len(ind) < 2:
                mb.showerror(title="Error", message="Invalid Stations Selected")
            
            _actual = path[ind[0][0]:ind[1][0]+1]
            _fin = [[cur, _board[0][1]] ,_actual]
            data['path']=_fin
            _data = json.dumps(data)
            cu.execute("update ticketiternary set iternary=%s where uid=%s and trainno=%s", (_data, self.uid, self.trainno))
            db.commit()
            return True, mb.showinfo(title="Done", message="Boarding Changed!")        

class basic:
    def getdata(
                type:str, 
                name: str
                ):
        cu.execute(f'select {type} from {name}')
        k = cu.fetchall()
        return k
    def getdatawhere(
                    type:str, 
                    name:str, 
                    where:str
                    ):
        cu.execute(f'select {type} from {name} where {where}')
        k = cu.fetchall()
        return k 
def gettime(train):
        time = basic.getdatawhere('departure', 'schedules', f'train_number={train}')[0][0]
        time = time.split(':')
        if int(time[0]) < 12:
            ap='am'
            l = time[0]
        else:
            ap='pm'
            l = str(int(time[0]) - 12)
        time = l + ":" + time[1] + f' {ap}'
        return time 

class user:
    def login(user: str, password: str):
        current_device = hex(uuid.getnode())

        cu.execute(
            'SELECT log FROM userlogin WHERE name = %s',
            (user,)
        )

        status = cu.fetchall()

        if not status:
            return False

        stored_device = status[0][0]

        if stored_device != "0" and stored_device != current_device:
            mb.showerror(
                'Error',
                'Already logged in from another computer!'
            )
            return False
        elif stored_device==current_device:
            mb.showerror(
                "Error",
                "Already Running Another Instance!")
            return False
        
        cu.execute(
            'UPDATE userlogin SET log = %s WHERE name = %s',
            (current_device, user)
        )

        db.commit()

        return True
    
    def logout(*args: str):
        for user in args:     
            cu.execute(f'update userlogin set log = "0" where name = "{user}"')
            mydb.commit()
        return True, print('Logout Successfull')
        
    def register(name, 
                 password, 
                 confirm_password, 
                 phone, 
                 email
                 ):
        if name == "" or password == "" or confirm_password == "" or phone == "" or email == "":
            return False, mb.showerror("Error", "Details Missing")
        if "@" not in email:
            return False, mb.showerror("Error", "Invalid Email!")
        cu.execute('Select * from userlogin')
        checkdata = cu.fetchall()
        if len(phone) != 10: 
            mb.showerror("Error", 
                         "Phone number must be 10 digits")
            return False
        for i in checkdata:
            if i[0] == name:
                mb.showerror("Error", 
                             "Username already exists")
                return False
            elif i[2] == phone:
                mb.showerror("Error", 
                             "Phone number already exists")
                return False
            
            elif i[3] == email:
                mb.showerror("Error", 
                             "Email already exists")
                return False
        if confirm_password != password:
            mb.showerror("Error", 
                         "Confirmed Password do not match")
            return False
        
        id = None
        cu.execute('Select id from userlogin')
        fetch = cu.fetchall()
        if fetch == []:
            id = random.randint(100000000, 999999999)
        else:
            for i in fetch:
                id = random.randint(100000000, 999999999)
                if i != id:
                    print('id successful: ', id)
                    loopcount = 1
                    break
                else:
                    print("id Generated")

        cu.execute('Insert into userlogin (name, password, phone, email, wallet, id, log) values (%s, %s, %s, %s,%s, %s, %s)', 
                   (name, 
                    password, 
                    phone, 
                    email, 
                    5000.00, 
                    id, 
                    "0")) 
        mb.showinfo(title="Successfull", message="User Registered.")  
        mydb.commit() 
        return True



class admin:
    def __init__(self, 
                 username:str, 
                 password:str
                 ):
        self.username = username
        self.password = password

    def login(self):
        print('Admin Login Called..')
        cu.execute(f'Select * from adminlogin where uniqueid = "{self.username}"') 
        fetch = cu.fetchall()
        if fetch == []:
            return print("Username does not exist"), False
        elif self.username == fetch[0][0] and self.password == fetch[0][1]:
            return print('Login successful'), True
        else:
            return print("Incorrect Password"), False
        
class traindata:
    def __init__(self, 
                 trainno: str):
        self.number = trainno
        self.trainpath = json.loads(basic.getdatawhere('stxdata', 'traininfo', f'fromnum = "{self.number}"')[0][0])
        self.stx = []
        g = basic.getdata('name, cords, code', 'stations')
        for i in g:
            self.stx.append([i[0], json.loads(i[1]), i[2]])

    def get_train(self):
        data = basic.getdatawhere('*', 'traininfo', f'fromnum = "{self.number}"')
        return data

    def get_schedule(self):
        result = []
        for i in self.trainpath:
            print(i)
            for l in self.stx:
                if i == l[1]:
                    result.append([l[0], l[2]])
                else:
                    print('err')
        return result

class mainwindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.searched_train = None
        self.title('Train Ticket Reservation Window')
        self.geometry("900x500")
        self.option_add("*Font", "Consolas 10")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.resizable(False, False)
        container = tk.Frame(self)
        container.grid(row = 0, column=0, sticky='nsew')
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames={}

        for currentpage in (loginpage, secondpage):
            name = currentpage.__name__
            frame = currentpage(parent=container, controller=self)
            self.frames[name] = frame
            frame.grid(row=0, column=0, sticky='nsew')
        self.show_frame("loginpage")

    
    def show_frame(self, frname: Literal["loginpage", "secondpage"]):
        frame = self.frames[frname]
        frame.tkraise()

class loginpage(tk.Frame):
    def __init__(self,
                 parent, 
                 controller
                 ):
        super().__init__(parent)
        self.controller = controller
        img = Image.open("assets/fajrbackground.png")
        img = img.resize((900, 500))
        self.bgimage = ImageTk.PhotoImage(img)   
        self.bg = tk.Label(self, image=self.bgimage)
        self.bg.place(x=0,     
                      y=0, relwidth=1, relheight=1)

        img = Image.open("assets/title.png")
        img = img.resize((900, 39))

        self.titleimg = ImageTk.PhotoImage(img)
        

        self.title = tk.Label(self, image = self.titleimg,
                              padx=0,
                              pady=0,
                              borderwidth=0,
                              relief="flat",
                              highlightthickness=1,
                              highlightbackground="black",
                              )
        self.title.place(x=0, y=0)


        simg = Image.open('assets/dawnbackground.png')
        simg = simg.resize((450, 390))
        self.searchbgimg = ImageTk.PhotoImage(simg)
        self.searchbg = tk.Label(self, 
                                 image=self.searchbgimg,
                                 padx=0,
                                 pady=0,
                                 bg="#76ABAE",
                                 highlightthickness=1,
                                 highlightbackground="black",
                                 relief="solid",
                                 borderwidth=3).place(x=55,
                                                        y=75,
                                                        width=450,
                                                        height=390)

        self.froentry = tk.Entry(self)
        self.froentry.place(x=110, y=115, width=115, height=20)

        self.toentry = tk.Entry(self)
        self.toentry.place(x=230, y=115, width=115, height=20)
        self.searchbtn = tk.Button(self, 
                                   text="Search Trains", 
                                   relief="raised", 
                                   bg="#AEE2FF",
                                   font="consolas 9 bold",
                                   command=lambda: search_cmd())
        #20+(115-101)
        self.searchbtn.place(x=350, y=115, height=20, width=100)
        
        self.frolab = tk.Label(self, 
                               text="From Station", 
                               bg="#C7C4D9",
                               font=('consolas', 9, 'bold'),
                               anchor="w").place(x=110, 
                                                   y=101, 
                                                   width = 115,
                                                   height=11,)
        self.tolab = tk.Label(self, 
                              text="To Station", 
                              bg="#C7C4D9",
                              anchor="w",
                              font=('consolas', 9, 'bold')).place(x=230, y=101, 
                                                  width = 115, 
                                                  height=11)
        self.stx = []
        self.stations=[]   
        g = basic.getdata('name, cords, code', 'stations')
        for i in g:
            self.stx.append([i[0], json.loads(i[1]), i[2]])
            self.stations.append(f"{i[0]} - {i[2]}")

        self.optionslist = tk.Listbox(self)
        self.optionslist.bind("<ButtonRelease-1>", 
                              lambda event: self.select_option(event, self.froentry, self.optionslist))
        
        self.froentry.bind(
            "<KeyRelease>",
            lambda event: self.filter_options(
                event, self.froentry, self.stations, self.optionslist))
        self.froentry.bind(
            "<FocusIn>", 
            lambda event: self.show_dropdown(self.froentry, self.optionslist))
        self.froentry.bind(
            "<FocusOut>",
            lambda event: self.hide_dropdown(self.optionslist, None))

        self.optionslist2 = tk.Listbox(self)
        self.optionslist2.bind("<ButtonRelease-1>",
                               lambda event: self.select_option(event, self.toentry, self.optionslist2))
        self.toentry.bind(
            "<KeyRelease>",
            lambda event: self.filter_options(
                event, self.toentry, self.stations, self.optionslist2))
        self.toentry.bind(
            "<FocusIn>", 
            lambda event: self.show_dropdown(self.toentry, self.optionslist2))
        self.toentry.bind(
            "<FocusOut>",
            lambda event: self.hide_dropdown(self.optionslist, None))


        self.resultscontainer = tk.Frame(self)
        _h=285
        self.resultscontainer.place(
            x=110,
            y=150,
            width=340,
            height=_h
        )

        self.resultscanvas = tk.Canvas(
            self.resultscontainer,
            highlightthickness=0,
            bg="#F8F3D9"
        )

        self.resultsscrollbar = tk.Scrollbar(
            self.resultscontainer,
            orient="vertical",
            command=self.resultscanvas.yview,
        )

        self.resultsframe = tk.Frame(
            self.resultscanvas,
            bg="#F8F3D9"
        )

        self.resultsframe.bind(
            "<Configure>",
            lambda e: self.resultscanvas.configure(
                scrollregion=self.resultscanvas.bbox("all")
            )
        )

        self.resultscanvas.create_window(
            (0, 0),
            window=self.resultsframe,
            anchor="nw",
            width=320,
        )

        self.resultscanvas.configure(
            yscrollcommand=self.resultsscrollbar.set
        )

        self.resultscanvas.place(
            x=0,
            y=0,
            width=320,
            height=_h
        )

        self.resultsscrollbar.place(
            x=320,
            y=0,
            width=20,
            height=_h
        )
        self.resultscontainer.grid_rowconfigure(
            0,
            weight=1
        )
        self.resultscontainer.grid_columnconfigure(
            0,
            weight=1
        )

        def search_cmd():
            if self.froentry.get() == "" or self.toentry.get() == "":
                mb.showerror(title="Error!", message="No Stations Selected")
                return False
            fromcode = self.froentry.get().split(" - ")[1]
            tocode = self.toentry.get().split(" - ")[1]
            cu.execute("""
                    SELECT DISTINCT a.trainno
                    FROM train_stops a
                    JOIN train_stops b
                        ON a.trainno = b.trainno
                    WHERE a.station_code=%s
                    AND b.station_code=%s
                    AND a.stop_order < b.stop_order;
                    """,
                    (
                    fromcode, 
                    tocode
                )
            )
            data = cu.fetchall()
            if data==[]:
                mb.showerror(title="Error", message="No Trains Found!")
                return False
            _fin = {}
            for i in data:
                val = ticket(
                    trainno=i[0],
                    fromst=fromcode,
                    tost=tocode
                )
                w = basic.getdatawhere('name', 'traininfo', f'fromnum="{i[0]}"')
                _fin[i[0]] = (val.generate_ticket('check'), w)
            for widget in self.resultsframe.winfo_children():
                widget.destroy()
            bgclr = "#F8DFB7"
            im = Image.open("assets/search.png")
            im = im.resize((320, 100))
            self.timg = ImageTk.PhotoImage(im)
            for train in _fin:
                trainframe=tk.Frame(
                    self.resultsframe,
                    bd=2,
                    relief="flat",
                    width=320,
                    height=100,
                    borderwidth=.5,
                )
                trainframe.pack(
                    padx=5,
                    pady=5    
                )
                inl = tk.Label(trainframe,
                               image=self.timg,
                               padx=0,
                               pady=0,
                               borderwidth=0.5,
                               relief="flat",).place(x=0,
                                                     y=0)
                trainframe.pack_propagate(False)
                tk.Label(
                    trainframe,
                    text=f"Train No: {train}",
                    bg=bgclr
                ).place(x=10,
                        y=10,
                        height=10
                    )
                tk.Label(
                    trainframe,
                    text=f"{fromcode} → {tocode}",
                    bg=bgclr
                ).place(
                    x=200,
                    y=10,
                    height=10
                )
                try:
                    name=_fin[train][1][0][0]
                except:
                    name="Name Not Found!"
                tk.Label(
                    trainframe,
                    text=name,
                    bg=bgclr
                ).place(x=10,
                        y=30,
                        height=15
                    )
                time = basic.getdatawhere('departure', 'schedules', f'train_number={train}')[0][0]
                time = time.split(':')
                if int(time[0]) < 12:
                    ap='am'
                    l = time[0]
                else:
                    ap='pm'
                    l = str(int(time[0]) - 12)
                time = l + ":" + time[1] + f' {ap}'
                tk.Label(
                    trainframe,
                    text=f"First Departure: {time}",
                    bg=bgclr
                ).place(x=10,
                        y=50,
                        height=15
                    )
                tk.Button(
                    trainframe,
                    text="Book",
                    command=lambda trainno=train: booktrain(trainno, fromcode, tocode)
                ).place(x=10,
                        y=70,
                        height=20,
                        width=130
                    )
                
                tk.Button(
                    trainframe,
                    text="Info",
                    command=lambda trainno=train: traininfo(trainno, fromcode, tocode)
                ).place(x=160,
                        y=70,
                        height=20,
                        width=130
                    )
            
            def traininfo(trainnum, fro, to):
                pop = tk.Toplevel(self,
                                  bg="#FFF0BE")
                pop.title("Traininfo")
                pop.geometry("550x160")
                pop.resizable(False, False)
                pop.grab_set()

                tk.Label(
                    pop,
                    text=f"{_fin[trainnum][1][0][0]} ({trainnum})",
                    bg="#FFF0BE",
                    font="courier 15 bold"
                ).place(
                    x=10,
                    y=10    
                )
                sc = basic.getdatawhere('path', 'trst', f'number={int(trainnum)}')[0][0]
                sc= json.loads(sc)
                sn = basic.getdatawhere('name', 'stations', f'code="{sc[0]}"')
                sn2 = basic.getdatawhere('name', 'stations', f'code="{sc[-1]}"')
                x = ticket(
                        trainno=trainnum,
                        fromst=fro,
                        tost=to
                    ).generate_ticket('check')
                
                nx=220
                cx=475
                
                start = sc[0]
                end = sc[-1]
                tk.Label(
                    pop,
                    text=f"Starts at:",
                    bg="#FFF0BE",
                    font="courier 11"
                ).place(
                    x=10,
                    y=40
                )
                tk.Label(
                    pop,
                    text=f"Ends at:",
                    bg="#FFF0BE",
                    font="courier 11"
                ).place(
                    x=10,
                    y=60
                )
                tk.Label(
                    pop,
                    text=f"{sn[0][0]}",
                    bg="#FFF0BE",
                    font="courier 11"
                ).place(
                    x=nx,
                    y=40
                )
                tk.Label(
                    pop,
                    text=f"{sn2[0][0]}",
                    bg="#FFF0BE",
                    font="courier 11"
                ).place(
                    x=nx,
                    y=60
                )
                tk.Label(
                    pop,
                    text=f'{start}',
                    bg="#FFF0BE",
                    font="courier 11"
                ).place(
                    x=cx,
                    y=40
                )
                tk.Label(
                    pop,
                    text=f'{end}',
                    bg="#FFF0BE",
                    font="courier 11"
                ).place(
                    x=cx,
                    y=60
                )
                tk.Label(
                    pop,
                    text=f"{fro} → {to}",
                    bg="#FFF0BE",
                    font="courier 11"
                ).place(
                    x=nx,
                    y=100
                )
                tk.Label(
                    pop,
                    text=f"Train No.:",
                    bg="#FFF0BE",
                    font="courier 11"
                ).place(
                    x=10,
                    y=80
                )
                tk.Label(
                    pop,
                    text=f"{trainnum}",
                    bg="#FFF0BE",
                    font="courier 11"
                ).place(
                    x=nx,
                    y=80
                )
                tk.Label(
                    pop,
                    text=f"Selected:",
                    bg="#FFF0BE",
                    font="courier 11"
                ).place(
                    x=10,
                    y=100
                )
                tk.Label(
                    pop,
                    text=f"Ticket Cost:",
                    bg="#FFF0BE",
                    font="courier 11"
                ).place(
                    x=10,
                    y=120
                )
                tk.Label(
                    pop,
                    text=f"₹{x['cost']}",
                    bg="#FFF0BE",
                    font="courier 11"
                ).place(
                    x=nx,
                    y=120
                )
                l = 80
                for i in range(3):
                    tk.Label(
                        pop,
                        text=f"---",
                        bg="#FFF0BE",
                        font="courier 11"
                    ).place(
                        x=cx,
                        y=l
                    )
                    l+=20
                
           
            def booktrain(t, fro, to):
                if basic.getdatawhere('log', 'userlogin', f'log="{hex(uuid.getnode())}"') == []:
                    mb.showerror(
                        title="Error",
                        message="Can't find user data\nTry Logging in!"
                    )
                    return False
                else:
                    user = basic.getdatawhere('id, name, email, wallet, phone', 'userlogin', f'log="{hex(uuid.getnode())}"')[0]
                    print(user)
                    book = tk.Toplevel(self)
                    book.title("Booking Window")
                    book.geometry("675x400")
                    book.resizable(False, False)
                    book.grab_set()
                    img = Image.open("assets/bookingbackground.png")
                    img = img.resize((675, 400))
                    book.bgimage = ImageTk.PhotoImage(img)
                    bg = tk.Label(
                        book,
                        image=book.bgimage
                    )
                    bg.place(
                        x=0,
                        y=0,
                        relwidth=1,
                        relheight=1
                    )
                    title=Image.open("assets/Templates/title.png")
                    book.timg = ImageTk.PhotoImage(title)
                    title = tk.Label(book,
                                     image=book.timg,
                                     relief="flat"
                                     ).place(x=0, 
                                            y=0)
                    book.altopt = tk.Frame(book)
                    _h=300
                    _w=260
                    book.altopt.place(
                        x=400,
                        y=80,
                        width=_w,
                        height=_h
                        )
                    book.altoptcanvas = tk.Canvas(
                        book.altopt,
                        highlightthickness=0,
                        bg="#F8F3D9"
                    )
                    book.altoptscrollbar = tk.Scrollbar(
                        book.altopt,
                        orient="vertical",
                        command=book.altoptcanvas.yview
                    )
                    book.altoptframe = tk.Frame(
                        book.altoptcanvas,
                        bg="#F8F3D9"
                    )
                    book.altoptframe.bind(
                        "<Configure>",
                        lambda e: book.altoptcanvas.configure(
                            scrollregion=book.altoptcanvas.bbox("all")
                        )
                    )
                    book.altoptcanvas.create_window(
                        (0,0),
                        window=book.altoptframe,
                        anchor="nw",
                        width=_w-20,
                    )
                    book.altoptcanvas.configure(
                        yscrollcommand=book.altoptscrollbar.set
                    )
                    book.altoptcanvas.place(
                        x=0,
                        y=0,
                        width=_w-20,
                        height=_h
                    )
                    book.altoptscrollbar.place(
                        x=_w-20,
                        y=0,
                        width=20,
                        height=_h
                    )
                    book.altopt.grid_rowconfigure(
                        0,
                        weight=1
                    )
                    book.altopt.grid_columnconfigure(   
                        0,
                        weight=1
                    )
                    tk.Label(book, 
                            text="Alternate Trains",
                            bg="#F8F3D9",
                            font="Consolas 10 bold", 
                            anchor="c").place(
                                x=400,
                                y=60,
                                width=_w
                                )
                    book.background = tk.Label(book,
                                              bg="#F8F3D9",
                                              borderwidth=0,).place(
                                                  x=15,
                                                  y=60,
                                                  width=370,
                                                  height=320)
                    book.trainname = tk.Label(book,
                                              bg="#F8F3D9",
                                              font="Consolas 10 bold",
                                              anchor="w",
                                              text=f"{_fin[t][1][0][0]}")
                    book.trainname.place(
                                              x=20,
                                              y=70
                                              )

                    book.firstdep = tk.Label(book,
                                              bg="#F8F3D9",
                                            font="Consolas 10 bold",
                                            anchor="w",
                                            text=f"First Station Departure: {gettime(t)}")
                    book.firstdep.place(
                        x=20,
                        y=90
                    )
                    book.cost = tk.Label(book,
                                        bg="#F8F3D9",
                                        font="Consolas 10 bold",
                                        anchor="w",
                                        text=f"Cost: ₹{_fin[t][0]['cost']}")
                    book.cost.place(
                        x=20,
                        y=110
                    )
                    book.path = tk.Label(book,
                                        bg="#F8F3D9",
                                        font="Consolas 10 bold",
                                        anchor="w",
                                        text=f"Path: {fro} → {to}")
                    book.path.place(
                        x=220,
                        y=130
                    )
                    book.trainno = tk.Label(book,
                                           bg="#F8F3D9",
                                           font="Consolas 10 bold",
                                           anchor="w",
                                           text=f"Train Number: {t}")
                    book.trainno.place(
                        x=20,
                        y=130
                    )
                    tk.Label(book,
                                    bd=1,
                                    relief="sunken",
                                    bg="black").place(x=20, 
                                                      y=150, 
                                                      width=360, 
                                                      height=2)
                    tk.Label(
                        book,
                        text="Boarding",
                        font='consolas 10 bold',
                        bg="#F8F3D9",).place(
                            x=20,
                            y=160
                            )
                    today = date.today()
                    max_date = today + relativedelta(months=2)
                    tk.Label(
                        book,
                        text="Date Of Journey: ",
                        font='consolas 10 bold',
                        bg="#F8F3D9",
                    ).place(
                        x=90, y=180
                    )
                    date_entry = DateEntry(
                        book,
                        date_pattern="dd/mm/yyyy",
                        mindate=today,
                        maxdate=max_date
                    )
                    date_entry.place(
                        x=220,
                        y=180
                    )
                    opt = ticket(t, fro, to).generate_ticket('check')['path'][1]
                    opt = opt[0:-1]
                    def getselect():
                        selected_item = combo.get()
                        return selected_item
                    combo = ttk.Combobox(book,
                                         values=opt,
                                         state='readonly')
                    combo.set(fro)
                    combo.place(x=90, y=160, width=100)
                    def changecombopath(event, combo=combo, path_label=book.path, to=to):
                        nfro = combo.get()
                        path_label.config(text=f"Path: {nfro} → {to}")
                    book.passengers = tk.Label(
                        book,
                        text="No of Passengers: 0",
                        font="consolas 10 bold",
                        bg = "#F8F3D9"
                    )
                    book.passengers.place(
                        x=220,
                        y=160,
                        height=20
                    )
                    combo.bind("<<ComboboxSelected>>", changecombopath)
                    book.passe = tk.Frame(book)
                    h_=140
                    w_=360
                    book.passe.place(
                        x=20,
                        y=210,
                        width=w_,
                        height=h_
                        )
                    book.passecanvas = tk.Canvas(
                        book.passe,
                        highlightthickness=0,
                        bg="#fff3b3")
                    book.passescrollbaar = tk.Scrollbar(
                        book.passe,
                        orient="vertical" ,
                        command=book.passecanvas.yview   
                    )
                    book.passeframe = tk.Frame(
                        book.passecanvas,
                        bg="#fff3b3"
                    )
                    book.passeframe.bind(
                        "<Configure>",
                        lambda e: book.passecanvas.configure(
                            scrollregion=book.passecanvas.bbox("all")
                        )
                    )
                    book.passecanvas.create_window(
                        (0,0),
                        window=book.passeframe,
                        anchor="nw",
                        width=w_-20
                        )
                    book.passecanvas.configure(
                        yscrollcommand=book.passescrollbaar.set
                    )
                    book.passecanvas.place(
                        x=0,
                        y=0,
                        width=w_-20,
                        height=h_
                    )
                    book.passescrollbaar.place(
                        x=w_-20,
                        y=0,
                        width=20,
                        height=h_
                    )
                    book.passe.grid_rowconfigure(
                        0,
                        weight=1
                    )
                    book.passe.grid_columnconfigure(   
                        0,
                        weight=1
                    )
                    tk.Label(book,
                             bg="#313338").place(
                                 x=20,
                                 y=350,
                                 width=360,
                                 height=21)
                    book.totalcost = tk.Label(
                        book,
                        text="Total Cost: ₹0",
                        font="consolas 10 bold",
                        bg = "#313338",
                        fg='#FFFFFF'
                    )
                    book.totalcost.place(
                        x=100,
                        y=350
                    )
                    book.add_img = tk.PhotoImage(file="assets/pass/add.png")
                    btn = tk.Button(
                        book,
                        image=book.add_img,
                        highlightthickness=0,
                        bd=0,
                        command=lambda: addpass()
                    )
                    multi_ticket_entry = []
                    def addpass():
                        optframe = tk.Frame(
                            book.passeframe,
                            bd=2,
                            relief="flat",
                            width=w_-20,
                            height=100,
                            borderwidth=.5
                        )
                        optframe.pack(
                            padx=5,
                            pady=5
                        )
                        optframe.bgimg = tk.PhotoImage(file="assets/gender/base.png")
                        tk.Label(
                            optframe,
                            image=optframe.bgimg,
                            padx=0,
                            pady=0,
                            borderwidth=.5,
                            relief='flat'
                        ).place(x=0,
                                y=0)
                        optframe.pack_propagate(False)
                        optframe.delbtnimg = tk.PhotoImage(file="assets/pass/deletebtn.png")
                        delete_btn = tk.Button(
                            optframe,
                            image=optframe.delbtnimg,
                            command=lambda: optframe.destroy(),
                            relief='flat'
                        )
                        delete_btn.place(
                            x=310,
                            y=80,
                            height=11,
                            width=11,
                        )
                        name = tkmisc.PlaceholderEntry(
                            optframe,
                            placeholder="Name of Passenger*",
                        )
                        name.place(
                            x=10,
                            y=10,
                            width=160,
                            height=20
                        )
                        gens = ['Male', 'Female', 'Other']
                        gencombo = ttk.Combobox(
                            optframe,
                            values=gens,
                            state='readonly'
                        )
                        gencombo.set('Gender*')
                        gencombo.place(
                            x=250,
                            y=10,
                            width=70,
                            height=20
                        )
                        age=[]
                        for i in range(5, 150):
                            age.append(str(i))
                        agecombo = ttk.Combobox(
                            optframe,
                            values=age,
                            state='readonly'
                        )
                        agecombo.set('Age*')
                        agecombo.place(
                            x=180,
                            y=10,
                            width=60,
                            height=20
                        )
                        tk.Label(
                            optframe,
                            text=f"{user[0]}",
                            bg="#FFD666",
                        ).place(x=10, 
                                y=80,
                                height=10,
                            )
                        tk.Label(
                            optframe,
                            text="Class",
                            bg="#FFD666",
                        ).place(
                            x=10,
                            y=40,
                            height=10
                        )
                        classcomb = ttk.Combobox(
                            optframe,
                            values=['General'],
                            state='readonly'
                        )
                        classcomb.set('General')
                        classcomb.place(
                            x=10,
                            y=55,
                            width=70,
                            height=20
                        )
                        tk.Label(
                            optframe,
                            text="Seat",
                            bg="#FFD666",
                        ).place(
                            x=100,
                            y=40,
                            height=10
                        )
                        seatcombo = ttk.Combobox(
                            optframe,
                            values=['None'],
                            state='readonly'
                        )
                        seatcombo.set('None')
                        seatcombo.place(
                            x=100,
                            y=55,
                            width=70,
                            height=20
                        )
                        confirmbtn = tk.Button(
                            optframe,
                            text="Confirm Passenger",
                            bg="#D0F890",
                            command=lambda: confirmpassenger(),
                            anchor='c',
                            relief='raised'
                        )
                        confirmbtn.place(
                            x=180,
                            y=40,
                            height=34,
                            width=140
                        )
                        def confirmpassenger():
                            if name.get_value() == "" or agecombo.get() == "Age*" or gencombo.get() == "Gender*":
                                mb.showerror(
                                    title="Error",
                                    message="Please fill all the Necessary fields"
                                )
                                return False
                            resp = mb.askyesno(
                                title="Confirm Passenger",
                                message=f"""Are you sure you want to add this passenger?

Name: {name.get_value()}
Age: {agecombo.get()}
Gender: {gencombo.get()}
Class: {classcomb.get()}
Seat: {seatcombo.get()}

Note:  This can't be undone!
                                """
                            )
                            if resp:
                                pass
                            else:
                                return False
                            det = (name.get_value(), 
                                   agecombo.get(), 
                                   gencombo.get())
                            print(det)
                            multi_ticket_entry.append(det)
                            print(multi_ticket_entry)
                            optframe.disabled = True
                            for child in optframe.winfo_children():
                                try:
                                    child.configure(state="disabled")
                                except:
                                    pass
                            cost = book.cost.cget("text").split("₹")[1]
                            cost = int(cost)
                            book.totalcost.config(text=f"Total Cost: ₹{cost*len(multi_ticket_entry)}")
                            book.passengers.config(text=f"No of Passengers: {len(multi_ticket_entry)}")
                    btn.place(
                        x=21,
                        y=351,
                        height=19,
                    )
                    book.finalconfirm = tk.Button(
                        book,
                        text="Checkout",
                        bg="#D0F890",
                        command=lambda: confirmticket(),
                        anchor='c',
                        relief='flat'
                    )
                    book.finalconfirm.place(
                        x=270,
                        y=351,
                        height=19,
                        width=109
                    )
                    def confirmticket():
                        disabled = 0
                        enabled = 0

                        for child in book.passeframe.winfo_children():
                            if getattr(child, "disabled", False):
                                disabled += 1
                            else:
                                enabled += 1

                        if enabled == 0:
                            pass
                        elif enabled != 0:
                            conf = mb.askyesno(
                                title="Are you sure?",
                                message=f"""You have {enabled} not selected passengers
Do you want to Continue?"""
                            )
                            if conf:
                                pass
                            else:
                                return False
                        if len(multi_ticket_entry) == 0:
                            mb.showerror(
                                title="Error",
                                message="No Passengers Selected"
                            )
                            return False
                        else:
                            uid = basic.getdatawhere('id', 'userlogin', f'log="{hex(uuid.getnode())}"')[0][0]
                            wallet = basic.getdatawhere('wallet', 'userlogin', f'id={uid}')[0][0]
                            cost = book.totalcost.cget("text").split("₹")[1]
                            cost = int(cost)
                            if wallet < cost*len(multi_ticket_entry):
                                mb.showerror(
                                    title="Error",
                                    message="Insufficient Balance"
                                )
                                return False
                            else:
                                confirm = mb.askyesno(
                                    title="Confirm",
                                    message=f"""Are you sure you want to buy this ticket?

Total Cost: ₹{cost*len(multi_ticket_entry)}
Trainno: {book.trainno.cget("text").split(": ")[1]}
Current Wallet Balance: ₹{wallet}

Note:  This can't be undone!
""")
                                if confirm:
                                    try:
                                        proc = ticket(
                                            trainno=book.trainno.cget("text").split(": ")[1],
                                            fromst=combo.get(),
                                            tost=to,
                                            uid=uid
                                            )
                                        proc.multigenerate(date_entry.get_date(),*tuple(multi_ticket_entry))
                                        mb.showinfo(
                                            title="Success",
                                            message="Ticket Generated!\nHave a Great Journey!"
                                        )
                                        book.destroy()
                                        print("Ticket Generated")
                                        return True
                                    except Exception as e:
                                        mb.showerror(
                                            title="Error",
                                            message="Invalid Stations Selected"
                                        )
                                        raise e
                                else:
                                    return False
                    def _updatecheck(nt):        
                        update(nt)
                        book.trainname.config(text=f"{_fin[nt][1][0][0]}")
                        book.firstdep.config(text=f"First Station Departure: {gettime(nt)}")
                        book.cost.config(text=f"Cost: ₹{_fin[nt][0]['cost']}")
                        book.trainno.config(text=f"Train Number: {nt}")
                        nopt = ticket(nt, fro, to).generate_ticket('check')['path'][1]
                        nopt = nopt[0:-1]
                        combo.configure(values=nopt)
                        combo.set(fro)
                        book.path.config(text=f"Path: {fro} → {to}")
                        cost = book.cost.cget("text").split("₹")[1]
                        cost = int(cost)
                        book.totalcost.config(text=f"Total Cost: ₹{cost*len(multi_ticket_entry)}")
                    def update(_t):
                        for widget in book.altoptframe.winfo_children():
                            widget.destroy()
                        
                        im = Image.open("assets/altsearch.png")
                        im = im.resize((_w-20, 100))
                        book.ximg = ImageTk.PhotoImage(im)
                        for train in _fin:
                            if train == _t:
                                continue
                            altframe = tk.Frame(
                                book.altoptframe,
                                bd=2,
                                relief='flat',
                                width=_w-20,
                                height=100,
                                borderwidth=.5
                            )
                            altframe.pack(
                                padx=5,
                                pady=5
                            )
                            inl = tk.Label(
                                altframe,
                                image=book.ximg,
                                padx=0,
                                pady=0,
                                borderwidth=.5,
                                relief="flat").place(x=0,
                                                    y=0)
                            altframe.pack_propagate(False)
                            tk.Label(
                                altframe,
                                text=f"Train No: {train}",
                                bg=bgclr
                            ).place(x=10,
                                    y=30,
                                    height=10
                                )
                            try:
                                name=_fin[train][1][0][0]
                            except:
                                name="Name Not Found!"
                            tk.Label(
                                altframe,
                                text=name,
                                bg=bgclr
                            ).place(x=10,
                                    y=10,
                                    height=15
                                )
                            time = basic.getdatawhere('departure', 'schedules', f'train_number={train}')[0][0]
                            time = time.split(':')
                            if int(time[0]) < 12:
                                ap='am'
                                l = time[0]
                            else:
                                ap='pm'
                                l = str(int(time[0]) - 12)
                            time = l + ":" + time[1] + f' {ap}'
                            tk.Label(
                                altframe,
                                text=f"{time}",
                                bg=bgclr
                            ).place(x=10,
                                    y=45,
                                    height=15
                            )
                            tk.Button(
                                altframe,
                                text="Check",
                                bg="#F8DF90",
                                command=lambda train=train: _updatecheck(train)
                            ).place(x=10,
                                    y=67.5,
                                    height=20,
                                    width=_w-50
                            )

                    update(t)
                    _updatecheck(t)
                    addpass()


        limg = Image.open("assets/dawnbackground.png")
        limg = limg.resize((315,390))
        self.limg = ImageTk.PhotoImage(limg)
        self.loginbg = tk.Label(self,   image=self.limg,
                                        padx=0,
                                        pady=0,
                                        highlightthickness=1,
                                        highlightbackground="black",
                                        relief="solid",
                                        borderwidth=2).place(x=530,
                                                                y=75,
                                                                height=390)
        self.boldfont = tkFont.Font(size = 10, weight = "bold")
        self.loginlb = tk.Label(self,
                                text="Login / Register",
                                bg="#C7C4D9", 
                                font = ('consolas', 11, 'bold underline'), 
                                anchor="center",
                                borderwidth=0,
                                relief="solid")
        self.loginlb.place(x=600, y=101, width=175)
        self.username = tkmisc.PlaceholderEntry(self, placeholder="Username")
        self.username.place(x = 600, y = 130, width=175)
        self.password = tkmisc.PlaceholderEntry(self, placeholder="Password")
        self.password.place(x = 600, y = 160, width=175)

        def loginuser(name, paswd):
            if name == "" or paswd == "":
                mb.showerror(
                    title="Invalid Credentials",
                    message="Kindly provide the credentials properly."
                )
                return False

            test = basic.getdatawhere(
                'name, password',
                'userlogin',
                f'name="{name}"'
            )

            if not test:
                return False

            if test[0][1] != paswd:
                mb.showerror(
                    title="Error",
                    message="Password Incorrect!"
                )
                return False

            try:
                success = user.login(name, paswd)

                if success:
                    mb.showinfo(
                        title="Successful",
                        message="Logged In!"
                    )
                    return True
                else:
                    return False

            except Exception as e:
                print("LOGIN ERROR:", e)
                mb.showerror(
                    title="Unsuccessful",
                    message="Login Attempt Unsuccessful!"
                )
                return False
            
        self.adminlogbtn = tk.Button(
            self,
            text="Admin Login",
            bg="#313338",
            fg="#FFFFFF",
            command=lambda: adminlogin()
        )
        self.adminlogbtn.place(
            x=600,
            y=250,
            width=175
        )
        def adminlogin():
            pop = tk.Toplevel(self)
            pop.title("Admin Login")
            pop.geometry("700x500")
            pop.resizable(False, False)
            pop.grab_set()

            tk.Label(
                pop, 
                bg="#1e2124",
                relief="flat").place(
                    x=0,
                    y=0,
                    height=500,
                    width=700
                )
            ttimg = Image.open("assets/admin/title.png")
            ttimg = ttimg.resize((700, 50))
            pop.lbg = ImageTk.PhotoImage(ttimg)
            tk.Label(
                pop,
                image=pop.lbg,
                padx=0,
                pady=0,
                borderwidth=0,
                relief="flat",
                highlightthickness=1,
                highlightbackground="black",
                ).place(
                    x=0,
                    y=0,
                )
            border = tk.Frame(
                pop,
                bg="white",
            )
            border.place(
                x=190,
                y=150,
                height=200,
                width=300
            )
            tk.Label(
                border,
                bg="#424549"
            ).place(
                x=2,
                y=2,
                height=196,
                width=296
            )
            tk.Label(
                border,
                text="Login as an Admin",
                anchor="c"
            ).place(
                x=2,
                y=10,
                width=296
            )
            
            for i in border.winfo_children():
                try:
                    i.configure(
                        bg="#424549",
                        fg="white"
                    )
                except:
                    pass


            
            
        def updateuserdata(type: Literal["login", "register", "in"] = "register"):
            if type=="login":
                test = basic.getdatawhere('name, password, log', 'userlogin', f'name="{self.username.get_value()}"')
                if test[0][1] != self.password.get_value():
                    return False
            f = basic.getdatawhere(type="*",name="userlogin",where=f"log='{hex(uuid.getnode())}'")
            self.regbtn.place_forget()
            self.logbtn.place_forget()
            self.username.place_forget()
            self.password.place_forget()
            self.loginlb.place_forget()
            self.adminlogbtn.place_forget()
            name=f[0][0]
            mob=f[0][2]
            mail=f[0][3]
            uid=f[0][5]
            wallet=f[0][4]
            bgclr = "#F7F4ED"
            self.namelabel=tk.Label(self, text="Welcome, " + name.capitalize().split(" ")[0], font="Consolas 15 bold", anchor="w", bg="#C7C4D9")
            self.namelabel.place(x=570, y=105, width=235)
            self.uidlabel = tk.Label(
                self,
                text=f"""UID: {uid}
Email: {mail}
Mobile No.: {mob}""",
                font=("Consolas", 10),
                anchor="nw",
                justify="left",
                bg="#F2C0BF",
                padx=0,
                pady=0,
                borderwidth=0,
                highlightthickness=0
            )
            self.walletlabel = tk.Label(
                self,
                text=f"Balance: ₹{wallet}/-",
                font=("Consolas", 12, "bold"),
                anchor="c",
                justify="left",
                bg="#75A2DB",
                padx=0,
                pady=0,
                borderwidth=0,
                highlightthickness=0
            )
            self.walletlabel.place(
                x=570, 
                y=210, 
                width=235, 
                height=30
            )
            self.uidlabel.place(
                x=570, 
                y=160, 
                width=235, 
                height=110
            )
            self.logoutbtn=tk.Button(
                self, 
                text="Logout", 
                bg="#D0DBA9"
            )#, command=lambda: logoutcmd())
            self.logoutbtn.place(
                x=689, 
                y=400, 
                width=116
            )
            tk.Label(
                self,
                bg="#C7C4D9",
            ).place(
                x=570,
                y=240,
                width=235,
                height=155,
            )
            self.upcomingjourneyslabel = tk.Label(
                self,
                bg="#C7C4D9",
                text="Upcoming Journeys",
                font=("Consolas", 10, "bold"),
                anchor="w",
                justify="left"
            ).place(
                x=570,
                y=240,
                height=20
            )
            self.upcomingjourneys = tk.Frame(self)
            wi = 235
            hi = 135
            self.upcomingjourneys.place(
                x=570,
                y=260,
                width=235,
                height=135
            )
            self.upcomingjourneyscanvas = tk.Canvas(
                self.upcomingjourneys,
                highlightthickness=0,
                bg="#C7C4D9"
            )
            self.upcomingjourneyscrollbar = tk.Scrollbar(
                self.upcomingjourneys,
                orient="vertical",
                command=self.upcomingjourneyscanvas.yview
            )
            self.upcomingjourneysframe = tk.Frame(
                self.upcomingjourneyscanvas,
                bg="#C7C4D9"
            )
            self.upcomingjourneysframe.bind(
                "<Configure>",
                lambda e: self.upcomingjourneyscanvas.configure(
                    scrollregion=self.upcomingjourneyscanvas.bbox("all")
                )
            )
            self.upcomingjourneyscanvas.create_window(
                (0,0),
                window=self.upcomingjourneysframe,
                anchor="nw",
                width=wi-20,
            )
            self.upcomingjourneyscanvas.configure(
                yscrollcommand=self.upcomingjourneyscrollbar.set
            )
            self.upcomingjourneyscanvas.place(
                x=0,
                y=0,
                width=wi-20,
                height=hi
            )
            self.upcomingjourneyscrollbar.place(
                x=wi-20,
                y=0,
                width=20,
                height=hi
            )
            self.upcomingjourneys.grid_rowconfigure(
                0,
                weight=1
            )
            self.upcomingjourneys.grid_columnconfigure(   
                0,
                weight=1
            )
            self.ticket_widgets = {}

            def updatelogdata():#event
                wi = 235
                hi = 135
                try:
                    f=basic.getdatawhere(type="*",name="userlogin",where=f"log='{hex(uuid.getnode())}'")
                    if f == []:
                        return
                    if f != []:
                        name=f[0][0]
                        mob=f[0][2]
                        mail=f[0][3]
                        uid=f[0][5]
                        wallet=f[0][4]
                        self.walletlabel.config(text=f"Balance: ₹{wallet}/-")
                    ticketdata = basic.getdatawhere(type="*", name="ticketiternary", where=f"uid='{uid}'")
                    if ticketdata == []:
                        return
                    for i in ticketdata:
                        iternary = json.loads(i[2])
                        tid = i[3]
                        dte = i[4]
                        path = f"{iternary['path'][0][0]} - {iternary['path'][0][1]}"
                        train = i[1]
                        if tid in self.ticket_widgets:
                            continue
                        iternary = json.loads(i[2])
                        ticketframe = tk.Frame(
                            self.upcomingjourneysframe,
                            bd=2,
                            relief="flat",
                            width=wi-20,
                            height=100,
                            borderwidth=.5,
                            bg="#9FA6DA"
                        )
                        ticketframe.pack(
                            padx=5,
                            pady=5
                        )
                        nopas = 0
                        for key, value in iternary.items():
                            nopas += 1
                        nopas = nopas - 1
                        tk.Label(
                            ticketframe,
                            text=f"""Train No: {train}
No Of Passengers: {nopas}
Date of Journey: {dte}
Path: {path}""",
                            bg="#9FA6DA",
                            font="consolas 10 bold",
                            anchor="w",
                            justify="left"
                        ).place(
                            x=1,
                            y=1
                        )
                        cancelbtn = tk.Button(
                            ticketframe,
                            text="Cancel",
                            bg="#565B68",
                            command=lambda tid=tid: cancelticket(tid)
                        )
                        cancelbtn.place(
                            x=1,
                            y=70,
                            height=20,
                            width=80
                        )
                        infobtn = tk.Button(
                            ticketframe,
                            text="Info",
                            bg="#565B68",
                            command=lambda tid=tid: ticketinfo(tid)
                        )
                        infobtn.place(
                            x=87,
                            y=70,
                            height=20,
                            width=113
                        )
                        self.ticket_widgets[tid] = ticketframe
                        def ticketinfo(tid):
                            inf = tk.Toplevel(self,)
                            inf.title("Ticket Info")
                            inf.geometry("400x200")
                            inf.resizable(False, False)
                            inf.grab_set()
                            k=Image.open("assets/noonbackground.png")
                            k=k.resize((400, 200))
                            inf.inimg = ImageTk.PhotoImage(k)
                            tk.Label(inf, image=inf.inimg,
                                            padx=0,
                                            pady=0,
                                            borderwidth=0,
                                            relief="flat",
                                            highlightthickness=1,
                                            highlightbackground="black",
                                            ).place(
                                                x=0,
                                                y=0,
                                                relwidth=1,
                                                relheight=1
                                            )
                            tk.Label(
                                inf,
                                text=f"{train}",
                                bg="#F6D5C0",
                                font="courier 9 bold"
                            ).place(
                                x=1,
                                y=1,
                                height=20
                            )
                            trainname = basic.getdatawhere('name', 'traininfo', f'fromnum="{train}"')[0][0]
                            tk.Label(
                                inf,
                                text=f"{trainname}",
                                bg="#F6D5C0",
                                font="courier 9 bold"
                            ).place(
                                x=1,
                                y=21,
                                height=20
                            )
                            tk.Label(
                                inf,
                                text=path,
                                bg="#F6D5C0",
                                font="courier 9 bold"
                            ).place(
                                x=270,
                                y=21,
                            )
                            tk.Label(
                                inf,
                                text=f"On: {dte}",
                                bg="#F6D5C0",
                                font="courier 9 bold"
                            ).place(
                                x=270,
                                y=1
                            )
                            tk.Label(
                                inf,
                                text=f"Cost: ₹{iternary['1']['cost']}",
                                bg="#F6D5C0",
                                font="courier 9 bold"
                            ).place(
                                x=140,
                                y=1
                            )
                            wid = 390
                            hi = 135
                            inf.pasinfo = tk.Frame(inf)
                            tk.Label(
                                inf,
                                text="Passengers",
                                bg="#F6ECC6",
                                anchor="w",
                                font="courier 10 bold"
                            ).place(
                                x=5,
                                y=41,    
                                height=20,
                                width=wid
                            )
                            inf.pasinfo.place(
                                x=5,
                                y=61,
                                width=390,
                                height=135
                            )
                            inf.pasinfocanvas = tk.Canvas(
                                inf.pasinfo,
                                highlightthickness=0,
                                bg="#F6ECC6"
                            )
                            inf.pasinfoscrollbar = tk.Scrollbar(
                                inf.pasinfo,
                                orient="vertical",
                                command=inf.pasinfocanvas.yview
                            )
                            inf.pasinfoframe = tk.Frame(
                                inf.pasinfocanvas,
                                bg="#F6ECC6"
                            )
                            inf.pasinfoframe.bind(
                                "<Configure>",
                                lambda e: inf.pasinfocanvas.configure(
                                    scrollregion=inf.pasinfocanvas.bbox("all")
                                )
                            )
                            inf.pasinfocanvas.create_window(
                                (0,0),
                                window=inf.pasinfoframe,
                                anchor="nw",
                                width=wid-20,
                            )
                            inf.pasinfocanvas.configure(
                                yscrollcommand=inf.pasinfoscrollbar.set
                            )
                            inf.pasinfocanvas.place(
                                x=0,
                                y=0,
                                width=wid-20,
                                height=hi
                            )
                            inf.pasinfoscrollbar.place(
                                x=wid-20,
                                y=0,
                                width=20,
                                height=hi
                            )
                            inf.pasinfo.grid_rowconfigure(
                                0,
                                weight=1
                            )
                            inf.pasinfo.grid_columnconfigure(   
                                0,
                                weight=1
                            )
                            for key in iternary:
                                try:
                                    name = iternary[key]['name']
                                    gender = iternary[key]['gender']
                                    age = iternary[key]['age']
                                    pasframe = tk.Frame(
                                        inf.pasinfoframe,
                                        bd=2,
                                        relief="flat",
                                        width=wid-20,
                                        height=70,
                                        borderwidth=1,
                                        bg="#F2AB82"
                                    )
                                    pasframe.pack(
                                        padx=5,
                                        pady=5
                                    )
                                    tk.Label(
                                        pasframe,
                                        text=f"{name}",
                                        bg="#F2AB82",
                                        font="courier 10 bold"
                                    ).place(
                                        x=1,
                                        y=1
                                    )
                                    tk.Label(
                                        pasframe,
                                        text=f"Gender: {gender}",
                                        bg="#F2AB82",
                                        font="courier 10 bold"
                                    ).place(
                                        x=1,
                                        y=21
                                    )
                                    tk.Label(
                                        pasframe,
                                        text=f"Age: {age}",
                                        bg="#F2AB82",
                                        font="courier 10 bold"
                                    ).place(
                                        x=1,
                                        y=41
                                    )
                                except Exception as e:
                                    pass

                            


                        def cancelticket(tid):
                            ticket_object = ticket(train,
                                                iternary['path'][0][0],
                                                iternary['path'][0][1])
                            if ticket_object.cancel_ticket(tid):
                                ticketframe.destroy()
                                self.ticket_widgets.pop(tid)
                        

                except Exception as e:
                        print(e)
                finally:
                    self.after(1000, lambda: updatelogdata())
            updatelogdata()

            """self.bind_all("<Key>",lambda event: updatelogdata(event))
            self.bind_all("<Button>",lambda event: updatelogdata(event))
            self.bind_all("<Motion>", lambda event: updatelogdata(event))"""
           
            
        def logbtncmd():
            success = loginuser(
                self.username.get_value(),
                self.password.get_value()
            )    

            if success:
                updateuserdata("login")
                    
        self.logbtn = tk.Button(self,
                                text="Login",
                                borderwidth=.5,
                                command=lambda:logbtncmd())
        self.logbtn.place(x = 600, y = 190, width = 175)
        
            
        def registerpopup():
            popup = tk.Toplevel(self)
            popup.title("Register")
            popup.geometry("350x250")
            popup.resizable(False, False)
            popup.grab_set()
            
            bg = Image.open("assets/sunsetbackground.png")
            bg = bg.resize((350, 250))
            lbg = ImageTk.PhotoImage(bg)
            bgimg = tk.Label(popup, image=lbg,
                                  padx=0,
                                  pady=0,
                                  relief="solid")
            bgimg.image = lbg
            bgimg.place(x=0,y=0, height=250, width=350)
            
            label = tk.Label(popup, text="Create New Account", anchor="w", font="consolas 12 bold", bg="#62ECF8")
            label.place(x=40, y=17.5, width=270)
            
            username = tkmisc.PlaceholderEntry(popup, placeholder="Username")
            username.place(x=40, y=50, width=270, height=20)
            password = tkmisc.PlaceholderEntry(popup, placeholder="Password")
            password.place(x=40, y=75, width=270, height=20)
            cnpassword = tkmisc.PlaceholderEntry(popup, placeholder="Confirm Password")
            cnpassword.place(x=40, y=100, width=270, height=20)
            phone = tkmisc.PlaceholderEntry(popup, placeholder="Enter Mobile No. (10 digits)")
            phone.place(x=40, y=125, widt=270, height=20)
            email = tkmisc.PlaceholderEntry(popup, placeholder="Enter Email ID")
            email.place(x=40, y=150, width=270, height=20)
            
            def registerfinal():
                w = user.register(username.get_value(), password.get_value(), cnpassword.get_value(), phone.get_value(), email.get_value())
                if w==True:
                    user.login(username.get_value(), password.get_value())
                    print("Commited")
                    updateuserdata()
                    popup.grab_release()
                    popup.destroy()
                    
            reg = tk.Button(popup, 
                            text="Register", 
                            command=registerfinal, 
                            bg="#97E7EE",
                            borderwidth=1)
            reg.place(x=40, y=175, width=270)
            
            def closepopup():
                popup.grab_release()
                popup.destroy()
            retbtn = tk.Button(popup,
                                    text="Login Instead..",
                                    borderwidth=.5,
                                    command=closepopup,
                                    bg="#97E7EE")
            retbtn.place(x=40, y=205, width=270)
        
                
        self.regbtn = tk.Button(self,
                                text="Register New User",
                                borderwidth=.5,
                                command=registerpopup)
        self.regbtn.place(x=600, y=220, width=175)


    def select_option(self, event, wid, li):
        selected_item = li.get(tk.ANCHOR)
        if selected_item:
            wid.delete(0, tk.END)
            wid.insert(0, selected_item)
        li.place_forget()

    def hide_dropdown(self, wid, event=None):
        self.after(150, lambda: wid.place_forget())
    
    def show_dropdown(self, wid, li ,event=None):
        if not li.winfo_ismapped():
            x = wid.winfo_x()
            y = wid.winfo_y() + 20
            w = wid.winfo_width()
            li.place(x=x, y=y, width=w)
            li.lift()
    
    def update_menu(self, data, li):
        li.delete(0, tk.END)
        for item in data:
            li.insert(tk.END, item)
    
    def filter_options(self, event, entry, options, li):
        typed_text = entry.get()
        if typed_text == '':
            filtered_data = options
        else:
            filtered_data = [item for item in options if typed_text.lower() in item.lower()]

        self.update_menu(filtered_data, li)
        self.show_dropdown(entry, li)
    
    

class secondpage(tk.Frame):
    def __init__(self, 
                 parent, 
                 controller
                ):
        super().__init__(parent, 
                         bg="#00CCFF"
                        )
        self.controller = controller
        img = Image.open("assets/fajrbackground.png")
        img = img.resize((900, 500))
        self.bgimage = ImageTk.PhotoImage(img)   
        self.bg = tk.Label(self, 
                           image=self.bgimage
                           )
        self.bg.place(x=0,     
                      y=0, 
                      relwidth=1, 
                      relheight=1)

        img = Image.open("assets/title.png")
        img = img.resize((900, 39))

        self.titleimg = ImageTk.PhotoImage(img)

        self.title = tk.Label(self, image = self.titleimg,
                              padx=0,
                              pady=0,
                              borderwidth=0,
                              relief="flat",
                              highlightthickness=1,
                              highlightbackground="black",
                              )
        self.title.place(x=0, y=0)
        
        self.Label = tk.Label(self, text=self.controller.searched_train, font="Consolas 12 bold", bg="#00CCFF")
        self.Label.place(x=10, y=50)

if __name__ == "__main__":
    def delete_win():
        u=basic.getdata('name, log', 'userlogin')
        for i in u:
            if i[1] == hex(uuid.getnode()):
                user.logout(i[0])
        app.destroy()
    app = mainwindow()
    app.protocol(
                'WM_DELETE_WINDOW',
                 delete_win
                )
    app.mainloop()