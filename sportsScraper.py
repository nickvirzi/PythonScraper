import time
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import datetime

#Take in team name and return the ESPN team abbreviation
def getESPNTeamAbbreviation(teamName):
    teamAbbreviationDictionary = {
        'Atlanta': 'ATL', 'Boston': 'BOS', 'Charlotte': 'CHA', 'Chicago': 'CHI', 'Cleveland': 'CLE', 'Dallas': 'DAL', 'Denver': 'DEN', 'Detroit': 'DET', 'Houston': 'HOU', 'Indiana': 'IND', 'Memphis': 'MEM',
        'Miami': 'MIA', 'Miluakee': 'MIL', 'Minnesota': 'MIN', 'Orlando': 'ORL', 'Philadelphia': 'PHI', 'Phoenix': 'PHO', 'Portland': 'POR', 'Sacramento': 'SAC', 'Toronto': 'TOR', 'Utah': 'UTA', 'Washington': 'WAS',
        'Golden State': 'GS', 'New Orleans': 'NO', 'New York': 'NY', 'San Antonio': 'SA'
    }
    abbreviation = teamAbbreviationDictionary[teamName]
    return abbreviation

playerName = input("Enter player name: ")

#Gets current month
currentDate = datetime.datetime.now()
currentMonth = currentDate.strftime("%B")

DRIVER_PATH = r'C:\Users\navir\Documents\ChromeDriver\chromedriver.exe'
driver = webdriver.Chrome(executable_path=DRIVER_PATH)
driver.get('https://www.espn.com/')

#Search players name on ESPN
clickSearch = driver.find_element_by_xpath('//*[@id="global-search-trigger"]').click()
inputPlayerName = driver.find_element_by_xpath('//*[@id="global-search"]/input[1]').send_keys(playerName)
confirmSearch = driver.find_element_by_xpath('//*[@id="global-search"]/input[2]').click()

window_after = driver.window_handles[0]
driver.switch_to.window(window_after)

time.sleep(2)

#Filter results to players only to avoid clicking articles
filterPlayersOnly = driver.find_element_by_xpath('//*[@id="fittPageContainer"]/div[2]/div/div/ul/li[2]/a').click()

window_after = driver.window_handles[0]
driver.switch_to.window(window_after)

time.sleep(2)

#Select player
selectPlayer = driver.find_element_by_xpath('//*[@id="fittPageContainer"]/div[2]/div/div/section/div/ul/div/div/li/section').click()

window_after = driver.window_handles[0]
driver.switch_to.window(window_after)

#Get players name formatted properly
formattedFirstName = driver.find_element_by_xpath('//*[@id="fittPageContainer"]/div[2]/div[1]/div/div/div[1]/div[1]/div[2]/h1/span[1]').text
formattedLastName = driver.find_element_by_xpath('//*[@id="fittPageContainer"]/div[2]/div[1]/div/div/div[1]/div[1]/div[2]/h1/span[2]').text

formattedPlayerName = formattedFirstName + ' ' + formattedLastName

#Grabe average stats for the player for the season
averagePoints = driver.find_element_by_xpath('//*[@id="fittPageContainer"]/div[2]/div[1]/div/div/div[2]/aside/ul/li[1]/div/div[2]').text
averageRebounds = driver.find_element_by_xpath('//*[@id="fittPageContainer"]/div[2]/div[1]/div/div/div[2]/aside/ul/li[2]/div/div[2]').text
averageAssists = driver.find_element_by_xpath('//*[@id="fittPageContainer"]/div[2]/div[1]/div/div/div[2]/aside/ul/li[3]/div/div[2]').text

playerURL = driver.current_url

time.sleep(2)

driver.execute_script("window.scrollTo(0,0)")

#Click the players team and grab team name
playersTeam = driver.find_element_by_xpath('//*[@id="fittPageContainer"]/div[2]/div[1]/div/div/div[1]/div[1]/div[2]/div/ul/li[1]/a').text
clickPlayersTeam = driver.find_element_by_xpath('//*[@id="fittPageContainer"]/div[2]/div[1]/div/div/div[1]/div[1]/div[2]/div/ul/li[1]').click()

window_after = driver.window_handles[0]
driver.switch_to.window(window_after)

#Clicking teams schedule 
clickSchedule = driver.find_element_by_xpath('//*[@id="global-nav-secondary"]/div[2]/ul/li[4]/a').click()

window_after = driver.window_handles[0]
driver.switch_to.window(window_after)

#Grabbing next opponent for the players team
for tableRow in driver.find_elements_by_xpath('//*[@id="fittPageContainer"]/div[2]/div[5]/div/div[1]/section/div/section/section/div/div/div/div[2]/table//tr'): 
    dataThree = [item.text for item in tableRow.find_elements_by_xpath(".//*[self::td]")]
    if len(dataThree) > 3:
        if dataThree[3] == '':
            nextOpponent = dataThree[1]
            break

#Formatting and handling the team name and getting the abbreviation
if '@' in nextOpponent:
    nextOpponentFormatted = nextOpponent[2:]
else:
    nextOpponentFormatted = nextOpponent[3:]

nextOpponentAbbreviated = getESPNTeamAbbreviation(nextOpponentFormatted)

addVSAbbrev = 'vs ' + nextOpponentAbbreviated

#Go back to the players profile to then determine splits based upon opponent 
driver = webdriver.Chrome(executable_path=DRIVER_PATH)
driver.get(playerURL)

window_after = driver.window_handles[0]
driver.switch_to.window(window_after)

#Click Game Splits
clickGameSplits = driver.find_element_by_xpath('//*[@id="fittPageContainer"]/div[2]/div[2]/nav/ul/li[5]/a').click()

window_after = driver.window_handles[0]
driver.switch_to.window(window_after)

dataCounterOne = 0
dataCounterTwo = 0
vsTeamCounter = 0

#Set up to find days rest in the table
daysRest = ["0 Days Rest", "1 Days Rest", "2 Days Rest", "3+ Days Rest"]

time.sleep(2)

#ESPN has a headers column, this grabs the location to use in the table of data for corresponding row
for tableRow in driver.find_elements_by_xpath('//*[@id="fittPageContainer"]/div[2]/div[5]/div/div[1]/div[1]/section/div[1]/div[2]/div/table//tr'): 
    data = [item.text for item in tableRow.find_elements_by_xpath(".//*[self::td]")]
    dataCounterOne += 1
    if currentMonth == data[0]:
        curMonthCounter = dataCounterOne
    elif daysRest[0] == data[0]:
        zeroDaysRestCounter = dataCounterOne
    elif daysRest[1] == data[0]:
        oneDaysRestCounter = dataCounterOne
    elif daysRest[2] == data[0]:
        twoDaysRestCounter = dataCounterOne
    elif daysRest[3] == data[0]:
        threePlusDaysCounter = dataCounterOne
    elif addVSAbbrev == data[0]:
        vsTeamCounter = dataCounterOne

#This loop grabs the stats from the other side of the table
for tableRow in driver.find_elements_by_xpath('//*[@id="fittPageContainer"]/div[2]/div[5]/div/div[1]/div[1]/section/div[1]/div[2]/div/div/div[2]/table//tr'): 
    dataTwo = [item.text for item in tableRow.find_elements_by_xpath(".//*[self::td]")]
    dataCounterTwo += 1
    if curMonthCounter == dataCounterTwo:
        curMonthSplits = dataTwo
    elif zeroDaysRestCounter == dataCounterTwo:
        zeroDaysRestSplits = dataTwo
    elif oneDaysRestCounter == dataCounterTwo:
        oneDaysRestSplits = dataTwo
    elif twoDaysRestCounter == dataCounterTwo:
        twoDaysRestSplits = dataTwo
    elif threePlusDaysCounter == dataCounterTwo:
        threePlusDaysRestSplits = dataTwo
    elif vsTeamCounter == dataCounterTwo:
        vsTeamSplits = dataTwo

#Sets up all stats for the current month
gamesPlayedInCurMonth = curMonthSplits[0]
fgPercentInCurMonth = curMonthSplits[3]
threePtPercentCurMonth = curMonthSplits[5]
avgPtsCurMonth = curMonthSplits[16]
avgRebCurMonth = curMonthSplits[10]
avgAstCurMonth = curMonthSplits[11]

#Sets up all stats vs opponents team if the player has played them before
if vsTeamCounter != 0:
    gamesPlayedVSOpp = vsTeamSplits[0]
    fgPercentVSOpp = vsTeamSplits[3]
    threePtPercentVSOpp = vsTeamSplits[5]
    avgPtsVSOpp = vsTeamSplits[16]
    avgRebVSOpp = vsTeamSplits[10]
    avgAdtVSOpp = vsTeamSplits[11]

#Outputing the data in written form
print(' ')
print(formattedPlayerName + ' has averaged ' + averagePoints + ' points, ' + averageRebounds + ' rebounds, and ' + averageAssists + ' assists.')
print(formattedPlayerName + ' in ' + currentMonth + ' has averaged ' + avgPtsCurMonth + ' points, ' + avgRebCurMonth + ' rebounds, and ' + avgAstCurMonth + ' assists in ' + gamesPlayedInCurMonth + ' games.')
if vsTeamCounter != 0:
    print(formattedPlayerName + ' has played ' + nextOpponentFormatted + ' ' + gamesPlayedVSOpp + ' times. He has averaged ' + avgPtsVSOpp + ' points, ' + avgRebVSOpp + ' rebounds, and ' + avgAdtVSOpp + ' assists.')
    print(formattedPlayerName + ' is shooting ' + fgPercentVSOpp + ' percent from the field and ' + threePtPercentVSOpp + ' percent from three against ' + nextOpponentFormatted + '.')
else:
    print(formattedPlayerName + ' has not played ' + nextOpponentFormatted + ' yet.')
print(' ')

#Below is the basketball reference code I decided to axe bc it was not effective

#driver.get('https://www.basketball-reference.com/')

#search = driver.find_element_by_xpath('//*[@id="header"]/div[3]/form/div/div/input[2]').send_keys(playerName)
#isRetired = driver.find_element_by_xpath('//*[@id="header"]/div[3]/form/div/div/div/div[1]/div[2]/div[1]/div/span[1]').text
#submit = driver.find_element_by_xpath('//*[@id="header"]/div[3]/form/div/div/div/div[1]/div[2]/div[1]').click()

#window_after = driver.window_handles[0]
#driver.switch_to.window(window_after)

#playerName = driver.find_element_by_xpath('//*[@id="meta"]/div[2]/h1/span').text

#if len(isRetired) > 4:
#    isRetired = isRetired[5:9]

#if isRetired != "2021":
#    careerAvgPts = driver.find_element_by_xpath('//*[@id="info"]/div[4]/div[2]/div[2]/p[2]').text
#    careerAvgReb = driver.find_element_by_xpath('//*[@id="info"]/div[4]/div[2]/div[3]/p[2]').text
#    careerAvgAst = driver.find_element_by_xpath('//*[@id="info"]/div[4]/div[2]/div[4]/p[2]').text

#    print(playerName + ' is retired. For his career he averaged ' + careerAvgPts + ' points, ' + careerAvgReb + ' rebounds, and ' + careerAvgAst + ' assists.')
#    sys.exit()

#currentSeason = driver.find_element_by_xpath('//*[@id="per_game.2021"]/th/a').click() 

#window_after = driver.window_handles[0]
#driver.switch_to.window(window_after)

#points = []
#rebounds = []
#assists = []

#for table in driver.find_elements_by_xpath('//*[@id="pgl_basic"]//tr'): 
#    data = [item.text for item in table.find_elements_by_xpath(".//*[self::td]")]
#    if len(data) > 10:
#        points.append(int(data[26]))
#        rebounds.append(int(data[20]))
#        assists.append(int(data[21]))

#averagePoints = sum(points) / len(points)
#averageRebounds = sum(rebounds) / len(rebounds)
#averageAssists = sum(assists) / len(assists)

#formattedAvgPts = "{:.1f}".format(averagePoints)
#formattedAvgReb = "{:.1f}".format(averageRebounds)
#formattedAvgAst = "{:.1f}".format(averageAssists)

#lastFivePoints = []
#lastFiveRebounds = []
#lastFiveAssists = []

#for x in range(len(points) - 5, len(points)):
#    lastFivePoints.append(points[x])
#    lastFiveRebounds.append(rebounds[x])
#    lastFiveAssists.append(assists[x])

#lastFiveAveragePoints = sum(lastFivePoints) / len(lastFivePoints)
#lastFiveAverageRebounds = sum(lastFiveRebounds) / len(lastFiveRebounds)
#lastFiveAverageAssists = sum(lastFiveAssists) / len(lastFiveAssists)

#formattedL5AvgPts = "{:.1f}".format(lastFiveAveragePoints)
#formattedL5AvgReb = "{:.1f}".format(lastFiveAverageRebounds)
#formattedL5AvgAst = "{:.1f}".format(lastFiveAverageAssists)

#print(playerName + ' has averaged ' + formattedAvgPts + ' points, ' + formattedAvgReb + ' rebounds, and ' + formattedAvgAst + ' assists.')
#print(playerName + ' has averaged ' + formattedL5AvgPts + ' points, ' + formattedL5AvgReb + ' rebounds, and ' + formattedL5AvgAst + ' assists in his last 5 games.')