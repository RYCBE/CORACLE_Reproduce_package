import os
import clone_1 as clone
from copy_TBFs_to_dst_3 import copy_tbf
import utils
import from_bfc_get_TBFs_2
import getNewDefectModules as gg
import _2023util_TBFcut2unionDict as t2u

from utils import FinalResDir, JsonDir, cwd, sourceCodeDir, graphDir, jiraDir, linkresDir, TBFcutresDir, TagsDir, SelectedDir, BugFixFilesDir
from utils import unionDictDir, TBFJsonDir

utils.mkdirifnotexist(sourceCodeDir)
utils.mkdirifnotexist(graphDir)
utils.mkdirifnotexist(jiraDir)
utils.mkdirifnotexist(linkresDir)
utils.mkdirifnotexist(TBFcutresDir)
utils.mkdirifnotexist(TagsDir)
utils.mkdirifnotexist(SelectedDir)
utils.mkdirifnotexist(JsonDir)
utils.mkdirifnotexist(FinalResDir)
utils.mkdirifnotexist(unionDictDir)
utils.mkdirifnotexist(TBFJsonDir)


listfile = 'list.txt'
UT = utils.utils(listfile)
Lowlist = UT.getListOfProjectsLow()
Highlist = UT.getListOfProjectsHigh()

clone.gitclone(Lowlist, sourceCodeDir)
os.chdir(cwd)

# input
# 1.Vans BFC (./bugFixFiles)
# 2.v2v
# 3.VanVersioncsv

from_bfc_get_TBFs_2.from_git_get_TBFs(
    cwd, Lowlist, Highlist, BugFixFilesDir, TBFJsonDir, sourceCodeDir)
os.chdir(cwd)

copy_tbf(cwd, Lowlist, Highlist, sourceCodeDir, TBFcutresDir)
os.chdir(cwd)

t2u.TBF2Union(Lowlist, Highlist)
os.chdir(cwd)

gg.getDefectModules(Lowlist, Highlist)
os.chdir(cwd)
