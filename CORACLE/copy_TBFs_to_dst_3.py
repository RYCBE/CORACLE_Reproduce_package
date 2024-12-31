import json
import os
from utils import SelectedDir, copyfile2dirifexist, cwd, mkdirifnotexist, sourceCodeDir, TagsDir, TBFJsonDir, TBFcutresDir


def get_TBF_sum_from_TBFJson(pro, TBFJson, TBFcutDir):
    jf = open(TBFJson)
    input_data = json.load(jf)
    tbf_list = []
    for key in input_data:
        for item in input_data[key]:
            tbf_list.extend(item["TBFs"])
    jf.close()
    TBFsumLines = sorted(list(set(tbf_list)))

    # Output to TBFcut folder
    tf = open(TBFcutDir+pro+"TBFsumCut.txt", 'w')
    tf.write('\n'.join(TBFsumLines)+'\n')
    tf.close()

    return TBFsumLines


def copy_tbf(cwd, Lowlist, Highlist, sourceCodeDir, TBFcutDir):
    def copySrcFilesToDst(pro, tagInfo, TBFJson, dst):
        taglines = open(tagInfo).readlines()
        TBFsumLines = get_TBF_sum_from_TBFJson(pro, TBFJson, TBFcutDir)
        for x in taglines:
            text = x[0:-1].split(',')
            folderName = text[0].replace('/', '')
            mkdirifnotexist(dst+'/'+folderName)

            commitsha = text[2][7:]
            if len(commitsha) != 40:
                continue
            os.popen('git checkout -f '+commitsha).read()
            for j, y in enumerate(TBFsumLines):
                relfilename = y.split('/')[-1]
                if copyfile2dirifexist(y, dst+'/'+folderName):
                    os.rename(dst+'/'+folderName+'/'+relfilename, dst + '/' +
                              folderName+'/'+str(j)+'-'+relfilename)
        return

    for i in range(len(Lowlist)):
        os.chdir(sourceCodeDir+Lowlist[i])
        tagInfo = TagsDir+Lowlist[i]+'tagInfo.csv'
        copySrcFilesToDst(Lowlist[i],
                          tagInfo, TBFJsonDir+Highlist[i]+"_TBFJson.json", SelectedDir+Lowlist[i])
        os.chdir(cwd)


if __name__ == '__main__':
    a = get_TBF_sum_from_TBFJson("E:/E/20241125/old_JsonDir/CXF_TBFJson.json")
    copy_tbf("E:/E/20241125",
             ["openmeetings"], ["OPENMEETINGS"], "E:/E/20241125/sourceCode/", "E:/E/20241125/TBFCuts/")
