from selenium import webdriver

driver = webdriver.Chrome("C:/Users/jaeyun/Desktop/chromedriver_win32/chromedriver")
driver.get("http://www.opinet.co.kr/")
driver.implicitly_wait(10)
driver.find_element_by_xpath("""//*[@id="quick_ul"]/li[2]/a""").click()
driver.implicitly_wait(10)
gu_list_raw = driver.find_element_by_xpath("""//*[@id="SIGUNGU_NM0"]""")
gu_list = gu_list_raw.find_elements_by_tag_name("option")
gu_names = [option.get_attribute("value") for option in gu_list]
gu_names.remove('')

for gu in gu_names[18:]:
    element = driver.find_element_by_id("SIGUNGU_NM0")
    element.send_keys(gu)
    driver.implicitly_wait(10)
    driver.find_element_by_xpath("""//*[@id="searRgSelect"]/span""").click()
    driver.implicitly_wait(10)
    driver.find_element_by_xpath("""//*[@id="glopopd_excel"]/span""").click()
    driver.implicitly_wait(10)





