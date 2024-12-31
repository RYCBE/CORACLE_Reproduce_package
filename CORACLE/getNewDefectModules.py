import json
import time
import pendulum
from operator import itemgetter
import os
import sys
import unionFindSet as uf
import utils as gen

# Input: this script file, git repository, version conversion requires Unionfindset.exe
# TBFSumcut.txt (old version is TBFSum. txt) uninDict.txt
# taginfo  tag.txt
# VansVersionInfo.csv
# Vandehei's BFC.csv and adjust it in the parameters of the startup file

from utils import FinalResDir, JsonDir, BugFixFilesDir, VanVersioncsvDir, copyfile2dirifexist, mkdirifnotexist, plstr2stmp, pystr2stmp, unionDictDir
from utils import cwd, sourceCodeDir, graphDir, v2vDir, TBFJsonDir, TBFcutresDir, TagsDir, clearSpace


def getDefectModules(listfilelow, listfilehigh):
    for x, y in zip(listfilelow, listfilehigh):
        if not os.path.exists(FinalResDir+x+'final.txt'):
            os.chdir(sourceCodeDir+x)
            _2023util_getDefectModules(x, y)
            os.chdir(sourceCodeDir)


def _2023util_getDefectModules(lowPro, highPro):
    v2vtxt = v2vDir+lowPro+'v2v.txt'

    van2My = gen.readNum2Version(v2vtxt, 0, 1)
    my2Van = gen.readNum2Version(v2vtxt, 1, 0)
    myVersion2Commit = gen.readNum2Version(
        TagsDir+lowPro+'tagInfo.csv', 0, 2)

    def timeCompare(stmp, tagInfoFilename):
        """
            input: RYCBE's Tag (git tag is not accurate)
        """
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
            if x[1] < stmp:
                AVs.append(x)
        return AVs

    def getVersionCommitDict(VanVersion):
        """
            input: Vandehei's Tag
        """

        res = van2My[VanVersion]

        return myVersion2Commit[res]

    def newTimeCompreWithVanTag(stmp, tagInfoFilename):
        """
            input: Vandehei's Tag
        """
        tf = open(tagInfoFilename)
        lines = tf.readlines()
        res = []

        for x in lines[1:]:
            x = x[0:-1]
            taginfo = x.split(',')
            taginfo[3] = plstr2stmp(taginfo[3])
            text1 = van2My[taginfo[2]]
            if text1 == "XXX":
                continue
            res.append([text1, taginfo[3], getVersionCommitDict(taginfo[2])])

        res = sorted(res, key=itemgetter(1))
        AVs = []
        for x in res:
            if x[1] < stmp:
                AVs.append(x)
        return AVs

    def getTBFListandTBFdict(TBFsumtxt):
        '''
        input : filename of TBFsum
        output: 
        '''
        tf = open(TBFsumtxt)
        tflines = tf.readlines()
        TBFsumList = [x[0:-1].split('/')[-1] for x in tflines]
        fullTBFsumList = [x[0:-1] for x in tflines]
        TBFsumDict = {}
        for i, x in enumerate(fullTBFsumList):
            TBFsumDict.setdefault(x, i)
        tf.close()
        return TBFsumList, fullTBFsumList, TBFsumDict

    def getUnionFindDict(UnionList, TBFcutfilename):
        ufh = open(UnionList)
        text = ufh.readlines()
        for i, x in enumerate(text):
            text[i] = eval(x)
        tgf = open(TagsDir+lowPro+'tag.txt')
        allTagList = [x[0:-1].replace('/', '') for x in tgf.readlines()]
        tgf.close()
        tbf = open(TBFcutfilename)
        TBFsumList = [x[0:-1].split('/')[-1] for x in tbf.readlines()]
        tbf.close()
        allUnionSetList = [uf.UnionFindSet(allTagList)
                           for i in range(len(TBFsumList))]
        if not text:
            return allUnionSetList
        for i, x in enumerate(allUnionSetList):
            allUnionSetList[i].father_dict = text[i]
        ufh.close()
        return allUnionSetList

    def getnewFinal(TBFsumtxt, uniondicttxt, taginfocsv, outputFile):
        # outputFile = 'final_BFCsame.txt'
        # resTBF = set()
        TBFSumList, fullTBFSumList, TBFSumDict = getTBFListandTBFdict(
            TBFsumtxt)
        with open(TBFJsonDir+highPro+"_TBFJson.json") as rf:
            res_dict = json.load(rf)
        unionDictList = getUnionFindDict(uniondicttxt, TBFsumtxt)
        # bfcf = open(BugFixFilesDir+highPro+'BugFixes.csv')
        # bfcflines = bfcf.readlines()
        resDictList = {}

        for k, v in res_dict.items():
            for x in v:
                TBFs = x.get("TBFs", [])
                TBVs = []
                if taginfocsv == TagsDir+lowPro+'tagInfo.csv':
                    TBVs = timeCompare(plstr2stmp(x["date"]), taginfocsv)
                elif taginfocsv == VanVersioncsvDir+highPro+'VersionInfo.csv':
                    TBVs = newTimeCompreWithVanTag(
                        plstr2stmp(x["date"]), taginfocsv)

                if not TBVs:
                    continue
                stdBuggyVersion = TBVs[-1][0].replace('/', '')
                for j, y in enumerate(reversed(TBVs)):
                    versionName = y[0].replace('/', '')
                    if j == 0:
                        for z in TBFs:
                            resDictList.setdefault(
                                (versionName, z, k, x["sha"]), True)
                            # print('fbuggy '+str(z))
                    else:
                        for z in TBFs:
                            if unionDictList[TBFSumDict[z]].is_same_set(versionName, stdBuggyVersion):
                                resDictList.setdefault(
                                    (versionName, z, k, x["sha"]), True)
                                # print('buggy '+str(z))

        of = open(outputFile, 'w')
        for x in list(resDictList):
            of.write(str(x)+'\n')
        of.close()
        return unionDictList

    getnewFinal(TBFcutresDir+lowPro+'TBFsumCut.txt', unionDictDir+lowPro+'unionDict.txt',
                VanVersioncsvDir+highPro+'VersionInfo.csv', FinalResDir+lowPro+'final.txt')
