from selenium import webdriver

DRIVER_PATH = r'C:\Users\navir\Documents\ChromeDriver\chromedriver.exe'
driver = webdriver.Chrome(executable_path=DRIVER_PATH)
driver.get('https://www.basketball-reference.com/players/b/balllo01/gamelog/2021')

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

print("{:.1f}".format(averagePoints))
print("{:.1f}".format(averageRebounds))
print("{:.1f}".format(averageAssists))

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

print("{:.1f}".format(lastFiveAveragePoints))
print("{:.1f}".format(lastFiveAverageRebounds))
print("{:.1f}".format(lastFiveAverageAssists))

driverBovada = webdriver.Chrome(executable_path=DRIVER_PATH)
driverBovada.get('https://www.basketball-reference.com/players/b/balllo01/gamelog/2021')