import pandas as pd
import numpy as np
import platform

path = "C:/Windows/Fonts/210 맨발의청춘L.ttf"
from matplotlib import font_manager, rc
font_name = font_manager.FontProperties(fname=path).get_name()
rc("font",family=font_name)

population = pd.read_excel("C:/Users/jaeyun/Desktop/github/data_analysis/5.Population/data/population_data.xlsx",header=1,engine='openpyxl')
population.fillna(method="pad",inplace=True)
population.rename(columns={'행정구역(동읍면)별(1)':'광역시도',
                           '행정구역(동읍면)별(2)':'시도',
                           '계':'인구수'},inplace=True)
population = population[(population["시도"] != "소계")]
population.rename(columns = {'항목':'구분'},inplace=True)
population.loc[population["구분"] == "총인구수 (명)","구분"] = "합계"
population.loc[population["구분"] == "남자인구수 (명)","구분"] = "남자"
population.loc[population["구분"] == "여자인구수 (명)","구분"] = "여자"

population['20-39세'] = population['20 - 24세'] + population['25 - 29세'] + population['30 - 34세'] + population['35 - 39세']
population['65세이상'] = population['65 - 69세'] + population['70 - 74세'] + population['75 - 79세'] + population['80 - 84세'] \
                      + population['85 - 89세'] + population['90 - 94세'] + population['95 - 99세'] + population['100+']

pop = pd.pivot_table(population, index=["광역시도","시도"],
                     columns=["구분"],
                     values=["인구수","20-39세","65세이상"])

pop["소멸비율"] = pop["20-39세","여자"] / (pop["65세이상","합계"]/2)

pop["소멸위기지역"] = pop["소멸비율"] < 1.0
pop[pop["소멸위기지역"]==True].index.get_level_values(1)

pop.reset_index(inplace=True)

tmp_columns = [pop.columns.get_level_values(0)[n] +
               pop.columns.get_level_values(1)[n]
               for n in range(0,len(pop.columns.get_level_values(0)))]
pop.columns = tmp_columns

pop.to_excel("C:/Users/jaeyun/Desktop/github/data_analysis/5.Population/data/edit_data.xlsx")