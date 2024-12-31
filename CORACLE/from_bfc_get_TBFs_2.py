# Enter Vandehei's BFCfile
# Output a Json similar to the following
'''
{
    "CAMEL-158": [
        {
            "sha": "4567tgybhbasfa8yfga0",
            "TBFs": [
                "ggg/ggg.java",
                "ggg2/ggg2.java",
            ]
        },
        {
            "sha": "safasgadnanan",
            "TBFs": [
                "ggagadhg/gggadhah.java",
                "gahddgg2/ggahahg2.java",
            ]
        }
    ],
    "CAMEL-158": [
        {
            "sha": "4567tgybhbasfa8yfga0",
            "TBFs": [
                "ggg/ggg.java",
                "ggg2/ggg2.java",
            ]
        },
        {
            "sha": "safasgadnanan",
            "TBFs": [
                "ggagadhg/gggadhah.java",
                "gahddgg2/ggahahg2.java",
            ]
        }
    ]
}
'''

import json
import os
import re

from utils import SelectedDir, cwd, sourceCodeDir, graphDir, jiraDir, linkresDir, TBFcutresDir, TagsDir

from filter import getFiltered


def from_git_get_TBFs(cwd, Lowlist, Highlist, bugFixFilesDir, JsonDir, sourceCodeDir):

    def from_bfc_get_TBFs(pro, PRO, BFCfile, Jsonfile):
        bfcf = open(BFCfile)
        bfcflines = bfcf.readlines()
        bfcf.close()

        resdict = {}

        for i in range(1, len(bfcflines)):
            bugid, bfcsha, bfcdate = bfcflines[i][:-1].split(',')
            oldv = resdict.get(bugid, [])
            TBFs, ps, pr = getFiltered(bfcsha, sourceCodeDir+pro, JsonDir)
            print(TBFs, ps, pr)
            os.chdir(cwd)

            res = {"sha": bfcsha, "TBFs": TBFs, "date": bfcdate}
            oldv.append(res)
            resdict[bugid] = oldv

        json_data = json.dumps(resdict)
        with open(Jsonfile, 'w') as file:
            file.write(json_data)

    def tag_operate(pro):
        def showTags(tagFilename):
            f = open(tagFilename)
            lines = f.readlines()
            f.close()
            for x in lines:
                x = x[0:-1]
                text = 'git show '+x+' > '+x.replace('/', '') + '.txt\n'
                os.system(text)

        def readTagInfo(tagFilename, tagInfoFileName):
            res = []
            f = open(tagFilename)
            lines = f.readlines()
            f.close()
            for x in lines:
                x = x[0:-1]
                filename = x.replace('/', '') + '.txt'
                tf = open(filename, encoding='utf-8', errors='ignore')
                tflines = tf.readlines()
                tflines = ''.join(tflines)

                a = re.search(r'(Date:)(.*)([-+]\d*)', tflines)
                b = re.search(r'(commit)(.*)(\w*)', tflines)
                if a and b:
                    date = a.group()
                    sha = b.group()
                    res.append([x, date, sha])

            rf = open(tagInfoFileName, 'w')
            for x in res:
                rf.write(','.join(x)+'\n')
            rf.close()

        def deltagInfofiles(tagTxt):
            taglist = open(tagTxt).readlines()
            for x in taglist:
                os.popen('rm '+x[:-1].replace('/', '') + '.txt').read()

        os.popen('git tag > '+TagsDir+pro+'tag.txt').read()
        tagTxt = TagsDir+pro+'tag.txt'
        tagInfo = TagsDir+pro+'tagInfo.csv'

        showTags(tagTxt)

        readTagInfo(tagTxt, tagInfo)

        deltagInfofiles(tagTxt)

    for i in range(len(Lowlist)):
        os.chdir(sourceCodeDir+Lowlist[i])
        tag_operate(Lowlist[i])
        from_bfc_get_TBFs(
            Lowlist[i], Highlist[i], bugFixFilesDir+Highlist[i]+"BugFixes.csv", JsonDir+Highlist[i]+"_TBFJson.json")
        os.chdir(cwd)
