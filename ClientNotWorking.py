import socket
from breezypythongui import EasyFrame
import sys

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
hostname = socket.gethostname()
host = socket.gethostbyname(hostname)
port = 8888

PB = {}

class PhoneClient(EasyFrame):
    """the beginning of the gui for the client side of the phone book"""

    def __init__(self):
        """sets up window and all the widgets"""
        EasyFrame.__init__(self, title="""Address Book""")

        self.addLabel(text="First Name:", row=0, column=0, sticky="NSEW")
        self.inputField1 = self.addTextField(text="", row=0, column=1, width=5, sticky="NSEW")   # first name

        self.addLabel(text="Last Name:", row=1, column=0, sticky="NSEW")
        self.inputField2 = self.addTextField(text="", row=1, column=1, width=5, sticky="NSEW")    # last name

        self.addLabel(text="Phone number:", row=2, column=0, sticky="NSEW")
        self.inputField3 = self.addIntegerField(value=0, row=2, column=1, width=5, sticky="NSEW")  # phone Number

        self.addLabel(text="Address:", row=0, column=2, sticky="NSEW")
        self.inputField4 = self.addTextField(text="", row=0, column=3, width=5, sticky="NSEW")     # address

        self.addLabel(text="City/State (Ex: Bristol, RI):", row=1, column=2, sticky="NSEW")        # city or state
        self.inputField5 = self.addTextField(text="", row=1, column=3, width=5, sticky="NSEW")

        self.addLabel(text="Zip Code:", row=2, column=2, sticky="NSEW")                             # zipcode
        self.inputField6 = self.addIntegerField(value=0, row=2, column=3, width=5, sticky="NSEW")

        # Text field for address book results
        self.Results = self.addTextArea(text="", row=4, column=0, rowspan=8, columnspan=4)

        # Add to address book button
        self.AddTo = self.addButton(text="Add",
                                    row=3,
                                    column=0,
                                    command=self.add,
                                    state="active")

        self.connectBtn = self.addButton(text="Connect",
                                         row=14, column=2,
                                         command=self.connect)

        self.disconnectBtn = self.addButton(text="Disconnect",
                                            row=14, column=3,
                                            command=self.disconnect)

        self.Search = self.addButton(text="Search",
                                    row=3,
                                    column=2,
                                    command=self.search,
                                    state="active")

    def connect(self):

        try:
            self.server = soc
            self.server.connect((host, port))
            self.messageBox(title="IMPORTANT",
                            message="To disconnect press the exit window button in the top corner.")
        except:
            self.messageBox(title="ERROR",
                            message="The connection was not successful.")
            sys.exit()

    def disconnect(self):
        self.server = soc
        self.server.close()

    def add(self):

            try:
                message = (self.inputField2.getText() + " " + self.inputField1.getText() + " " + self.inputField3.get() +
                        " " + self.inputField4.get() + " " + self.inputField5.get() + " " + self.inputField6.get())
                PB[self.inputField2.getText()] = self.inputField2.getText(), self.inputField1.getText(), self.inputField3.get(), \
                                                 self.inputField4.get(), self.inputField5.get(), self.inputField6.get()


            except ValueError:
                self.messageBox(title="ERROR",
                                message="Please enter all information correctly.")

            soc.sendall(message.encode("utf8"))
            if soc.recv(5120).decode("utf8") == "-":
                pass  # null operation

    def search(self):
        name = self.prompterBox(promptString="Enter last name.")
        if name == "": return
        x = PB[name]
        self.Results["text"] = x

def main():
    PhoneClient().mainloop()

if __name__ == "__main__":
    main()