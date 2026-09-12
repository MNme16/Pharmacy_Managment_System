#######Importing external libraries#########
import sqlite3
import tkinter as tk
from tkinter import *
from tkinter import Entry
from tkinter import messagebox
from datetime import date

# global variables
CurrentUsername = ""

# connecting to database
# NOTE: previously this used "with sqlite3.connect(...) as db:" and then
# immediately let the "with" block end. That is misleading (the "with"
# statement for a sqlite3 connection only manages commit/rollback, not
# closing), so the connection kept working, but it's confusing to read.
# Opened plainly here instead - same behaviour, clearer code.
db = sqlite3.connect("databasepharmacy.db")
cursor = db.cursor()

###Creating tables within the database only if they don't already exist.
cursor.execute(
    """CREATE TABLE IF NOT EXISTS User ( UserID integer PRIMARY KEY,Name	TEXT, Email	TEXT,ContactNumber	TEXT,Gender	TEXT,Country	TEXT,Password	TEXT,Username	TEXT);""")
cursor.execute("""CREATE TABLE IF NOT EXISTS Medicine ( MedicineID integer PRIMARY KEY,
	Description	TEXT,
	QuantityInStock	INTEGER);""")
cursor.execute(
    """CREATE TABLE IF NOT EXISTS Prescription(PrescriptionID integer PRIMARY KEY, UserID integer, DateIssued integer);""")
cursor.execute(
    """CREATE TABLE IF NOT EXISTS MedLinked(MedicineID integer, PrescriptionID integer, Quantity integer, PRIMARY KEY (MedicineID, PrescriptionID));""")
db.commit()


# setting up frame
class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

    def show(self):
        self.lift()

    def hide(self):
        self.lower()


####Home Page#####
class HomePage(Page):
    def __init__(self, parent, controller, *args, **kwargs):
        Page.__init__(self, parent, *args, **kwargs)
        self.controller = controller
        MainTitle = Label(self,
                          text="Welcome To Bio Gems Pharmacy Management System",
                          background='#7aa8bd',
                          font='MSSerif 14 bold')
        MainTitle.place(x=85, y=40, width=650, height=40)

        def showregister():
            self.controller.show_frame("P1")

        def showlogin():
            self.controller.show_frame("P2")

        def showstafflogin():
            self.controller.show_frame("P3")

        RegisterPagepagebtn = Button(self,
                                     text="Register",
                                     background='#d3d3d3',
                                     font='Arial 12 bold',
                                     command=showregister)
        RegisterPagepagebtn.place(x=150, y=230, width=105, height=25)
        LoginPagebtn = Button(self,
                              text="Login",
                              background='#d3d3d3',
                              font='Arial 12 bold',
                              command=showlogin)
        LoginPagebtn.place(x=300, y=230, width=105, height=25)
        StaffLoginPagebtn = Button(self,
                                   text="Staff Login",
                                   background='#d3d3d3',
                                   font='Arial 12 bold',
                                   command=showstafflogin)
        StaffLoginPagebtn.place(x=450, y=230, width=130, height=25)


############Start of register page###################
class RegisterPage(Page):
    def __init__(self, parent, controller, *args, **kwargs):
        Page.__init__(self, parent, *args, **kwargs)
        self.controller = controller

        def register():
            InputUsername = username.get()
            InputPassword = password.get()
            InputName = name.get()
            InputEmail = email.get()
            InputContactNumber = ContactNumber.get()
            InputGender = Gender.get()
            InputCountry = Country.get()
            CompleteEntry = True

            if InputUsername == "" or InputPassword == "" or InputName == "" or InputEmail == "" or InputContactNumber == "" or InputGender == "" or InputCountry == "":
                messagebox.showinfo("Error", "Fields cannot be empty. Please enter your login details")
                CompleteEntry = False

            if CompleteEntry:
                ValidUser = True
                cursor.execute("Select username from User")
                for count in cursor.fetchall():
                    User = count[0]
                    if InputUsername == User:
                        ValidUser = False

                if not ValidUser:
                    messagebox.showinfo("Error", "Username in use.")
                else:
                    cursor.execute(
                        "INSERT INTO User(Name, Email, ContactNumber, Gender, Country, Password, Username)VALUES(?, ?, ?, ?, ?, ?, ?)",
                        (InputName, InputEmail, InputContactNumber, InputGender, InputCountry,
                         InputPassword, InputUsername))
                    db.commit()
                    messagebox.showinfo("Success", "Registered Successfully")
                    ClearBoxes()
                    self.controller.show_frame("P0")

        def ClearBoxes():
            username.delete(0, END)
            password.delete(0, END)
            name.delete(0, END)
            email.delete(0, END)
            ContactNumber.delete(0, END)
            Gender.delete(0, END)
            Country.delete(0, END)

        def ShowMenu():
            self.controller.show_frame("P0")

        MainTitle = Label(self,
                          text="Bio Gems",
                          background='#7aa8bd',
                          font='Arial 12 bold')
        MainTitle.place(x=175, y=40, width=300, height=25)

        y = 100
        usernamelbl = Label(self, text="Username", background='#7aa8bd', font='Arial 12 bold')
        usernamelbl.place(x=175, y=90, width=200, height=25)
        username = tk.Entry(self, text="")
        username.place(x=400, y=90, width=100, height=25)

        passwordlbl = Label(self, text="Password", background='#7aa8bd', font='Arial 12 bold')
        passwordlbl.place(x=175, y=y + 50, width=200, height=25)
        password = tk.Entry(self, text="", show="*")
        password.place(x=400, y=y + 50, width=100, height=25)

        namelbl = Label(self, text="Name", background='#7aa8bd', font='Arial 12 bold')
        namelbl.place(x=175, y=y + 100, width=200, height=25)
        name = tk.Entry(self, text="")
        name.place(x=400, y=y + 100, width=100, height=25)

        emaillbl = Label(self, text="Email", background='#7aa8bd', font='Arial 12 bold')
        emaillbl.place(x=175, y=y + 150, width=200, height=25)
        email = tk.Entry(self, text="")
        email.place(x=400, y=y + 150, width=100, height=25)

        ContactNumberlbl = Label(self, text="Contact Number", background='#7aa8bd', font='Arial 12 bold')
        ContactNumberlbl.place(x=175, y=y + 200, width=200, height=25)
        ContactNumber = tk.Entry(self, text="")
        ContactNumber.place(x=400, y=y + 200, width=100, height=25)

        Genderlbl = Label(self, text="Gender", background='#7aa8bd', font='Arial 12 bold')
        Genderlbl.place(x=175, y=y + 250, width=200, height=25)
        Gender = tk.Entry(self, text="")
        Gender.place(x=400, y=y + 250, width=100, height=25)

        Countrylbl = Label(self, text="Country", background='#7aa8bd', font='Arial 12 bold')
        Countrylbl.place(x=175, y=y + 300, width=200, height=25)
        Country = tk.Entry(self, text="")
        Country.place(x=400, y=y + 300, width=100, height=25)

        RegisterCreatebtn = Button(self, text="Create", background='#d3d3d3', font='Arial 12 bold', command=register)
        RegisterCreatebtn.place(x=200, y=y + 350, width=105, height=25)
        Backbtn = Button(self, text="Back", background='#d3d3d3', font='Arial 12 bold', command=ShowMenu)
        Backbtn.place(x=400, y=y + 350, width=105, height=25)


##########################Login page###################
class LoginPage(Page):
    def __init__(self, parent, controller, *args, **kwargs):
        Page.__init__(self, parent, *args, **kwargs)
        self.controller = controller

        def ShowMenu():
            self.controller.show_frame("P0")

        def LoginProcess():
            global CurrentUsername
            InputUsername = username.get()
            CurrentPassword = password.get()
            if CurrentPassword == "" or InputUsername == "":
                messagebox.showinfo("Error", "Fields cannot be empty. Please enter your login details")
                return

            cursor.execute("SELECT Username, Password FROM User")
            InvalidUser = True

            for count in cursor.fetchall():
                TempUser = count[0]
                TempPass = count[1]
                if TempUser == InputUsername and TempPass == CurrentPassword:
                    CurrentUsername = InputUsername
                    username.delete(0, END)
                    password.delete(0, END)
                    self.controller.show_frame("P8")
                    InvalidUser = False
                    break
            if InvalidUser:
                messagebox.showinfo("Error", "Incorrect username or password. Please try again.")

        MainTitle = Label(self, text="Login", background='#7aa8bd', font='Arial 12 bold')
        MainTitle.place(x=175, y=40, width=300, height=25)
        usernamelbl = Label(self, text="Username", background='#7aa8bd', font='Arial 12 bold')
        usernamelbl.place(x=175, y=90, width=200, height=25)
        username = tk.Entry(self, text="")
        username.place(x=400, y=90, width=100, height=25)

        passwordlbl = Label(self, text="Password", background='#7aa8bd', font='Arial 12 bold')
        passwordlbl.place(x=175, y=140, width=200, height=25)
        password = tk.Entry(self, text="", show="*")
        password.place(x=400, y=140, width=100, height=25)

        Backbtn = Button(self, text="Back", background='#d3d3d3', font='Arial 12 bold', command=ShowMenu)
        Backbtn.place(x=400, y=230, width=105, height=25)
        LoginCreatebtn = Button(self, text="Login", background='#d3d3d3', font='Arial 12 bold', command=LoginProcess)
        LoginCreatebtn.place(x=200, y=230, width=105, height=25)


########Start of Staff Login Page##############
class StaffLoginPage(Page):
    def __init__(self, parent, controller, *args, **kwargs):
        Page.__init__(self, parent, *args, **kwargs)
        self.controller = controller

        def ShowMenu():
            self.controller.show_frame("P0")

        def StaffLoginProcess():
            user = username.get()
            pas = password.get()
            if user == "" or pas == "":
                messagebox.showinfo("Error", "Fields cannot be empty. Please try again.")
            elif user == "biogemsstaff" and pas == "staff!":
                username.delete(0, END)
                password.delete(0, END)
                self.controller.show_frame("P4")
            else:
                messagebox.showinfo("Error", "Invalid log in details")

        MainTitle = Label(self, text="Staff Login", background='#7aa8bd', font='Arial 12 bold')
        MainTitle.place(x=175, y=40, width=300, height=25)
        usernamelbl = Label(self, text="Username", background='#7aa8bd', font='Arial 12 bold')
        usernamelbl.place(x=175, y=90, width=200, height=25)
        username = tk.Entry(self, text="")
        username.place(x=400, y=90, width=100, height=25)

        passwordlbl = Label(self, text="Password", background='#7aa8bd', font='Arial 12 bold')
        passwordlbl.place(x=175, y=140, width=200, height=25)
        password = tk.Entry(self, text="", show="*")
        password.place(x=400, y=140, width=100, height=25)

        Backbtn = Button(self, text="Back", background='#d3d3d3', font='Arial 12 bold', command=ShowMenu)
        Backbtn.place(x=400, y=230, width=105, height=25)
        StaffLoginbtn = Button(self, text="Login", background='#d3d3d3', font='Arial 12 bold',
                               command=StaffLoginProcess)
        StaffLoginbtn.place(x=200, y=230, width=105, height=25)


############Start of Staff Menu Page##################
class StaffMenuPage(Page):
    def __init__(self, parent, controller, *args, **kwargs):
        Page.__init__(self, parent, *args, **kwargs)
        self.controller = controller

        MainTitle = Label(self, text="Staff Menu", background='#7aa8bd', font='Arial 12 bold')
        MainTitle.place(x=175, y=40, width=300, height=25)

        def ShowMedical():
            self.controller.show_frame("P5")

        Medicalpagebtn = Button(self, text="Medical stock", background='#d3d3d3', font='Arial 12 bold',
                                command=ShowMedical)
        Medicalpagebtn.place(x=100, y=230, width=150, height=25)

        def ShowOrders():
            self.controller.show_frame("P6")

        Orderspagebtn = Button(self, text="Orders Made", background='#d3d3d3', font='Arial 12 bold', command=ShowOrders)
        Orderspagebtn.place(x=500, y=230, width=150, height=25)

        def SignOut():
            self.controller.show_frame("P0")

        SignOutbtn = Button(self, text="Sign Out", background='#d3d3d3', font='Arial 12 bold', command=SignOut)
        SignOutbtn.place(x=300, y=230, width=150, height=25)


##############Start of patient menu page################
class PatientMenuPage(Page):
    def __init__(self, parent, controller, *args, **kwargs):
        Page.__init__(self, parent, *args, **kwargs)
        self.controller = controller

        MainTitle = Label(self, text="Customer Menu", background='#7aa8bd', font='Arial 12 bold')
        MainTitle.place(x=175, y=40, width=300, height=25)

        def ShowDetails():
            self.controller.show_frame("P7")

        MyDetailspagebtn = Button(self, text="My Details", background='#d3d3d3', font='Arial 12 bold',
                                  command=ShowDetails)
        MyDetailspagebtn.place(x=330, y=230, width=105, height=25)

        def MakeOrder():
            self.controller.show_frame("P9")

        MakeOrderpagebtn = Button(self, text="Order a Prescription", background='#d3d3d3', font='Arial 12 bold',
                                  command=MakeOrder)
        MakeOrderpagebtn.place(x=80, y=230, width=200, height=25)

        def SignOut():
            self.controller.show_frame("P0")

        SignOutbtn = Button(self, text="Sign Out", background='#d3d3d3', font='Arial 12 bold', command=SignOut)
        SignOutbtn.place(x=500, y=230, width=150, height=25)


##############Start of Show Medical page############
class ShowMedical(Page):
    def __init__(self, parent, controller, *args, **kwargs):
        Page.__init__(self, parent, *args, **kwargs)
        self.controller = controller

        MainTitle = Label(self, text="Medication in Stock", background='#7aa8bd', font='Arial 12 bold')
        MainTitle.place(x=174, y=40, width=300, height=25)

        def addingmedication():
            InputMedicineID = MedicineID.get().strip()
            InputDescription = Description.get().strip()
            InputQuantityInStock = QuantityInStock.get().strip()

            if InputMedicineID == "" or InputDescription == "" or InputQuantityInStock == "":
                messagebox.showinfo("Error", "Fields cannot be empty. Please enter medication")
                return

            if not InputMedicineID.isdigit() or not InputQuantityInStock.isdigit():
                messagebox.showinfo("Error", "MedicineID and Quantity must be numbers")
                return

            try:
                cursor.execute(
                    "INSERT INTO Medicine(MedicineID , Description, QuantityInStock)VALUES(?, ?, ?)",
                    (int(InputMedicineID), InputDescription, int(InputQuantityInStock)))
                db.commit()
                messagebox.showinfo("Success", "Added Successfully")
                MedicineID.delete(0, END)
                Description.delete(0, END)
                QuantityInStock.delete(0, END)
                self.refresh()
            except sqlite3.IntegrityError:
                messagebox.showinfo("Error", "That MedicineID already exists")

        def updatingmedication():
            InputMedicineIDVal = MedicineID.get().strip()
            InputQuantityInStockVal = QuantityInStock.get().strip()

            if InputMedicineIDVal == "" or InputQuantityInStockVal == "":
                messagebox.showinfo("Error", "Enter a MedicineID and a Quantity to update")
                return
            if not InputMedicineIDVal.isdigit() or not InputQuantityInStockVal.isdigit():
                messagebox.showinfo("Error", "MedicineID and Quantity must be numbers")
                return

            sql = "Update Medicine set QuantityinStock =? where MedicineID = ?"
            cursor.execute(sql, (int(InputQuantityInStockVal), int(InputMedicineIDVal)))
            if cursor.rowcount == 0:
                messagebox.showinfo("Error", "No medicine found with that MedicineID")
                return
            db.commit()
            messagebox.showinfo("Success", "Updated Successfully")
            MedicineID.delete(0, END)
            QuantityInStock.delete(0, END)
            self.refresh()

        UpdateStockbtn = Button(self, text="Update", background='#d3d3d3', font='Arial 12 bold',
                                command=updatingmedication)
        UpdateStockbtn.place(x=700, y=300, width=105, height=25)

        MainTitleAdd = Label(self, text="Add Medication", background='#ff781f', font='Arial 12 bold')
        MainTitleAdd.place(x=500, y=100, width=200, height=25)

        MedicineIDlbl = Label(self, text="MedicineID", background='#ff781f', font='Arial 12 bold')
        MedicineIDlbl.place(x=500, y=140, width=100, height=20)
        MedicineID = tk.Entry(self, text="")
        MedicineID.place(x=600, y=140, width=100, height=20)

        Descriptionlbl = Label(self, text="Name", background='#ff781f', font='Arial 12 bold')
        Descriptionlbl.place(x=500, y=190, width=100, height=20)
        Description = tk.Entry(self, text="")
        Description.place(x=600, y=190, width=100, height=20)

        QuantityInStocklbl = Label(self, text="Quantity", background='#ff781f', font='Arial 12 bold')
        QuantityInStocklbl.place(x=500, y=240, width=100, height=20)
        QuantityInStock = tk.Entry(self, text="")
        QuantityInStock.place(x=600, y=240, width=100, height=20)

        MedicineAddbtn = Button(self, text="Add", background='#d3d3d3', font='Arial 12 bold', command=addingmedication)
        MedicineAddbtn.place(x=600, y=300, width=105, height=25)

        def ShowStaffMenu():
            self.controller.show_frame("P4")

        Backbtn = Button(self, text="Back", background='#d3d3d3', font='Arial 12 bold', command=ShowStaffMenu)
        Backbtn.place(x=500, y=300, width=105, height=25)

        self.MyList = Listbox(self)
        self.MyList.place(x=175, y=100, width=300, height=400)

        self.HighestStocklbl = Label(self, text="", background='#7aa8bd', font='Arial 12 bold')
        self.HighestStocklbl.place(x=175, y=560, width=600, height=25)

        self.LowestStocklbl = Label(self, text="", background='#7aa8bd', font='Arial 12 bold')
        self.LowestStocklbl.place(x=175, y=530, width=600, height=25)

        # populate the list/labels for the first time
        self.refresh()

    def refresh(self):
        """Reload the medicine list and the highest/lowest stock labels from the database.
        Called on init and every time this page is shown, so it stays in sync with the DB
        instead of only ever reflecting the data that existed when the app started."""
        self.MyList.delete(0, END)
        self.MyList.insert(END, "ID" + "   " + " Name " + "     " + "Quantity in grams")
        cursor.execute("select MedicineID, Description, QuantityInStock from Medicine")
        for count in cursor.fetchall():
            TempMedicineID = count[0]
            TempDescription = count[1]
            TempQuantityInStock = count[2]
            self.MyList.insert(END,
                          str(str(TempMedicineID) + "    " + TempDescription + "      " + str(TempQuantityInStock)))

        cursor.execute(
            "select MedicineID, Description, QuantityInStock, max(QuantityInStock) as maxQuantityInStock from Medicine")
        res_max = cursor.fetchall()
        TempDescriptionMax = res_max[0][1] if res_max and res_max[0][1] is not None else "None"
        TempMax = str(res_max[0][3]) if res_max and res_max[0][3] is not None else "0"
        self.HighestStocklbl.config(text="Highest in Stock is " + str(TempDescriptionMax) + " with " + str(TempMax))

        cursor.execute(
            "select MedicineID, Description, QuantityInStock, min(QuantityInStock) as minQuantityInStock from Medicine")
        res_min = cursor.fetchall()
        TempDescriptionMin = res_min[0][1] if res_min and res_min[0][1] is not None else "None"
        TempMin = str(res_min[0][3]) if res_min and res_min[0][3] is not None else "0"
        self.LowestStocklbl.config(text="Lowest In Stock is " + str(TempDescriptionMin) + " with " + str(TempMin))

    def show(self):
        self.refresh()
        Page.show(self)


#########Start of Show Orders made page###############
class ShowOrdersMade(Page):
    def __init__(self, parent, controller, *args, **kwargs):
        Page.__init__(self, parent, *args, **kwargs)
        self.controller = controller
        self.orders = []  # list of (UserID/Username, DateIssued, Quantity, MedicineID, PrescriptionID)
        self.selected_index = None

        MainTitle = Label(self, text="Orders Made", background='#7aa8bd', font='Arial 12 bold')
        MainTitle.place(x=174, y=40, width=300, height=25)

        Prescriptionlbl = Label(self, text="Select the Prescription you want to approve", background='#ff781f',
                                font='Arial 12 bold')
        Prescriptionlbl.place(x=175, y=90, width=450, height=25)

        # A Listbox is used instead of the previous OptionMenu. The OptionMenu only ever fired
        # its command when the user actively changed the selection, so if staff clicked "Approve"
        # without touching the dropdown, the code acted on stale/empty global values. A Listbox
        # lets us read the current selection directly (and default to the first item) whenever
        # Approve is pressed.
        self.PrescriptionList = Listbox(self, exportselection=False)
        self.PrescriptionList.place(x=175, y=120, width=450, height=90)

        def ShowStaffMenu():
            self.controller.show_frame("P4")

        Backbtn = Button(self, text="Back", background='#d3d3d3', font='Arial 12 bold', command=ShowStaffMenu)
        Backbtn.place(x=300, y=230, width=105, height=25)

        def approve():
            if not self.orders:
                messagebox.showinfo("No pending orders", "There are no pending orders to approve")
                return

            selection = self.PrescriptionList.curselection()
            index = selection[0] if selection else 0

            _username, _date, quantity, medicineid, prescriptionid = self.orders[index]

            cursor.execute("Select QuantityInStock from Medicine where MedicineID = ?", (medicineid,))
            row = cursor.fetchone()
            stock = row[0] if row else None

            if stock is None:
                messagebox.showinfo("Error", "That medicine no longer exists in stock")
                return

            if int(stock) >= int(quantity):
                NewQuantity = int(stock) - int(quantity)
                cursor.execute("Update Medicine SET QuantityInStock = ? where MedicineID = ?",
                               (NewQuantity, medicineid))
                cursor.execute("Delete from Prescription where PrescriptionID = ?", (prescriptionid,))
                cursor.execute("Delete from MedLinked where PrescriptionID = ?", (prescriptionid,))
                db.commit()
                messagebox.showinfo("Order Complete", "Successfully approved prescription")
                self.refresh()
            else:
                messagebox.showinfo("Not in stock", "Insufficient amount of medication in stock")

        approvebtn = Button(self, text="Approve", background='#d3d3d3', font='Arial 12 bold', command=approve)
        approvebtn.place(x=400, y=230, width=105, height=25)

        self.refresh()

    def refresh(self):
        """Reload the list of pending prescriptions from the database. Called on init and every
        time this page is shown, so newly-placed orders and previously-approved orders are
        reflected instead of showing a snapshot from when the app started."""
        self.orders = []
        self.PrescriptionList.delete(0, END)

        cursor.execute(
            "select User.Username, Prescription.DateIssued, MedLinked.Quantity, MedLinked.MedicineID, "
            "Prescription.PrescriptionID from Prescription "
            "inner join User on User.Username = Prescription.UserID "
            "inner join MedLinked on MedLinked.PrescriptionID = Prescription.PrescriptionID")
        for count in cursor.fetchall():
            self.orders.append((count[0], count[1], count[2], count[3], count[4]))

        if not self.orders:
            self.PrescriptionList.insert(END, "No pending orders")
        else:
            for username_, date_, quantity_, medicineid_, prescriptionid_ in self.orders:
                self.PrescriptionList.insert(
                    END,
                    f"{username_}     {date_}    Qty:{quantity_}     MedID:{medicineid_}     PrescID:{prescriptionid_}")
            self.PrescriptionList.selection_set(0)

    def show(self):
        self.refresh()
        Page.show(self)


#############Start of My details page############
class MyDetails(Page):
    def __init__(self, parent, controller, *args, **kwargs):
        Page.__init__(self, parent, *args, **kwargs)
        self.controller = controller

        self.Name1 = StringVar()
        self.Email1 = StringVar()
        self.ContactNumber1 = StringVar()
        self.Gender1 = StringVar()
        self.Country1 = StringVar()
        self.Password1 = StringVar()
        self.Username1 = StringVar()

        Namelbl = Label(self, text="Name", background='#ff781f', font='Arial 12 bold')
        Namelbl.place(x=175, y=140, width=400, height=25)
        self.EditName = tk.Entry(self, textvariable=self.Name1)
        self.EditName.place(x=600, y=140, width=150, height=25)

        Emaillbl = Label(self, text="Email", background='#ff781f', font='Arial 12 bold')
        Emaillbl.place(x=175, y=190, width=400, height=25)
        self.EditEmail = tk.Entry(self, textvariable=self.Email1)
        self.EditEmail.place(x=600, y=190, width=150, height=25)

        ContactNumberlbl = Label(self, text="Contact Number", background='#ff781f', font='Arial 12 bold')
        ContactNumberlbl.place(x=175, y=240, width=400, height=25)
        self.EditContactNumber = tk.Entry(self, textvariable=self.ContactNumber1)
        self.EditContactNumber.place(x=600, y=240, width=150, height=25)

        Genderlbl = Label(self, text="Gender", background='#ff781f', font='Arial 12 bold')
        Genderlbl.place(x=175, y=290, width=400, height=25)
        self.EditGender = tk.Entry(self, textvariable=self.Gender1)
        self.EditGender.place(x=600, y=290, width=150, height=25)

        Countrylbl = Label(self, text="Country", background='#ff781f', font='Arial 12 bold')
        Countrylbl.place(x=175, y=340, width=400, height=25)
        self.EditCountry = tk.Entry(self, textvariable=self.Country1)
        self.EditCountry.place(x=600, y=340, width=150, height=25)

        Usernamelbl = Label(self, text="Username", background='#ff781f', font='Arial 12 bold')
        Usernamelbl.place(x=175, y=390, width=400, height=25)
        self.EditUsername = tk.Entry(self, textvariable=self.Username1)
        self.EditUsername.place(x=600, y=390, width=150, height=25)

        Passwordlbl = Label(self, text="Password", background='#ff781f', font='Arial 12 bold')
        Passwordlbl.place(x=175, y=440, width=400, height=25)
        self.EditPassword = tk.Entry(self, textvariable=self.Password1)
        self.EditPassword.place(x=600, y=440, width=150, height=25)

        def UpdateUser():
            global CurrentUsername
            TempName = self.EditName.get()
            TempEmail = self.EditEmail.get()
            TempContactNumber = self.EditContactNumber.get()
            TempGender = self.EditGender.get()
            TempCountry = self.EditCountry.get()
            TempUsername = self.EditUsername.get()
            TempPassword = self.EditPassword.get()

            if TempUsername == "" or TempPassword == "":
                messagebox.showinfo("Error", "Username and Password cannot be empty")
                return

            cursor.execute(
                "UPDATE User SET Name =?, Email =?, ContactNumber =?, Gender =?, Country =?, Username =?, Password =? where Username = ?",
                (TempName, TempEmail, TempContactNumber, TempGender, TempCountry, TempUsername, TempPassword,
                 CurrentUsername))
            db.commit()
            # IMPORTANT FIX: the global CurrentUsername must be updated if the user changed
            # their username, otherwise every later query keyed on CurrentUsername (this page,
            # ordering prescriptions, etc.) would silently keep looking up the OLD username.
            CurrentUsername = TempUsername
            messagebox.showinfo("Information Updated", "You have successfully updated your details.")

        updateuser1 = Button(self, text="Update Information", command=UpdateUser)
        updateuser1.place(x=475, y=500, width=130, height=25)

        MainTitle = Label(self, text="MyDetails", background='#7aa8bd', font='Arial 12 bold')
        MainTitle.place(x=230, y=80, width=500, height=25)

        def ShowPatientMenu():
            self.controller.show_frame("P8")

        Backbtn = Button(self, text="Back", background='#d3d3d3', font='Arial 12 bold', command=ShowPatientMenu)
        Backbtn.place(x=605, y=500, width=105, height=25)

        self.SubTitle = Label(self, text="", background='#7aa8bd', font='Arial 12 bold')
        self.SubTitle.place(x=175, y=10, width=600, height=25)

        self.refresh()

    def refresh(self):
        """Reload this user's details from the DB. Called on init and every time the page is
        shown, since CurrentUsername (and the underlying row) can change between visits."""
        cursor.execute(
            "SELECT Name, Email, ContactNumber, Gender, Country, Username, Password FROM User WHERE Username = ?",
            (CurrentUsername,))
        row = cursor.fetchone()
        if row:
            self.Name1.set(row[0])
            self.Email1.set(row[1])
            self.ContactNumber1.set(row[2])
            self.Gender1.set(row[3])
            self.Country1.set(row[4])
            self.Username1.set(row[5])
            self.Password1.set(row[6])
        self.SubTitle.config(text="Welcome, " + str(CurrentUsername) + ". See below your details")

    def show(self):
        self.refresh()
        Page.show(self)


############Start of Order a prescription Page#################
class OrderAPrescription(Page):
    def __init__(self, parent, controller, *args, **kwargs):
        Page.__init__(self, parent, *args, **kwargs)
        self.controller = controller
        self.med_map = {}  # Description -> MedicineID

        MainTitle = Label(self, text="Request a prescription ", background='#7aa8bd', font='Arial 12 bold')
        MainTitle.place(x=174, y=40, width=300, height=25)

        def ShowPatientMenu():
            self.controller.show_frame("P8")

        Backbtn = Button(self, text="Back", background='#d3d3d3', font='Arial 12 bold', command=ShowPatientMenu)
        Backbtn.place(x=400, y=230, width=105, height=25)

        Medicationlbl = Label(self, text="Select Medication", background='#7aa8bd', font='Arial 12 bold')
        Medicationlbl.place(x=175, y=90, width=200, height=25)

        self.Medication = StringVar(self)
        self.SelectedMedication = OptionMenu(self, self.Medication, "")
        self.SelectedMedication.place(x=400, y=90, width=150, height=25)

        quantitylbl = Label(self, text="Quantity in grams", background='#7aa8bd', font='Arial 12 bold')
        quantitylbl.place(x=175, y=120, width=200, height=25)
        quantity = tk.Entry(self, text="")
        quantity.place(x=400, y=120, width=150, height=25)

        def addingPrescription():
            global CurrentUsername
            if not self.med_map:
                messagebox.showinfo("Error", "There is no medication available to order")
                return
            try:
                InputQuantity = int(quantity.get())
                if InputQuantity <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showinfo("Error", "Enter a positive number in the Quantity field")
                return

            SelectedDescription = self.Medication.get()
            # FIX: the dropdown shows medicine *names* (Description), but the old code inserted
            # that name straight into MedLinked.MedicineID, which is a numeric foreign key into
            # the Medicine table. That mismatch meant approvals in the staff "Orders Made" page
            # could never find the medicine's stock. Look the real MedicineID up from the map
            # built in refresh() instead.
            InputMedicineID = self.med_map.get(SelectedDescription)
            if InputMedicineID is None:
                messagebox.showinfo("Error", "Please select a valid medication")
                return

            InputToday = date.today().isoformat()

            cursor.execute("INSERT INTO Prescription (UserID, DateIssued) VALUES(?,?)",
                           (CurrentUsername, InputToday))
            PrescriptionID = cursor.execute("SELECT MAX(PrescriptionID) FROM Prescription").fetchone()[0]

            cursor.execute("INSERT INTO MedLinked (MedicineID, PrescriptionID, Quantity) VALUES(?,?,?)",
                           (InputMedicineID, PrescriptionID, InputQuantity))
            db.commit()
            messagebox.showinfo("Success", "Ordered Successfully")
            quantity.delete(0, END)
            self.controller.show_frame("P8")

        Submitpre = Button(self, text="Request", background='#d3d3d3', font='Arial 12 bold', command=addingPrescription)
        Submitpre.place(x=200, y=230, width=105, height=25)

        self.refresh()

    def refresh(self):
        """Reload available medicines from the DB and rebuild the dropdown + name->ID map.
        Called on init and every time this page is shown, so newly-added stock (or removed
        medicines) shows up without restarting the app."""
        self.med_map = {}
        cursor.execute("Select MedicineID, Description from Medicine")
        for medicine_id, desc in cursor.fetchall():
            self.med_map[desc] = medicine_id

        menu = self.SelectedMedication["menu"]
        menu.delete(0, "end")

        if not self.med_map:
            self.Medication.set("No medicines available")
            menu.add_command(label="No medicines available", command=lambda: self.Medication.set("No medicines available"))
        else:
            for desc in self.med_map:
                menu.add_command(label=desc, command=lambda v=desc: self.Medication.set(v))
            self.Medication.set(next(iter(self.med_map)))

    def show(self):
        self.refresh()
        Page.show(self)


##################Page Display#######################################
class MainView(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        self.frames = {}
        frame_classes = {
            "P0": HomePage,
            "P1": RegisterPage,
            "P2": LoginPage,
            "P3": StaffLoginPage,
            "P4": StaffMenuPage,
            "P5": ShowMedical,
            "P6": ShowOrdersMade,
            "P7": MyDetails,
            "P8": PatientMenuPage,
            "P9": OrderAPrescription
        }

        for key, F in frame_classes.items():
            frame = F(container, self, background='#ffcd91')
            self.frames[key] = frame
            frame.place(x=0, y=0, relwidth=1, relheight=1)

        self.show_frame("P0")

    def show_frame(self, page_number):
        frame = self.frames[page_number]
        frame.show()


#######Main#############################
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Bio Gems")
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("800x800")
    root.mainloop()
