# Extracting-translations-from-wiktionary
Wiktionary dump files are in xml-format, but the actual page text is not in xml. Every page element in the xml-dump-file has a text element where the page text is stored as plain text.
But the page text follows an own format indicating it's sturcture. The article2xml files use this structure to parse the information the page text gives about the meaning of the word the page is about and translations into other languages to a new xml-formatted file. Those files are used by the readin files to create dictionaries. Because the page text structure differs between the wiktionaries in different languages, one needs a special article2xml and readin file for every language.
## Article2xml Files
python English_article2xml.py enwiktionary-20210420-pages-articles.xml

This is an example how to run the article2xml files. They take an wiktionary dump file in the appropiate language (Catalan_article2xml.py needs a dump file of the Catalan wiktionary and Swedish_article2xml.py a dump file of the Swedish wiktionary etc.). The output is a xml-file called articles.xml
## Readin Files
