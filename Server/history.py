import datetime
from os import path

class History:
    def __init__(self):
        pass

    @staticmethod
    def load(force_load):
        filename = "chat/Main/" + str(datetime.date.today()) + ".chat"
        global ftext
        global Cfile
        ftext = []  # Reset array
        if path.isfile(filename) and force_load:  # If it exists add the text to array
            Cfile = open(filename, "r")  # Open file
            ftext = Cfile.readlines()  # Read lines to array
            Cfile.close()  # Close the file
            Cfile = open(filename, "a")  # Opens that file in write mode

        elif not path.isfile(filename):  # If file dose not exist make it
            Cfile = open(filename, "w")  # open file

    @staticmethod
    def add(text):  # To add text to the history
        filename = "chat/Main/" + str(datetime.date.today()) + ".chat"
        if not path.isfile(filename):  # If file dose not exist make it
            global ftext
            global Cfile
            Cfile.close()  # Close old file
            ftext = []  # Reset Array
            Cfile = open(filename, "w")  # Open file

        ftext.append(text + "\n")  # Add text to string
        Cfile.write(text + "\n")  # Add t
        # ext to file
