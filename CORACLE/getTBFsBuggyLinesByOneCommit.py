import os

cwd = os.getcwd().replace('\\', '/')


def getTBFsBuggyLinesByOneCommit(gitroot, commithash):
    '''
    input: commit hash
    output: [TBFs]
    '''
    os.chdir(gitroot)
    cmd = 'git show '+commithash+' --pretty=medium *.java'
    cmdf = os.popen(cmd)
    a = cmdf.buffer.read().decode(encoding='utf-8', errors='ignore')

    cmd = 'git show '+commithash+' --name-status'
    cmdf = os.popen(cmd)
    b = cmdf.buffer.read().decode(encoding='utf-8', errors='ignore')
    ModifiedFileList = b.split('\n')
    resFiles = []
    for x in ModifiedFileList:
        if x.endswith('.java') and '\t' in x:
            resFiles.append(x.split('\t')[1])
    resFiles = ''.join(resFiles)

    fileList = a.split('diff --git ')[1:]
    res = {}
    for x in fileList:
        xfile = '/'.join((x.split('\n')[0]).split('/')[1:]).split(' ')[0]
        text = x.split('\n@@')
        text = text[1:]
        if xfile in resFiles:
            tmplineres = []
            for y in text:
                texty = y.split('\n')
                startline, linenum = texty[0].split(
                    '@@')[0].strip(' ').split('+')[-1].split(',')
                startline, linenum = int(startline), int(linenum)
                k = 0
                for z in texty[1:]:
                    if (z.startswith('+')):
                        tmplineres.append(startline+k)
                    k += 1
                    if z.startswith('-'):
                        k -= 1
            res[xfile] = tmplineres
    os.chdir(cwd)
    return res


if __name__ == "__main__":
    getTBFsBuggyLinesByOneCommit(
        'E:/E/20241125/sourceCode/ignite', '6e00766a20459571247fafac22e2a0cbb8d979a1')
