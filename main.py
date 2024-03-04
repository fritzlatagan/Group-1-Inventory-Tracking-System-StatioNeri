from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter
from PIL import Image, ImageTk
import random
import pymysql
import csv
from datetime import datetime

#Initializes main window
main_window=tkinter.Tk()
main_window.title("StatioNeri Inventory Management")
main_window.geometry("1165x840")
main_window.configure(background="#52C3BE")
data_table=ttk.Treeview(main_window, show='headings', height=20)
style=ttk.Style()

#Some used variables
placeholderArray=['','','','','']
numeric='1234567890'
alpha='ABCDEFGHIJKLMNOPQRSTUVWXYZ'

#Mainly Responsible For Connecting to Localhost SQL Database
def connection():
    conn=pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='stockmanagementsystem'
    )
    return conn

conn=connection()
cursor=conn.cursor()

for i in range(0,5):
    placeholderArray[i]=tkinter.StringVar()

#Reads the database items
def read():
    cursor.connection.ping()
    sql=f"SELECT `item_id`, `name`, `price`, `quantity`, `description`, `date` FROM stocks ORDER BY `id` DESC"
    cursor.execute(sql)
    results=cursor.fetchall()
    conn.commit()
    conn.close()
    return results

#Refreshes the table everytime an action is performed
def refreshTable():
    for data in data_table.get_children():
        data_table.delete(data)
    for array in read():
        data_table.insert(parent='', index='end', iid=array, text="", values=(array), tag="bg_color")
    data_table.tag_configure('bg_color', background="#70DFDA")
    data_table.pack()


#Gives values to placeholderarray
def setph(word,num):
    for ph in range(0,5):
        if ph == num:
            placeholderArray[ph].set(word)

#Generates a random item ID using setph and
def generateRand():
    itemId=''
    for i in range(0,3):
        randno=random.randrange(0,(len(numeric)-1))
        itemId=itemId+str(numeric[randno])
    randno=random.randrange(0,(len(alpha)-1))
    itemId=itemId+'-'+str(alpha[randno])
    print("generated: "+itemId)
    setph(itemId,0)

#Adds/Saves items in entry to the database
def save():
    itemId=str(itemIdEntry.get())
    name=str(nameEntry.get())
    price=str(priceEntry.get())
    qnt=str(qntEntry.get())
    des=str(descriptionEntry.get())
    valid=True
    if not(itemId and itemId.strip()) or not(name and name.strip()) or not(price and price.strip()) or not(qnt and qnt.strip()) or not(des and des.strip()):
        messagebox.showwarning("","Please fill up all entries")
        return
    if len(itemId) < 5:
        messagebox.showwarning("","Invalid Item Id")
        return
    if(not(itemId[3]=='-')):
        valid=False
    for i in range(0,3):
        if(not(itemId[i] in numeric)):
            valid=False
            break
    if(not(itemId[4] in alpha)):
        valid=False
    if not(valid):
        messagebox.showwarning("","Invalid Item Id")
        return
    try:
        cursor.connection.ping()
        sql=f"SELECT * FROM stocks WHERE `item_id` = '{itemId}' "
        cursor.execute(sql)
        checkItemNo=cursor.fetchall()
        if len(checkItemNo) > 0:
            messagebox.showwarning("","Item Id already used")
            return
        else:
            cursor.connection.ping()
            sql=f"INSERT INTO stocks (`item_id`, `name`, `price`, `quantity`, `description`) VALUES ('{itemId}','{name}','{price}','{qnt}','{des}')"
            cursor.execute(sql)
        conn.commit()
        conn.close()
        for num in range(0,5):
            setph('',(num))
    except Exception as e:
        print(e)
        messagebox.showwarning("","Error while saving ref: "+str(e))
        return
    refreshTable()

#Updates The Selected item
def update():
    selectedItemId = ''
    try:
        selectedItem = data_table.selection()[0]
        selectedItemId = str(data_table.item(selectedItem)['values'][0])
    except:
        messagebox.showwarning("", "Please select a data row")
    print(selectedItemId)
    itemId = str(itemIdEntry.get())
    name = str(nameEntry.get())
    price = str(priceEntry.get())
    qnt = str(qntEntry.get())
    des = str(descriptionEntry.get())
    if not(itemId and itemId.strip()) or not(name and name.strip()) or not(price and price.strip()) or not(qnt and qnt.strip()) or not(des and des.strip()):
        messagebox.showwarning("","Please fill up all entries")
        return
    if(selectedItemId!=itemId):
        messagebox.showwarning("","You can't change Item ID")
        return
    try:
        cursor.connection.ping()
        sql=f"UPDATE stocks SET `name` = '{name}', `price` = '{price}', `quantity` = '{qnt}', `description` = '{des}' WHERE `item_id` = '{itemId}' "
        cursor.execute(sql)
        conn.commit()
        conn.close()
        for num in range(0,5):
            setph('',(num))
    except Exception as err:
        messagebox.showwarning("","Error occured ref: "+str(err))
        return
    refreshTable()

#Deletes the selected item
def delete():
    try:
        if(data_table.selection()[0]):
            decision = messagebox.askquestion("", "Delete the selected data?")
            if(decision != 'yes'):
                return
            else:
                selectedItem = data_table.selection()[0]
                itemId = str(data_table.item(selectedItem)['values'][0])
                try:
                    cursor.connection.ping()
                    sql=f"DELETE FROM stocks WHERE `item_id` = '{itemId}' "
                    cursor.execute(sql)
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("","Data has been successfully deleted")
                except:
                    messagebox.showinfo("","Sorry, an error occured")
                refreshTable()
    except:
        messagebox.showwarning("", "Please select a data row")

#Used to select an item
def select():
    try:
        selectedItem = data_table.selection()[0]
        itemId = str(data_table.item(selectedItem)['values'][0])
        name = str(data_table.item(selectedItem)['values'][1])
        price = str(data_table.item(selectedItem)['values'][2])
        qnt = str(data_table.item(selectedItem)['values'][3])
        des = str(data_table.item(selectedItem)['values'][4])
        setph(itemId,0)
        setph(name,1)
        setph(price,2)
        setph(qnt,3)
        setph(des,4)
    except:
        messagebox.showwarning("", "Please select a data row")

#Finds an item based on one of the user's entry
def find():
    itemId = str(itemIdEntry.get())
    name = str(nameEntry.get())
    price = str(priceEntry.get())
    qnt = str(qntEntry.get())
    des = str(descriptionEntry.get())
    cursor.connection.ping()
    if(itemId and itemId.strip()):
        sql = f"SELECT `item_id`, `name`, `price`, `quantity`, `description`, `date` FROM stocks WHERE `item_id` LIKE '%{itemId}%' "
    elif(name and name.strip()):
        sql = f"SELECT `item_id`, `name`, `price`, `quantity`, `description`, `date` FROM stocks WHERE `name` LIKE '%{name}%' "
    elif(price and price.strip()):
        sql = f"SELECT `item_id`, `name`, `price`, `quantity`, `description`, `date` FROM stocks WHERE `price` LIKE '%{price}%' "
    elif(qnt and qnt.strip()):
        sql = f"SELECT `item_id`, `name`, `price`, `quantity`, `description`, `date` FROM stocks WHERE `quantity` LIKE '%{qnt}%' "
    elif(des and des.strip()):
        sql = f"SELECT `item_id`, `name`, `price`, `quantity`, `description`, `date` FROM stocks WHERE `description` LIKE '%{des}%' "
    else:
        messagebox.showwarning("","Please fill up one of the entries")
        return
    cursor.execute(sql)
    try:
        result = cursor.fetchall();
        for num in range(0,5):
            setph(result[0][num],(num))
        conn.commit()
        conn.close()
    except:
        messagebox.showwarning("","No data found")

#Clears the entry form
def clear():
    for num in range(0,5):
        setph('',(num))

#Exports the database to an excel file
def exportExcel():
    cursor.connection.ping()
    sql=f"SELECT `item_id`, `name`, `price`, `quantity`, `description`, `date` FROM stocks ORDER BY `id` DESC"
    cursor.execute(sql)
    dataraw=cursor.fetchall()
    date = str(datetime.now())
    date = date.replace(' ', '_')
    date = date.replace(':', '-')
    dateFinal = date[0:16]
    with open("stocks_"+dateFinal+".csv",'a',newline='') as f:
        w = csv.writer(f, dialect='excel')
        for record in dataraw:
            w.writerow(record)
    print("saved: stocks_"+dateFinal+".csv")
    conn.commit()
    conn.close()
    messagebox.showinfo("","Excel file downloaded")

#Frame formating for succeding objects
frame=tkinter.Frame(main_window,bg="#70DFDA")
frame.pack()

#button color
btnColor="#1A9A96"

#Actions Frame
actions_frame=tkinter.LabelFrame(frame, text="Actions", borderwidth=5)
actions_frame.grid(row=1, column=0, sticky="w", padx=[20, 1500], pady=[10, 10], ipadx=[6])

saveBtn=Button(actions_frame, text="SAVE", width=10, borderwidth=3, bg=btnColor, fg='white', command=save)
updateBtn=Button(actions_frame, text="UPDATE", width=10, borderwidth=3, bg=btnColor, fg='white', command=update)
deleteBtn=Button(actions_frame, text="DELETE", width=10, borderwidth=3, bg=btnColor, fg='white', command=delete)
selectBtn=Button(actions_frame, text="SELECT", width=10, borderwidth=3, bg=btnColor, fg='white', command=select)
findBtn=Button(actions_frame, text="FIND", width=10, borderwidth=3, bg=btnColor, fg='white', command=find)
clearBtn=Button(actions_frame, text="CLEAR", width=10, borderwidth=3, bg=btnColor, fg='white', command=clear)
exportBtn=Button(actions_frame, text="EXPORT EXCEL", width=15, borderwidth=3, bg=btnColor, fg='white', command=exportExcel)

saveBtn.grid(row=0,column=1,padx=5,pady=5)
updateBtn.grid(row=0,column=2,padx=5,pady=5)
deleteBtn.grid(row=0,column=3,padx=5,pady=5)
selectBtn.grid(row=0,column=5,padx=[430,5],pady=5)
findBtn.grid(row=0,column=4,padx=5,pady=5)
clearBtn.grid(row=0,column=0,padx=5,pady=5)
exportBtn.grid(row=0,column=6,padx=5,pady=5)

#Entries Frame
entriesFrame=tkinter.LabelFrame(frame,text="Entry",borderwidth=5)
entriesFrame.grid(row=0,column=0,sticky="w",padx=[20,1500],pady=[10,0],ipadx=[6])

itemIdLabel=Label(entriesFrame,text="ITEM ID",anchor="e",width=15)
nameLabel=Label(entriesFrame,text="NAME",anchor="e",width=15)
priceLabel=Label(entriesFrame,text="PRICE",anchor="e",width=15)
qntLabel=Label(entriesFrame,text="QUANTITY",anchor="e",width=15)
descriptionLabel=Label(entriesFrame,text="DESCRIPTION",anchor="e",width=15)

itemIdLabel.grid(row=0,column=0,padx=15)
nameLabel.grid(row=1,column=0,padx=15)
priceLabel.grid(row=2,column=0,padx=15)
qntLabel.grid(row=3,column=0,padx=15)
descriptionLabel.grid(row=4,column=0,padx=15)

itemIdEntry=Entry(entriesFrame,width=50,textvariable=placeholderArray[0])
nameEntry=Entry(entriesFrame,width=50,textvariable=placeholderArray[1])
priceEntry=Entry(entriesFrame,width=50,textvariable=placeholderArray[2])
qntEntry=Entry(entriesFrame,width=50,textvariable=placeholderArray[3])
descriptionEntry=Entry(entriesFrame,width=50,textvariable=placeholderArray[4])

itemIdEntry.grid(row=0,column=2,padx=5,pady=5)
nameEntry.grid(row=1,column=2,padx=5,pady=5)
priceEntry.grid(row=2,column=2,padx=5,pady=5)
qntEntry.grid(row=3,column=2,padx=5,pady=5)
descriptionEntry.grid(row=4,column=2,padx=5,pady=5)

#Generate Random ID Button
generateIdBtn=Button(entriesFrame,text="GENERATE ID",borderwidth=3,bg=btnColor,fg='white',command=generateRand)
generateIdBtn.grid(row=0,column=3,padx=5,pady=5)

#Main Data Table
style.configure(main_window)
data_table['columns']=("Item Id", "Name", "Price", "Quantity", "Description", "Date")
data_table.column("#0", width=0, stretch=NO)
data_table.column("Item Id", anchor=W, width=125)
data_table.column("Name", anchor=W, width=275)
data_table.column("Price", anchor=W, width=125)
data_table.column("Quantity", anchor=W, width=120)
data_table.column("Description", anchor=W, width=325)
data_table.column("Date", anchor=W, width=175)
data_table.heading("Item Id", text="Item Id", anchor=W)
data_table.heading("Name", text="Name", anchor=W)
data_table.heading("Price", text="Price", anchor=W)
data_table.heading("Quantity", text="Quantity", anchor=W)
data_table.heading("Description", text="Description", anchor=W)
data_table.heading("Date", text="Date", anchor=W)
data_table.tag_configure('bg_color', background="#E2BFB3")
data_table.pack(side="left", fill="y", padx=20,pady=20)


#LOGO / IMAGE
logo = Image.open("Stationeri.png")
test = ImageTk.PhotoImage(logo)
logo_hold = tkinter.Label(image=test)
logo_hold.image = test
logo_hold.place(x=625, y=10)

#Calls refreshTable()
refreshTable()

#Closing of mainoop
main_window.resizable(False,False)
main_window.mainloop()