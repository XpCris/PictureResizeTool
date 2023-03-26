from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import os
import gc
import tkinter.messagebox as msgbox
import sys
import base64

if len(sys.argv) > 1:
    sourcepath = sys.argv[1]
else:
    sourcepath = filedialog.askopenfilename()
filename = os.path.basename(sourcepath)

global sourceimg
global sourceimgpreview
global sourceimgtk
global srcthumbtk
global sourcethumb
global preview

sourcethumb = Image.open(sourcepath)

def renderthumb():
    global preview
    global srcthumbtk
    sourcethumb.thumbnail((445,250))
    sourcethumbres = sourcethumb.resize((int(widthscale.get())+1,int(heightscale.get())+1))#,Image.ANTIALIAS)
    geometrydisplay.configure(text=str(int(widthscale.get())+1)+"x"+str(int(heightscale.get())+1))
    sourcethumbres.thumbnail((445,250))
    
    srcthumbtk = ImageTk.PhotoImage(sourcethumbres)
    preview.create_image(445/2,250/2,image=srcthumbtk,anchor="center")
    app.after(100,renderthumb)

def changeres():
    widthscale.set(widthentry.get())
    heightscale.set(heightentry.get())

def overwrite():
    imagefinal = sourceimg.resize((int(widthscale.get()),int(heightscale.get())))
    imagefinal.save(sourcepath)
    msgbox.showinfo(title="ImageResizeTool",message="Overwrote "+os.path.basename(sourcepath))
    
def saveas():
    outputpath = filedialog.asksaveasfilename()
    imagefinal = sourceimg.resize((int(widthscale.get()),int(heightscale.get())))
    imagefinal.save(outputpath)
    msgbox.showinfo(title="ImageResizeTool",message="Image exported as "+os.path.basename(outputpath))

def makebase64():
    imagefinal = sourceimg.resize((int(widthscale.get()),int(heightscale.get())))
    imagefinal.save("temp000.png")
    f = open("temp000.png","rb")
    baseencoded = base64.b64encode(f.read()).decode()
    f.close()
    app.clipboard_clear()
    app.clipboard_append("data:image/png;base64,"+baseencoded)
    os.remove("temp000.png")
    msgbox.showinfo(title="ImageResizeTool",message="Copied base64 to the clipboard.")

app = tk.Tk()

sourcethumb = Image.open(sourcepath)
sourceimg = Image.open(sourcepath)

app.geometry("500x450")
app.title("("+str(sourceimg.size[0])+"x"+str(sourceimg.size[1])+") "+filename+" - ImageResizeTool")
app.iconbitmap("icon.ico")
app.resizable(False,False)

# set-up widgets
preview = tk.Canvas(app,width=445,height=250,background="white")
widthscale = ttk.Scale(app,to=2047)
heightscale = ttk.Scale(app,orient="vertical",to=2047)
widthentry = ttk.Entry(app)
heightentry = ttk.Entry(app)
tk.Label(text="Width:").place(x=10,y=310)
tk.Label(text="Height:").place(x=10,y=335)
setbutton = ttk.Button(text="Set", command=changeres)
overwritebutton = ttk.Button(text="Overwrite "+filename,command=overwrite)
saveasbutton = ttk.Button(text="Save as...",command=saveas)
tk.Label(text="Made by XpCris").place(x=10,y=425)
geometrydisplay = tk.Label(text="")
exportbasebutton = ttk.Button(text="Copy Image as Base64",command=makebase64)

geometrydisplay.place(x=400,y=425)
exportbasebutton.place(x=260,y=395,width=230,height=25)
saveasbutton.place(x=10,y=370,width=240,height=50)
overwritebutton.place(x=260,y=370,width=230,height=25)
setbutton.place(x=170,y=309,width=320,height=48)
widthentry.place(x=60,y=310,width=100)
heightentry.place(x=60,y=335,width=100)
preview.place(x=10,y=10)
widthscale.place(x=10,y=280,width=445)
heightscale.place(x=465,y=10,height=250)

widthscale.set(sourcethumb.size[0])
heightscale.set(sourcethumb.size[1])

renderthumb()

app.mainloop()