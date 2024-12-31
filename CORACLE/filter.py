
import re
import os
import commit2refactoringLines
import getTBFsBuggyLinesByOneCommit
import eventlet
eventlet.monkey_patch()


def passRefactorByOneCommit(commitsha, gitroot, jsonResDir):
    """passRefactorByOneCommit

    Args:
        commitsha (string): sha
        gitroot (string): gitroot
        jsonResDir (string): targetResDir
    return:
        a set of passedFilesByRefactor
    """
    res = set()
    TBFBuggyLines = getTBFsBuggyLinesByOneCommit.getTBFsBuggyLinesByOneCommit(
        gitroot, commitsha)
    with eventlet.Timeout(180, False):
        jsonResFile = commit2refactoringLines.commit2json(
            commitsha, jsonResDir+'/'+commitsha+'.json', gitroot)
        try:
            RefactoringLines = commit2refactoringLines.getRefactoringLinesFromJson(
                jsonResFile)
        except:
            print("RefactoringMiner Error!")
            return set()
        for k, v in TBFBuggyLines.items():
            rlines = set(RefactoringLines.get(k, []))
            if set(v).issubset(set(rlines)):
                res.add(k)
        return res
    print("TimeOutError!")
    return set()


def getTBFsByOneCommit(commithash, gitroot):
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
        if x.endswith('.java') and '\t' in x and ('test/' not in x and 'example/' not in x and 'tests/' not in x and 'examples/' not in x):
            ttt = x.split('\t')
            if ttt[0] != 'A':
                res.append(x.split('\t')[1])
    return res


def passSameByOneCommit(commitsha, gitroot):
    TBFsNoFiltered = getTBFsByOneCommit(commitsha, gitroot)
    os.chdir(gitroot)
    res = set()

    tocomparea, tocompareb = {}, {}

    os.popen('git reset --hard '+commitsha).read()
    acmdf = os.popen('git log --pretty=format:\'%H\' -n 1')
    print(acmdf.buffer.read().decode(encoding='utf-8', errors='ignore'))
    for x in TBFsNoFiltered:
        if os.path.exists(gitroot+'/'+x):
            af = open(gitroot+'/'+x, encoding='utf-8', errors='ignore')
            a = ''.join(af.readlines())
            af.close()
            tocomparea[x] = a

    os.popen('git reset --hard \"HEAD^\"').read()
    bcmdf = os.popen('git log --pretty=format:\'%H\' -n 1')
    print(bcmdf.buffer.read().decode(encoding='utf-8', errors='ignore'))
    for x in TBFsNoFiltered:
        if os.path.exists(gitroot+'/'+x):
            bf = open(gitroot+'/'+x, encoding='utf-8', errors='ignore')
            b = ''.join(bf.readlines())
            bf.close()
            tocompareb[x] = b
    for k, v in tocomparea.items():
        vb = tocompareb.get(k, '')
        if vb != '':
            if cmpFileStr(v, vb):
                res.add(k)
    return set(TBFsNoFiltered)-res, res


def clearSpace(s):
    return s.strip(' ').replace('\n', '').replace('\t', '').replace('\r', '').replace('\r\n', '')


def cmpFileStr(afile, bfile):
    def sw(s):
        return not s.startswith('//')
    resa = [clearSpace(x) for x in afile.split('\n')]
    resa = filter(sw, resa)
    rresa = ''.join(list(resa))
    resb = [clearSpace(x) for x in bfile.split('\n')]
    resb = filter(sw, resb)
    rresb = ''.join(list(resb))
    a, n = re.subn(r'/\*.*?\*/', '', ''.join(rresa))
    b, n = re.subn(r'/\*.*?\*/', '', ''.join(rresb))
    a.replace(' ', '')
    b.replace(' ', '')
    return a == b


def getFiltered(commitsha, gitroot, jsonResDir):
    ps, s = passSameByOneCommit(commitsha, gitroot)
    pr = passRefactorByOneCommit(commitsha, gitroot, jsonResDir)
    return list(ps-pr), list(s), list(pr)
