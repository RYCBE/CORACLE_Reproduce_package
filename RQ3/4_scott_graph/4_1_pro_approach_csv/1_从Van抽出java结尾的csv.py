
import csv
import json


approch_list = [
    # 'Actual',
    'Proportion_ColdStart',
    'Proportion_ColdStart+',
    'Proportion_Increment',
    'Proportion_Increment+',
    'Proportion_MovingWindow',
    'Proportion_MovingWindow+',
    'Simple',
    'SZZ_B',
    'SZZ_B+',
    'SZZ_RA',
    'SZZ_RA+',
    'SZZ_U',
    'SZZ_U+'
]

approch_index = {}
for i in range(len(approch_list)):
    approch_index[approch_list[i]] = i

Pro_list = [
    'CAMEL',
    'CXF',
    'IGNITE',
    'JCR',
    'KARAF',
    'MNG',
    'MYFACES',
    'OPENMEETINGS',
    'PDFBOX',
    'WICKET',
]

ordered_prolist = ["camel",
                   "cxf",
                   "ignite",
                   "jackrabbit",
                   "karaf",
                   "maven",
                   "myfaces",
                   "openmeetings",
                   "pdfbox",
                   "wicket"]

P2p = {}
for i in range(len(ordered_prolist)):
    P2p[Pro_list[i]] = ordered_prolist[i]

Pindex = {}
pindex = {}
for i in range(len(ordered_prolist)):
    Pindex[Pro_list[i]] = i
    pindex[ordered_prolist[i]] = i

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


def get_coracle_tp_list(pro):
    of = open("../../../RQ1/Sample/coracle_labels/"+P2p[pro]+"final.txt")
    oflines = of.readlines()
    return [x.split(', ')[0]+", "+x.split(', ')[1]+")" for x in oflines]


def label_with_coracle_GT(n2v, v2m, text, tp_labels):
    v, f, label = v2m[n2v[text[0]]], text[1], text[-1]
    converted_vf = "(\'"+v+"\', \'"+f+"\')"
    if label == "Yes":
        if converted_vf in tp_labels:
            text.append("Yes")
            return ','.join(text)+"\n", "TP"
        else:
            text.append("No")
            return ','.join(text)+"\n", "FP"
    else:
        if converted_vf in tp_labels:
            text.append("Yes")
            return ','.join(text)+"\n", "FN"
        else:
            text.append("No")
            return ','.join(text)+"\n", "TN"


res_sta = [[{"TP": 0, "FP": 0, "FN": 0, "TN": 0, "Precision": 0, "Recall": 0, "F1Score": 0},
            {"TP": 0, "FP": 0, "FN": 0, "TN": 0,
                "Precision": 0, "Recall": 0, "F1Score": 0},
            {"TP": 0, "FP": 0, "FN": 0, "TN": 0,
                "Precision": 0, "Recall": 0, "F1Score": 0},
            {"TP": 0, "FP": 0, "FN": 0, "TN": 0,
                "Precision": 0, "Recall": 0, "F1Score": 0},
            {"TP": 0, "FP": 0, "FN": 0, "TN": 0,
                "Precision": 0, "Recall": 0, "F1Score": 0},
            {"TP": 0, "FP": 0, "FN": 0, "TN": 0,
                "Precision": 0, "Recall": 0, "F1Score": 0},
            {"TP": 0, "FP": 0, "FN": 0, "TN": 0,
                "Precision": 0, "Recall": 0, "F1Score": 0},
            {"TP": 0, "FP": 0, "FN": 0, "TN": 0,
                "Precision": 0, "Recall": 0, "F1Score": 0},
            {"TP": 0, "FP": 0, "FN": 0, "TN": 0,
                "Precision": 0, "Recall": 0, "F1Score": 0},
            {"TP": 0, "FP": 0, "FN": 0, "TN": 0,
                "Precision": 0, "Recall": 0, "F1Score": 0},
            {"TP": 0, "FP": 0, "FN": 0, "TN": 0,
                "Precision": 0, "Recall": 0, "F1Score": 0},
            {"TP": 0, "FP": 0, "FN": 0, "TN": 0,
                "Precision": 0, "Recall": 0, "F1Score": 0},
            {"TP": 0, "FP": 0, "FN": 0, "TN": 0,
                "Precision": 0, "Recall": 0, "F1Score": 0},
            ] for _ in range(10)]

for Pro in Pro_list:
    num2van = readNum2Version(
        base_dir+"CORACLE/VanVersioncsv/"+Pro+"VersionInfo.csv", 0, 2)
    van2my = readNum2Version(base_dir+"CORACLE/v2v/"+P2p[Pro]+"v2v.txt", 0, 1)
    coracle_tp_list = get_coracle_tp_list(Pro)

    for apr in approch_list:
        ofile = Pro+'_'+apr

        open_file = base_dir + "Van/" + Pro + '/' + ofile+'_Complete.csv'

        lf = open(open_file)
        lines = lf.readlines()
        lf.close()
        res_file = './' + Pro + '/' + ofile+'_JAVA_PART.csv'
        res = []
        for x in lines[1:]:
            text = x[:-1].split(',')
            if text[1].endswith('.java') and ('test/' not in text[1]) and ('tests/' not in text[1]) \
                    and ('example/' not in text[1]) and ('examples/' not in text[1]):
                append_new_label_text, tp_tn_fp_fn = label_with_coracle_GT(num2van, van2my,
                                                                           text, coracle_tp_list)
                res_sta[Pindex[Pro]
                        ][approch_index[apr]][tp_tn_fp_fn] += 1
                res.append(append_new_label_text)

        rf = open(res_file, 'w')
        for x in res:
            rf.write(x)
        rf.close()

with open('res_sta.json', 'w') as f:
    json.dump(res_sta, f)
