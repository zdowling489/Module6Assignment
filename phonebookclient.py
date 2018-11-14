"""
File: phonebookclient.py
Project 10.10
This module defines the PhonebookClient class, which provides a window
for a phonebook.
"""

from socket import *
from codecs import decode
from breezypythongui import EasyFrame

HOST = "localhost"
PORT = 5000
ADDRESS = (HOST, PORT)
BUFSIZE = 1024
CODE = "ascii"


class PhoneClient(EasyFrame):
    """Represents the window for a user to add a person
       to a phonebook or search for a persons phone number."""

    def __init__(self):
        """Sets up the window and widgets."""
        EasyFrame.__init__(self, title="""Address Book""")

        # Label and field for first name
        self.addLabel(text="First Name:",
                      row=0, column=0,
                      sticky="NSEW")
        self.inputField1 = self.addTextField(text="",
                                             row=0,
                                             column=1,
                                             width=5,
                                             sticky="NSEW")

        # Label and field for last name
        self.addLabel(text="Last Name:",
                      row=1, column=0,
                      sticky="NSEW")
        self.inputField2 = self.addTextField(text="",
                                             row=1,
                                             column=1,
                                             width=5,
                                             sticky="NSEW")

        # Label and field for phone number
        self.addLabel(text="Phone number:",
                      row=2, column=0,
                      sticky="NSEW")
        self.inputField3 = self.addIntegerField(value=0,
                                                row=2,
                                                column=1,
                                                width=5,
                                                sticky="NSEW")

        # Label and field for address
        self.addLabel(text="Address:",
                      row=0, column=2,
                      sticky="NSEW")
        self.inputField3 = self.addTextField(text="",
                                             row=0,
                                             column=3,
                                             width=5,
                                             sticky="NSEW")

        # Label and field for city/state
        self.addLabel(text="City/State (Ex: Bristol, RI):",
                      row=1, column=2,
                      sticky="NSEW")
        self.inputField3 = self.addTextField(text="",
                                             row=1,
                                             column=3,
                                             width=5,
                                             sticky="NSEW")

        # Label and field for zip code
        self.addLabel(text="Zip Code:",
                      row=2, column=2,
                      sticky="NSEW")
        self.inputField3 = self.addIntegerField(value=0,
                                                row=2,
                                                column=3,
                                                width=5,
                                                sticky="NSEW")

        # Add to address book button
        self.AddTo = self.addButton(text="Add",
                                    row=3,
                                    column=0,
                                    command=self.AddTo,
                                    state="disabled")

        # Update person in address book
        self.Update = self.addButton(text="Update",
                                     row=3,
                                     column=1,
                                     command=self.Update,
                                     state="disabled")

        # Search within address book button
        self.Search = self.addButton(text="Search",
                                     row=3,
                                     column=3,
                                     command=self.Search,
                                     state="disabled")

        # Text field for address book results
        self.Results = self.addTextArea(text="",
                                        row=4,
                                        column=0,
                                        rowspan=8,
                                        columnspan=4)

        # Connect to address book server button
        self.connectButton = self.addButton(text="Connect",
                                            row=13, column=1,
                                            command=self.connect)

        # Disconnect from address book server button
        self.Disconnect = self.addButton(text="Disconnect",
                                         row=13,
                                         column=2,
                                         command=self.disconnect,
                                         state="disabled")

    # Connect to the address book server
    def connect(self):
        """Attempts to connect to the server.  If successful,
        enables the send and disconnect buttons."""
        name = self.prompterBox(title = "Input Dialog",
                                promptString = "Your name:")
        if name == "": return
        self.server = socket(AF_INET, SOCK_STREAM)
        self.server.connect(ADDRESS)
        self.server.send(bytes(name, CODE))
        reply = decode(self.server.recv(BUFSIZE), CODE)
        if reply:
            self.Results.setText(reply)
            self.AddTo["state"] = "normal"
            self.Update["state"] = "normal"
            self.Search["state"] = "normal"
            self.Disconnect["state"] = "normal"
            self.connectButton["state"] = "disabled"
        else:
            self.messageBox(title="ERROR",
                            message="Could not connect")

    # Disconnect from address book server
    def disconnect(self):
        """Disconnects the client, clears the text areas,
        disables the send button, and enables connect."""
        self.server.send(bytes("DISCONNECT", CODE))
        self.server.close()
        self.Results.setText("")
        self.AddTo["state"] = "disabled"
        self.Update["state"] = "disabled"
        self.Search["state"] = "disabled"
        self.Disconnect["state"] = "disabled"
        self.connectButton["state"] = "normal"
        self.connectButton["command"] = self.connect

    # Add person to the address book
    def AddTo(self):
        """Adds input user to phonebook."""
        try:
            x = self.inputField3.getNumber()
            self.Results.setText(str(x))
        except ValueError:
            self.messageBox(title="ERROR",
                            message="Please enter phone number without any"
                                    "additional symbols such as () or -.")

    # Update/Edit existing person in address book
    def Update(self):
        """Updates info in phonebook."""
        try:
            x = self.inputField3.getNumber()
            self.Results.setText(str(x))
        except ValueError:
            self.messageBox(title="ERROR",
                            message="Please enter phone number without any"
                                    "additional symbols such as () or -.")

    # Search for a specific person within address book
    def Search(self):
        """Searches the phonebook and returns results"""
        try:
            x = self.inputField3.getNumber()
            self.Results.setText(str(x))
        except ValueError:
            self.messageBox(title="ERROR",
                            message="Please enter a last name only.")

def main(fileName=None):
    """Creates the bank with the optional file name,
    wraps the window around it, and opens the window.
    Saves the bank when the window closes."""
    PhoneClient().mainloop()


if __name__ == "__main__":
    main()
