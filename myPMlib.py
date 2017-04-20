# This is a file for the myProjectmanagement toolset
# it is all main class ciintainer file


# Library imports

import pickle
from os import path
import random


# Global functions and procedures
def saveObj(obj, filename):
    '''This functions save object data to disk - as pickle do'''
    with open(filename, 'wb') as output:
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)


def load_object(filename):
    '''load object data from file - as pickle do'''
    with open(filename, 'rb') as myInput:
        return pickle.load(myInput)


# Global classes
class myProject:
    '''This is main conitainer class.
    it will hold all data and allow for a save and resotre it
    on save or load'''

    def __init__(self, name, owner='', filename=__file__):
        '''this is the main initilisation method'''
        # Basic data
        self.name = name
        self.owner = owner

        # some technicals
        self.dir = path.dirname(filename)
        self.status = True

        # cointainers for sub objects People, Goals, Tasks
        self.tasks = []
        self.team = []
        self.goals = []

    def __repr__(self):
        '''standard repr respnse defininion'''
        return 'This is {} project. It\'s owned by {}.'.format(self.name,
                                                               self.owner)

    def __str__(self):
        '''standard string respnse defininion'''
        return 'This is {} project. It\'s owned by {}. Active: {}'.\
            format(self.name, self.owner, self.status)

    def save(self, filename):
        with open(filename, 'wb') as output:
            pickle.dump(self, output, pickle.HIGHEST_PROTOCOL)

    def addToTeam(self, member):
        '''this method add person to team list'''
        self.team.append(member)
        # TODO: making sure we dont duplicate team members!

    def addToTasks(self, task):
        '''this method add person to team list'''
        self.tasks.append(task)
        # TODO: making sure we dont duplicate team members!

    def listTasks(self):
        '''This procedure print out the task list'''
        for i, task in enumerate(self.tasks):
            print('[{}]: {} /id:{}/ L:{}'.format(i, task.name, task.iD,
                                                 task.level))

    def getTaskBy_iD(self, iD):
        '''This is function to return task index in myProject.tasks
        with given id
        in case of doubled iD it will return forst one'''

        for index, task in enumerate(self.tasks):
            if task.iD == iD:
                return index
        return False

    def info(self):
        '''This procedure print out project info'''

        print('********* PROJECT INFO **********')
        print('Name: {}'.format(self.name))
        print('Owner: {}'.format(self.owner))
        print('Is active: {}'.format(self.status))
        print('*********   TEAM      **********')

        for i, t in enumerate(self.team):
            print('({}): {}'.format(i, t.fullname))

        print('*********   TASKS     **********')

        for task in self.tasks:
            if task.level == 0:
                task.info()

        print('*********   END       **********')

    def t(self, iD):
        '''A shorcut function to get project task from list'''
        try:
            return self.tasks[iD]
        except:
            return False


class teamMember:
    '''This is main class to define a teammemeber'''
    def __init__(self, project,  name, secondname, nick=False, role=None):

        # Basic setup of team member
        self.project = project
        self.name = name
        self.secondname = secondname
        self.fullname = '{} {}'.format(name, secondname)

        # Defining persion nick - this will be our iD for team member
        if not nick:
            self.nick = '{}{}'.format(self.name, self.secondname[0])
        else:
            self.nick = nick

        # Some cointainers
        self.tasks = []
        self.goals = []

        # Some initial actions to be done
        self.project.addToTeam(self)

    def __str__(self):
        return 'I\'m {} and I work in {} project.'.format(self.fullname,
                                                          self.project.name)

    def __repr__(self):
        return 'I\'m {} and I work in {} project.'.format(self.fullname,
                                                          self.project)


class task:
    '''This is the calss that describe the tasks in the project
    task is the chunk of work that lead to goal '''

    def __init__(self, project, name, desc='New task', duration=1):
        '''This is the main set up function'''

        self.project = project
        # Adding task to the project tasks list
        self.project.addToTasks(self)

        # Some basic setup
        self.name = name
        self.desc = desc
        self.duration = duration

        # More detiled setup
        # This is the level of the task in sub task tree
        # 0 is the top most level of tasks
        self.level = 0
        self.iD = name.strip()[0] + \
            str(random.randrange(10)) + '_' + str(random.randrange(10000))

        # Cointainer for sub tasks (to make structure)
        self.subTasks = []
        self.parentiD = None

    def __str__(self):
        '''This define the aswer to string reqiuest'''
        return 'Task: {}, desc: {}, iD: {}'.format(self.name,
                                                   self.desc, self.iD)

    def __repr__(self):
        '''This define the aswer to string reqiuest'''
        return 'Task: {}, iD: {} Level: {}'.format(self.name, self.iD,
                                                   self.level)

    def addSubTask(self, subtask):
        '''adding task to self subtasks'''
        if subtask.level == 0:
            self.subTasks.append(subtask)
            subtask.level = self.level + 1
            subtask.parentiD = self.iD
            return True
        else:
            print('This task alredy have parent. Parent iD: {}'
                  .format(subtask.parentiD))
            return False

    def removeSubTask(self, iD):
        '''This function remove the task of given iD form sub tasks list'''

        for task in self.subTasks:
            if task.iD == iD:
                self.subTasks.remove(task)

    def clearLevel(self):
        '''This clears sefl parent and make the task level 0
        and remove all sub tasks dependences.
        Use with caution!!! '''
        # Cleaning parent
        # Getting the paren index in project.tasks
        index = self.project.getTaskBy_iD(self.parentiD)
        parent = self.project.tasks[index]
        parent.removeSubTask(self.iD)

        # Clearing subtasks (shifting level up to self parent)
        # TODO : need to be placed hre

        # Cleaning myself
        self.parentiD = None
        self.level = 0
        del(self.subTasks)
        self.subTasks = []

    def printInfo(self, task):
        '''Main printer for a task'''

        index = self.project.getTaskBy_iD(task.iD)

        string = '({})'.format(index)

        if task.level > 0:
            for x in range(3 * task.level - 1):
                string += ' '
            string += '\u21B3'

        print(string + '[{}]: {} | {} |duration: {} |level:{}'
              .format(task.iD, task.name, task.desc,
                      task.duration, task.level))

    def info(self):
        '''printing out the global infor of this task'''
        self.printInfo(self)

        if len(self.subTasks) > 0:
            for subtask in self.subTasks:
                subtask.info()


# Some hard coded definiiton for developemnt only
#pf = 'projekt.save'
#
#P = myProject('EntellEon', 'Tomek')
#M = teamMember(P, 'Marcin', 'Pruski')
#R = teamMember(P, 'Robert', 'Czerner')
#B = teamMember(P,'Przemysław', 'Fałkowski', 'Buźka')
#
#
#T0 = task(P, 'Nowe MCC')
#T1 = task(P, 'Shutters')
#T2 = task(P, 'Shutters main')
#T3 = task(P, 'Shutters cover')
#
#T0.addSubTask(T1)
#T1.addSubTask(T2)
#T0.addSubTask(T3)
