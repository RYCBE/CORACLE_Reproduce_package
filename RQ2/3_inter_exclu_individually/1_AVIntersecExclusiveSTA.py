
import csv
import os


prolist = [
    "camel",
    "cxf",
    "ignite",
    "jackrabbit",
    "karaf",
    "maven",
    "myfaces",
    "openmeetings",
    "pdfbox",
    "wicket",
]

Prolist = [
    "CAMEL",
    "CXF",
    "IGNITE",
    "JCR",
    "KARAF",
    "MNG",
    "MYFACES",
    "OPENMEETINGS",
    "PDFBOX",
    "WICKET",
]

ProSum = {
    "CAMEL": 17506,
    "CXF": 10614,
    "IGNITE": 3094,
    "JCR": 6984,
    "KARAF": 3105,
    "MNG": 993,
    "MYFACES": 3218,
    "OPENMEETINGS": 591,
    "PDFBOX": 5565,
    "WICKET": 8099,
}

Pp = [
    "Camel",
    "CXF",
    "Ignite",
    "Jackrabbit",
    "Karaf",
    "Maven",
    "MyFaces",
    "OpenMeetings",
    "PDFBox",
    "Wicket",
]
P2Pp = dict(zip(Prolist, Pp))

p2P = dict(zip(prolist, Prolist))


approch_list = [
    'Proportion_ColdStart',
    'Proportion_ColdStart+',
    'Proportion_Increment',
    'Proportion_Increment+',
    'Proportion_MovingWindow',
    'Proportion_MovingWindow+',
    'SZZ_B',
    'SZZ_B+',
    'SZZ_RA',
    'SZZ_RA+',
    'SZZ_U',
    'SZZ_U+',
    'Simple'
]
# Simple,Proportion_ColdStart,Proportion_Increment,Proportion_MovingWindow,SZZ_U,SZZ_B,SZZ_RA,Proportion_ColdStart+,Proportion_Increment+,Proportion_MovingWindow+,SZZ_U+,SZZ_B+,SZZ_RA+,Actual

labelmap = {
    1: 0,
    2: 2,
    3: 4,
    4: 10,
    5: 6,
    6: 8,
    7: 1,
    8: 3,
    9: 5,
    10: 11,
    11: 7,
    12: 9,
    0: 12
}

flipped_labelmap = {v: k for k, v in labelmap.items()}


def create_folder(folder_path):
    """
    创建指定的文件夹，如果路径已存在则不创建。

    Args:
        folder_path (str): 要创建的文件夹路径。
    """
    if not os.path.exists(folder_path):
        try:
            os.makedirs(folder_path)
            print(f"成功创建文件夹: {folder_path}")
        except OSError as e:
            print(f"创建文件夹 {folder_path} 失败: {e}")
    else:
        print(f"文件夹 {folder_path} 已存在，无需创建。")


def write2csv(matrix, dir, filename):
    # 将矩阵输出到 CSV 文件
    create_folder(dir)
    with open(dir+'/'+filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([' ']+approch_list)
        for i, row in enumerate(matrix):
            writer.writerow([approch_list[i]]+row)
    print("数据已成功写入 "+filename+" 文件。")


def makeVenn(i, j, pflines):

    inter, union = 0, 0

    for x in pflines:
        text = x.split(',')
        text[-1] = text[-1][:-1]
        BugId = text[1]
        version = text[4]
        labels = text[6:]
        if labels[flipped_labelmap[i]] == labels[flipped_labelmap[j]] and labels[flipped_labelmap[j]] == labels[-1] and labels[-1] == "Yes":
            inter += 1
        if (labels[flipped_labelmap[i]] == labels[-1] or labels[-1] == labels[flipped_labelmap[j]]) and labels[-1] == "Yes":
            union += 1
    return inter, union


def genHeatmap(Pro):

    pf = open("../1_pro_approah_csv/My_data/"+Pro+"/"+Pro+"_My_VRes.csv")
    pflines = pf.readlines()

    approMatrix = [[0]*13 for _ in range(13)]

    # 计算交集和总数，然后用交集部分除以总的部分
    for i in range(len(approch_list)):
        for j in range(i, len(approch_list)):
            if j == i:
                approMatrix[i][j] = approMatrix[j][i] = 1.0
                continue
            approx, approy = approch_list[i], approch_list[j]
            inter, union = makeVenn(i, j, pflines)
            approMatrix[i][j] = approMatrix[j][i] = inter/union
    write2csv(approMatrix, './'+Pro +
              '/csvAVheatmap', P2Pp[Pro]+'_AVheatmap.csv')


def check_extension_relationship(approach1, approach2):
    """
    检查两个元素是否存在扩展关系。
    扩展关系定义为: A 与 B 有扩展关系等价于 A = B + '+' 或 B = A + '+'.

    参数:
    approach1 (str): 第一个元素
    approach2 (str): 第二个元素

    返回:
    bool: 如果存在扩展关系,返回 True,否则返回 False
    """
    if approach1.endswith('+') and approach2 == approach1[:-1]:
        return True
    elif approach2.endswith('+') and approach1 == approach2[:-1]:
        return True
    else:
        return False


def genExcluesive(Pro):
    pf = open("../1_pro_approah_csv/My_data/"+Pro+"/"+Pro+"_My_VRes.csv")
    pflines = pf.readlines()

    def exclue(labels, index):
        newi = flipped_labelmap[index]
        res = True
        # for i, x in enumerate(labels):
        for i in range(0, 13):
            if i == newi or check_extension_relationship(approch_list[index], approch_list[labelmap[i]]):
                continue
            res = labels[i] != "Yes"
            if res == False:
                return res
        return res
        # key 方法，value 独特的TP
    resdict = {}

    for i in range(len(approch_list)):
        res = 0
        for x in pflines:
            text = x.split(',')
            text[-1] = text[-1][:-1]
            BugId = text[1]
            version = text[4]
            labels = text[6:]
            if labels[flipped_labelmap[i]] == labels[-1] and labels[-1] == "Yes" and exclue(labels, i):
                res += 1
        resdict[approch_list[i]] = str(res)+"/"+str(ProSum[Pro])

    create_folder('./'+Pro + "/exclusiveRes")
    of = open('./'+Pro + "/exclusiveRes/" +
              Pro + "_exclusiveRes.csv", 'w')
    for key, value in resdict.items():
        of.write(str(key)+","+str(value)+"\n")
    of.close()


if __name__ == '__main__':
    for x in prolist:
        xx = p2P[x]
        genHeatmap(xx)
        genExcluesive(xx)
