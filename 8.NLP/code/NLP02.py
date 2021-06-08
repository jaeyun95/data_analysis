import nltk
from konlpy.corpus import kobill

files_ko = kobill.fileids()
doc_ko = kobill.open("1809890.txt").read()

from konlpy.tag import Okt

t = Okt()
token_ko = t.nouns(doc_ko)
ko = nltk.Text(token_ko, name="대한민국 국회 의안 제 1809890호")

import matplotlib.pyplot as plt

path = "C:/Windows/Fonts/210 맨발의청춘L.ttf"
from matplotlib import font_manager, rc
font_name = font_manager.FontProperties(fname=path).get_name()
rc("font",family=font_name)

#plt.figure(figsize=(12,6))
#ko.plot(50)
#plt.show()

stop_words = [".","(",")",",","'","%","-","X",").","x","의","자","에","안","번","호","을","이","다","만","로","가","를"]
ko = [each_word for each_word in ko if each_word not in stop_words]

ko = nltk.Text(ko, name="대한민국 국회 의안 제 1809890호")
#plt.figure(figsize=(12,6))
#ko.plot(50)
#plt.show()

#plt.figure(figsize=(12,6))
#ko.dispersion_plot(["육아휴직","초등학교","공무원"])

#print(ko.concordance("초등학교"))
from wordcloud import WordCloud, STOPWORDS

data = ko.vocab().most_common(150)
wordcloud = WordCloud(font_path=path,relative_scaling=0.2,background_color="white").generate_from_frequencies(dict(data))
plt.figure(figsize=(12,8))
plt.imshow(wordcloud)
plt.axis("off")
plt.show()