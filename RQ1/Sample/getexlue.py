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

'''
camel 17506 26078
cxf 10614 15885
ignite 3094 6451
jackrabbit 6984 10778
karaf 3105 4105
maven 993 1428
myfaces 3218 4874
openmeetings 591 1794
pdfbox 5565 6832
wicket 8099 12424
'''

for pro in prolist:
    of = open("./coracle_labels/"+pro+"final.txt")
    oflines = of.readlines()
    of.close()

    resv = set()
    resm = set()

    for line in oflines:
        elements = line[1:-1].split("\', \'")
        resv.add((elements[0], elements[2]))
        resm.add((elements[0], elements[1]))

    print(pro, len(resv), len(resm))
