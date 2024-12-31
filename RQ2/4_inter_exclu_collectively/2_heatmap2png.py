import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


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
Pp2P = dict(zip(Pp, Prolist))


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

proPRO = [
    "Camel_AVheatmap.csv",
    "CXF_AVheatmap.csv",
    "Ignite_AVheatmap.csv",
    "Jackrabbit_AVheatmap.csv",
    "Karaf_AVheatmap.csv",
    "Maven_AVheatmap.csv",
    "MyFaces_AVheatmap.csv",
    "OpenMeetings_AVheatmap.csv",
    "PDFBox_AVheatmap.csv",
    "Wicket_AVheatmap.csv",
]

proPRO2 = [
    ("Camel_AVheatmap.csv", "CXF_AVheatmap.csv"),
    ("Ignite_AVheatmap.csv", "Jackrabbit_AVheatmap.csv"),
    ("Karaf_AVheatmap.csv", "Maven_AVheatmap.csv"),
    ("MyFaces_AVheatmap.csv", "OpenMeetings_AVheatmap.csv"),
    ("PDFBox_AVheatmap.csv", "Wicket_AVheatmap.csv"),
]

desired_order = [
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


def absf2matrix(absf):
    df = pd.read_csv(absf, index_col=0)
    df = df[desired_order]
    df = df.loc[desired_order]
    # df = df.drop(df.columns[0], axis=1)
    labels_x = df.columns

    labels_xx = []
    for x in labels_x:
        if x.startswith("P") and x.endswith("+"):
            continue
        labels_xx.append(ld[x])
    labels_x = labels_xx
    labels_y = labels_x

    # 将数据转换为Numpy数组
    matrix1 = df.values
    return matrix1, labels_x, labels_y


def first():
    def twofile(filename1, filename2, absf1, absf2):
        # 读取CSV文件
        matrix1, labels_x, labels_y = absf2matrix(absf1)

        # 读取CSV文件
        matrix2, _, _ = absf2matrix(absf2)

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
        plt.title(filename1[:-4].split("_")[0], fontsize=21, pad=10)
        plt.ylabel(filename2[:-4].split("_")[0], fontsize=21, labelpad=5)

        plt.tight_layout()
        plt.savefig("./figres/" +
                    filename1[:-4]+"_"+filename2[:-4]+".png", dpi=300)

    for x in proPRO2:
        a = Pp2P[x[0].split("_")[0]]
        b = Pp2P[x[1].split("_")[0]]
        twofile(x[0], x[1], "./"+a+"/csvAVheatmap/" +
                x[0], "./"+b+"/csvAVheatmap/"+x[1])


first()
