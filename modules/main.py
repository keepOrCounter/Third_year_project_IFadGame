from status_record import *
from PCGsys import *
from interactionSys import *

if __name__ == "__main__":
    begin = True
    while begin:
        user_input = input("What would you do?>>>")
        if user_input == "__exit":
            begin = False