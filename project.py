# This script defines the class "project" and "task"
from logging import exception
import json

class Task:
    def __init__(self, name, desc, status, numid):
        self.name = name
        self.desc = desc
        self.status = status
        self.numid = numid # Necessary for removing stuff

    def ChangeStatus(self, newstatus):
        self.status = newstatus

    def ReturnStatus(self):
        if type(self.status) is bool:
            if self.status:
                return "DONE"

            else:
                return "PLANNED"

        else:
            return "WORK IN PROGRESS"

    def JSONify(self):
        return json.dumps({"TaskName": self.name, "TaskDesc": self.desc, "TaskStatus": self.status, "TaskNUMID": self.numid})

class Project:
    def __init__(self, name, desc, tasks=[]):
        self.name = name
        self.desc = desc
        self.tasks = tasks

    def ShowInfo(self):
        return f"{self.name}: {self.desc}"

    def AddTask(self, taskname, taskdesc, taskstatus):
        num = len(self.tasks)
        self.tasks.append(Task(taskname, taskdesc, taskstatus, num))
    
    def RemoveTask(self, numid): # Fix a potential bug with NUMids (task 4)
        try:
            self.tasks.pop(numid)

        except:
            exception("IndexError")

    def ModifyTask(self, numid, newstatus):
        try:
            self.tasks[numid]

        except:
            return "Error"
        
        else:
            self.tasks[numid].ChangeStatus(newstatus)

    def DumpJSON(self):
        # JSONify tasks
        JSONifiedTasks = []
        for task in self.tasks:
            JSONifiedTasks.append(task.JSONify())

        return json.dumps({"name": self.name, "desc": self.desc, "tasks": JSONifiedTasks})

    def IterateTasks(self):
        DaTasks = {}
        for task in self.tasks:
            TheThing = f"{task.numid} | {task.name}: {task.desc}"
            DaTasks[TheThing] = task.ReturnStatus()

        return DaTasks

def LoadProject(project):
    deJSONifiedTasks = []
    for task in project["tasks"]:
        LoadedTask = json.loads(task)
        IteratedTask = Task(LoadedTask["TaskName"], LoadedTask["TaskDesc"], LoadedTask["TaskStatus"], LoadedTask["TaskNUMID"])
        deJSONifiedTasks.append(IteratedTask)

    return Project(project["name"], project["desc"], deJSONifiedTasks)