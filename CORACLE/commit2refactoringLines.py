import json
import os
from utils import mkdirifnotexist


def commit2json(commitsha, json, gitroot):
    '''
        RefactoringMiner -c <git-repo-folder> <commit-sha1> -json <path-to-json-file>      
    '''
    mkdirifnotexist('/'.join(json.split('/')[:-1]))
    cmd = 'RefactoringMiner -c ' + gitroot + ' ' + commitsha + ' -json '+json
    os.popen(cmd).read()
    return json


def getRefactoringLinesFromJson(jsonPath):
    """input a json file, output a dict{ key: filename, value: lines}

    Args:
        jsonPath (_type_): _description_
        res (dict) 
    """
    jf = open(jsonPath)
    try:
        txt = json.load(jf)
    except:
        return dict()

    res = {}

    for refactor in txt['commits'][0]['refactorings']:
        rightSide = refactor['rightSideLocations']
        if rightSide:
            for rr in rightSide:

                xfile = rr['filePath']
                tmpres = list(range(rr['startLine'], rr['endLine']+1))
                oldv = res.get(xfile, [])
                oldv.extend(tmpres)
                res[xfile] = oldv
    jf.close()
    return res
