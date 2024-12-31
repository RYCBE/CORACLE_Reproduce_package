from operator import itemgetter
import os
import shutil
import time
import pendulum

cwd = os.getcwd().replace('\\', '/')
sourceCodeDir = cwd+'/../rycbe/'+'sourceCode/'
graphDir = cwd+'/'+'Graphs/'
jiraDir = cwd+'/'+'JiraReportFiles/'
linkresDir = cwd+'/'+'LinkJiraToCommit/'
TBFcutresDir = cwd+'/'+'TBFCuts/'
TagsDir = cwd+'/'+'Tags/'
SelectedDir = cwd+'/'+'SelectedTBFs/'
unionDictDir = cwd+'/'+'UnionDictDir/'
FinalResDir = cwd+'/'+'FinalRes/'
v2vDir = cwd+'/'+'v2v/'
# VansBFCDir = cwd+'/VansBFC/'
VanVersioncsvDir = cwd+'/VanVersioncsv/'
JsonDir = cwd+'/JsonDir/'

BugFixFilesDir = cwd+'/bugFixFiles/'
TBFJsonDir = cwd+'/TBFJsonDir/'


class utils:
    """
        A filename contains the list of Apache projects you want to include.
    """

    def __init__(self, value):
        self.listfile = value
        lf = open(self.listfile)
        self.projects, self.PROs = list(
            zip(*[x[:-1].split(' ') for x in lf.readlines()]))
        lf.close()

    def getListOfProjectsLow(self):
        """
            get first list that is camel...
        """
        return list(self.projects)

    def getListOfProjectsHigh(self):
        """
            get second list that is CAMEL...
        """
        return list(self.PROs)


def readNum2Version(filename, m, n):
    res = {}
    vf = open(filename)
    vflines = vf.readlines()
    for x in vflines:
        if 'Index' not in x:
            text = x[:-1].split(',')
            res[text[m]] = text[n]
    vf.close()
    return res


def mkdirifnotexist(dst):
    if not os.path.exists(dst):
        os.makedirs(dst)


def pystr2stmp(strTime):
    '''
        Input: String time format is a% b% d% H:% M:%S %Y
        Output: timestamp
    '''
    structtime = time.strptime(strTime, '%a %b %d %H:%M:%S %Y')
    timestamp = time.mktime(structtime)
    return timestamp


def plstr2stmp(strtime):
    '''
        Input: The time format of the string is
        Output: timestamp
    '''
    res = pendulum.parse(strtime)
    return res.int_timestamp


def copyfile2dirifexist(file, dir):
    try:
        shutil.copy(file, dir)
        return 1
    except:
        return 0


def getTBFsBuggyLinesByOneCommit(gitroot, commithash):
    '''
    input: commit hash
    output: [TBFs]
    '''
    os.chdir(gitroot)
    cmd = 'git show '+commithash+' --name-status'
    cmdf = os.popen(cmd)
    a = cmdf.buffer.read().decode(encoding='utf-8', errors='ignore')
    # print(a)
    ModifiedFileList = a.split('\n')
    res = []
    for x in ModifiedFileList:
        if x.endswith('.java') and '\t' in x:
            res.append(x.split('\t')[1])
    os.chdir(cwd)
    return res


def readJson(JsonFilename):
    js = open(JsonFilename)
    d = js.readline()
    d = eval(d)
    return d


def clearSpace(s):
    return s.replace(' ', '').replace('\n', '').replace('\t', '').replace('\r', '').replace('\r\n', '')


def timeCompare(strTime, tagInfoFilename):
    tf = open(tagInfoFilename)
    lines = tf.readlines()
    res = []
    for x in lines:
        x = x[0:-1]
        taginfo = x.split(',')
        taginfo[1] = pystr2stmp(taginfo[1][8:-6])
        res.append(taginfo)

    res = sorted(res, key=itemgetter(1))

    AVs = []

    for x in res:
        if x[1] < strTime:
            AVs.append(x)
    return AVs
