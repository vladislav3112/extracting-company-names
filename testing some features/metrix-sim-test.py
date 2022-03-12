import distance
import csv
from os import write
from pyjarowinkler import distance

strarr1 = []
strarr2 = []
with open('matching-results-bert.txt', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    for row in reader:
        str = row[0]
        str = str.split('\t')
        s1 = str[0]
        s2 = str[1]
        metrix = float(str[3])
        if(metrix < 1.0):
            strarr1.append(s1)
            strarr2.append(s2)
    for i in range(len(strarr1)):
        s1 = strarr1[i]
        s2 = strarr2[i]
        #distance.get_jaro_distance("hello", "haloa", winkler=True, scaling=0.1)
        print(i,' | ',distance.get_jaro_distance(s1, s2, winkler=True, scaling=0.1),s1,' ',s2)        