import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import platform

stations = pd.read_csv("C:/Users/jaeyun/Desktop/github/data_analysis/4.Seoul Gas Station/data/station.csv",index_col=0)

path = "C:/Windows/Fonts/210 맨발의청춘L.ttf"
from matplotlib import font_manager, rc
font_name = font_manager.FontProperties(fname=path).get_name()
rc("font",family=font_name)

## box plot for price/self
'''
stations.boxplot(column="Price", by="Self",figsize=(12,8))
plt.show()
'''

## box plot for brand/price/self
'''
sns.boxplot(x="Brand",y="Price", hue="Self",data=stations,palette="Set3")
plt.show()
'''

## swarmplot for brand/price
'''
sns.boxplot(x="Brand",y="Price",data=stations,palette="Set3")
sns.swarmplot(x="Brand",y="Price",data=stations,color=".6")
plt.show()
'''

