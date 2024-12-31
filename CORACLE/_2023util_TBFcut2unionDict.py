# by 522022330050 RYCBE 952713875@qq.com
# python 3.9.2


import re
import os
import unionFindSet as uf
from utils import SelectedDir, copyfile2dirifexist, mkdirifnotexist, pystr2stmp, unionDictDir
from utils import cwd, sourceCodeDir, graphDir, jiraDir, linkresDir, TBFcutresDir, TagsDir, clearSpace


def TBF2Union(listfilelow, listfilehigh):
    for x, y in zip(listfilelow, listfilehigh):
        if not os.path.exists(unionDictDir+x+'unionDict.txt'):
            os.chdir(sourceCodeDir+x)
            _2023util_TBFcut2unionDict(x, y)
            os.chdir(sourceCodeDir)


def _2023util_TBFcut2unionDict(projectName, PRONAME):

    def cmpFile(oldFile, newFile):
        with open(oldFile, encoding='utf-8', errors='ignore') as of:
            res = []
            lines = of.readlines()
            for x in lines:
                s = clearSpace(x)
                if s.startswith('//'):
                    pass
                else:
                    res.append(s)
            a, number = re.subn(r'/\*.*?\*/', '', ''.join(res))
        with open(newFile, encoding='utf-8', errors='ignore') as of:
            res = []
            lines = of.readlines()
            for x in lines:
                s = clearSpace(x)
                if s.startswith('//'):
                    pass
                else:
                    res.append(s)
            b, number = re.subn(r'/\*.*?\*/', '', ''.join(res))
        return a == b

    TBFsum = TBFcutresDir+projectName+'TBFsumCut.txt'
    tagTxt = TagsDir+projectName+'tag.txt'

    ijfile = graphDir+projectName+'ijfile.txt'
    unionDictOut = unionDictDir+projectName+'unionDict.txt'

    oldVersionDirPre = SelectedDir+projectName
    newVersionDirPre = SelectedDir+projectName

    allTagList = [x[0:-1].replace('/', '') for x in open(tagTxt).readlines()]
    open(tagTxt).close()
    TBFsumList = [x[0:-1].split('/')[-1] for x in open(TBFsum).readlines()]
    fullTBFsumList = [x[0:-1] for x in open(TBFsum).readlines()]
    TBFsumDict = {}
    for i, x in enumerate(fullTBFsumList):
        TBFsumDict.setdefault(x, i)
    open(TBFsum).close()
    preFixTBFsumList = [str(i)+'-'+x for i, x in enumerate(TBFsumList)]
    allUnionSetList = [uf.UnionFindSet(allTagList)
                       for i in range(len(TBFsumList))]

    # cmpVersion will change the content of allUnionSetList
    def cmpVersion(oldVersion, newVersion, NNCFs):
        oldVersionDir = oldVersionDirPre+'/'+oldVersion+'/'
        newVersionDir = newVersionDirPre+'/'+newVersion+'/'

        oldfileset = set(os.listdir(oldVersionDir))
        newfileset = set(os.listdir(newVersionDir))

        fileList = sorted(list((newfileset & oldfileset) - set(NNCFs)))

        for file in fileList:
            flag = cmpFile(oldVersionDir+file, newVersionDir+file)
            if flag:
                print(file, ': same')
                prefixFilename = int(file.split('-')[0])
                allUnionSetList[prefixFilename].union(oldVersion, newVersion)
            else:
                print(file, ': not same')

    def getNoNeedToComparedFiles(unionSetList, oldVersionName, newVersionName):
        res = []
        for i, x in enumerate(unionSetList):
            if x.is_same_set(oldVersionName, newVersionName):
                res.append(preFixTBFsumList[i])
        return res

    def cmpAllVersions():
        for i, old in enumerate(allTagList):
            for j in range(i, len(allTagList)):
                if i == j:
                    pass
                else:
                    oldVersionName = old
                    newVersionName = allTagList[j]
                    with open(ijfile, 'a') as ijf:
                        ijf.write(str(i)+','+str(j)+'\n')

                    NNCFs = getNoNeedToComparedFiles(
                        allUnionSetList, oldVersionName, newVersionName)

                    cmpVersion(oldVersionName, newVersionName, NNCFs)
        ufhandler = open(unionDictOut, 'w')
        for x in allUnionSetList:
            ufhandler.write(str(x)+'\n')
        ufhandler.close()

    cmpAllVersions()
