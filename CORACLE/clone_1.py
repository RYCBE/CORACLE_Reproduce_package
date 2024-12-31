import utils
import os


def gitclone(lowList, dstdir):
    utils.mkdirifnotexist(dstdir)
    os.chdir(dstdir)

    for x in lowList:
        os.popen('git clone git@github.com:apache/'+x+'.git').read()


if __name__ == '__main__':
    gitclone(['pdfbox', 'wicket', 'jackrabbit', 'cxf', 'ignite',
             'myfaces', 'camel', 'karaf', 'maven', 'openmeetings'], "./sourceCode")
