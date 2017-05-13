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
from matplotlib.backends.backend_pdf import PdfPages

# Some handy aliases
d2n = matplotlib.dates.date2num
n2d = matplotlib.dates.num2date

# Some global definitoins
# Colorscale here:

colorsIn = [(255, 49, 145), (197, 130, 194), (138, 211, 243), (82, 208, 192),
            (27, 176, 107), (0, 125, 77), (0, 54, 104), (0, 0, 110),
            (0, 0, 55), (0, 0, 0)]

colors = []
for color in colorsIn:
    colors.append(tuple(x / 255 for x in color))
del(colorsIn)


# Global functions and procedures
def getWeek(date):
    '''Just handy wrapper around the isocalendar method
    it returns the week number in the year (ISO week) of
    a given date.

    Inputs:
    date: date in datetime module format

    Returns:
    Number of a week of the year
    False - if conversion didn't work'''

    try:
        return date.isocalendar()[1]
    except:
        return False


def getYear(date):
    '''Just handy wrapper around the isocalendar method
    it returns the year of the given date.

    Inputs:
    date: date in datetime module format

    Returns:
    Yeaa in 4 digit format
    False - if conversion didn't work
    '''
    try:
        return date.isocalendar()[0]
    except:
        return False


def saveObj(obj, filename):
    '''This procedure save object data to disk.
    it uses the Pickle module to derialize the objects.

    Inputs:
    obj: object to be saved.
    Generally intention is to be the main project object as
    it contins inside all the project dta, objects, lists and varialbles
    by this it's saving all the project data.

    filename: file to save the data to with properly delivered path.
    If the file don't exist it will be created.

    Returns:
    Nothing - it's procedure.

    Example use:``
    exaveObj(P, 'project.save')
    where P is myProject class object.
    '''
    with open(filename, 'wb') as output:
        pickle.dump(obj, output, pickle.DEFAULT_PROTOCOL)


def loadObj(filename):
    '''load object data from file that was saved by saveObj function.
    Inputs:
    filename: file to save the data to with properly delivered path.

    Returns:
    Recreated object

    Example use:``

    P = loadObj('project.save')
    recreate P as myProject class object.
    '''
    with open(filename, 'rb') as myInput:
        return pickle.load(myInput)


# Global classes
class myProject:
    '''This is main conitainer class for the project.
    it will hold all data and allow for a save and resotre it
    on save or load

    All work need to start with creation of a project object.

    Usage example:

    P = myProject('Project Name', 'PM')

    Inputs:
    name: a name for the project (string)
    owner: project owner (string)
    '''

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
        '''This procedure save object data to disk.
        it uses the Pickle module to derialize the objects.

        Inputs:

        filename: file to save the data to with properly delivered path.
        If the file don't exist it will be created.

        Returns:
        Nothing - it's procedure.

        Example use:

        P.save('project.save')

        where P is myProject class object.
        '''
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

    # @property
    def infoHTML(self, L=None):
        '''This procedure get back info in form of HTML
        language'''

        print('------------------------------------------')
        for task in self.tasks:
            if task.level == 0:
                task.infoHTML(outL=L)
        print('------------------------------------------')

    @property
    def info(self):
        '''This procedure print out project info
        it is set up to don't need brackets when called'''

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

    def tasksSummary(self):
        '''This precedure create the matplotlib of tasks summary'''
        tempList = []
        self.infoHTML(L=tempList)
        self.summaryGraph(tempList[::-1], self.milestones)

    def listTasksSummary(self):
        '''This precedure create the matplotlib of tasks summary'''
        tempList = []
        self.infoHTML(L=tempList)
        return tempList

    def wbs(self, tasklist=None):
        '''This procedure printsout the WBS strycture in plt plot'''
        plt.style.use('seaborn-muted')

        if tasklist is None:
            tasklist = []
            self.infoHTML(tasklist)

        # Figuring out the max level depth - to make the lines wider :)
        levels = []
        for t in tasklist:
            levels.append(t.level)
        maxLevel = max(levels)+1
        del(levels)

        if len(tasklist) > 0:
            fig = plt.figure('WBS Plot')
            # fig.set_size_inches(22, 12)
            fig.clear()

            ax_t = plt.subplot2grid((1, 1), (0, 0), rowspan=1, colspan=1)

            y_labels = []
            y_width = []
            y_left = []
            y_color = []
            y_pos = []
            y_text = []
            y_start = []
            y_duration = []
            y_end = []

            for index, task in enumerate(tasklist):
                masterindex = self.getTaskBy_iD(task.iD)
                y_labels.append('[{}]{}'.format(masterindex, task.name))
                y_width.append(maxLevel - task.level)
                y_left.append(task.level * 1)

                if task.done:
                    y_color.append('green')
                else:
                    y_color.append(colors[task.level])

                y_pos.append(index)
                y_text.append('{}'.format(task.name))
                y_start.append(d2n(task.start))
                y_duration.append(task.duration.days)
                y_end.append(d2n(task.end))

                # Adding names of owners to bottom Gantt chart
                owner_label = task.getOwner()
                if owner_label is not False:
                    # prining the owner nick
                    ax_t.text(d2n(task.start) + y_duration[-1] + 1, index,
                              owner_label.nick, color='black',
                              fontsize=8, verticalalignment='center')


            # Drawing the main rectangle fro WBS structure
            ax_t.barh(y_pos, y_width, left=y_left, color=y_color,
                      edgecolor='black', linewidth=1)


            # Set up the ticks on y axes
            ax_t.yaxis.tick_right()
            ax_t.set_yticks(y_pos)
            ax_t.set_yticklabels(y_labels)

            ax_t.invert_yaxis()  # labels read top-to-bottom

            plt.sca(ax_t)
#            plt.xticks(xTck, '', color='red')
            plt.grid(which='major', alpha=0.25)

            # Interactivity
            # self.cid = fig.canvas.mpl_connect('button_press_event', onClick)

            plt.tight_layout()
            plt.show()


    def gt(self, milestones, ax=None, x_scale=None,  y_scale=None,
           y_labels=None, text=None, clrs=None):
        '''This is a procesdure to display the gantt chart
        its designed to work in a way that it will operate on the pointed
        matplotlib element whis allows to use it as single window or as
        subplot of more complex set.

        gt stands for Gantt Chart

        Inputs:

        milestones - list of objects (of newTask class) to beplaced on graph

        ax - (optional) axis of matplotlib figure where to draw the plot
            if not specified - new plot window will be created

        x_scale - (optional) the scale for timeline axis (x)

        y_scale - (optional) list of posotion for particular tasks on y axis
            if not defined each task willhave it own line with the order from
            the milestones list. If you want to have all task on one y position
            deliver the list of y_scale = [1,1,1,1,1,...] with lenght as
            milestones lenght (i.e.: y_scale = [1] * len(milestones) )

        y_labels - (optional) list of labels for each y axis position

        text - (optional) the text to be placed at the end of the stak bar
                if not set as a list then it will be task name

        clrs - colors (optional) the list of colors for each task. If not set color
            from list will be choosen by tasks level
        '''

        # Ceckinf if plot axis object is delivered and if not creating new
        if ax is None:
            fig = plt.figure('{} Timeline'.format(self.name))
            fig.clear()
            ax = plt.subplot(111)

        # Determining how the y_scale is delivered
        if y_scale is None:
            # in such case the Y sace will be just base on numbers of elements
            y_scale = range(len(milestones))
        else:
            try:
                # checking if the y position list have info for all
                # elements in milestones ()
                if len(y_scale) == len(milestones):
                    pass
                else:
                    y_scale = range(len(milestones))
            except:
                y_scale = range(len(milestones))

        # Plotting milestones if delivered by milestones
        if len(milestones) > 0:
            # some variables preparation
            topWBS_timeline = []

            for index, mstone in enumerate(milestones):

                topWBS_y = y_scale[index]

                try:
                    color = clrs[index]
                except:
                    color = colors[mstone.level]


                ax.barh(topWBS_y, mstone.duration.days,
                          left=d2n(mstone.start),
                          color=color,
                          edgecolor='black', linewidth=1)

                # preparing the timeline x axis marks
                if d2n(mstone.end) not in topWBS_timeline:
                    topWBS_timeline.append(d2n(mstone.end))

                if d2n(mstone.start) not in topWBS_timeline:
                    topWBS_timeline.append(d2n(mstone.start))
                try:
                    tx = text[index]
                except:
                    tx = mstone.name

                ax.text(d2n(mstone.end) + 0.1,
                          topWBS_y - .4, '{}'.format(tx))

            # Adding extra space at end of timeline
            topWBS_timeline.append(max(topWBS_timeline) + 7)

            # fixing the y scale an labels
            ax.set_yticks(y_scale)
            if y_labels is not None:
                ax.set_yticklabels(y_labels)

            # Formatting time (x) axis and labels
            if x_scale is None:
                ax.set_xticks(topWBS_timeline)
            elif x_scale == 'w' or x_scale == 'weeks':
                # Drawing a week based timeline marks
                x_scale = np.arange(min(topWBS_timeline),
                                    max(topWBS_timeline)+14, 7)
                ax.set_xticks(x_scale)
            else:
                # Using the external delivered list for time marks
                ax.set_xticks(x_scale)

            myFmt = matplotlib.dates.DateFormatter("%d-%m-%y")
            ax.xaxis.set_major_formatter(myFmt)
            labelsx = ax.get_xticklabels()
            plt.setp(labelsx, rotation=45, fontsize=6, ha='right')
            ax.grid(which='major', alpha=0.25)

            # Drawing today line
            today = d2n(dt.datetime.today())
            ax.axvline(x=today, ls='--', linewidth=1, color='red')
            # Leaved here in case the today txt is needed next to line
            # ax.text(today, topWBS_y + 0.5, 'TODAY', color='red')

            return True
        else:
            print('No milestone list delivered')
            return False


    def summaryGraph(self, tasklist=None, milestones=None):
        '''This procedure prepare and display tasks structure graph'''

        def onClick(event):
            if event.xdata is not None and event.ydata is not None:
                if int(event.ydata) >= 0 and int(event.ydata) < len(tasklist):
                    print(tasklist[int(event.ydata + .4)])

        plt.style.use('seaborn-muted')

        if tasklist is None:
            tasklist = self.tasks

        if len(tasklist) > 0:
            fig = plt.figure('Summary Plot')
            # fig.set_size_inches(22, 12)
            fig.clear()

            ax_t = plt.subplot2grid((4, 5), (0, 0), rowspan=1, colspan=5)
            ax_r = plt.subplot2grid((4, 5), (1, 1), rowspan=3, colspan=4)
            ax_l = plt.subplot2grid((4, 5), (1, 0), rowspan=3, colspan=1)

            y_labels = []
            y_width = []
            y_left = []
            y_color = []
            y_pos = []
            y_text = []
            y_start = []
            y_duration = []
            y_end = []

            topWBS_y = 0
            topWBS_yticks = []
            topWBS_timeline = []

            for index, task in enumerate(tasklist):
                masterindex = self.getTaskBy_iD(task.iD)
                y_labels.append('[{}]'.format(masterindex))
                y_width.append(1)
                y_left.append(task.level * 1)

                if task.done:
                    y_color.append('green')
                else:
                    y_color.append(colors[task.level])

                y_pos.append(index)
                y_text.append('{}'.format(task.name))
                y_start.append(d2n(task.start))
                y_duration.append(task.duration.days)
                y_end.append(d2n(task.end))

            # Drawing the main rectangle fro WBS structure
            ax_l.barh(y_pos, y_width, left=y_left, color=y_color,
                      edgecolor='black', linewidth=1)

            # Set up the ticks on y axes
            ax_l.yaxis.tick_right()
            ax_l.set_yticks(y_pos)
            ax_l.set_yticklabels(y_labels)

            # Worning on the x ticks for WBS plot
            xTck = []
            for val in y_left:
                if val + .05 not in xTck:
                    xTck.append(val + .05)

            plt.sca(ax_l)
            plt.xticks(xTck, '', color='red')
            plt.grid(which='major', alpha=0.25)

            # Plotting milestones if delivered by separate list
            if milestones is not None:
                self.gt(milestones=milestones, ax=ax_t, y_labels=None)
            else:
                milestones = [t for t in tasklist if t.level ==0]
                self.gt(milestones=milestones, ax=ax_t, y_labels=None)

            # Drawing the t bottom right gantt
            names = [t.name for t in tasklist]
            text = [t.getOwnerName() for t in tasklist]
            col = [colors[t.level] for t in tasklist]

            for i, x in enumerate(tasklist):
                if x.done:
                    col[i] = 'green'

            self.gt(milestones=tasklist, x_scale='w', ax=ax_r, y_labels=names, text=text,
                    clrs=col)



            # Turning off plot box lines
            ax_l.spines["top"].set_visible(False)
            ax_l.spines["right"].set_visible(False)
            # ax.spines["bottom"].set_visible(False)

            ax_r.spines["top"].set_visible(False)
            ax_r.spines["right"].set_visible(False)
            # ax_r.spines["bottom"].set_visible(False)
            ax_r.spines["left"].set_visible(False)

            ax_l.set_title('WBS (task structure)')
            ax_r.set_title('WBS tasks gant chart')
            ax_t.set_title('Milestones & Critical path')




            # Interactivity
            # self.cid = fig.canvas.mpl_connect('button_press_event', onClick)

            plt.tight_layout()
            plt.subplots_adjust(wspace=3, hspace=0.5)
            plt.show()

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

                    if task.done:
                        y_color.append('green')

                    elif task.level == 0:
                        y_color.append('blue')
                    else:
                        y_color.append(colors[task.level])

                    time_label.append('{:%d %m %Y}'.format(task.start))

                    owner_label = task.getOwner()
                    if owner_label is not False and names:
                        # prining the owner nick
                        ax.text(d2n(task.start) + duration + 1, index,
                                owner_label.nick, color='black',
                                fontsize=8, verticalalignment='center')

            # Adding last tick mark at the end
            time_label.append('{:%d %m %Y}'.format(task.end))

            y_pos = np.arange(len(y_labels))
            # Drawing the main rectangle
            ax.barh(y_pos, y_width, left=y_left, color=y_color,
                    edgecolor='black', linewidth=1)

            ax.set_yticks(y_pos)
            ax.set_yticklabels(y_labels)
            # ax.invert_yaxis()  # labels read top-to-bottom
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

    def saveGantt(self, filename=None):
        '''This function is about saving the current gant chart'''
        if filename:
            try:
                sFig = plt.figure('Gantt Chart')
                sFig.savefig(filename, bbox_inches='tight')
                return True
            except:
                return False

    def savePdf(self, filename=None):
        '''This procedure save multipage PDF as summary gantts for project'''
        if not filename:
            filename = 'multipage_pdf.pdf'

        with PdfPages(filename) as pdf:
            self.tasksSummary()

            plt.title('{} project WBS (Tasks structure)'.format(self.name))
            pFig = plt.figure('Summary Plot')
            pFig.set_size_inches(11.69, 16.53)
            # self.tasksSummary
            pdf.savefig(pFig, bbox_inches='tight')
            self.gantt()
            plt.title('{} project Gantt chart'.format(self.name))
            pFig = plt.figure('Gantt Chart')
            pFig.set_size_inches(16.53, 11.69)
            self.gantt()
            pdf.savefig(pFig, bbox_inches='tight')

            # and looping thrue all team members
            for m in range(1, len(self.team)):
                self.gantt(self.m(m).tasks)
                # self.summaryGraph(self.m(m).tasks)
                plt.title(self.m(m).fullname)
                pFig = plt.figure('Gantt Chart')
                # pFig = plt.figure('Summary Plot')
                pdf.savefig(pFig, bbox_inches='tight')

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

    def getOwnerName(self, task):
        '''This finction look up for the owner of a task'''

        for member in self.team:
            for memberTask in member.tasks:
                if memberTask is task:
                    return member.nick
        return ''

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

            # Going thrue all myProject variables and check if itm is
            # list with deleted task in it.
            # To make sure we delete the task from all timelines and similar
            for objVar in vars(self):
                try:
                    if task in vars(self)[objVar]:
                        for index, value in enumerate(vars(self)[objVar]):
                            if value is task:
                                print('Removing from position [{}] in {}'.
                                      format(index, objVar))
                                vars(self)[objVar].pop(index)
                except:
                    pass
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

    def infoHTML(self, L=None):
            '''This procedure get back info in form of HTML
            language'''

            if L is None:
                L = []

            print('------------------------------------------')
            for task in self.tasks:
                if task.level == 0:
                    task.infoHTML(outL=L)
            print('------------------------------------------')
            return L

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
        self.done = False

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
        self.duration = self.end - self.saart
        print (self.duration.days())
        

    def setDuration(self, wks):
        '''this set up the duration of the task'''
        self.duration = dt.timedelta(weeks=wks)
        self.end = self.start + self.duration

    def setStart(self, time):
        '''This procedure set up the start time of the task'''
        self.start = time
        print('Start date set as: {}'.format(self.start))

        self.end = self.start + self.duration

    def setEnd(self, time):
        '''This procedure set up the start time of the task'''
        self.end = time
        print('End date set as: {}'.format(self.start))

        self.start = self.end - self.duration

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

    # @property
    def infoHTML(self, outL=None):
        '''this procedure set out the html version of info'''
        self.printHTML(self)

        if outL is not None:
            outL.append(self)

        if len(self.subTasks) > 0:
            for subtask in self.subTasks:
                subtask.infoHTML(outL=outL)

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

    def getOwnerName(self):
        '''looking for this task owner'''
        for m in self.project.team:
            for t in m.tasks:
                if t is self:
                    return m.nick
        return ''

if __name__ == '__main__':
    # Some hard coded definition for developemnt only
    pf = 'projekt.save'
    P = loadObj(pf)
