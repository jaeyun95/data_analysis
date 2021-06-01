import pandas as pd
import numpy as np
import platform
import matplotlib.pyplot as plt

path = "C:/Windows/Fonts/210 맨발의청춘L.ttf"
from matplotlib import font_manager, rc
font_name = font_manager.FontProperties(fname=path).get_name()
rc("font",family=font_name)

population = pd.read_excel("C:/Users/jaeyun/Desktop/github/data_analysis/5.Population/data/edit_data.xlsx",engine='openpyxl',index_col=0)

si_name = [None]*len(population)
tmp_gu_dict = {"수원":["장안구","권선구","팔달구","영통구"],
               "성남":["수정구","중원구","분당구"],
               "안양":["만안구","동안구"],
               "안산":["상록구","단원구"],
               "고양":["덕양구","일산동구","일산서구"],
               "용인":["처인구","기흥구","수지구"],
               "청주":["상당구","서원구","흥덕구","청원구"],
               "천안":["동남구","서북구"],
               "전주":["완산구","덕진구"],
               "포항":["남구","북구"],
               "창원":["의창구","성산구","진해구","마산합포구","마산회원구"],
               "부천":["오정구","원미구","소사구"]}

for n in population.index:
    if population["광역시도"][n][-3:] not in ["광역시","특별시","자치시"]:
        if population["시도"][n][:-1] == "고성" and population["광역시도"][n] == "강원도":
            si_name[n] = "고성(강원)"
        elif population["시도"][n][:-1] == "고성" and population["광역시도"][n] == "경상남도":
            si_name[n] = "고성(경남)"
        else:
            si_name[n] = population["시도"][n][:-1]

        for keys, values in tmp_gu_dict.items():
            if population["시도"][n] in values:
                if len(population["시도"][n]) == 2:
                    si_name[n] = keys + ' ' + population["시도"][n]
                elif population["시도"][n] in ["마산합포구","마산회원구"]:
                    si_name[n] = keys + ' ' + population["시도"][n][2:-1]
                else:
                    si_name[n] = keys + ' ' + population["시도"][n][:-1]
    elif population["광역시도"][n] == "세종특별자치시":
        si_name[n] = "세종"
    else:
        if len(population["시도"][n]) == 2:
            si_name[n] = population["광역시도"][n][:2] + " " + population["시도"][n]
        else:
            si_name[n] = population["광역시도"][n][:2] + " " + population["시도"][n][:-1]

population["ID"] = si_name

del population["20-39세남자"]
del population["65세이상남자"]
del population["65세이상여자"]

draw_korea = pd.read_excel("C:/Users/jaeyun/Desktop/github/data_analysis/5.Population/data/draw_korea_raw.xlsx",engine='openpyxl')
draw_korea_stacked = pd.DataFrame(draw_korea.stack())
draw_korea_stacked.reset_index(inplace=True)
draw_korea_stacked.rename(columns={"level_0":"y", "level_1":"x", 0:"ID"},inplace=True)

draw_korea = draw_korea_stacked
BORDER_LINES = [
    [(5, 1), (5,2), (7,2), (7,3), (11,3), (11,0)], # 인천
    [(5,4), (5,5), (2,5), (2,7), (4,7), (4,9), (7,9),
     (7,7), (9,7), (9,5), (10,5), (10,4), (5,4)], # 서울
    [(1,7), (1,8), (3,8), (3,10), (10,10), (10,7),
     (12,7), (12,6), (11,6), (11,5), (12, 5), (12,4),
     (11,4), (11,3)], # 경기도
    [(8,10), (8,11), (6,11), (6,12)], # 강원도
    [(12,5), (13,5), (13,4), (14,4), (14,5), (15,5),
     (15,4), (16,4), (16,2)], # 충청북도
    [(16,4), (17,4), (17,5), (16,5), (16,6), (19,6),
     (19,5), (20,5), (20,4), (21,4), (21,3), (19,3), (19,1)], # 전라북도
    [(13,5), (13,6), (16,6)], # 대전시
    [(13,5), (14,5)], #세종시
    [(21,2), (21,3), (22,3), (22,4), (24,4), (24,2), (21,2)], #광주
    [(20,5), (21,5), (21,6), (23,6)], #전라남도
    [(10,8), (12,8), (12,9), (14,9), (14,8), (16,8), (16,6)], #충청북도
    [(14,9), (14,11), (14,12), (13,12), (13,13)], #경상북도
    [(15,8), (17,8), (17,10), (16,10), (16,11), (14,11)], #대구
    [(17,9), (18,9), (18,8), (19,8), (19,9), (20,9), (20,10), (21,10)], #부산
    [(16,11), (16,13)], #울산
    [(27,5), (27,6), (25,6)],
]

tmp_list = list(set(population["ID"].unique()) - set(draw_korea["ID"].unique()))
for tmp in tmp_list:
    population = population.drop(population[population["ID"]==tmp].index)
population = pd.merge(population, draw_korea, how="left", on=["ID"])

def draw(targetData, blockedMap, cmapname):
    gamma = 0.75
    whitelabelmin = (max(blockedMap[targetData]) -
                     min(blockedMap[targetData])) * 0.25 + \
                    min(blockedMap[targetData])
    datalabel = targetData
    vmin = min(blockedMap[targetData])
    vmax = max(blockedMap[targetData])

    mapdata = blockedMap.pivot_table(index='y', columns='x', values=targetData)
    masked_mapdata = np.ma.masked_where(np.isnan(mapdata), mapdata)

    plt.figure(figsize=(9, 11))
    plt.pcolor(masked_mapdata, vmin=vmin, vmax=vmax, cmap=cmapname,
               edgecolor='#aaaaaa', linewidth=0.5)

    for idx, row in blockedMap.iterrows():
        if len(row['ID'].split()) == 2:
            dispname = '{}\n{}'.format(row['ID'].split()[0], row['ID'].split()[1])
        elif row['ID'][:2] == '고성':
            dispname = '고성'
        else:
            dispname = row['ID']

        if len(dispname.splitlines()[-1]) >= 3:
            fontsize, linespacing = 10.0, 1.1
        else:
            fontsize, linespacing = 11, 1.
        annocolor = 'white' if row[targetData] > whitelabelmin else 'black'
        plt.annotate(dispname, (row['x'] + 0.5, row['y'] + 0.5), weight='bold',
                     fontsize=fontsize, ha='center', va='center', color=annocolor,
                     linespacing=linespacing)

    for path in BORDER_LINES:
        ys, xs = zip(*path)
        plt.plot(xs, ys, c='black', lw=2)
    plt.gca().invert_yaxis()
    plt.axis('off')
    cb = plt.colorbar(shrink=.1, aspect=10)
    cb.set_label(datalabel)
    plt.tight_layout()
    plt.show()

#draw("인구수합계",population,"Blues")
#population["소멸위기지역"] = [1 if con else 0 for con in population["소멸위기지역"]]
#draw("소멸위기지역",population,"Blues")

population_folium = population.set_index("ID")
population_folium.head()

import folium
import json

geo_path = "C:/Users/jaeyun/Desktop/github/data_analysis/5.Population/data/skorea_municipalities_geo_simple.json"
geo_data = json.load(open(geo_path,encoding='utf-8'))

map = folium.Map(location=[36.2002,127.054],zoom_start=7)
map.choropleth(geo_data=geo_data,
               data=population_folium["인구수합계"],
               columns=[population_folium.index, population_folium["인구수합계"]],
               fill_color="YlGnBu",
               key_on="feature.id")

#map.save("C:/Users/jaeyun/Desktop/github/data_analysis/5.Population/data/seoul_map1.html")

map = folium.Map(location=[36.2002,127.054],zoom_start=7)
map.choropleth(geo_data=geo_data,
               data=population_folium["소멸위기지역"],
               columns=[population_folium.index, population_folium["소멸위기지역"]],
               fill_color="PuRd",
               key_on="feature.id")

map.save("C:/Users/jaeyun/Desktop/github/data_analysis/5.Population/data/seoul_map2.html")