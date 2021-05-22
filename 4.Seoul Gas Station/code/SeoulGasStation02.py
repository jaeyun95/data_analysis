import pandas as pd
from glob import glob

files = glob("C:/Users/jaeyun/Downloads/지역*.xls")
tmp_raw = []

for file in files:
    tmp = pd.read_excel(file,header=2)
    tmp_raw.append(tmp)
station_raw = pd.concat(tmp_raw)

stations = pd.DataFrame({"Oil_store":station_raw["상호"],
                         "Address":station_raw["주소"],
                         "Price":station_raw["휘발유"],
                         "Self":station_raw["셀프여부"],
                         "Brand":station_raw["상표"]})

stations["Location"] = [area.split()[1] for area in stations["Address"]]

stations = stations[stations["Price"] != "-"]
stations["Price"] = [float(price) for price in stations['Price']]
