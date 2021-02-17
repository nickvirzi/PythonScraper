from selenium import webdriver

DRIVER_PATH = r'C:\Users\navir\Documents\ChromeDriver\chromedriver.exe'
driver = webdriver.Chrome(executable_path=DRIVER_PATH)
driver.get('https://www.basketball-reference.com/boxscores')

date = driver.find_element_by_xpath('//*[@id="content"]/div[1]/span').text

