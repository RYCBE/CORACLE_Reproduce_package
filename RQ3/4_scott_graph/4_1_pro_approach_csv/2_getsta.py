
import csv
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

with open('res_sta.json', 'r') as f:
    res_sta = json.load(f)


def get_pre_recall_f1():
    for row in res_sta:
        for item in row:
            item["Precision"] = item["TP"] / \
                (item["TP"] + item["FP"]) if (item["TP"] + item["FP"]) != 0 else 0
            item["Recall"] = item["TP"] / \
                (item["TP"] + item["FN"]) if (item["TP"] + item["FN"]) != 0 else 0
            item["F1Score"] = 2 * (item["Precision"] * item["Recall"]) / (
                item["Precision"] + item["Recall"]) if (item["Precision"] + item["Recall"]) != 0 else 0
    # 输出Precision.csv
    with open('Precision.csv', 'w', newline='') as precision_csv:
        fieldnames = ["//"] + ["PC", "PC+", "PI", "PI+", "PM", "PM+",
                               "Simple", "SZZ_B", "SZZ_B+", "SZZ_RA", "SZZ_RA+", "SZZ_U", "SZZ_U+"]
        writer = csv.DictWriter(precision_csv, fieldnames=fieldnames)

        writer.writeheader()
        for i, row in enumerate(res_sta):
            precision_row = {"//": Pro_list[i]}
            for j, metric in enumerate(fieldnames[1:]):
                precision_row[metric] = row[j]["Precision"]
            writer.writerow(precision_row)

    # 输出Recall.csv
    with open('Recall.csv', 'w', newline='') as recall_csv:
        fieldnames = ["//"] + ["PC", "PC+", "PI", "PI+", "PM", "PM+",
                               "Simple", "SZZ_B", "SZZ_B+", "SZZ_RA", "SZZ_RA+", "SZZ_U", "SZZ_U+"]
        writer = csv.DictWriter(recall_csv, fieldnames=fieldnames)

        writer.writeheader()
        for i, row in enumerate(res_sta):
            recall_row = {"//": Pro_list[i]}
            for j, metric in enumerate(fieldnames[1:]):
                recall_row[metric] = row[j]["Recall"]
            writer.writerow(recall_row)

    # 输出F1Score.csv
    with open('F1Score.csv', 'w', newline='') as f1score_csv:
        fieldnames = ["//"] + ["PC", "PC+", "PI", "PI+", "PM", "PM+",
                               "Simple", "SZZ_B", "SZZ_B+", "SZZ_RA", "SZZ_RA+", "SZZ_U", "SZZ_U+"]
        writer = csv.DictWriter(f1score_csv, fieldnames=fieldnames)

        writer.writeheader()
        for i, row in enumerate(res_sta):
            f1score_row = {"//": Pro_list[i]}
            for j, metric in enumerate(fieldnames[1:]):
                f1score_row[metric] = row[j]["F1Score"]
            writer.writerow(f1score_row)


get_pre_recall_f1()
