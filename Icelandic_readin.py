import xml.etree.ElementTree as ET
from collections import defaultdict
import re
import json
import codecs
import sys

postranslation = {"atviksorð":"Adverb","nafnorð":"Noun","lýsingarorð":"Adjective","sagnorð":"Verb"}

trpattern = re.compile("{{þýðingar|(.*?)}}")
mpattern1 = re.compile("\[\[(.*?)\]\]")
mpattern2 = re.compile("{{(.*?)}}")

# file = 'articles.xml'
file = sys.argv[1]

data = ET.parse(file)
root = data.getroot()
articles = root.findall('article')

translationsdict = defaultdict(lambda: defaultdict(lambda:defaultdict(list)))
inferenzdict = {"no":{"sv":defaultdict(dict)},"sv":{"no":defaultdict(dict)}}
inferenz = defaultdict(lambda:defaultdict(lambda:defaultdict(list)))

test = 0
for article in articles:
    word = article.attrib['info']
    if "/lýsingarorðsbeyging" in word:
        word = word.replace("/lýsingarorðsbeyging","")
    for l in article.findall('language'):
        sprache = l.attrib['info']
        if sprache =="is": 
            for p in l.findall('pos'):
                pos = p.attrib['info']
                if p.find('translations'):
                    trans = p.find('translations')
                    for t in trans.findall('translation'):
                        meaning = t.attrib["info"]
                        for tr in t.findall('tr'):
                            for sp in ['no','sv']:
                                if sp+"=" in tr.text:
                                    liste = []
                                        
                                    for tw in trpattern.findall(tr.text):
                                        if "|" in tw:
                                            if (tw.split("|")[-1].isnumeric()) or ("," in tw.split("|")[-1]):
                                                liste.append(tw.split("|")[-2])
                                            else:
                                                liste.append(tw.split("|")[-1])
                                    translationsdict[sp][pos][word].append((meaning,liste))
                                    for x in liste:
                                        inferenz[word][pos][sp].append((meaning,x))
                               
        else:
            if sprache in inferenzdict:
                for p in l.findall('pos'):
                    pos = p.attrib['info']
                    for m in p.findall('meaning'):
                        liste = []
                        meaning = m.text
                        for mea in mpattern1.findall(meaning)+mpattern2.findall(meaning):
                            if "|" in mea:
                                if not "gloss" in mea:
                                    liste.append(mea.split("|")[-1])
                            else:
                                liste.append(mea)
                        for element in liste:
                            #translationsdict[sp][pos][element].append(("None",[word]))
                            inferenz[element][pos][sprache].append((mea,word))

                

           
for enword in inferenz:
    for pos in inferenz[enword]:
        for sp in inferenz[enword][pos]:
            for meaning,word in inferenz[enword][pos][sp]:
                for sp2 in ['no','sv']:
                    if sp2 != sp:
                        try:
                            if translationsdict[sp2][pos][enword]:
                                inferenzdict[sp][sp2][pos][word] = translationsdict[sp2][pos][enword]
                        except KeyError:
                            pass

for s in translationsdict:
    with codecs.open("is-"+s+".txt","w","utf-8") as new:
        for pos in sorted(translationsdict[s]):
            for word in sorted(translationsdict[s][pos]):
                translations = translationsdict[s][pos][word]
                if translations:
                    translationset = set()
                    for sem,trlist in translations:
                        for tr in trlist:
                            translationset.add(tr)
                    for tr in sorted(translationset):
                        new.write(word+"\t"+tr+"\t"+postranslation[pos]+"\n")

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
                                new.write(word+"\t"+tr+"\t"+postranslation[pos]+"\n")
        
        

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
