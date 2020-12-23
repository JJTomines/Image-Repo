import tkinter as tk
import shutil as stl
from PIL import ImageTk, Image
from tkinter import filedialog, messagebox, scrolledtext
from os import remove,listdir


def UploadImages(Event=None):
    filelocation = filedialog.askopenfilenames(initialdir="./")
    badfiles = []
    #stores file data as (src,name)
    goodfiles = []

    try:
        for file in filelocation:
            filename = file.split('/')[-1]

            if not IsImage(file):
                badfiles.append(file)
            else:
                goodfiles.append((file,filename))

        for file in goodfiles:
            repolocation = "Images/" + file[1]
            stl.copyfile(file[0], repolocation)

            DisplayImage(repolocation)

        tk.messagebox.showinfo(title="Success", message="Image has been added!")
        if len(badfiles) > 0:
            tk.messagebox.showerror(title="Invalid File Type", message="The following are not images:\n"+str(badfiles))

    except:
        tk.messagebox.showerror(title="Same File", message="That file is already in the directory!")

def DeleteImages(Event=None):
    filelocation = filedialog.askopenfilenames(initialdir="Images")

    userconfirmation = tk.messagebox.askquestion('Confirm choice','Are you sure you want to delete the chosen images?')

def IsImage(file):
    try:
        newimg = Image.open(str(file))
        return 1
    except:
        return 0

def DisplayImage(file):
    global img
    newimg = Image.open(str(file))
    width, height = newimg.size
    if width > 100 or height > 100:
        newimg = newimg.resize((width // 2, height // 2), Image.ANTIALIAS)

    img = ImageTk.PhotoImage(newimg)

    imagecanvas.create_image(400, 250, anchor="center", image=img)
    imagelabel.set(file.split('/')[1])

def ListDir(Event=None):
    global imagelist
    images = ""
    imagelist = scrolledtext.ScrolledText(displayframe, width=90, height=5, font=("Courier", 8))
    for file in listdir("Images"):
        DisplayImage("Images/"+file)
        images += file + "\n"
    imagelist.insert(tk.INSERT,images)
    imagelist.configure(state="disabled")
    imagelist.pack(side="right")


def EmptyDir(Event=None):
    userconfirmation = tk.messagebox.askquestion('Confirm choice','Are you sure you want to delete the directory?')

def NextImage(Event=None):
    nextimage = False
    for file in listdir("Images"):
        if file == imagelabel.get():
            nextimage = True
        elif nextimage:
            DisplayImage("Images/"+file)
            break

def PreviousImage(Event=None):
    nextimage = False
    images = listdir("Images")
    images.reverse()
    for file in images:
        if file == imagelabel.get():
            nextimage = True
        elif nextimage:
            DisplayImage("Images/" + file)
            break

root = tk.Tk()
root.geometry("1100x820")
root.resizable(False,False)
root.title("File Repository")

menubar = tk.Menu(root)
menubar.add_command(label="Login...",command=root.quit)
defaultimg = Image.open("Default.jpg")
width, height = defaultimg.size
defaultimg = defaultimg.resize((width//2,height//2),Image.ANTIALIAS)
img = ImageTk.PhotoImage(defaultimg)

tk.Label(root,text="IMAGE REPOSITORY",font=("Courier",30)).pack(side="top")

#Image Preview

previewframe = tk.LabelFrame(root,text="Image Preview")
imagecanvas = tk.Canvas(previewframe,width=800,height=500)
imagecanvas.pack(side="top")
imagecanvas.create_image(400,250,anchor="center",image=img)

imagelabel = tk.StringVar()
imagelabel.set("")

tk.Label(previewframe,textvariable=imagelabel,font=("bold",16)).pack(side="top")

previous = tk.Button(root,text="Prev. Image",height=20,width=10,command=PreviousImage)
next = tk.Button(root,text="Next Image",height=20,width=10,command=NextImage)

prevwindow = imagecanvas.create_window(-78,250,anchor="w",window=previous)
nextwindow = imagecanvas.create_window(883,250,anchor="e",window=next)
previewframe.pack(side="top",fill="x")

#Buttons
controlsframe = tk.LabelFrame(root,text="Controls")
buttonframe = tk.Frame(controlsframe)
buttonrow1 = tk.Frame(buttonframe)
buttonrow2 = tk.Frame(buttonframe)
displayframe = tk.LabelFrame(controlsframe,text="Image List")

buttonframe.pack(side="left")
displayframe.pack(side="left")
buttonrow1.pack(side="top",fill="x")
buttonrow2.pack(side="top",fill="x",pady=30)

uploadimagebutton = tk.Button(buttonrow1, text="Upload Images", command=UploadImages, width=20)
uploadimagebutton.pack(side="left",padx=15)

getlistbutton = tk.Button(buttonrow1, text="Display Repository", command=ListDir, width=20)
getlistbutton.pack(side="left",padx=15)

deleteimagebutton = tk.Button(buttonrow2,text="Delete Images", command=DeleteImages, width=20)
deleteimagebutton.pack(side="left",padx=15)

emptyrepositorybutton = tk.Button(buttonrow2,text="Empty Repository", command=EmptyDir, width=20)
emptyrepositorybutton.pack(side="left",padx=15)

controlsframe.pack(side="top",fill="both")

root.config(menu=menubar)
root.mainloop()