import pandas as pd


presidential = pd.read_csv("C:/Users/jaeyun/Desktop/github/data_analysis/6.Presidential Election/data/presidential.csv",index_col=0)
sido = presidential["광역시도"]
sido = [name[:2] if name[:2] in ["서울","부산","대구","광주","인천","대전","울산"] else "" for name in sido]

def cut_char_sigu(name):
    return name if len(name) == 2 else name[:-1]

sigun = [""]*len(presidential)
for n in presidential.index:
    each = presidential["시군"][n]
    if each[:2] in ["수원","성남","안양","안산","고양","용인","청주","천안","전주","포항","창원"]:
        sigun[n] = each.split("시")[0] +" "+ cut_char_sigu(each.split("시")[1])
    else: sigun[n] = cut_char_sigu(each)

ID = [sido[n] + " " + sigun[n] for n in range(len(sigun))]
ID = [name[1:] if name[0] == " " else name for name in ID]
ID = [name[:2] if name[:2] == "세종" else name for name in ID]

presidential["ID"] = ID

presidential[["rate_moon","rate_hong","rate_ahn","rate_yu","rate_sim"]] = presidential[["moon","hong","ahn","yu","sim"]].div(presidential['pop'],axis=0)
presidential[["rate_moon","rate_hong","rate_ahn","rate_yu","rate_sim"]] *= 100

#print(presidential.sort_values(["rate_moon"],ascending=[False]).head())
#print(presidential.sort_values(["rate_hong"],ascending=[False]).head())

path = "C:/Windows/Fonts/210 맨발의청춘L.ttf"
from matplotlib import font_manager, rc
font_name = font_manager.FontProperties(fname=path).get_name()
rc("font",family=font_name)

draw_korea = pd.read_csv("C:/Users/jaeyun/Desktop/github/data_analysis/6.Presidential Election/data/draw_korea.csv",encoding="utf-8")

#print(presidential[presidential["ID"] == "고성"])
presidential.loc[125,"ID"] = "고성(강원)"
presidential.loc[233,"ID"] = "고성(경남)"

presidential.loc[228,"ID"] = "창원 합포"
presidential.loc[229,"ID"] = "창원 회원"

ahn_tmp = presidential.loc[85, 'ahn']/3
hong_tmp = presidential.loc[85, 'hong']/3
moon_tmp = presidential.loc[85, 'moon']/3
yu_tmp = presidential.loc[85, 'yu']/3
sim_tmp = presidential.loc[85, 'sim']/3
pop_tmp = presidential.loc[85, 'pop']/3

rate_moon_tmp = presidential.loc[85, 'rate_moon']
rate_hong_tmp = presidential.loc[85, 'rate_hong']
rate_ahn_tmp = presidential.loc[85, 'rate_ahn']
rate_yu_tmp = presidential.loc[85, 'rate_yu']
rate_sim_tmp = presidential.loc[85, 'rate_sim']

presidential.loc[250] = [sim_tmp, yu_tmp, ahn_tmp, hong_tmp, moon_tmp, pop_tmp,
                           '경기도', '부천시', '부천 소사',
                           rate_moon_tmp, rate_hong_tmp, rate_ahn_tmp, rate_yu_tmp, rate_sim_tmp]
presidential.loc[251] = [sim_tmp, yu_tmp, ahn_tmp, hong_tmp, moon_tmp, pop_tmp,
                           '경기도', '부천시', '부천 오정',
                           rate_moon_tmp, rate_hong_tmp, rate_ahn_tmp, rate_yu_tmp, rate_sim_tmp]
presidential.loc[252] = [sim_tmp, yu_tmp, ahn_tmp, hong_tmp, moon_tmp, pop_tmp,
                           '경기도', '부천시', '부천 원미',
                           rate_moon_tmp, rate_hong_tmp, rate_ahn_tmp, rate_yu_tmp, rate_sim_tmp]

presidential.drop([85],inplace=True)

final_data = pd.merge(presidential,draw_korea,how="left",on=["ID"])

final_data["moon_vs_hong"] = final_data["rate_moon"] - final_data["rate_hong"]
final_data["moon_vs_ahn"] = final_data["rate_moon"] - final_data["rate_ahn"]
final_data["moon_vs_yu"] = final_data["rate_moon"] - final_data["rate_yu"]
final_data["moon_vs_sim"] = final_data["rate_moon"] - final_data["rate_sim"]

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
import matplotlib.pyplot as plt
import numpy as np

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
        annocolor = 'black'#'white' if row[targetData] > whitelabelmin else 'black'
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

#draw("moon_vs_hong",final_data,"RdBu")
#draw("moon_vs_ahn",final_data,"RdBu")
#draw("moon_vs_yu",final_data,"RdBu")
draw("moon_vs_sim",final_data,"RdBu")