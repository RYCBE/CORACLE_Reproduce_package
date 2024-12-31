
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
    "Simple",
    "Proportion_ColdStart",
    "Proportion_Increment",
    "Proportion_MovingWindow",
    "SZZ_U", "SZZ_B", "SZZ_RA",
    "Proportion_ColdStart+",
    "Proportion_Increment+",
    "Proportion_MovingWindow+",
    "SZZ_U+", "SZZ_B+", "SZZ_RA+"
]


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


def makeVenn(i, j, pflines, Pro):

    inter, union = 0, 0

    for x in pflines:
        text = x.split(',')
        text[-1] = text[-1][:-1]
        version = text[1]
        pro = text[0]
        if p2P[pro] != Pro:
            continue
        labels = text[2:]
        if labels[i] == labels[j] and labels[j] == labels[-1] and labels[-1] == "Yes":
            inter += 1
        if (labels[i] == labels[-1] or labels[-1] == labels[j]) and labels[-1] == "Yes":
            union += 1
    return inter, union


def genHeatmap(Pro):

    pf = open("output.csv")
    pflines = pf.readlines()[1:]
    pf.close()

    approMatrix = [[0]*13 for _ in range(13)]

    # 计算交集和总数，然后用交集部分除以总的部分
    for i in range(len(approch_list)):
        for j in range(i, len(approch_list)):
            if j == i:
                approMatrix[i][j] = approMatrix[j][i] = 1.0
                continue
            approx, approy = approch_list[i], approch_list[j]
            inter, union = makeVenn(i, j, pflines, Pro)
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
    pf = open("output.csv")
    pflines = pf.readlines()[1:]
    pf.close()
    # su = len(pflines)

    def exclue(labels, index):
        res = True
        # for i, x in enumerate(labels):
        for i in range(0, 13):
            if i == index or check_extension_relationship(approch_list[index], approch_list[i]):
                continue
            res = labels[i] != "Yes"
            if res == False:
                return res
        return res
        # key 方法，value 独特的TP
    resdict = {}

    for i in range(len(approch_list)):
        res = 0
        su = 0
        for x in pflines:
            text = x.split(',')
            text[-1] = text[-1][:-1]
            version = text[1]
            pro = text[0]
            labels = text[2:]
            if p2P[pro] != Pro:
                continue
            su += 1
            if labels[i] == labels[-1] and labels[-1] == "Yes" and exclue(labels, i):
                res += 1
        resdict[approch_list[i]] = str(res)+"/"+str(su)

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
