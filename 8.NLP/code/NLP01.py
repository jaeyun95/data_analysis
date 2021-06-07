from konlpy.tag import Kkma

kkma = Kkma()
#print(kkma.sentences("한국어 분석을 시작합니다 재밌습니당~"))

#print(kkma.nouns("한국어 분석을 시작합니다 재밌습니당~"))

#print(kkma.pos("한국어 분석을 시작합니다 재밌습니당~"))

from konlpy.tag import Hannanum

hannanum = Hannanum()

#print(hannanum.nouns("한국어 분석을 시작합니다 재밌습니당~"))

#print(hannanum.morphs("한국어 분석을 시작합니다 재밌습니당~"))
#print(hannanum.pos("한국어 분석을 시작합니다 재밌습니당~"))

from wordcloud import WordCloud, STOPWORDS
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

text = open("C:/Users/jaeyun/Desktop/github/data_analysis/8.NLP/data/alice.txt").read()
alice_mask = np.array(Image.open("C:/Users/jaeyun/Desktop/github/data_analysis/8.NLP/data/alice_mask.png"))

path = "C:/Windows/Fonts/210 맨발의청춘L.ttf"
from matplotlib import font_manager, rc
font_name = font_manager.FontProperties(fname=path).get_name()
rc("font",family=font_name)

wc = WordCloud(background_color="white",max_words=2000,mask=alice_mask,stopwords=STOPWORDS)
wc = wc.generate(text)

#plt.figure(figsize=(12,12))
#plt.imshow(wc, interpolation="bilinear")
#plt.axis("off")
#plt.show()

text = open("C:/Users/jaeyun/Desktop/github/data_analysis/8.NLP/data/a_new_hope.txt").read()
stormtrooper_mask = np.array(Image.open("C:/Users/jaeyun/Desktop/github/data_analysis/8.NLP/data/stormtrooper_mask.png"))

text = text.replace("HAN","Han")
text = text.replace("LUKE'S","Luke")

wc = WordCloud(background_color="white",max_words=2000,mask=stormtrooper_mask,stopwords=STOPWORDS)
wc = wc.generate(text)
plt.figure(figsize=(12,12))
plt.imshow(wc, interpolation="bilinear")
plt.axis("off")
plt.show()