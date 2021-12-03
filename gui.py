from pathlib import Path

from tkinter import Frame, Label, Listbox, Scrollbar, Tk, Canvas, Entry, Text, Button, PhotoImage, Toplevel
from tkinter.constants import ACTIVE, BOTTOM, BROWSE, CENTER, GROOVE, LEFT, RAISED, RIDGE, RIGHT, SINGLE, SUNKEN, TOP
from types import CellType
import requests
from datetime import datetime


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")
DESC_WIDTH = 10

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def grabJson(pageNum, Auth):
    URL = "https://zcctmart.zendesk.com/api/v2/tickets.json?per_page=25&page=" + str(pageNum)
    return requests.get(url=URL, auth=Auth).json()

class GUI:
    def __init__(self, data, Auth) -> None:
        self.data = data
        self.listbox = None
        self.master = None
        self.pageLabel = None
        self.page = 1
        self.Auth = Auth
        self.ticketFrame = None
        self.run()

    def buildTicket(self, ticket):
        # Select items to display in the list
        summarize = ticket["subject"] if len(ticket["subject"]) < 15 else ticket["subject"][:15] + "..."
        ans = (str(ticket["id"]), summarize, "Opened by: " + str(ticket["requester_id"]), "on " + str(datetime.strptime(ticket["created_at"], "%Y-%m-%dT%H:%M:%SZ").date()))
        return " ".join(ans)

    def buildTicketFrame(self, ticketID, master):
        # TODO: Must build a try except block as some json tags are not required
        ticket = self.data["tickets"][(int(ticketID)%25)-1]
        frame = Frame( master=master , bg="#FFFFFF" )
        if self.ticketFrame is not None:
            self.ticketFrame.destroy()
        self.ticketFrame = frame
        Label( frame, text="Ticket Stub:", pady=4, font=("NotoSerif Regular", 20 * -1), fg="#283423", bg="#FFFFFF").pack( side=TOP )
        Label( frame, text="Subject: \"" + str(ticket["subject"]).capitalize() + "\"", pady=2, font=("NotoSerif Regular", 12 * -1), fg="#283423", bg="#FFFFFF").pack( side=TOP, anchor="w" )
        Label( frame, text="Owner ID: " + str(ticket["requester_id"]), pady=2, font=("NotoSerif Regular", 12 * -1), fg="#283423", bg="#FFFFFF").pack( side=TOP, anchor="w" )
        Label( frame, text="Created at: " + str(datetime.strptime(ticket["created_at"], "%Y-%m-%dT%H:%M:%SZ").date()) + " Time: " + str(ticket["created_at"])[-9:-1], pady=2, font=("NotoSerif Regular", 12 * -1), fg="#283423", bg="#FFFFFF").pack( side=TOP, anchor="w" )
        Label( frame, text="Priority: " + str(ticket["priority"]).capitalize(), pady=2, font=("NotoSerif Regular", 12 * -1), fg="#283423", bg="#FFFFFF").pack( side=TOP, anchor="w" )
        Label( frame, text="Status: " + str(ticket["status"]).capitalize(), pady=2, font=("NotoSerif Regular", 12 * -1), fg="#283423", bg="#FFFFFF").pack( side=TOP, anchor="w" )
        Label( frame, text="Description: ", pady=2, font=("NotoSerif Regular", 12 * -1), fg="#283423", bg="#FFFFFF").pack( side=TOP, anchor="w" )
        descAc = str(ticket["description"]).split(" ")
        numLines = int(len(descAc)/DESC_WIDTH)
        for i in range(0,numLines):
            Label( frame, text=" ".join(descAc[i*DESC_WIDTH:i*DESC_WIDTH+DESC_WIDTH]), font=("NotoSerif Regular", 10 * -1), fg="#283423", bg="#FFFFFF").pack( side=TOP )
        Label( frame, text=" ".join(descAc[DESC_WIDTH*numLines:]), font=("NotoSerif Regular", 10 * -1), fg="#283423", bg="#FFFFFF").pack( side=TOP )
        frame.place(
            x=455,
            y=118,
            width=420
        )

    def clickListEvent(self, event):
        ticket = self.listbox.get(self.listbox.curselection())
        self.buildTicketFrame( ticketID=ticket.split(" ")[0], master=self.master)

    def clickChangePage(self, dir, enter):
        page = self.page+dir
        if enter:
            page = dir
        if page <= 0:
            return
        data = grabJson(pageNum=page, Auth=self.Auth)
        if data is not None and data["tickets"]:
            self.setupList(values=data)
            self.page = page
            self.data = data
            self.pageLabel.delete(0, 'end')
            self.pageLabel.insert(0, page)
            return
        self.pageLabel.delete(0, 'end')
        self.pageLabel.insert(0, int(self.page))

    def setupList(self, values):
        self.listbox.delete(0,'end')
        counter = 0
        for i in values["tickets"]:
            counter += 1
            self.listbox.insert(counter, self.buildTicket(i))

    def run(self):
        window = Tk()
        window.title("Zendesk Ticket Viewer")
        window.geometry("901x640")
        window.configure(bg = "#FFFFFF")


        canvas = Canvas(
            window,
            bg = "#FFFFFF",
            height = 640,
            width = 901,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        canvas.place(x = 0, y = 0)
        image_image_1 = PhotoImage(
            file=relative_to_assets("image_1.png"))
        canvas.create_image(
            449.25694465637207,
            319.8826389312744,
            image=image_image_1
        )

        canvas.create_text(
            352.2659606933594,
            60.692359924316406,
            anchor="nw",
            text="Ticket Viewer",
            fill="#283423",
            font=("NotoSerif Regular", 30 * -1)
        )

        canvas.create_text(
            262.7916564941406,
            23.150693893432617,
            anchor="nw",
            text="Zendesk Coding Challenge",
            fill="#283423",
            font=("NotoSerif Regular", 30 * -1)
        )

        if self.data is None or not self.data["tickets"]:
            canvas.create_text(
                262.7916564941406,
                350,
                anchor="nw",
                text="Oops...Unable to load tickets",
                fill="#283423",
                font=("NotoSerif Regular", 30 * -1)
            )
            window.mainloop()
            return

        buttonFrame = Frame( 
            master=window,
            bg="#FFFFFF"
        )
        pageNavLbl = Label(
            master = buttonFrame,
            text = "Page Navigator",
            fg = "#283423",
            bg = "#FFFFFF",
            font = ("NotoSerif Regular", 20 * -1)
        )
        pageNavLbl.pack( side=TOP )
        tickets = Listbox(
            master = buttonFrame,
            selectmode = SINGLE,
            height = 25,
            borderwidth=2,
            width = 100,
            highlightbackground="#283423",
            bg = "#FFFFFF",
            relief=RIDGE,
            exportselection=False
        )
        self.listbox = tickets
        self.master = window
        self.setupList( self.data )
        self.buildTicketFrame( self.data["tickets"][0]["id"], window )
        tickets.pack( side=TOP )
        leftButton = Button(
            buttonFrame,
            text="Prev",
            fg="#283423",
            bg="#FFFFFF",
            highlightbackground="#FFFFFF",
            command=lambda: self.clickChangePage(dir=-1, enter=False)
        )
        leftButton.pack( side=LEFT )
        rightButton = Button(
            buttonFrame,
            text="Next",
            fg="#283423",
            bg="#FFFFFF",
            highlightbackground="#FFFFFF",
            command=lambda: self.clickChangePage(dir=1, enter=False)
        )
        rightButton.pack( side=RIGHT )
        buttonFrame.place(
            x=20,
            y=120,
            width=430
        )
        pageNum = Entry(
            buttonFrame,
            fg="#283423",
            bg="#FFFFFF",
            width=2,
            highlightbackground="#FFFFFF"
        )
        pageNum.insert(0,str(self.page))
        pageNum.bind('<Return>', lambda x: self.clickChangePage(int(pageNum.get()), enter=True))
        self.pageLabel=pageNum
        pageNum.pack( side=BOTTOM )
        tickets.bind('<<ListboxSelect>>', self.clickListEvent)
        
        window.resizable(False, False)
        window.mainloop()


