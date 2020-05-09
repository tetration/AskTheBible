#!/usr/bin/env python 
#AskTheBible made by Rafael Oliveira/Tetration
#Github author address: https://github.com/tetration
#Github repository: tetration/AskTheBible
#Contact: rafael@theancientscroll.com
#Written for Python 3.X

import time
import re
import secrets
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from operator import methodcaller


versesList = [None]
searchList = ["jesus","struggles", "challenges", "bearing with one another","dreams","love","life", "marriage", "gold", "humility", "humble", "Kingdom come","wisdom", "judgement", "judgemental", "patience", "destiny", "sheep","path", "rewards", "enemies", "betrayal", "hardships", "overcoming hardships", "peace", "forgiving", "temptation" , "christ", "devil", "heaven", "hell", "damnation", "child", "wine", "food", "shelter", "future", "present", "past", "disease", "diseases", "cure", "heal", "holy spirit", "defile"]

class Biblical_verse:
    def __init__(self, verse_location, bible_version, verse_content):
        self.verse_location = verse_location
        self.bible_version = bible_version
        self.verse_content = verse_content
    def show_verse(self):
        print(self.verse_location)
        print("Bible version:", self.bible_version, sep=" ")
        print(self.verse_content)


def remove_html_tags(text):
    """Remove html tags from a string"""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)
def getNumbers(str): 
    array = re.findall(r'[0-9]+', str)
    return array 

def RemoveEverythingAfter(word ,removeeverythingafterThisWord):
    split_string = word.split(removeeverythingafterThisWord, 1)
    substring = split_string[0]
    return substring

def GetBiblicalVerses(driver, userQuestion):
    print("Getting a list of verses about", userQuestion,"...", sep=" ")
    
    try:
        table= driver.find_element_by_id("vote")
        WebDriverWait(driver, 4).until(table)
    except:
        print ('Timed out waiting for page to load') 
    
    biblicalVerse = table.find_elements_by_tag_name('div') 

    for items in biblicalVerse:
        title = items.find_element_by_css_selector("h3 > a").text
        bible_version = RemoveEverythingAfter(items.find_element_by_css_selector("h3 > span.note").text, "/")
        content = items.find_element_by_tag_name("p").text
        #print("The title is: ", title)
        #print("Bible version is: ", bible_version)
        #print("Content :",content)
        create_verse = Biblical_verse(title, bible_version, content)
        #create_verse.show_verse()
        versesList.append(create_verse)

    versesList.pop(0) 
    for create_verse in versesList:
        create_verse.show_verse()
    print("\n This is a list of biblical verses found. Press enter to continue...")
    userpress=input()
    driver.quit() 

def SearchAboutUserQuestionInTheBible(userQuestion):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless");
    options.add_argument("--disable-gpu");
    options.add_argument("--disable-images");
    options.add_argument('--disable-extensions')
    options.add_argument("--ignore-certificate-errors");
    options.add_argument("--disable-popup-blocking");

    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    prefs = {"profile.managed_default_content_settings.popups":2,"profile.default_content_setting_values.notifications": 2,"profile.default_content_setting_values.images": 2,"profile.password_manager_enabled": False, "credentials_enable_service": False}
    options.add_experimental_option("prefs", prefs)
    
    driver = webdriver.Chrome(chrome_options=options)
    driver.get("https://www.openbible.info/topics/")
    element = driver.find_element_by_id("search")
    element.send_keys(userQuestion)
    try:
        element.send_keys(Keys.ENTER)
    except:
        print("Trying to search again")
        element.send_keys(Keys.ENTER)
    found=driver.find_element_by_css_selector("#body > h1 > span").get_attribute("innerHTML")
    found = remove_html_tags(found)
    found = re.findall(r'[0-9]+', found)
    #found = getNumbers(found)
    #re.match(r'^[-+]?([1-9]\d*|0)$', found)
    print("Found", found, "Bible verses about", userQuestion ,sep=" ")
    GetBiblicalVerses(driver,userQuestion);

def WhatToDo():
    option=menu()
    if option =='1':
        print("Type what you would like to search about in the Bible")
        question=input();
        SearchAboutUserQuestionInTheBible(question)
    elif option == '2':
        randomPick=secrets.choice(searchList)
        SearchAboutUserQuestionInTheBible(randomPick)
    elif option =='3':
        print("The program will now exit")

def menu():
    userInput="";
    corretOption= False
    while corretOption==False:
        print("What would you like to do today?")
        print("1- Search what does the Bible say about something")
        print("2- Surprise me")
        print("3- Exit")
        userInput=input();
        if userInput=='1':
            corretOption=True
            break
        elif userInput=='2':
            corretOption=True
            break
        elif userInput=='3':
            corretOption=True
            break
        else:
            print("Invalid choice, please pick one of the options avaliable")
    return userInput


def main():
        print("Welcome to AskTheBible!")
        WhatToDo()
        print("Thanks for using AskTheBible")
        print("The program will now exit")
        exit()

main()