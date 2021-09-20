rom os import getgid
import sys
import pandas as pd
from selenium import webdriver
from itertools import combinations
from time import sleep
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
from random import random

LOGIN_PAGE = 'https://www.linkedin.com/login'

# Local references.
CHROMIUM_DRIVER = './selenium_driver/chromedriver.exe'
DATA_FILE = 'data.xlsx'
NAMES_COLUMN = 'NAMES'
COLUMN_BREAK = 'done'
SUCCESS_MONITOR = 'successfulConnections.txt'
UNSUCCESS_MONITOR = 'unsuccessfulConnections.txt'

# Page elements.
USERNAME_TEXTBOX = 'username'
PASSWORD_TEXTBOX = 'password'
SIGN_IN_BUTTON = "//*[@id='organic-div']/form/div[3]/button"
CONNECT_BUTTON = '//span[text()="Connect"]'
ADD_NOTE_BUTTON = "//button/span[text()='Add a note']/.."
MESSAGE_BOX = 'custom-message'  
SEND_NOTE_BUTTON =  'ml1'

# Personalization.
MSG = ''                       					# <--------------- Personnalized message here
SCHOOL_NAME = ''                                                # <--------------- School keyword here.
USERNAME = ''                                                   # <--------------- LinkedIn email or phone here.
PASSWORD = ''                                                   # <--------------- LinkedIn password here.
MIN_DELAY = 1
MAX_DELAY = 5

def config() :
    browser = webdriver.Chrome(CHROMIUM_DRIVER)
    browser.get(LOGIN_PAGE)

    elementID = browser.find_element_by_id(USERNAME_TEXTBOX)
    elementID.send_keys(USERNAME)                                                

    elementID = browser.find_element_by_id(PASSWORD_TEXTBOX)                      
    elementID.send_keys(PASSWORD)

    browser.find_element_by_xpath(SIGN_IN_BUTTON).click()

    input('\nComplete POTENTIAL 2-step auth. and press ENTER (if not completed, could cause error).......\n')

    return browser

def timeStamp(note) :
    with open(SUCCESS_MONITOR, 'a') as succesfulConFile:
        succesfulConFile.write('\n--------------------|' + note + ':     ' + str(datetime.now()) + '     |--------------------\n')
    succesfulConFile.close()
    with open(UNSUCCESS_MONITOR, 'a') as unsuccesfulConFile:
        unsuccesfulConFile.write('\n--------------------|' + note + ':     ' + str(datetime.now()) + '     |--------------------\n')
    unsuccesfulConFile.close()

timeStamp('START')

# Setup
workbook = pd.read_excel(DATA_FILE)
workbook.head()
browser = config()
names = workbook[NAMES_COLUMN]

# Main execution
for name in names :
    if name == COLUMN_BREAK : break

    # Data manipulation.
    firstName = name[0 : name.index(' ')]
    name = name.replace(firstName + ' ', '')
    lastNames = []
    # Lists all middle and last names, to permutate and match them in the LinkedIn search filter.
    while len(name) != 0 :
        try :
            temp = name[0 : name.index(' ')]
        except ValueError:
            temp = name[0 : len(name)]
        lastNames.append(temp)
        name = name.replace(temp + ' ', '')
        name = name.replace(temp, '')
    combinationsTwo = list(combinations(lastNames, 2))
    combinationsThree = list(combinations(lastNames, 3))
    for combination in combinationsTwo :
        lastNames.append(combination[0] + '%20' + combination[1])
    for combination in combinationsThree :
        lastNames.append(combination[0] + '%20' + combination[1] + '%20' + combination[2])

    # Searching and attempting to connect to respective name given multiple last name permutations.
    # When a name is succesfully sent a connection request, the other last name permutation searches are skiped.
    for lastName in lastNames :
	sleep(random.uniform(MIN_DELAY, MAX_DELAY))
        link = 'https://www.linkedin.com/search/results/people/?firstName=' + firstName + '&lastName=' + lastName + '&origin=FACETED_SEARCH&schoolFreetext=%22' + SCHOOL_NAME + '%22&sid=)k5'
        browser.get(link)

        try :
            # Attempt connection
            browser.find_element_by_xpath(CONNECT_BUTTON).click()
            browser.find_element_by_xpath(ADD_NOTE_BUTTON).click()
            elementID = browser.find_element_by_id(MESSAGE_BOX)
            elementID.send_keys(MSG)
            browser.find_element_by_class_name(SEND_NOTE_BUTTON).click()
            
            # Monitoring
            with open(SUCCESS_MONITOR, 'a') as succesfulConFile:
                succesfulConFile.write(firstName + ' ' + lastNames[len(lastNames) - 1].replace('%20', ' ') + '\n')
            succesfulConFile.close()
            print('CONNECTED to:    ' + firstName)

            # Moves to next name
            break
        except NoSuchElementException :
            # Since trying multiple last-name permutations
            if lastNames[len(lastNames) - 1] == lastName :
                # Monitoring
                print('Did NOT connect to:    ' + firstName)
                with open(UNSUCCESS_MONITOR, 'a') as unsuccesfulConFile:
                    unsuccesfulConFile.write(firstName + ' ' + lastNames[len(lastNames) - 1].replace('%20', ' ') + '\n')
                unsuccesfulConFile.close()


browser.close
timeStamp('END')
