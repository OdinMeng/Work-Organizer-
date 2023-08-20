""" APP BLUEPRINT
This app can read a 'project file' which contains tasks, which can be marked as following:
- To do (False)
- Working on (int)
- Done (True)
If possible, it will also display percentuals according to work done.

Possibility: the 'project file' can be divided even into further parts.
E.g. Calendar -> Stuff ==> TASKS or Calendar -> Stuff2 ==> TASKS2
"""

# IMPORT STUFF HERE
import os
import project as PROJECT
import json
from colorama import Style, Fore, Back
import colorama
import time

# GLOBAL VARIABLES HERE
global cwd 
cwd = os.getcwd()
colorama.init()

# DEFINE FUNCTIONS HERE
hbar = lambda: print(Fore.BLACK + Back.WHITE + "="*35 + Style.RESET_ALL)

def exitapp():
    colorama.deinit()
    print("Alright! Goodbye in...")
    time.sleep(1)
    print("3...")
    time.sleep(1)
    print("2..")
    time.sleep(1)
    print("1...")
    time.sleep(1)
    exit()

def StartProject():
    hbar()
    print("So... you would like to start a project. Sure thing!")
    print(Back.RED + Fore.BLACK + "(WARNING ! THE NAME HAS TO BE UNIQUE, AS IT WILL BE USED FOR THE FILE PROJECT)\n" + Style.RESET_ALL)
    projname = input("Name | ")
    desc = input("Short description | ")
    print("Alright...")
    with open(cwd+"\\PROJECTS\\"+projname+".json", "w") as file:
        file.write(PROJECT.Project(projname, desc).DumpJSON())

    while 1:
        print("Alright! Everything's done! Would you like to immediately load it? \n"+Back.GREEN+"Y"+Style.RESET_ALL+": Yes \n"+Back.RED+"N"+Style.RESET_ALL+": No")
        selector = input("> ")
        ChoiceInputs = {"Y": LoadProject, "N": lambda x: None}
        if selector not in ChoiceInputs:
            print("Error: Invalid choice. Try again.")
            continue

        else:
            ChoiceInputs[selector](projname)
            print(Fore.GREEN + "Welcome back! What would you like to do? \n 1: Start a project \n 2: Load a project \n 3: Exit" + Style.RESET_ALL)
            break

def LoadProject(name = None): 
    hbar()
    LoadedJSON = None
    LoadedProject = None

    if name:
        with open(cwd+"\\PROJECTS\\"+name+".json", "r") as file:
            LoadedJSON = json.loads(file.read())
            LoadedProject = PROJECT.LoadProject(LoadedJSON)

    else:
        # Iterate through the folder for projects
        print("Alright, which project would you like to load? Here are the following options: ")
        ProjectNames = []
        for file in os.scandir(cwd+"\\PROJECTS"):
            ProjectNames.append(file.name)
            print(file.name)

        while 1:
            name = input("> ")
            if f"{name}.json" not in ProjectNames:
                print("Error. Try again.")
                continue

            else:
                with open(cwd+"\\PROJECTS\\"+name+".json", "r") as file:
                    LoadedJSON = json.loads(file.read())
                    LoadedProject = PROJECT.LoadProject(LoadedJSON)
                    break

    # Project has been loaded and defined
    hbar()
    print("Project loaded! What would you like to do?")
    while 1:
        print(" 1: See tasks \n 2: Add task \n 3: Remove task \n 4: Modify task status \n 5: Save project \n 6: Exit project")
        selector = input("> ")
        ChoiceInputs = ["1", "2", "3", "4", "5", "6"]
        if selector not in ChoiceInputs:
            print("Error: Invalid choice. Try again.")
            continue

        else:
            if selector == "1":
                print("Loading tasks...")
                hbar()
                Tasks = LoadedProject.IterateTasks()
                Keys = {"DONE": Back.GREEN, "PLANNED": Back.RED, "WORK IN PROGRESS": Back.YELLOW}
                for Task in Tasks:
                    print(Task)
                    print(Keys[Tasks[Task]] + ">>> STATUS: "+ Tasks[Task] + Style.RESET_ALL)
                    time.sleep(0.1)
                hbar()

            elif selector == "2":
                hbar()
                taskn = input("Task Name | ")
                taskd = input("Task description | ")
                LoadedProject.AddTask(taskn, taskd, False)

            elif selector == "3":
                hbar()
                p = input("Task NUMID | ") # p = numid

                try:
                    int(p)

                except:
                    print("Error: input not an integer")
                    continue

                else:
                    LoadedProject.RemoveTask(int(p))
                    print("Deleted without problems.")
                    hbar()

            elif selector == "4":
                hbar()
                p = input("Task NUMID | ") # p = numid
                news = input("New Task Status (0 = Planned, 1 = Done, Anything else = W.I.P.) \n> ")
                Key = {"0": False, "1": True}
                if news in Key:
                    news = Key[news]

                else:
                    news = 1

                LoadedProject.ModifyTask(int(p), news)
                hbar()

            elif selector == "5":
                print("Saving...")
                hbar()
                with open(cwd+"\\PROJECTS\\"+name+".json", "w") as file:
                    file.write(LoadedProject.DumpJSON())

                print("Saving done! What now?")

            elif selector == "6":
                print("Exiting...")
                hbar()
                print(Fore.GREEN + "Welcome again! What would you like to do? \n 1: Start a project \n 2: Load a project \n 3: Exit" + Style.RESET_ALL)
                break

# MAIN SCRIPT STARTS HERE
print(Fore.GREEN + "Welcome! What would you like to do? \n 1: Start a project \n 2: Load a project \n 3: Exit" + Style.RESET_ALL)
while 1:
    selector = input("> ")
    ChoiceInputs = {"1": StartProject, "2": LoadProject, "3": exitapp}
    if selector not in ChoiceInputs:
        print("Error: Invalid choice. Try again.")
        continue

    else:
        ChoiceInputs[selector]()
