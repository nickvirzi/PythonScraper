import time
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import datetime

#Get initial input
playerNameInput = input("Enter player name: ")

#Gets current month
currentDate = datetime.datetime.now()
currentMonth = currentDate.strftime("%B")

#Sets up driver
DRIVER_PATH = r'C:\Users\navir\Documents\ChromeDriver\chromedriver.exe'
driver = webdriver.Chrome(executable_path=DRIVER_PATH)
driver.get('https://www.espn.com/')

#Take in team name and return the ESPN team abbreviation
def getESPNTeamAbbreviation(teamName):
    teamAbbreviationDictionary = {
        'Atlanta': 'ATL', 'Boston': 'BOS', 'Charlotte': 'CHA', 'Chicago': 'CHI', 'Cleveland': 'CLE', 'Dallas': 'DAL', 'Denver': 'DEN', 'Detroit': 'DET', 'Houston': 'HOU', 'Indiana': 'IND', 'Memphis': 'MEM',
        'Miami': 'MIA', 'Miluakee': 'MIL', 'Minnesota': 'MIN', 'Orlando': 'ORL', 'Philadelphia': 'PHI', 'Phoenix': 'PHO', 'Portland': 'POR', 'Sacramento': 'SAC', 'Toronto': 'TOR', 'Utah': 'UTA', 'Washington': 'WAS',
        'Golden State': 'GS', 'New Orleans': 'NO', 'New York': 'NY', 'San Antonio': 'SA'
    }
    abbreviation = teamAbbreviationDictionary[teamName]
    return abbreviation

def findAndSelectPlayerESPN(playerName):
    #Search players name on ESPN
    driver.find_element_by_xpath('//*[@id="global-search-trigger"]').click()
    driver.find_element_by_xpath('//*[@id="global-search"]/input[1]').send_keys(playerName)
    driver.find_element_by_xpath('//*[@id="global-search"]/input[2]').click()

    window_after = driver.window_handles[0]
    driver.switch_to.window(window_after)

    time.sleep(2)

    #Filter results to players only to avoid clicking articles
    driver.find_element_by_xpath('//*[@id="fittPageContainer"]/div[2]/div/div/ul/li[2]/a').click()

    window_after = driver.window_handles[0]
    driver.switch_to.window(window_after)

    time.sleep(2)

    #Select player
    driver.find_element_by_xpath('//*[@id="fittPageContainer"]/div[2]/div/div/section/div/ul/div/div/li/section').click()

    window_after = driver.window_handles[0]
    driver.switch_to.window(window_after)

def getTeamSchedule():
    #Click the players team
    driver.find_element_by_xpath('//*[@id="fittPageContainer"]/div[2]/div[1]/div/div/div[1]/div[1]/div[2]/div/ul/li[1]').click()

    window_after = driver.window_handles[0]
    driver.switch_to.window(window_after)

    #Clicking teams schedule 
    driver.find_element_by_xpath('//*[@id="global-nav-secondary"]/div[2]/ul/li[4]/a').click()

    window_after = driver.window_handles[0]
    driver.switch_to.window(window_after)

def goToPlayerSplits():
    #Click Game Splits
    driver.find_element_by_xpath('//*[@id="fittPageContainer"]/div[2]/div[2]/nav/ul/li[5]/a').click()

    window_after = driver.window_handles[0]
    driver.switch_to.window(window_after)

    time.sleep(5)

class player:
    def __init__(self,name):
        self.name = name

    def getFormattedName(self):
        #Get players name formatted properly
        formattedFirstName = driver.find_element_by_xpath('//*[@id="fittPageContainer"]/div[2]/div[1]/div/div/div[1]/div[1]/div[2]/h1/span[1]').text
        formattedLastName = driver.find_element_by_xpath('//*[@id="fittPageContainer"]/div[2]/div[1]/div/div/div[1]/div[1]/div[2]/h1/span[2]').text

        self.formattedPlayerName = formattedFirstName + ' ' + formattedLastName

    def getSeasonAverages(self):
        #Grabe average stats for the player for the season
        self.averagePoints = driver.find_element_by_xpath('//*[@id="fittPageContainer"]/div[2]/div[1]/div/div/div[2]/aside/ul/li[1]/div/div[2]').text
        self.averageRebounds = driver.find_element_by_xpath('//*[@id="fittPageContainer"]/div[2]/div[1]/div/div/div[2]/aside/ul/li[2]/div/div[2]').text
        self.averageAssists = driver.find_element_by_xpath('//*[@id="fittPageContainer"]/div[2]/div[1]/div/div/div[2]/aside/ul/li[3]/div/div[2]').text

        self.playerURL = driver.current_url

        time.sleep(2)

        driver.execute_script("window.scrollTo(0,0)")

    def getPlayersTeam(self):
        self.teamName = driver.find_element_by_xpath('//*[@id="fittPageContainer"]/div[2]/div[1]/div/div/div[1]/div[1]/div[2]/div/ul/li[1]/a').text

    def getNextOpponentAndDaysRest(self):
        previousMatchupClause = True

        #Grabbing next opponent for the players team
        for tableRow in driver.find_elements_by_xpath('//*[@id="fittPageContainer"]/div[2]/div[5]/div/div[1]/section/div/section/section/div/div/div/div[2]/table//tr'): 
            dataThree = [item.text for item in tableRow.find_elements_by_xpath(".//*[self::td]")]
            if len(dataThree) > 3: #This if statement helps to prevent postponed games
                if dataThree[3] == '':
                    self.nextOpponent = dataThree[1]
                    nextGameDateUnformatted = dataThree[0]
                    break
                elif len(dataThree) == 5 and previousMatchupClause == True:
                    previousMatchupData = previousData
                    previousMatchupClause = False
                previousData = dataThree

        nextGameDate = nextGameDateUnformatted[9:]
        previousGameDate = previousMatchupData[0][9:]
        self.daysRestInt = (int(nextGameDate) - int(previousGameDate)) - 1

    def getNextOpponentFormattedAndAbbreviated(self):
        #Formatting and handling the team name and getting the abbreviation and determine home or away game
        if '@' in self.nextOpponent:
            self.nextOpponentFormatted = self.nextOpponent[2:]
            self.nextGame = 'Road'
        else:
            self.nextOpponentFormatted = self.nextOpponent[3:]
            self.nextGame = 'Home'

        nextOpponentAbbreviated = getESPNTeamAbbreviation(self.nextOpponentFormatted)

        self.addVSAbbrev = 'vs ' + nextOpponentAbbreviated

    def getPlayerSplits(self,currentMonth):
        dataCounterOne = 0
        dataCounterTwo = 0
        awayGameCounter = 0
        homeGameCounter = 0
        
        self.vsTeamCounter = 0

        #Set up to find days rest in the table
        daysRest = ["0 Days Rest", "1 Days Rest", "2 Days Rest", "3+ Days Rest"]

        time.sleep(5)

        #ESPN has a headers column, this grabs the location to use in the table of data for corresponding row
        for tableRow in driver.find_elements_by_xpath('//*[@id="fittPageContainer"]/div[2]/div[5]/div/div/div[1]/section/div[1]/div[2]/div/table//tr'): 
            data = [item.text for item in tableRow.find_elements_by_xpath(".//*[self::td]")]
            dataCounterOne += 1
            if currentMonth == data[0]:
                curMonthCounter = dataCounterOne
            elif 'Home' == data[0]:
                homeGameCounter = dataCounterOne
            elif 'Road' == data[0]:
                awayGameCounter = dataCounterOne
            elif daysRest[0] == data[0]:
                zeroDaysRestCounter = dataCounterOne
            elif daysRest[1] == data[0]:
                oneDaysRestCounter = dataCounterOne
            elif daysRest[2] == data[0]:
                twoDaysRestCounter = dataCounterOne
            elif daysRest[3] == data[0]:
                threePlusDaysCounter = dataCounterOne
            elif self.addVSAbbrev == data[0]:
                self.vsTeamCounter = dataCounterOne

        self.awayGameSplits = []
        self.homeGameSplits = []

        #This loop grabs the stats from the other side of the table
        for tableRow in driver.find_elements_by_xpath('//*[@id="fittPageContainer"]/div[2]/div[5]/div/div/div[1]/section/div[1]/div[2]/div/div/div[2]/table//tr'): 
            dataTwo = [item.text for item in tableRow.find_elements_by_xpath(".//*[self::td]")]
            dataCounterTwo += 1
            if curMonthCounter == dataCounterTwo:
                self.curMonthSplits = dataTwo
            elif homeGameCounter == dataCounterTwo:
                self.homeGameSplits = dataTwo
            elif awayGameCounter == dataCounterTwo:
                self.awayGameSplits = dataTwo
            elif zeroDaysRestCounter == dataCounterTwo:
                self.zeroDaysRestSplits = dataTwo
            elif oneDaysRestCounter == dataCounterTwo:
                self.oneDaysRestSplits = dataTwo
            elif twoDaysRestCounter == dataCounterTwo:
                self.twoDaysRestSplits = dataTwo
            elif threePlusDaysCounter == dataCounterTwo:
                self.threePlusDaysRestSplits = dataTwo
            elif self.vsTeamCounter == dataCounterTwo:
                self.vsTeamSplits = dataTwo

    def printPlayerData(self,currentMonth):
        #Outputing the data in written form
        print(' ')

        print(self.formattedPlayerName + ' has averaged ' + self.averagePoints + ' points, ' + self.averageRebounds + ' rebounds, and ' + self.averageAssists + ' assists this season.')

        print(' ')

        print(self.formattedPlayerName + ' in ' + currentMonth + ' has averaged ' + self.curMonthSplits[16] + ' points, ' + self.curMonthSplits[10] + ' rebounds, and ' + self.curMonthSplits[11] + ' assists in ' + self.curMonthSplits[0] + ' games.')
        print(self.formattedPlayerName + ' in ' + currentMonth + ' is shooting ' + self.curMonthSplits[3] + ' percent from the field and ' + self.curMonthSplits[5] + ' percent from three.')
        
        print(' ')

        if self.vsTeamCounter != 0:
            print(self.formattedPlayerName + ' has played ' + self.nextOpponentFormatted + ' ' + self.vsTeamSplits[0] + ' times. He has averaged ' + self.vsTeamSplits[16] + ' points, ' + self.vsTeamSplits[10] + ' rebounds, and ' + self.vsTeamSplits[11] + ' assists.')
            print(self.formattedPlayerName + ' is shooting ' + self.vsTeamSplits[3] + ' percent from the field and ' + self.vsTeamSplits[5] + ' percent from three against ' + self.nextOpponentFormatted + '.')
        else:
            print(self.formattedPlayerName + ' has not played ' + self.nextOpponentFormatted + ' yet.')

        print(' ')

        if self.daysRestInt == 0:
            print(self.formattedPlayerName + ' has had ' + str(self.daysRestInt) + ' days since his last game.')
            print(self.formattedPlayerName + ' has averaged ' + self.zeroDaysRestSplits[16] + ' points, ' + self.zeroDaysRestSplits[10] + ' rebounds, and ' + self.zeroDaysRestSplits[11] + ' assists with ' + str(self.daysRestInt) + ' days rest in ' + self.zeroDaysRestSplits[0] + ' games.')
            print(self.formattedPlayerName + ' is shooting ' + self.zeroDaysRestSplits[3] + ' percent from the field and ' + self.zeroDaysRestSplits[5] + ' percent from three with ' + str(self.daysRestInt) + ' days rest in ' + self.zeroDaysRestSplits[0] + ' games.')
        elif self.daysRestInt == 1:
            print(self.formattedPlayerName + ' has had ' + str(self.daysRestInt) + ' days since his last game.')
            print(self.formattedPlayerName + ' has averaged ' + self.oneDaysRestSplits[16] + ' points, ' + self.oneDaysRestSplits[10] + ' rebounds, and ' + self.oneDaysRestSplits[11] + ' assists with ' + str(self.daysRestInt) + ' days rest in ' + self.oneDaysRestSplits[0] + ' games.')
            print(self.formattedPlayerName + ' is shooting ' + self.oneDaysRestSplits[3] + ' percent from the field and ' + self.oneDaysRestSplits[5] + ' percent from three with ' + str(self.daysRestInt) + ' days rest in ' + self.oneDaysRestSplits[0] + ' games.')
        elif self.daysRestInt == 2:
            print(self.formattedPlayerName + ' has had ' + str(self.daysRestInt) + ' days since his last game.')
            print(self.formattedPlayerName + ' has averaged ' + self.twoDaysRestSplits[16] + ' points, ' + self.twoDaysRestSplits[10] + ' rebounds, and ' + self.twoDaysRestSplits[11] + ' assists with ' + str(self.daysRestInt) + ' days rest in ' + self.twoDaysRestSplits[0] + ' games.')
            print(self.formattedPlayerName + ' is shooting ' + self.twoDaysRestSplits[3] + ' percent from the field and ' + self.twoDaysRestSplits[5] + ' percent from three with ' + str(self.daysRestInt) + ' days rest in ' + self.twoDaysRestSplits[0] + ' games.')
        elif self.daysRestInt >= 3:
            print(self.formattedPlayerName + ' has had ' + str(self.daysRestInt) + ' days since his last game.')
            print(self.formattedPlayerName + ' has averaged ' + self.threePlusDaysRestSplits[16] + ' points, ' + self.threePlusDaysRestSplits[10] + ' rebounds, and ' + self.threePlusDaysRestSplits[11] + ' assists with ' + str(self.daysRestInt) + ' days rest in ' + self.threePlusDaysRestSplits[0] + ' games.')
            print(self.formattedPlayerName + ' is shooting ' + self.threePlusDaysRestSplits[3] + ' percent from the field and ' + self.threePlusDaysRestSplits[5] + ' percent from three with ' + str(self.daysRestInt) + ' days rest in ' + self.threePlusDaysRestSplits[0] + ' games.')
        
        print(' ')

        if self.nextGame == 'Home':
            print(self.formattedPlayerName + ' has a ' + self.nextGame + ' game next.')
            print(self.formattedPlayerName + ' in ' + self.nextGame + ' games has averaged ' + self.homeGameSplits[16] + ' points, ' + self.homeGameSplits[10] + ' rebounds, and ' + self.homeGameSplits[11] + ' assists in ' + self.homeGameSplits[0] + ' games.')
            print(self.formattedPlayerName + ' in ' + self.nextGame + ' games is shooting ' + self.homeGameSplits[3] + ' percent from the field and ' + self.homeGameSplits[5] + ' percent from three in ' + self.homeGameSplits[0] + ' games.')
        elif self.nextGame == 'Road':
            print(self.formattedPlayerName + ' has a ' + self.nextGame + ' game next.')
            print(self.formattedPlayerName + ' in ' + self.nextGame + ' games has averaged ' + self.awayGameSplits[16] + ' points, ' + self.awayGameSplits[10] + ' rebounds, and ' + self.awayGameSplits[11] + ' assists in ' + self.awayGameSplits[0] + ' games.')
            print(self.formattedPlayerName + ' in ' + self.nextGame + ' games is shooting ' + self.awayGameSplits[3] + ' percent from the field and ' + self.awayGameSplits[5] + ' percent from three in ' + self.awayGameSplits[0] + ' games.')
        
        print(' ')

#Begin Main
player = player(playerNameInput)

findAndSelectPlayerESPN(player.name)

player.getFormattedName()
player.getSeasonAverages()
player.getPlayersTeam()

getTeamSchedule()

player.getNextOpponentAndDaysRest()
player.getNextOpponentFormattedAndAbbreviated()

#Go back to the players profile to then determine splits based upon opponent 
driver = webdriver.Chrome(executable_path=DRIVER_PATH)
driver.get(player.playerURL)

window_after = driver.window_handles[0]
driver.switch_to.window(window_after)

goToPlayerSplits()

player.getPlayerSplits(currentMonth)
player.printPlayerData(currentMonth)

#TODO Potentially add code to check how injured games are handled by days rest
#TODO Add matchup defense data