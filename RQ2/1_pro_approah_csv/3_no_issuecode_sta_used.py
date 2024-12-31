import json


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

p2P = dict(zip(prolist, Prolist))

approch_list = [
    'Simple',
    'Proportion_ColdStart',
    'Proportion_Increment',
    'Proportion_MovingWindow',
    'SZZ_U',
    'SZZ_B',
    'SZZ_RA',
    'Proportion_ColdStart+',
    'Proportion_Increment+',
    'Proportion_MovingWindow+',
    'SZZ_U+',
    'SZZ_B+',
    'SZZ_RA+',
    'Actual',
    # 'CORACLE',
]


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

# Simple,Proportion_ColdStart,Proportion_Increment,Proportion_MovingWindow,SZZ_U,SZZ_B,SZZ_RA,Proportion_ColdStart+,Proportion_Increment+,Proportion_MovingWindow+,SZZ_U+,SZZ_B+,SZZ_RA+,Actual,CORACLE


# {camel: {version:[yesyesyesnonono]} }
resd = {}

for pro in prolist:
    of = open("./My_data/"+p2P[pro]+"/"+p2P[pro]+"_My_VRes.csv")
    oflines = of.readlines()
    of.close()

    # Open the CORACLE tag and collect AV directly
    cf = open("../../RQ1/Sample/coracle_labels/"+pro+"final.txt")
    cflines = cf.readlines()
    coracle_avs = set([x[2:-3].split('\', \'')[0] for x in cflines])
    cf.close()

    # v2m
    van2My = readNum2Version("../../CORACLE/v2v/"+pro+"v2v.txt", 0, 1)

    resv = {}

    for line in oflines:
        elements = line[:-1].split(",")
        version = elements[4]
        oldv = resv.get(version, ["No"]*15)
        for i, approach in enumerate(approch_list):
            if elements[i+6] == "Yes":
                oldv[i] = "Yes"
        if van2My[version] in coracle_avs:
            oldv[-1] = "Yes"
        resv[version] = oldv

    resd[pro] = resv

with open('no_issue_code_av.json', 'w') as f:
    json.dump(resd, f)
