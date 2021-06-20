import codecs
import sys

pathtomy = sys.argv[1]#"dictionariesEnglishOld/Romance/English-Romanian.txt"#"dictionariesEnglishOld/North-Germanic/English-Swedish.txt"
pathtomuse = sys.argv[2]#"MUSEComparison/en-sw.txt"

setmuse = set()
setmy = set()

with codecs.open(pathtomuse,"r","utf-8") as f:
    for line in f:
        setmuse.add(tuple(line.strip().split(" ")))
        
with codecs.open(pathtomy,"r","utf-8") as f:
    for line in f:
        w1,w2 = line.strip().split("\t")[:-1]
        setmy.add(tuple((w1.lower(),w2.lower())))
        

x = setmy.intersection(setmuse)
print(len(x))
#for tupel in x:
    #print(tupel)

