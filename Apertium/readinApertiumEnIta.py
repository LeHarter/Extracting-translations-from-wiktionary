import re
import codecs

grouppattern = re.compile("          group(.*)")
wort1pattern = re.compile("<l>(.*?)</l>")
wort2pattern = re.compile("<r>(.*?)</r>")
pospattern = re.compile("<par n=\"(.*?)\"/>")

wort1pattern2 = re.compile("<l>(.*?)<s")
wort2pattern2 = re.compile("<r>(.*?)<s")

qpattern = re.compile("<s n=\".+?\"/>")


file = "apertium-eng-ita.eng-ita.dix"
file2 = "English-Italian-wiktionaries.txt"
nomen = "__n"
verb = "vb"
adj = "adj"
adv = "\"adv\""

pos = None 
sectionTest = False

#with codecs.open("hilf.txt","w","utf-8") as hilf:
    #pass
apartiumdict = {"n":set(),"v":set(),"adj":set(),"adv":set()}
overlapdict = {"n":0,"v":0,"adj":0,"adv":0}
posdict = {"Noun":"n","v":0,"Adjective":"adj","Adverb":"adv","Verb":"v"}

with codecs.open(file,"r","utf-8") as data:
    with codecs.open("Apertium-en-it_readable.txt","w","utf-8") as new:
        for line in data:
            if "<e" in line:
                if pos:
                    if pospattern.search(line):
                        l = wort1pattern.search(line)
                        r = wort2pattern.search(line)
                    else:
                        l = wort1pattern2.search(line)
                        r = wort2pattern2.search(line)
                    if l and r:
                        left = l.group(1).replace("<b/>"," ").replace("<g>"," ").replace("</g>","").replace("<s n=\"num\"/>","").replace("<s n=\"sp\"/>","")
                        right = r.group(1).replace("<b/>"," ").replace("<g>"," ").replace("</g>","")
                        for x in qpattern.findall(left):                           
                            left = left.replace(x,"")
                        for x in qpattern.findall(right):
                            right = right.replace(x,"")
                        #right = qpattern.sub("", right)
                        pair = (left,right)
                        if pos in ["adj_symbol","adjant_symbol"]:
                            apartiumdict["adj"].add(pair)
                        elif pos in ["adv_symbol","cnjadv_symbol","pre_adv"]:
                            apartiumdict["adv"].add(pair)
                        elif pos in ["vblex_symbol","vbmod_symbol"]:
                            apartiumdict["v"].add(pair)
                        elif pos in ["n_symbol","np_symbol"]:
                            apartiumdict["n"].add(pair)
                        else:
                            pass
                        #if pos == "pr_symbol":
                            #print(left,right)
                        new.write(left+"\t"+right+"\n")
            else:
                if line == "</section>":
                    sectionTest = True
                    pos = None
                else:
                    if not sectionTest:
                        x = grouppattern.match(line)
                        #with codecs.open("hilf.txt","a","utf-8") as hilf:
                            #hilf.write(line)
                        if x:
                            pos = x.group(1).strip()
                            #print(pos)

with codecs.open(file2,"r","utf-8") as wiki:
    for line in wiki:
        e,c,p = line.strip().split("\t")
        p = posdict[p]
        pair = (e,c)
        if pair in apartiumdict[p]:
            overlapdict[p]+=1
         

for key in apartiumdict:
    print(key,len(apartiumdict[key]))
print("\n")
for key in overlapdict:
    print(key,overlapdict[key])
