import os
from databda import data

def main():
    while True:
        os.system("cls")
        choice = str(input("What do you want to do, register or log in?(R/e)"))
        if choice.lower() == "r":
            os.system("cls")
            data.registration()
        elif choice.lower() == "e":
            os.system("cls")
            data.entrance()
        else:
            os.system("cls")