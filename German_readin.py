import xml.etree.ElementTree as ET
from collections import defaultdict
import re
import json
import codecs
import sys

TEST = ["Kartoffel","Handy","Sonne","Weihnachtsmann","Aufnahme","legen","Ausfahrt","Popcorn","Klappe","Kescher","Patin","Hiobsbotschaft","Farre","rentieren","Nuckel"]
# file = 'articles.xml'
file = sys.argv[1]

posdict = {"Adverb":"Adverb","Adjektiv":"Adjective","Verb":"Verb","Substantiv":"Noun"}
sprachendict = {"nb":"Norwegian Bokmål","no":"Norwegisch","sv":"Schwedisch","is":"Isländisch"}

mpattern1 = re.compile("\[\[(.*?)\]\]")
mpattern2 = re.compile("\|(.*?)}}")
qpattern = re.compile("{{reg\.\|.*?}}")

data = ET.parse(file)
root = data.getroot()
articles = root.findall('article')

translationsdict = defaultdict(lambda: defaultdict(lambda:defaultdict(list)))
inferenzdict = {"Norwegian Bokmål":{"Schwedisch":defaultdict(dict),"Isländisch":defaultdict(dict)},"Schwedisch":{"Norwegian Bokmål":defaultdict(dict),"Isländisch":defaultdict(dict)},"Isländisch":{"Norwegian Bokmål":defaultdict(dict),"Schwedisch":defaultdict(dict)}}
inferenz = defaultdict(lambda:defaultdict(lambda:defaultdict(list)))

test = 0
for article in articles:
    word = article.attrib['info']
    if "/translations" in word:
        word = word.replace("/translations","")
    for l in article.findall('language'):
        sprache = l.attrib['info']
        if sprache =="Deutsch":
            for p in l.findall('pos'):
                pos = p.attrib['info']
                if p.find('translations'):
                    trans = p.find('translations')
                    for t in trans.findall('translation'):
                        meaning = t.attrib["info"]
                        for tr in t.findall('tr'):
                            for sp in ['{{sv}}','{{is}}','{{nb}}']:
                                if sp in tr.text:
                                    sp = sprachendict[sp.replace('{','').replace('}','')]
                                    liste = []
                                    text = qpattern.sub("", tr.text)
                                    for tw in mpattern2.findall(text):
                                        if tw not in "1234567890":
                                            if not ":" in tw:
                                                if "|" in tw:
                                                    if tw.split("|")[-1] in ["n","f","m","?","c","n-p","p"]:
                                                        if tw.split("|")[-2] in ["n","f","m","?","c","n-p","p"]:
                                                            liste.append(tw.split("|")[-3].replace("[","").replace("]",""))
                                                        else:
                                                            liste.append(tw.split("|")[-2].replace("[","").replace("]",""))
                                                    else:
                                                        liste.append(tw.split("|")[-1].replace("[","").replace("]",""))
                                                else:
                                                    liste.append(tw.replace("[","").replace("]",""))
                                        
                                    translationsdict[sp][pos][word].append((meaning,liste))
                                    for x in liste:
                                        if not "/" in x:
                                            if "=" in x:
                                                x = x.split("=")[1]
                                            x = x.replace("(","").replace(")","")
                                            inferenz[word][pos][sp].append((meaning,x))
                                
        else:
            if sprache in inferenzdict:
                for p in l.findall('pos'):
                    pos = p.attrib['info']
                    for m in p.findall('meaning'):
                        liste = []
                        try:
                            meaning = m.text.replace("[","").replace("]","").replace("1","").replace("2","").replace("3","").replace("4","").replace("5","").replace("6","").replace("7","").replace("8","").replace("9","")
                            if " of|" in meaning:
                                pass
                            else:
                                for mea in meaning.split(","):
                                    if "|" in mea:
                                        if not "gloss" in mea:
                                            liste.append(mea.split("|")[-1])
                                    else:
                                        liste.append(mea)
                                if not liste:
                                    liste = meaning.split(",")
                                for element in liste:
                                    if "[" in element:
                                        if ";" in element:
                                            seperator = "; "
                                        else:
                                            seperator =", "
                                        for el in element.split(seperator):
                                            el = el.replace("[","").replace("]","")
                                            if ("to") in el:
                                                el = el.replace("to ","")
                                            inferenz[el][pos][sprache].append((mea,word))
                                    else:
                                        inferenz[element][pos][sprache].append((mea,word))
                        except AttributeError:
                            pass
                            #print(m.text)

                

              
for enword in inferenz:
    for pos in inferenz[enword]:
        for sp in inferenz[enword][pos]:
            for meaning,word in inferenz[enword][pos][sp]:
                for sp2 in ['Norwegian Bokmål','Schwedisch','Isländisch']:
                    if sp2 != sp:
                        try:
                            if translationsdict[sp2][pos][enword]:
                                inferenzdict[sp][sp2][pos][word] = translationsdict[sp2][pos][enword]
                        except KeyError:
                            pass

for s in translationsdict:
    with codecs.open("Deutsch-"+s+".txt","w","utf-8") as new:
        for pos in sorted(translationsdict[s]):
            for word in sorted(translationsdict[s][pos]):
                translations = translationsdict[s][pos][word]
                if translations:
                    translationset = set()
                    for sem,trlist in translations:
                        for tr in trlist:
                            translationset.add(tr)
                    for tr in sorted(translationset):
                        new.write(word+"\t"+tr+"\t"+posdict[pos]+"\n")

for sp1 in inferenzdict:
    for sp2 in inferenzdict[sp1]:
        with codecs.open(sp1+"-"+sp2+".txt","w","utf-8") as new:
            for pos in sorted(inferenzdict[sp1][sp2]):
                for word in sorted(inferenzdict[sp1][sp2][pos]):
                    translations = inferenzdict[sp1][sp2][pos][word]
                    if translations:
                        translationset = set()
                        for sem,trlist in translations:
                            for tr in trlist:
                                translationset.add(tr)
                        for tr in sorted(translationset):
                            if (not "/" in tr) and (not "not translated;" in tr):
                                if "=" in tr:
                                    tr = tr.split("=")[1]
                                new.write(word+"\t"+tr+"\t"+posdict[pos]+"\n")
        
        

"""   
for s in translationsdict:
    print(s)
    for pos in translationsdict[s]:
        print("\t",pos,len(translationsdict[s][pos]))
        with codecs.open("Englisch-"+s+"_"+pos+".txt","w","utf-8") as j:
            for word in translationsdict[s][pos]:
                translations = translationsdict[s][pos][word]
                if translations:
                    jsonobj = str({'word':word, 'translations':translations})
                    j.write(jsonobj+"\n")
               
print("----------------------")
for sp1 in inferenzdict:
    print(sp1)
    for sp2 in inferenzdict[sp1]:
        print("\t"+sp2)
        for pos in inferenzdict[sp1][sp2]:
            print("\t\t"+pos,len(inferenzdict[sp1][sp2][pos]))
            with codecs.open(sp1+"-"+sp2+"_"+pos+".txt","w","utf-8") as j:
                for word in inferenzdict[sp1][sp2][pos]:
                    jsonobj = str({'word':word, 'translations':inferenzdict[sp1][sp2][pos][word]})
                    j.write(jsonobj+"\n")


"""
"""
for pos in inferenzdict["Catalan"]["Italian"]:
    print(pos)
    for word in sorted(inferenzdict["Catalan"]["Italian"][pos]):
        print("\t",word,inferenzdict["Catalan"]["Italian"][pos][word])
"""
