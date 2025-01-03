import os
import csv

# You need to modify it to our own path
base_dir = "E:/E/20241125/CORACLE_base/CORACLE/"


def readNum2Version(filename, m, n):
    res = {}
    vf = open(filename)
    vflines = vf.readlines()
    for x in vflines:
        if 'Index' not in x:
            text = x[:-1].split(',')
            res[text[m]] = text[n]
    vf.close()
    return res


def makeVenn(file1, file2, num2van, van2my, convert_flag):
    list1 = []
    with open(file1, encoding='utf-8') as f:
        f_lines = f.readlines()
        for x in f_lines:
            aa = x[:-1].split(', ')
            xx = aa[0] + ", " + aa[1]
            if not xx.endswith(")"):
                xx += ")"
            list1.append(xx)

    list2 = []
    with open(file2, encoding='utf-8') as f:
        f_lines = f.readlines()
        for x in f_lines:
            if convert_flag:
                xx = x.split(',')
                xx[0], xx[1]
                v = van2my[num2van[xx[0]]]
                if v == "XXX":
                    continue
                rr = "(\'" + v+"\', \'" + xx[1] + "\')"
            else:
                aa = x[:-1].split(', ')
                rr = aa[0] + ", " + aa[1]
                if not rr.endswith(")"):
                    rr += ")"
            list2.append(rr)

    intersec = list(set(list1) & set(list2))
    unionsec = list(set(list1) | set(list2))
    return intersec, unionsec


approch_list = [
    # 'Actual',
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


def output(inter, dir, txt):
    create_folder(dir)
    f = open(dir+'/'+txt, 'w')
    f.writelines(inter)
    f.close()


def write2csv(matrix, dir, filename):
    # 将矩阵输出到 CSV 文件
    create_folder(dir)
    with open(dir+'/'+filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([' ']+approch_list)
        for i, row in enumerate(matrix):
            writer.writerow([approch_list[i]]+row)
    print("数据已成功写入 "+filename+" 文件。")


if __name__ == '__main__':
    numofMethod = 13
    lf = open('list.txt')
    texts = lf.readlines()
    texts = [x[:-1].split(' ') for x in texts]
    lf.close()
    for pro, Pro, coraclenum in texts:
        num2van = readNum2Version(
            base_dir+"CORACLE/VanVersioncsv/"+Pro+"VersionInfo.csv", 0, 2)
        van2myv = readNum2Version(base_dir+"CORACLE/v2v/"+pro+"v2v.txt", 0, 1)
        TPlist = []
        excludeTPlist = []
        approMatrix = [[0]*numofMethod for _ in range(numofMethod)]
        # 先得出每个方法与CORACLE的交集（实际上就是TP的数量）
        for x in approch_list:
            inter, union = makeVenn(base_dir+"RQ1/Sample/coracle_labels/"+pro+"final.txt",
                                    base_dir+"RQ3/1_makecut/filted_data/cut_res/"+Pro+"/"+Pro+"_"+x+"_PART.csv",
                                    num2van, van2myv, True)
            TPlist.append(inter)
            inter = '\n'.join(inter)
            output(inter, base_dir+'RQ3/2_make_intersec_excluesive/'+Pro+'/TP_CORACLE_as_GT',
                   Pro+'_'+x+'_TP_CORACLE_as_GT.txt')
        # 计算excludeTPlist
        for i in range(len(TPlist)):
            res = set(TPlist[i])
            for j in range(len(TPlist)):
                if j == i or check_extension_relationship(approch_list[i], approch_list[j]):
                    continue
                res = res - set(TPlist[j])
            excludeTPlist.append(list(res))
        # alg, PRO, percen
        rescsv = ["algorithm,dataset_"+pro+",percentage"]
        for i, x in enumerate(excludeTPlist):
            rescsv.append(','.join([approch_list[i], str(
                len(x))+'/'+str(coraclenum), str(len(x)/int(coraclenum))]))
            x = '\n'.join(x)
            output(x, base_dir+'RQ3/2_make_intersec_excluesive/'+Pro+'/excluedTP', Pro +
                   '_'+approch_list[i]+'_excluedTP.txt')
        rescsv = '\n'.join(rescsv)
        output(rescsv, base_dir+'RQ3/2_make_intersec_excluesive/' +
               Pro+'/csvpercentage', Pro+'_percentage.csv')

        # 计算交集和总数，然后用交集部分除以总的部分
        for i in range(len(approch_list)):
            for j in range(i, len(approch_list)):
                if j == i:
                    approMatrix[i][j] = approMatrix[j][i] = 1.0
                    continue
                approx, approy = approch_list[i], approch_list[j]
                inter, union = makeVenn(base_dir+'RQ3/2_make_intersec_excluesive/'+Pro+'/TP_CORACLE_as_GT/' + Pro+'_'+approx + '_TP_CORACLE_as_GT.txt',
                                        base_dir+'RQ3/2_make_intersec_excluesive/'+Pro +
                                        '/TP_CORACLE_as_GT/' + Pro+'_'+approy + '_TP_CORACLE_as_GT.txt',
                                        None,
                                        None,
                                        False)
                approMatrix[i][j] = approMatrix[j][i] = len(inter)/len(union)
                inter = '\n'.join(inter)
                output(inter, base_dir+'RQ3/2_make_intersec_excluesive/'+Pro+'/heatmap', Pro +
                       '_'+approx+'_'+approy+'_intersec.txt')
        write2csv(approMatrix, base_dir+'RQ3/2_make_intersec_excluesive/'+Pro +
                  '/csvheatmap', Pro+'_heatmap.csv')
        a = 1
