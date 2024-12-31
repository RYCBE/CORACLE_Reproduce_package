
approch_list = [
    'Actual',
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
apr_list = [
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

# You need to download Vandehei's data here and modify it to our own path
# https://gitlab.com/Bvandehei/affectedversions
source_abs_dir = "E:/F/affectedversions-master/Datasets/RQ3/"

# You need to modify it to our own path
res_abs_dir = "E:/E/20241125/CORACLE仓库/CORACLE/RQ3/1_makecut/filted_data/cut_res/"

for apr in approch_list:
    for opened_project in apr_list:
        ofile = opened_project+'_'+apr

        open_file = source_abs_dir+ofile+'_Complete.csv'

        lf = open(open_file)
        lines = lf.readlines()

        java = 0
        res_file = ofile+'_PART.csv'
        res = []
        for x in lines[1:]:
            text = x[:-1].split(',')
            xx = text[1]
            if xx.endswith('.java') and ('test/' not in xx and 'example/' not in xx and 'tests/' not in xx and 'examples/' not in xx):
                java += 1
                if text[-1] == 'Yes':
                    res.append(x)
        lf.close()
        rf = open(res_abs_dir+ofile+'.txt', 'w')
        rf.write(str(java))
        rf.close()
        rf = open(res_abs_dir+opened_project+"/"+res_file, 'w')
        for x in res:
            rf.write(x)
        rf.close()
