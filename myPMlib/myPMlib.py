# This is a file for the myProjectManagement toolset
# it is all main class cointainer file


# Library imports

import pickle
from os import path
import random
import matplotlib.pyplot as plt
import matplotlib.dates
import numpy as np
import datetime as dt

# Some handy aliases

d2n = matplotlib.dates.date2num
n2d = matplotlib.dates.num2date


# Global functions and procedures
def getWeek(date):
    '''Just handy wrapper around the isocalendar method'''
    try:
        return date.isocalendar()[1]
    except:
        return False


def getYear(date):
    '''Just handy wrapper around the isocalendar method'''
    try:
        return date.isocalendar()[0]
    except:
        return False


def saveObj(obj, filename):
    '''This functions save object data to disk - as pickle do'''
    with open(filename, 'wb') as output:
        pickle.dump(obj, output, pickle.DEFAULT_PROTOCOL)


def loadObj(filename):
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
        self.timeline = []

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
            pickle.dump(self, output, pickle.DEFAULT_PROTOCOL)

    def addToTeam(self, member):
        '''this method add person to team list'''
        self.team.append(member)
        # TODO: making sure we dont duplicate team members!

    def addToTasks(self, task):
        '''this method add person to team list'''
        self.tasks.append(task)
        # TODO: making sure we dont duplicate team members!

    def listTasks(self, level=9999):
        '''This procedure print out the task list'''
        for i, task in enumerate(self.tasks):
            if task.level <= level:
                print('[{}]: {} /id:{}/ L:{}'.format(i, task.name,
                                                     task.iD, task.level))

    @property
    def listTimeline(self):
        '''This procedure print out the task list in the Timeline'''
        for i, task in enumerate(self.timeline):
            print('[{}]: {} /id:{}/ L:{}'.format(i, task.name, task.iD,
                                                 task.level))

    @property
    def listTeam(self):
        '''This procedure print out the project Team'''
        for i, member in enumerate(self.team):
            try:
                member.role
            except:
                member.role = None
            print('[{}]: {} /Nick: {}/ Role: {}'.format(i, member.fullname,
                                                        member.nick,
                                                        member.role))

    def getTaskBy_iD(self, iD):
        '''This is function to return task index in myProject.tasks
        with given id
        in case of doubled iD it will return forst one'''

        for index, task in enumerate(self.tasks):
            if task.iD == iD:
                return index
        return False

    @property
    def infoHTML(self):
        '''This procedure get back info in form of HTML
        language'''

        print('------------------------------------------')
        for task in self.tasks:
            if task.level == 0:
                task.infoHTML
        print('------------------------------------------')

    @property
    def info(self):
        '''This procedure print out project info
        it is set up to dont need brackets when called'''

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
                task.info

        print('*********   END       **********')
        return None

    def t(self, iD):
        '''A shorcut function to get project task from list'''
        try:
            return self.tasks[iD]
        except:
            return False

    def m(self, iD):
        '''A shorcut function to get team member'''
        try:
            return self.team[iD]
        except:
            return False

    def gantt(self, tasklist=None, maxlevel=9999, names=True):
        '''This procedure is about to draw simple gantt chart
        for tasks using matplotlib as framework'''

        # plt.style.use('seaborn-pastel')
        plt.style.use('seaborn-muted')

        if tasklist is None:
            tasklist = self.timeline

        if len(tasklist) > 0:
            fig = plt.figure('Gantt Chart')
            fig.clear()
            ax = fig.add_subplot(111)

            y_labels = []
            y_width = []
            y_left = []
            y_right = []
            y_color = []
            time_label = []

            for index, task in enumerate(tasklist):
                if task.level <= maxlevel:
                    # Get Master index
                    masterindex = self.getTaskBy_iD(task.iD)
                    # Set up the name
                    y_labels.append('{}: {} [{}]'.format(index, task.name,
                                                         masterindex))
                    # bar lenght on limescale
                    duration = task.duration.days
                    y_width.append(duration)
                    # task beggining on timescale
                    y_left.append(d2n(task.start))
                    y_right.append(d2n(task.start) + duration)

                    if task.level == 0:
                        y_color.append('blue')
                    else:
                        y_color.append('C{}'.format(task.level))

                    time_label.append('{:%d %m %Y}'.format(task.start))

                    owner_label = task.getOwner()
                    if owner_label is not False and names:
                        # prining the owner nick
                        ax.text(d2n(task.start) + duration + 1, index,
                                owner_label.nick, color='black',
                                fontsize=8, verticalalignment='center')

            # Adding last tick mark at the end
            time_label.append('{:%d %m %Y}'.format(task.end))
            # y_labels.append('END')
            # y_width.append(0.1)
            # y_left.append(max(y_right))
            # y_color.append('black')

            y_pos = np.arange(len(y_labels))
            # Drawing the main rectangle
            ax.barh(y_pos, y_width, left=y_left, color=y_color,
                    edgecolor='black', linewidth=1)

            ax.set_yticks(y_pos)
            ax.set_yticklabels(y_labels)
#            ax.invert_yaxis()  # labels read top-to-bottom
            plt.xticks(np.arange(min(y_left), max(y_right)+2*7, 7))
            myFmt = matplotlib.dates.DateFormatter("%d-%m-%Y")
            ax.xaxis.set_major_formatter(myFmt)

            # Drawing today line
            today = d2n(dt.datetime.today())
            ax.axvline(x=today, ls='--', linewidth=1, color='red')

            labelsx = ax.get_xticklabels()
            plt.setp(labelsx, rotation=45, fontsize=10, ha='right')

            ax.set_xlabel('Time [grid in weeks]')
            ax.set_title('Gantt Chart for {} project.'.format(self.name))

            plt.tight_layout()
            plt.grid(which='major', alpha=0.3)
            plt.show()

        else:
            print('No tasklist')
            return False

    def timeSort(self, timeline=None):
        '''This is procedure to sort task for Gantt chart creation
        it's using order of task in project.tasks list as timeline order
        and sort task as per this'''

        if timeline is None:
            timeline = self.timeline

        for index, task in enumerate(timeline):
            if index > 0:
                task.setStart(timeline[index-1].end)
                task.prevTask = timeline[index-1]

                if task is not timeline[-1]:
                    task.nextTask = timeline[index + 1]

                print('loop na: {}'.format(timeline[index-1].end))
            else:
                task.nextTask = timeline[index + 1]

    def getOwner(self, task):
        '''This finction look up for the owner of a task'''

        for member in self.team:
            for memberTask in member.tasks:
                if memberTask is task:
                    return member
        return False

    def delTask(self, task):
        '''This function delete the task from completly
        there's no undo use wisley!'''

        # let's level the task to main level
        try:
            task.clearLevel()
        except:
            return False
        else:
            # Removing task form member list
            owner = self.getOwner(task)
            if owner is False:
                print('No owner!')
            else:
                owner.remTask(task)

            index = self.getTaskBy_iD(task.iD)
            self.tasks.pop(index)

            return True

    def chain(self, *arg):
        '''this function returns a list of task objects based on the
        global index in project.tasks'''

        issue = False
        outList = []

        for t in arg:
            try:
                self.tasks[t].iD
            except:
                issue = True
            else:
                outList.append(self.tasks[t])
        if not issue:
            return outList
        else:
            return False


class teamMember:
    '''This is main class to define a teammemeber'''
    def __init__(self, project,  name, secondname, nick=False, role=None):

        # Basic setup of team member
        self.project = project
        self.name = name
        self.secondname = secondname
        self.fullname = '{} {}'.format(name, secondname)
        self.role = role

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

    def addTask(self, task):
        '''This function add task to member tasklist'''

        try:
            task.iD
        except:
            if isinstance(task, int) and task >= 0:
                self.tasks.append(self.project.t(task))
                return True
            else:
                return False
        else:
            self.tasks.append(task)
            return True

    def listTasks(self):
        '''This function prints out the member tasks with indexes'''
        if len(self.tasks) > 0:
            for index, task in enumerate(self.tasks):
                print('({}) {} / L:{}'.format(index, task.name, task.level))

    def remTask(self, task):
        '''This function removes given task form self tasks list'''
        if len(self.tasks) > 0:
            try:
                task.iD
            except:

                try:
                    self.tasks.pop(task)
                except:
                    return False
                else:
                    return True

            else:
                for i, t in enumerate(self.tasks):
                    if t is task:
                        self.tasks.pop(i)
                        return True

    @property
    def info(self):
        '''This procedure print out team member info'''

        print('********* MY INFO **********')
        print('Name: {}'.format(self.fullname))
        print('Project: {}'.format(self.project.name))
        print('*********   TASKS     **********')

        self.listTasks()

        print('*********   END       **********')


class newTask:
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
        self.duration = dt.timedelta(weeks=duration)

        # Timing management
        self.start = dt.datetime.now()
        self.end = self.start + self.duration

        self.prevTask = None
        self.nextTask = None

        # More detailed setup
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

    def getDuration(self):
        '''This function calculate the duration of
        the task based on sub tasks'''
        pass

    def setDuration(self, wks):
        '''this set up the duration of the task'''
        self.duration = dt.timedelta(weeks=wks)
        self.end = self.start + self.duration

    def setStart(self, time):
        '''This procedure set up the start time of the task'''
        self.start = time
        print('Start date set as: {}'.format(self.start))

        self.end = self.start + self.duration

    def addSubTask(self, subtask):
        '''adding task to self subtasks'''
        if subtask.parentiD is None:
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

    def raiseSubTasks(self):
        '''This procedure take care of raising up level of sub tasks'''
        # Raising my own level
        self.level -= 1

        # Ordering my sub tasks to rais levels
        for subtask in self.subTasks:
            subtask.raiseSubTasks()

    def clearLevel(self):
        '''This clears sefl parent and make the task level 0
        and remove all sub tasks dependences.
        Use with caution!!! '''
        # Cleaning parent
        # Getting the paren index in project.tasks

        if self.parentiD is not None:
            index = self.project.getTaskBy_iD(self.parentiD)
            parent = self.project.tasks[index]
            parent.removeSubTask(self.iD)
        else:
            parent = False
            print('No parent')

        # Clearing subtasks (shifting level up to self parent)
        # Setting up parent iD for my subtasks as my parent iD
        # and adding my subtasks to my paren subtask list
        if len(self.subTasks) > 0:
            for subtask in self.subTasks:
                subtask.parentiD = None

                # Raising sub task level
                subtask.raiseSubTasks()

                if parent is not False:
                    parent.addSubTask(subtask)

        # Cleaning myself
        self.parentiD = None
        self.level = 0
        del(self.subTasks)
        self.subTasks = []

    def printInfo(self, task):
        '''Main printer for a task'''

        index = self.project.getTaskBy_iD(task.iD)
        owner = self.getOwner()
        if owner is not False:
            owner = '\x1b[32m{}\x1b[0m'.format(owner.nick)
        else:
            owner = '\x1b[31mNo owner\x1b[0m'

        prestr = ''

        # Making all indexes print out as 4 symbols size
        if len(str(index)) < 4:
            for k in range(4-len(str(index))):
                prestr += '.'

        # Adding empty line for level 0 tasks
        if task.level == 0:
            string = '____\n{}{}| '.format(prestr, index)
            MaxL = 65
        else:
            string = '{}{}| '.format(prestr, index)
            MaxL = 60

        if task.level > 0:
            for x in range(3 * task.level - 1):
                string += ' '
            string += '\u21B3'

        if task in self.project.timeline:
            string += '\x1b[32m[ {} ]\x1b[0m'.format(task.name)
            MaxL = 69
        else:
            string += '[ {} ]'.format(task.name)

        for x in range(MaxL - len(string)):
            string += '_'

        duration = task.duration.days / 7
        duration_unit = 'weeks'
        if duration < 1:
            duration = task.duration.days
            duration_unit = 'days'
        print(string + '[{} {}] {}'
              .format(duration, duration_unit, owner))

    def printHTML(self, task):
        '''this procedure prepare simple data as html'''

        string = ''

        if task.level > 0:
            for x in range(6 * task.level - 1):
                string += '\x1b[30m.'
            string += '\x1b[0m\u21B3'

        print('{} \x1b[3{}m{}\x1b[0m'.format(string, int(task.level+1),
                                             task.name))

    @property
    def infoHTML(self):
        '''this procedure set out the html version of info'''
        self.printHTML(self)

        if len(self.subTasks) > 0:
            for subtask in self.subTasks:
                subtask.infoHTML

    @property
    def info(self):
        '''printing out the global infor of this task'''
        self.printInfo(self)

        if len(self.subTasks) > 0:
            for subtask in self.subTasks:
                subtask.info

    def setTimeBySub(self):
        '''this procedure set up start and end date form subtasks'''

        starts = []
        ends = []

        for task in self.subTasks:
            starts.append(task.start)
            ends.append(task.end)

        start = min(starts)
        end = max(ends)

        self.start = start
        self.end = end
        self.duration = end - start

        print(start, end)

    def getOwner(self):
        '''looking for this task owner'''
        for m in self.project.team:
            for t in m.tasks:
                if t is self:
                    return m
        return False


if __name__ == '__main__':
    # Some hard coded definition for developemnt only
    pf = 'projekt.save'
    P = loadObj(pf)

    # P = myProject('EntellEon', 'Tomek')
    # M = teamMember(P, 'Marcin', 'Pruski')
    # R = teamMember(P, 'Robert', 'Czerner')
    # B = teamMember(P,'Przemysław', 'Fałkowski', 'Buźka')
    #
    #
    # T0 = newTask(P, 'Nowe MCC')
    # T1 = newTask(P, 'Shutters')
    # T2 = newTask(P, 'Shutters main')
    # T3 = newTask(P, 'Shutters cover')
    #
    # T0.addSubTask(T1)
    # T1.addSubTask(T2)
    # T0.addSubTask(T3)
