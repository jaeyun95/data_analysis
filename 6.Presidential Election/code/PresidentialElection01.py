from selenium import webdriver

driver = webdriver.Chrome("C:/Users/jaeyun/Desktop/chromedriver_win32/chromedriver")
driver.get("http://info.nec.go.kr/")
driver.implicitly_wait(5)
driver.switch_to_default_content()
driver.switch_to_frame("main")
driver.find_element_by_xpath("""//*[@id="header"]/ul[1]/li[2]/a""").click()
driver.implicitly_wait(5)

driver.find_element_by_xpath("""//*[@id="presubmu"]/li[4]/a""").click()
driver.implicitly_wait(5)
driver.find_element_by_xpath("""//*[@id="header"]/div[4]/ul/li[5]/a""").click()
driver.implicitly_wait(5)
driver.find_element_by_xpath("""//*[@id="electionType1"]""").click()
driver.implicitly_wait(5)
driver.find_element_by_xpath("""//*[@id="electionName"]/option[2]""").click()
driver.implicitly_wait(5)
driver.find_element_by_xpath("""//*[@id="electionCode"]/option[2]""").click()
driver.implicitly_wait(5)
sido = driver.find_element_by_id("cityCode")
driver.implicitly_wait(5)
while True:
    sido_list = sido.find_elements_by_tag_name("option")
    if len(sido_list) > 2:
        sido_name_values = [option.text for option in sido_list]
        sido_name_values = sido_name_values[2:]
        break

def get_num(tmp):
    if type(tmp) == type(0): return tmp
    else: return float(tmp.split('(')[0].replace(',',''))

def move_sido(name):
    element = driver.find_element_by_id("cityCode")
    element.send_keys(name)
    driver.find_element_by_xpath("""//*[@id="searchBtn"]""").click()
    driver.implicitly_wait(5)

def append_data(df, sido_name, data):
    for each in df[0].values[1:]:
        data['광역시도'].append(sido_name)
        data['시군'].append(each[0])
        data['pop'].append(get_num(each[2]))
        data['moon'].append(get_num(each[3]))
        data['hong'].append(get_num(each[4]))
        data['ahn'].append(get_num(each[5]))
        data['yu'].append(get_num(each[6]))
        data['sim'].append(get_num(each[7]))


election_result_raw = {'광역시도' : [],
                       '시군' : [],
                       'pop' : [],
                       'moon' : [],
                       'hong' : [],
                       'ahn' : [],
                       'yu': [],
                       'sim': []}

from bs4 import BeautifulSoup
import pandas as pd

for each_sido in sido_name_values:
    move_sido(each_sido)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table')
    df = pd.read_html(str(table))
    append_data(df, each_sido, election_result_raw)

election_result = pd.DataFrame(election_result_raw,columns=['광역시도', '시군', 'pop', 'moon','hong','ahn','yu','sim'])
election_result.to_csv("C:/Users/jaeyun/Desktop/github/data_analysis/6.Presidential Election/data/presidential.csv")