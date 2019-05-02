import tkinter
import socket


#Add button to enable timeout and command entry

MAX_TEXT_INSERTS = 27
CONNECTION_MESSAGE = "Please enter connection settings below and press connect.\n"

TITLE_DISCONNECTED = 'Telescope Client: Disconnected'
TITLE_CONNECTED = 'Telescope Client: Connected'

class GUIModel:
    def __init__(self):
        self.text_inserts = 0
        self.joystickEnabled = False

class GUIView:
    def __init__(self, master):
        self.mainFrame = tkinter.Frame(master)
        self.mainFrame.pack()

        #Frame for text results
        self.textFrame = tkinter.Frame(self.mainFrame)
        self.textFrame.pack(side=tkinter.TOP)
        #Text results
        self.textResults = tkinter.Text(self.textFrame, height=28)
        self.textResults.pack(side=tkinter.TOP)
        self.textResults.configure(state=tkinter.DISABLED)


        separator = tkinter.Frame(self.mainFrame, height=20, width=400)
        separator.pack(side=tkinter.TOP)


        #Frame entering a command
        self.commandFrame = tkinter.Frame(self.mainFrame)
        self.commandFrame.pack(side=tkinter.TOP)
        #Send a command
        self.commandEntry = tkinter.Entry(self.commandFrame, bd=5)
        self.commandEntry.pack(side=tkinter.LEFT)
        self.commandEntryButton = tkinter.Button(self.commandFrame, text="Execute Command")
        self.commandEntryButton.pack(side=tkinter.LEFT)

        #Seperator frame
        separator = tkinter.Frame(self.mainFrame, height=40, width=400)
        separator.pack(side=tkinter.TOP)

        #Frame for IP widget
        self.ipFrame = tkinter.Frame(self.mainFrame)
        self.ipFrame.pack(side=tkinter.TOP)
        #Ip elements
        self.ipLabel = tkinter.Label(self.ipFrame, text="IP Address")
        self.ipLabel.pack(side=tkinter.LEFT)
        self.ipEntry = tkinter.Entry(self.ipFrame, bd=5)
        self.ipEntry.pack(side=tkinter.RIGHT)

        #Frame for port
        self.portFrame = tkinter.Frame(self.mainFrame)
        self.portFrame.pack(side=tkinter.TOP)
        #Port elements
        self.portLabel = tkinter.Label(self.portFrame, text="Port")
        self.portLabel.pack(side=tkinter.LEFT)
        self.portEntry = tkinter.Entry(self.portFrame, bd=5)
        self.portEntry.pack(side=tkinter.RIGHT)


        #Frame for connect button
        self.connectFrame = tkinter.Frame(self.mainFrame)
        self.connectFrame.pack(side=tkinter.TOP)
        #Button for connecting
        self.connectButton = tkinter.Button(self.connectFrame, text="Connect")
        self.connectButton.pack(side=tkinter.LEFT)


        #Seperator
        separator1 = tkinter.Frame(self.mainFrame, height=20, width=400)
        separator1.pack(side=tkinter.TOP)



class GUIController:
    #Do all view initialization here
    def __init__(self):
        self.root = tkinter.Tk()
        self.view = GUIView(self.root)
        self.model = GUIModel()
        self.socket = socket.socket()
        self.connected = False

    def _clear_console(self):
        self.view.textResults.configure(state=tkinter.NORMAL)
        self.view.textResults.delete("1.0", tkinter.END)
        self.view.textResults.configure(state=tkinter.DISABLED)
        self.model.text_inserts = 0

    def _console_delete(self):
        self.view.textResults.configure(state=tkinter.NORMAL)
        self.view.textResults.delete("1.0", "2.0")
        self.view.textResults.configure(state=tkinter.DISABLED)

    def _consoleWrite(self, text):
        if self.model.text_inserts > MAX_TEXT_INSERTS:
            self._console_delete()

        self.view.textResults.configure(state=tkinter.NORMAL)
        self.view.textResults.insert(tkinter.END, text)
        self.view.textResults.configure(state=tkinter.DISABLED)
        self.model.text_inserts += 1

    def _connectToServer(self, host, port):
        try:
            self.socket.connect((host, int(port)))
            self._consoleWrite("Success in connecting to " + host + " on " + port + '\n')
            self.root.title(TITLE_CONNECTED)
            self.connected = True
            return True
        except socket.error:
            self._consoleWrite("Error in connecting to " + host + " on " + port + '\n')
            return False
        except ValueError:
            self._consoleWrite("Error: Invalid port, please enter a number.\n")

    def _closeConnection(self):
        try:
            self.socket.close()
        except socket.error:
            pass
        self.connected = False
        self.root.title(TITLE_DISCONNECTED)
        self.view.connectButton.configure(state=tkinter.NORMAL)
        self._consoleWrite("Connection was closed\n")

    def _sendCommand(self, command):
        try:
            if len(command) > 10:
                self._consoleWrite('Invalid command length.  Must be under 10 characters.\n')
                return
            self.socket.send(command.encode('utf-8'))
            ret_status = self.socket.recv(1024).decode('utf-8')
            self._consoleWrite(ret_status)
        except socket.error:
            # Do error checking here to indicate something is wrong and you need to reconnect
            self._closeConnection()

    def commandDialogSend(self):
        self._consoleWrite('Attempting to run: '+self.view.commandEntry.get()+'\n')
        self._sendCommand(self.view.commandEntry.get())


    def connectButton(self):
        if self.view.portEntry.get() != "" and self.view.ipEntry.get() != "":
            connected = self._connectToServer(self.view.ipEntry.get().strip(), self.view.portEntry.get().strip())
            if connected:
                self.view.connectButton.configure(state=tkinter.DISABLED)

    def keyPress(self, event):
        #Probably gonna have to figure out how to limit this on client/server side to single.
        print(event)


    def keyRelease(self, event):
        #Left/Right/Up/Down
        print(event.keysym)


    def run(self):
        #Title
        self.root.title(TITLE_DISCONNECTED)

        #Setting up key press listeners
        self.root.bind("<KeyPress>", self.keyPress)
        self.root.bind("<KeyRelease>", self.keyRelease)

        #Setting up button connections
        self.view.connectButton['command'] = self.connectButton
        self.view.commandEntryButton['command'] = self.commandDialogSend

        #Write first message
        self._consoleWrite(CONNECTION_MESSAGE)

        #Start the main execution loop
        self.root.mainloop()



if __name__ == '__main__':
    client = GUIController()
    client.run()
    print("Goodbye!")
    client.socket.close()


