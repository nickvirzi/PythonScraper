import time
import sys
from selenium import webdriver

playerName = input("Enter player name: ")

DRIVER_PATH = r'C:\Users\navir\Documents\ChromeDriver\chromedriver.exe'
driver = webdriver.Chrome(executable_path=DRIVER_PATH)
driver.get('https://www.basketball-reference.com/')

search = driver.find_element_by_xpath('//*[@id="header"]/div[3]/form/div/div/input[2]').send_keys(playerName)
isRetired = driver.find_element_by_xpath('//*[@id="header"]/div[3]/form/div/div/div/div[1]/div[2]/div[1]/div/span[1]').text
submit = driver.find_element_by_xpath('//*[@id="header"]/div[3]/form/div/div/div/div[1]/div[2]/div[1]').click()

window_after = driver.window_handles[0]
driver.switch_to.window(window_after)

playerName = driver.find_element_by_xpath('//*[@id="meta"]/div[2]/h1/span').text

if len(isRetired) > 4:
    isRetired = isRetired[5:9]

if isRetired != "2021":
    careerAvgPts = driver.find_element_by_xpath('//*[@id="info"]/div[4]/div[2]/div[2]/p[2]').text
    careerAvgReb = driver.find_element_by_xpath('//*[@id="info"]/div[4]/div[2]/div[3]/p[2]').text
    careerAvgAst = driver.find_element_by_xpath('//*[@id="info"]/div[4]/div[2]/div[4]/p[2]').text

    print(playerName + ' is retired. For his career he averaged ' + careerAvgPts + ' points, ' + careerAvgReb + ' rebounds, and ' + careerAvgAst + ' assists.')
    sys.exit()

currentSeason = driver.find_element_by_xpath('//*[@id="per_game.2021"]/th/a').click()

window_after = driver.window_handles[0]
driver.switch_to.window(window_after)

points = []
rebounds = []
assists = []

for table in driver.find_elements_by_xpath('//*[@id="pgl_basic"]//tr'):
    data = [item.text for item in table.find_elements_by_xpath(".//*[self::td]")]
    if len(data) > 10:
        points.append(int(data[26]))
        rebounds.append(int(data[20]))
        assists.append(int(data[21]))

averagePoints = sum(points) / len(points)
averageRebounds = sum(rebounds) / len(rebounds)
averageAssists = sum(assists) / len(assists)

formattedAvgPts = "{:.1f}".format(averagePoints)
formattedAvgReb = "{:.1f}".format(averageRebounds)
formattedAvgAst = "{:.1f}".format(averageAssists)

lastFivePoints = []
lastFiveRebounds = []
lastFiveAssists = []

for x in range(len(points) - 5, len(points)):
    lastFivePoints.append(points[x])
    lastFiveRebounds.append(rebounds[x])
    lastFiveAssists.append(assists[x])

lastFiveAveragePoints = sum(lastFivePoints) / len(lastFivePoints)
lastFiveAverageRebounds = sum(lastFiveRebounds) / len(lastFiveRebounds)
lastFiveAverageAssists = sum(lastFiveAssists) / len(lastFiveAssists)

formattedL5AvgPts = "{:.1f}".format(lastFiveAveragePoints)
formattedL5AvgReb = "{:.1f}".format(lastFiveAverageRebounds)
formattedL5AvgAst = "{:.1f}".format(lastFiveAverageAssists)

print(playerName + ' has averaged ' + formattedAvgPts + ' points, ' + formattedAvgReb + ' rebounds, and ' + formattedAvgAst + ' assists.')
print(playerName + ' has averaged ' + formattedL5AvgPts + ' points, ' + formattedL5AvgReb + ' rebounds, and ' + formattedL5AvgAst + ' assists in his last 5 games.')