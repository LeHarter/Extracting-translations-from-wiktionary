import codecs
import re
import sys

word_pattern = re.compile('<title>(.*?)</title>')
language_pattern = re.compile('\({{Sprache\|(.*?)}}\) ==')
wanted_PoS = {"Adjektiv","Adverb","Substantiv","Verb"}
pos_pattern = re.compile("=== {{Wortart\|(.*?)\|.*?}}")
translation_pattern = re.compile("{{Ü-Tabelle|Ü-links=")

# file = "dewiktionary-20210501-pages-articles.xml"
file = sys.argv[1]

def articleformat_to_xml(text,word):
    article = "\t<article info=\""+word+"\">\n"
    level = 1
    bedeutungen = False
    for line in text:
        if level == 1: # no language found yet
            x = language_pattern.search(line)
            if x:
                language = x.group(1)
                level = 2
                article += "\t\t<language info=\""+language+"\">\n"
            # to do: LevelUp
        elif level == 2: #within a language
            x = pos_pattern.search(line)
            if x:
                pos = x.group(1)
                if pos in wanted_PoS:
                    level = 3
                    article += "\t\t\t<pos info=\""+pos+"\">\n"
            else:
                x = language_pattern.search(line)
                if x:
                    language = x.group(1)
                    article += "\t\t</language>\n"
                    article += "\t\t<language info=\""+language+"\">\n"
        elif level == 3: # within a pos
            if line == "{{Bedeutungen}}":
                bedeutungen = True
            if ":" in line and bedeutungen:
                meaning = line.replace(":","")
                article += "\t\t\t\t<meaning>"+meaning+"</meaning>\n"
            elif line == "==== {{Übersetzungen}} ====":
                bedeutungen = False
                level = 4
                article += "\t\t\t\t<translations>\n"
            else:
                x = pos_pattern.search(line)
                if x:
                    bedeutungen = False
                    pos = x.group(1)
                    article += "\t\t\t</pos>\n"
                    if pos in wanted_PoS:
                        article += "\t\t\t<pos info=\""+pos+"\">\n"
                    else:
                        level = 2
                else:
                    x = language_pattern.match(line)
                    if x:
                        bedeutungen = False
                        language = x.group(1)
                        level = 2
                        article += "\t\t\t</pos>\n"
                        article += "\t\t</language>\n"
                        article += "\t\t<language info=\""+language+"\">\n"
                        
                
        elif level == 4: # within the translations
            x = translation_pattern.match(line)
            if x:
                meaning = "None"
                article += "\t\t\t\t\t<translation info=\""+meaning+"\">\n"
                level = 5
            else:
                x = pos_pattern.search(line)
                if x:
                    article += "\t\t\t\t</translations>\n"
                    pos = x.group(1)
                    article += "\t\t\t</pos>\n"
                    if pos in wanted_PoS:
                        article += "\t\t\t<pos info=\""+pos+"\">\n"
                        level = 3
                    else:
                        level = 2
                else:
                    x = language_pattern.search(line)
                    if x:
                        language = x.group(1)
                        level = 2
                        article += "\t\t\t\t</translations>\n"
                        article += "\t\t\t</pos>\n"
                        article += "\t\t</language>\n"
                        article += "\t\t<language info=\""+language+"\">\n"
                        
        else: # within a translation block
            if line:
                if line[0] == "*":
                    article += "\t\t\t\t\t\t<tr>"+line+"</tr>\n"
                if line == "}}":
                    article += "\t\t\t\t\t</translation>\n"
                    level = 4
            else:
                level = 4
                article += "\t\t\t\t\t</translation>\n"
    """                   
    try:
        for a in article.split("\n"):
            print(a)
    except:
        pass    
    w = input("w")
    """
    
    if level == 4:
        article += "\t\t\t\t</translations>\n"
        level = 3
    if level == 3:
        article += "\t\t\t</pos>\n"
        level = 2
    if level == 2:
        article += "\t\t</language>\n"
    article += "\t</article>\n"
    return article



readin = False
text = ""
with codecs.open("articles.xml","w","utf-8") as xml:
    xml.write("<articles>\n")
    with codecs.open(file,"r","utf-8") as f:
        for line in f:
            if not readin:
                if  "<text bytes=" in line:
                    readin = True
                else:
                    x = word_pattern.search(line)
                    if x:
                        word = x.group(1)
            else:
                if not "</text>" in line:
                    text += line
                else:
                    if not ":" in word:
                        #for l in text.split("\n"):
                            #print(l)
                        #w = input("W")
                        article = articleformat_to_xml(text.split("\n"),word)
                        xml.write(article)
                    text = ""
                    readin = False
    xml.write("</articles>")
