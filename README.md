# Extracting-translations-from-wiktionary
Wiktionary dump files are in xml-format, but the actual page text is not in xml. Every page element in the xml-dump-file has a text element where the page text is stored as plain text.
But the page text follows an own format indicating it's sturcture. The article2xml files use this structure to parse the information the page text gives about the meaning of the word the page is about and translations into other languages to a new xml-formatted file. Those files are used by the readin files to create dictionaries. Because the page text structure differs between the wiktionaries in different languages, one needs a special article2xml and readin file for every language.
## Article2xml Files
python English_article2xml.py enwiktionary-20210420-pages-articles.xml

This is an example how to run the article2xml files. They take a wiktionary dump file in the appropiate language (Catalan_article2xml.py needs a dump file of the Catalan wiktionary and Swedish_article2xml.py a dump file of the Swedish wiktionary etc.). The output is a xml-file called articles.xml
## Readin Files
python English_readin_romance.py article.xml

This is an example how to run the readin files. They take an articel.xml file as argument and produce dictionaries. Note that the article.xml file has to extracted from the wiktionary in the correct language. Englisch_readin_romance.py and English_reading_northgermanic need an article.xml file from the English wiktioanry, Catalan_readin.py needs a article.xml file extracted from the Catalan wiktionary, etc.

## Comparisons with other dictionaries
### Comparison with Muse
Please go into the MUSEcomparison folder. There you can see the Muse dictionaries with languages that are also available in our dictionaries and the python file overlapMUSE.py. This file can be used to compare our dictionaries with the MUSE ones. It can be started like that:

python overlapMUSE.py path_to path_to_wiki_dictionary_file path_to_MUSE_dictionary_file
### Comparison with Apertium
In the Apertium folder are the relevant arpertium .dix files as well as python scripts that make the .dix files readable. In addition they comput the overlap between the .dix file and the dictionary extracted from the wiktionaries. When running those python files they have to be in the same file as the corresponing .dix file and the corresponding wictionary dictionary.
