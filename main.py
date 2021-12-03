import requests
import gui
from tkinter import Frame, Label, PhotoImage, Tk, Entry, Button, messagebox
from tkinter.constants import LEFT, RIGHT, TOP

#URL = "https://zcctmart.zendesk.com/api/v2/ticketz"
URL = "https://zcctmart.zendesk.com/api/v2/tickets.json?per_page=25&page=1"

# Login page
window = Tk()
window.title("Login Page")
window.geometry("450x200")
window.configure(bg = "#FFFFFF")
window.iconphoto(True, PhotoImage(file=gui.relative_to_assets("zendesk.png")))

def tryLoginAndJson( user , passw ):
    try:
        auth = (user, passw)
        re = requests.get(url=URL, auth=auth)
        if not re.ok:
            raise IOError(re.reason)
        window.destroy()
        g = gui.GUI(re.json(), auth)
    except IOError as e:
        if str(e) == "Unauthorized":
            messagebox.showerror(title="Login failed", message="Username and/or password are incorrect. Please try again")
        elif str(e) == "Not Found":
            messagebox.showerror(title="Login failed", message="Zendesk servers unavailable. Please try again at a later time.")
        else:
            messagebox.showerror(title="Login failed", message="Login failed for the following reason: " + str(e))

f = Frame(
    master=window,
    bg="#FFFFFF"
)
t = Label(
    f,
    text="Login details:",
    bg="#FFFFFF"
)
t.pack( side=TOP )
frameUser = Frame(
    f,
    bg="#FFFFFF"
)
user = Label(
    frameUser,
    text="Email: ",
    bg="#FFFFFF",
    padx=14
)
user.pack( side=LEFT )
userEntry = Entry(
    frameUser,
    bg="#FFFFFF",
    highlightbackground="#FFFFFF"
)
userEntry.pack( side=RIGHT )
frameUser.pack( side=TOP )
framePass = Frame(
    f,
    bg="#FFFFFF"
)
passw = Label(
    framePass,
    text="Password: ",
    bg="#FFFFFF"
)
passw.pack( side=LEFT )
passEntry = Entry(
    framePass,
    background="#FFFFFF",
    show="*",
    highlightbackground="#FFFFFF"
)
passEntry.pack( side=RIGHT )
framePass.pack( side=TOP )
enter = Button(
    f,
    text="Enter",
    bg="#FFFFFF",
    highlightbackground="#FFFFFF",
    command=lambda: tryLoginAndJson(userEntry.get(), passEntry.get())
)
enter.pack( side=TOP )
f.place(
    x = 100,
    y = 50
)

window.bind('<Return>', lambda x: enter.invoke())
window.mainloop()