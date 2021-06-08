import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from urllib.request import Request,urlopen
import urllib
import time

path = "C:/Windows/Fonts/210 맨발의청춘L.ttf"
from matplotlib import font_manager, rc
font_name = font_manager.FontProperties(fname=path).get_name()
rc("font",family=font_name)

url = 'https://search.naver.com/search.naver?where=kin&sm=tab_jum&query=%EB%82%A8%EC%9E%90%EC%B9%9C%EA%B5%AC+%EC%84%A0%EB%AC%BC'
request = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
html = urlopen(request).read()
soup = BeautifulSoup(html,"html.parser")
tmp = soup.find_all('li')
tmp_list = []
for line in tmp:
    tmp_list.append(line.text)

import nltk
from konlpy.tag import Okt

t = Okt()
present_text = ""
for each_line in tmp_list:
    present_text = present_text + each_line + "\n"

token_ko = t.morphs(present_text)
stop_words = ['.','가','요','답변','...','을','수','에','질문','제','를','이','도',
            '좋','1','는','로','으로','2','것','은','다',',','니다','대','들',
            '2017','들','데','..','의','때','겠','고','게','네요','한','일','할',
            '10','?','하는','06','주','려고','인데','거','좀','는데','~','ㅎㅎ',
            '하나','이상','20','뭐','까','있는','잘','습니다','다면','했','주려',
            '지','있','못','후','중','줄','6','과','어떤','기본','!!','!',' ','Q',
            '(',')','ㅠㅠ','@','에서','L','분',"\n","1:1","A","다음","전","2021.05","+",
            '단어','선물해','라고','중요한','합','가요','....','보이','네','무지']

tokens_ko = [each_word for each_word in token_ko if each_word not in stop_words]
ko = nltk.Text(tokens_ko, name='남자 친구 선물')

#plt.figure(figsize=(15,6))
#ko.plot(50)
#plt.show()

from wordcloud import WordCloud, STOPWORDS

data = ko.vocab().most_common(150)
wordcloud = WordCloud(font_path=path,relative_scaling=0.2,background_color="white").generate_from_frequencies(dict(data))
plt.figure(figsize=(12,8))
plt.imshow(wordcloud)
plt.axis("off")
plt.show()