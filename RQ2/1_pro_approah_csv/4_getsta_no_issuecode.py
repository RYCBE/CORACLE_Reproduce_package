import json

prolist = ["camel",
           "cxf",
           "ignite",
           "jackrabbit",
           "karaf",
           "maven",
           "myfaces",
           "openmeetings",
           "pdfbox",
           "wicket"]

p2i = dict([(x, i) for i, x in enumerate(prolist)])


def calculate_metrics(results):
    """
    Calculate TP, FP, FN, TN indicators based on the result list
    """
    tp = 0
    fp = 0
    fn = 0
    tn = 0
    if results[-1] == "Yes":
        for r in results[:-1]:
            if r == "Yes":
                tp += 1
            else:
                fn += 1
    else:
        for r in results[:-1]:
            if r == "Yes":
                fp += 1
            else:
                tn += 1
    return {"TP": tp, "FP": fp, "FN": fn, "TN": tn}


def process_data(data, ifcoracle):
    """
    Process the entire data and construct results in a two-dimensional table format
    """
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

    for k, v in data.items():
        for version, labels in v.items():
            if ifcoracle:
                gtlabel = labels[-1]
            else:
                gtlabel = labels[-2]
            ik = p2i[k]
            for i, x in enumerate(labels[:-2]):
                if x == "Yes":
                    if gtlabel == "Yes":
                        res_sta[ik][i]["TP"] += 1
                    else:
                        res_sta[ik][i]["FP"] += 1
                else:
                    if gtlabel == "Yes":
                        res_sta[ik][i]["FN"] += 1
                    else:
                        res_sta[ik][i]["TN"] += 1
    return res_sta


if __name__ == "__main__":
    with open("no_issue_code_av.json", "r") as f:
        data = json.load(f)
    result_table = process_data(data, True)
    with open('res_sta_no_issuecode_coracle.json', 'w') as f:
        json.dump(result_table, f)

    result_table = process_data(data, False)
    with open('res_sta_no_issuecode_actual.json', 'w') as f:
        json.dump(result_table, f)
