
import json


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
# Project Key,Bug ID,Bug Order,Version ID,Version Name,Version Index,Simple,Proportion_ColdStart,Proportion_Increment,Proportion_MovingWindow,SZZ_U,SZZ_B,SZZ_RA,Proportion_ColdStart+,Proportion_Increment+,Proportion_MovingWindow+,SZZ_U+,SZZ_B+,SZZ_RA+,Actual
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

P2p = dict(zip(Pro_list, ordered_prolist))
Pindex = {}
pindex = {}
for i in range(len(ordered_prolist)):
    Pindex[Pro_list[i]] = i
    pindex[ordered_prolist[i]] = i
label_index = ["Simple", "Proportion_ColdStart", "Proportion_Increment", "Proportion_MovingWindow", "SZZ_U", "SZZ_B", "SZZ_RA",
               "Proportion_ColdStart+", "Proportion_Increment+", "Proportion_MovingWindow+", "SZZ_U+", "SZZ_B+", "SZZ_RA+", "Actual"]

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


def get_coracle_true_labels(pro):
    of = open("../../RQ1/Sample/coracle_labels/"+pro+"final.txt")
    oflines = of.readlines()
    of.close()

    oflines = set([(x[2:-3].split("\', \'")[2], x[2:-3].split("\', \'")[0])
                   for x in oflines])
    return oflines


def get_filtered_issue_code(Pro):
    of = open("../../TBFJsonDir/"+Pro+"_TBFJson.json")
    res_json = json.load(of)
    of.close

    result_keys = set()
    for key, value in res_json.items():
        all_tbf_empty = True
        for item in value:
            if item["TBFs"]:
                all_tbf_empty = False
                break
        if all_tbf_empty:
            result_keys.add(key)
    print(Pro)
    print(result_keys)
    return result_keys


def get_intersecVersions(Pro):
    of = open("../intersecVersions/"+P2p[Pro]+"insecVersions.txt")
    oflines = of.readlines()
    oflines = [x[:-1] for x in oflines]
    of.close()

    return oflines


for Pro in Pro_list:
    van2My = readNum2Version(
        '../../RQ3-Module/1_makecut/'+Pro+'/'+'v2v.txt', 0, 1)

    of = open("./Van_data/"+Pro+"VRes.csv")
    oflines = of.readlines()
    of.close()

    true_labels = get_coracle_true_labels(P2p[Pro])

    filtered_issue_code = get_filtered_issue_code(Pro)

    intersecVersions = get_intersecVersions(Pro)

    my_vres = []

    for text in oflines:
        content = text[:-1].split(',')
        bugid = content[1]

        # Filter out those without any tbf under the issue code
        if bugid in filtered_issue_code:
            continue

        # Filter out those versions that are not in the intersection version
        myv = van2My[content[4]]
        if myv not in intersecVersions:
            continue

        to_compare = (bugid, myv)

        flag = to_compare in true_labels
        content.append("Yes" if flag else "No")
        my_vres.append(",".join(content)+"\n")

        for i in range(len(label_index)):
            if i == 13:
                continue
            if content[i+6] == "Yes":
                if to_compare in true_labels:
                    res_sta[Pindex[Pro]][i]["TP"] += 1
                else:
                    res_sta[Pindex[Pro]][i]["FP"] += 1
            else:
                if to_compare in true_labels:
                    res_sta[Pindex[Pro]][i]["FN"] += 1
                else:
                    res_sta[Pindex[Pro]][i]["TN"] += 1
    outf = open("./My_data/"+Pro+"/"+Pro+"_My_VRes.csv", 'w')
    outf.writelines(my_vres)
    outf.close()


with open('res_sta.json', 'w') as f:
    json.dump(res_sta, f)
