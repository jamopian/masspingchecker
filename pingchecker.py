from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import os











#define the window frame
class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()
        self.pingList = []#list containing the ping for each IP +"ms"
        self.serverList = []#list containing all IPs. stored as a string
        self.pingResults = ""#results from the mass ping of all the IPs, initially nothing
        #since the IP file has not been read in.

    #creation of init window inside this frame
    def init_window(self):
        #set title of widget
        self.master.title("Mass Ping Checker")
        #take up full space of root window
        self.pack(fill=BOTH, expand=1)

        #button to copy ping results
        copyButton = Button(self, text="Copy", command=self.copyToClipboard,compound=CENTER)

        #place button in window
        copyButton.place(x=228,y=0)

        # button to copy ping results
        clearButton = Button(self, text="Clear", command=self.clearText, compound=CENTER)

        # place button in window
        clearButton.place(x=288, y=0)

        # button to update ping results
        updateButton = Button(self, text="Update", command=self.updateResults, compound=CENTER)

        # place button in window
        updateButton.place(x=255, y=210)

        #textfield that stores ping info

        self.text = Text(self, width= 28, height=120)
        self.text.place(x=0, y=0)
        #self.text.pack(expand = FALSE)

        self.text.configure(state="disabled")




        #menu initialisation for "file"
        menu = Menu(self.master)
        self.master.config(menu=menu)
        file = Menu(menu)

        edit = Menu(menu)

        # add file to menu
        menu.add_cascade(label="File", menu=file)

        #file menu options

        # add an open file command
        file.add_command(label="Open", command=self.file_open)

        # add a save command - saves ping results
        file.add_command(label="Save", command=self.saveResults)

        #add an exit command to file menu
        file.add_command(label = "Exit", command = self.client_exit)




        #add edit section to menu
        menu.add_cascade(label = "Edit", menu = edit)

        #edit menu options
        edit.add_command(label="Copy", command=self.copyToClipboard)

        edit.add_command(label="Clear", command=self.clearText)




    #exit program
    def client_exit(self):
        exit()

    #processFile()
    #opens the list of IPs, storing them in a list and returning them to the calling function.

    def processFile(self, fileName):

        try:
            with open(fileName, 'r') as file:
                for line in file:
                    self.serverList.append(line.strip('\n'))
        except FileNotFoundError:
        #if user closed the open file dialog, an exception is thrown, however there's no point in doing
        #anything about it since it does not affect the program
            pass

    #ping(serverList)
    #iterates through the list of IPs, running the windows ping command, and stripping the result
    #to return only the latency value.
    def ping(self):


        for i in self.serverList:


            ping = os.popen('ping ' + i + ' -n 1')
            result = ping.readlines()
            if "could not find" in result[0]:
                messagebox.showinfo("Error", "A destination was found to be unreachable.")
                self.pingList.append("Destination unreachable")

            else :
                msLine = result[-1].strip()
                pingText = msLine.split(' = ')[-1]
                self.pingList.append(pingText)


    #file open dialog
    def file_open(self):
        if(self.text.get(1.0, END) is not None):#if there's text already in the textbox, i.e. a file has already
            #been opened.
            self.clearText()
            self.pingList.clear()#clear ping list and server list every time a new file is opened,
            #if not the pinglist and serverlist will still have the old file info.
            self.serverList.clear()

        filename =  filedialog.askopenfilename( initialdir="C:/", title="Select file",
                                           filetypes=(("text files", "*.txt"), ("all files", "*.*")))

        #read through file
        self.processFile(filename)

        self.text.configure(state="disabled")
        self.updateResults()

    def addPingResults(self):

        self.text.configure(state="normal")#allow input temporarily so we can enter ping results


        for i in range(len(self.serverList)):

            self.text.insert(END, self.serverList[i] + " -- " + self.pingList[i] + "\n")
        self.text.configure(state="disabled")  # disable input after
        self.pingResults = self.text.get(1.0, END)

    def saveResults(self):
        if self.pingResults!="":
            fileName = filedialog.asksaveasfile(mode = 'w', initialdir="C:/", title="Save file",
                                           filetypes=(("text files", ".txt"), ("all files", "*.*")))
            if fileName is not None:#None is returned if user closes the dialog
                fileName.write(self.pingResults)
                fileName.close()

        else:
            messagebox.showinfo("Error", "You have no ping results to save. Please open a txt file containing"
                                         " server IPs to ping them.")

    def copyToClipboard(self):
        self.clipboard_clear()
        self.clipboard_append(self.pingResults)

    def clearText(self):

        self.text.configure(state = "normal")
        self.text.delete(1.0, END)
        self.text.configure(state="disabled")

    def updateResults(self):
        self.clearText()
        self.pingList.clear()
        self.ping()

        self.addPingResults()






















#root window created
root = Tk()
#size of window
root.geometry("325x240")
app = Window(root)

root.mainloop()





