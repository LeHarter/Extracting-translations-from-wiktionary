import xml.etree.ElementTree as ET
from collections import defaultdict
import re
import json
import codecs
import sys

mpattern1 = re.compile("\[\[(.*?)\]\]")
mpattern2 = re.compile("\|(.*?)}}")

#file = 'articles.xml'
file = sys.argv[1]
data = ET.parse(file)
root = data.getroot()
articles = root.findall('article')

translationsdict = defaultdict(lambda: defaultdict(lambda:defaultdict(list)))
inferenzdict = {"Romanian":{"Catalan":defaultdict(dict),"Italian":defaultdict(dict),"Occitan":defaultdict(dict)},"Catalan":{"Romanian":defaultdict(dict),"Italian":defaultdict(dict),"Occitan":defaultdict(dict)},"Occitan":{"Romanian":defaultdict(dict),"Catalan":defaultdict(dict),"Italian":defaultdict(dict)},"Italian":{"Romanian":defaultdict(dict),"Occitan":defaultdict(dict),"Catalan":defaultdict(dict)}}
inferenz = defaultdict(lambda:defaultdict(lambda:defaultdict(list)))

test = 0
for article in articles:
    word = article.attrib['info'].replace("/translations","")
    for l in article.findall('language'):
        sprache = l.attrib['info']
        if sprache =="English": 
            for p in l.findall('pos'):
                pos = p.attrib['info']
                if p.find('translations'):
                    trans = p.find('translations')
                    for t in trans.findall('translation'):
                        meaning = t.attrib["info"]
                        for tr in t.findall('tr'):
                            for sp in ['Romanian','Catalan','Italian','Occitan']:
                                if sp in tr.text:
                                    liste = []
                                    for tw in mpattern1.findall(tr.text)+mpattern2.findall(tr.text):
                                        if "|" in tw:
                                            if (tw.split("|")[-1] in ["u","n-p","n","f","m","?","f-p","m-p","m-s","c","p"]) or ("=" in tw.split("|")[-1]):
                                                if (tw.split("|")[-2] in  ["u","n-p","n","f","f-p","m","?","m-p","m-s","c","p"]) or ("=" in tw.split("|")[-2]):
                                                    try:
                                                        tw.split("|")[-3].replace("[","").replace("]","")
                                                    except IndexError:
                                                        liste = mpattern1.findall(tr.text)
                                                        
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
                        meaning = m.text
                        if " of|" in meaning:
                            pass
                        else:
                            for mea in mpattern1.findall(meaning)+mpattern2.findall(meaning):
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

                

              
for enword in inferenz:
    for pos in inferenz[enword]:
        for sp in inferenz[enword][pos]:
            for meaning,word in inferenz[enword][pos][sp]:
                for sp2 in ['Romanian','Catalan','Italian','Occitan']:
                    if sp2 != sp:
                        try:
                            if translationsdict[sp2][pos][enword]:
                                inferenzdict[sp][sp2][pos][word] = translationsdict[sp2][pos][enword]
                        except KeyError:
                            pass

for s in translationsdict:
    with codecs.open("English-"+s+".txt","w","utf-8") as new:
        for pos in sorted(translationsdict[s]):
            for word in sorted(translationsdict[s][pos]):
                translations = translationsdict[s][pos][word]
                if translations:
                    translationset = set()
                    for sem,trlist in translations:
                        for tr in trlist:
                            translationset.add(tr)
                    for tr in sorted(translationset):
                        new.write(word+"\t"+tr+"\t"+pos+"\n")

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
                                new.write(word+"\t"+tr+"\t"+pos+"\n")
        
        

