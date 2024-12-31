import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


ld = {
    "Proportion_ColdStart": "PC",
    "Proportion_ColdStart+": "PC+",
    "Proportion_Increment": "PI",
    "Proportion_Increment+": "PI+",
    "Proportion_MovingWindow": "PM",
    "Proportion_MovingWindow+": "PM+",
    "SZZ_B": "SZZ_B",
    "SZZ_B+": "SZZ_B+",
    "SZZ_RA": "SZZ_RA",
    "SZZ_RA+": "SZZ_RA+",
    "SZZ_U": "SZZ_U",
    "SZZ_U+": "SZZ_U+",
    "Simple": "Simple"
}


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
    "wicket"
]

PROLIST = [
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

ProLIST = [
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


proPRO = {}
proPro = {}
for i in range(len(prolist)):
    proPRO[prolist[i]] = PROLIST[i]
    proPro[prolist[i]] = ProLIST[i]


proPRO2 = [
    ("camel", "cxf"),
    ("ignite", "jackrabbit"),
    ("karaf", "maven"),
    ("myfaces", "openmeetings"),
    ("pdfbox", "wicket"),
]

heatmap_dir = "../2_make_intersec_excluesive/"


def first():
    def twofile(pro1, pro2, Pro1, Pro2):
        # 读取CSV文件
        df = pd.read_csv(pro1)
        labels_x = df.columns[1:]

        labels_xx = []
        for x in labels_x:
            if x.startswith("P") and x.endswith("+"):
                continue
            labels_xx.append(ld[x])
        labels_x = labels_xx
        labels_y = labels_x

        df = df.iloc[:, 1:]
        # 将数据转换为Numpy数组
        matrix1 = df.values

        # 读取CSV文件
        df = pd.read_csv(pro2)
        labels_x = df.columns[1:]
        labels_xx = []
        for x in labels_x:
            if x.startswith("P") and x.endswith("+"):
                continue
            labels_xx.append(ld[x])
        labels_x = labels_xx
        labels_y = labels_x

        df = df.iloc[:, 1:]
        # 将数据转换为Numpy数组
        matrix2 = df.values

        # 创建合并矩阵
        combined_matrix = np.zeros((13, 13))

        # 填充上三角为图 A 的数据
        for i in range(0, 13):
            for j in range(i+1, 13):
                combined_matrix[i, j] = matrix1[i, j]

        # 填充下三角为图 B 的数据
        for i in range(0, 13):
            for j in range(0, i):
                combined_matrix[i, j] = matrix2[i, j]

        combined_matrix = np.delete(combined_matrix, [1, 3, 5], axis=1)
        combined_matrix = np.delete(combined_matrix, [1, 3, 5], axis=0)

        combined_matrix[np.diag_indices_from(combined_matrix)] = np.nan

        # 绘制热力图
        plt.figure(figsize=(10, 9))
        ax = sns.heatmap(combined_matrix, annot=True, cmap='Blues',
                         xticklabels=labels_x, yticklabels=labels_y, cbar=True, annot_kws={"size": 15})

        for _, spine in ax.spines.items():
            spine.set_visible(True)
            spine.set_linewidth(2)
            spine.set_edgecolor('grey')

        # 调整轴标签文字方向
        ax.set_xticklabels(ax.get_xticklabels(), rotation=90,
                           ha='right', fontdict={"size": 15})
        ax.set_yticklabels(ax.get_yticklabels(), rotation=0,
                           fontdict={"size": 15})

        # 调整颜色条字体大小
        cbar = ax.collections[0].colorbar
        cbar.ax.tick_params(labelsize=15)

        # plt.show()
        plt.title(Pro1, fontsize=21, pad=10)
        plt.ylabel(Pro2, fontsize=21, labelpad=5)

        plt.tight_layout()
        plt.savefig("./twoinone/" +
                    Pro1+"_"+Pro2+".png", dpi=300)

    for x in proPRO2:
        a = heatmap_dir+proPRO[x[0]]+"/csvheatmap/"+proPRO[x[0]]+"_heatmap.csv"
        b = heatmap_dir+proPRO[x[1]]+"/csvheatmap/"+proPRO[x[1]]+"_heatmap.csv"
        twofile(a, b, proPro[x[0]], proPro[x[1]])


first()
