#!/usr/bin/env python3
#AskTheBible made by Rafael Oliveira/Tetration
#Github author address: https://github.com/tetration
#Github repository: tetration/AskTheBible
#Contact: rafael@theancientscroll.com
#Written for Python 3.X
import os 
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
from gtts import gTTS 
from playsound import playsound

versesList = [None]
searchList = ["holy trinity","trinity", "father", "mother", "water", "wicked","worship","sea", "sloth", "fake friends","fish", "focus","jesus", "jew","jealous", "envy","forthcoming","struggles", "challenges", "witness","bearing with one another", "boredom", "being hated", "dreams", "daugther", "death", "darkness","prosperity","eternity", "book of life", "Lazarus","love","life", "light","marriage", "gold", "humility", "humble", "Kingdom","Kingdom come","wisdom", "judgement", "judgemental", "patience", "pride","destiny", "sheep","path", "rewards", "right girl","enemies", "betrayal", "traitor", "hardships", "hate", "heresy", "overcoming hardships", "peace", "redemption","forgiving", "temptation" , "christ", "devil", "demon", "persist","purgatory", "heaven", "hell", "damnation", "child", "wine", "food", "shelter", "future", "present", "past", "distress","disease", "diseases", "cure", "heal", "holy spirit", "defile", "repent", "son", "Solomon", "sin", "apocalypse", "slave", "free", "freedom", "plague", "egypt", "romans", "greek", "hebrew", "false prophet", "sorcery", "witchcraft", "serpent", "beast", "dragon", "rage","fallen angel", "flesh", "avenger", "authorities", "government", "governor","tax collector", "end of the world", "end of times"]

class Biblical_verse:
    def __init__(self, verse_location, bible_version, verse_content):
        self.verse_location = verse_location
        self.bible_version = bible_version
        self.verse_content = verse_content
    def show_verse(self):
        print(self.verse_location)
        print("Bible version:", self.bible_version, sep=" ")
        print(self.verse_content)
    def returnStringOfEntireVerse(self):
        entireVerse= self.verse_location+"\n"+self.bible_version+"\n"+self.verse_content+"\n"
        return entireVerse
    def Get_Verse_for_Audio_Conversion(self):
        everything = self.verse_location + " " + self.verse_content 
        return everything

def checkIfFileAlreadyExists(Filename):
    #checks if file exists in current directory this python script is located at
    tf=os.path.exists(Filename)
    return tf


def user_hasRequiredModules():
    print("Checking if user has required modules")

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
        index= versesList.index(create_verse)
        print("Position", index,sep = " ")
        print("")
        create_verse.show_verse()
        print("")
    driver.quit()
    print("\n This is a list of biblical verses about", userQuestion ,"found.\n", sep=" ")
     

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
    GetBiblicalVerses(driver,userQuestion)
    DecisionText(userQuestion)
    DecisionAudio(userQuestion)


def DecisionText(userQuestion):
    saveOrNot = saveTextMenu(userQuestion)
    if saveOrNot=='1' or saveOrNot =='2':
        saveFilesToTXTOrPDF(saveOrNot, userQuestion)

def DecisionAudio(userQuestion):
    saveAudioOrNot=saveAudioMenu(userQuestion)
    if saveAudioOrNot=='1':
        convertSpecificTextVerseToAudio(userQuestion)
    elif saveAudioOrNot == '2':
        convertAllTextVersesToAudio(userQuestion)
        

def saveTextMenu(userSearch):
    userInput=""
    corretOption= False
    while corretOption==False:
        print("Would you like to also save the biblical verses that we found about ", userSearch,"?" ,sep="")
        print("1- Save the Biblical verses in a txt file")
        print("2- Save the Biblical verses in a PDF file")
        print("3- Don't save")
        userInput=input();
        if userInput=='1':
            corretOption=True
            break
        elif userInput=="2":
            print("For now, option", userInput, "does nothing, come back later to check if the developer implements the option to save to pdf yet", sep=" ")
            corretOption=True
            break
        elif userInput=='3':
            corretOption=True
            break
        else:
            print("Invalid choice, please pick one of the options avaliable")
    return userInput

def saveAudioMenu(userSearch):
    userAnswer=""
    userAnswered=False
    while userAnswered==False:
        print("Convert Text to Speech Menu")
        print("Would you like to also Convert the biblical text that we found about", userSearch,"to Speech(audio file)?" ,sep=" ")
        print("1 - Convert a specific Biblical Verse to an Audio File (need to know its position number in our table)")
        print("2 - Convert all Biblical Texts found about",  userSearch, "to an Audio File ", "?", sep=" ")
        print("3 - Exit AskTheBible without converting verses about",  userSearch, "to an Audio File ", "?", sep=" ")
        userAnswer=input()
        if userAnswer=="1":
            userAnswered=True
            break
        elif userAnswer=="2":
            userAnswered=True
            break
        elif userAnswer=='3':
            userAnswered=True
            break
        else:
            print("Invalid choice, please pick one of the options avaliable")
        #print("Going back to SaveTextMenu....")
    return userAnswer

def convertAllTextVersesToAudio(userQuestion):
    if not versesList:
        print("Error can't convert any text the list seems empty")
        print("The program will now exit")
        exit()

    print("Converting all Biblical Texts about", userQuestion,"to an Audio File", sep=" ")
    mytext = ' Philippians 4:13 \n ESV \n I can do all things through him who strengthens me.'
    language = 'en'
    listSize=len(versesList)
    finalpath="biblical_verses_about_{userQ}".format(userQ=userQuestion)
    os.mkdir(finalpath)
    for create_verse in versesList:
        index= versesList.index(create_verse)
        #print("Position", index,sep = " ")
        mytext=create_verse.Get_Verse_for_Audio_Conversion()
        myobj = gTTS(text=mytext, lang=language, slow=False)
        oldname= create_verse.verse_location
        oldname = oldname.replace(":", "_")
        filename=oldname+".mp3"
        myobj.save("biblical_verses_about_{userQ}\{filenam}".format(userQ=userQuestion,filenam=filename)) 
        filelocation= os.path.dirname(os.path.realpath(finalpath+"\\"+filename))
        print("Created mp3 file for verse", create_verse.verse_location,"which can be located at", filelocation,"under the name of", filename, sep=" ")
        print(versesList.index(create_verse)+1, "out of", listSize,"verses to convert to mp3 left", sep=" ")
    print("")
    print("Finished converting all Biblical verses about", userQuestion, "to mp3 files", sep= " ")
     
    
def convertSpecificTextVerseToAudio(userQuestion):
    if not versesList:
        print("Error cant convert any text the list seems empty")
        print("The program will now exit")
        exit()
    for create_verse in versesList:
        index= versesList.index(create_verse)
        print("Position", index,sep = " ")
        print("")
        create_verse.show_verse()
        print("")

    print("Which verse would you like to pick? Please, type its position on the list as shown in the list above")
    userAnswer=""
    userAnswered=False
    listSize=len(versesList)
    shift = -1
    while 0 > shift or listSize < shift and userAnswered==False:
        try:
            print("Please enter the location of the verse you which to convert to mp3 (0 - ", len(versesList), ") : ",sep="")
            shift = int(input())
            userAnswer=True
        except ValueError:
            print ("Error: Value typed is out of range, please type a number in the range of biblical verses found about", userQuestion, sep=" ")
    mytext = ''
    language = 'en'
    verse= versesList[shift]
    #print("Position", index,sep = " ")
    mytext=verse.Get_Verse_for_Audio_Conversion()
    myobj = gTTS(text=mytext, lang=language, slow=False)
    oldname= verse.verse_location
    oldname = oldname.replace(":", "_")
    filename=oldname+".mp3"
    myobj.save(filename) 
    filelocation= os.path.dirname(os.path.realpath(filename))
    print("Created mp3 file for verse", verse.verse_location,"which can be located at", filelocation, "under the name of", filename, sep=" ")

def saveFilesToTXTOrPDF(userChoice, userQuestion):
    if not versesList:
        print("Error cant convert any text the list seems empty")
        print("The program will now exit")
        exit()
    print("Saving log in")
    if userChoice=='1':
        print("Saving verses about", userQuestion,"to a txt file...", sep=" ")
        filename= "BibleVersesAbout_"+userQuestion+".txt"
        with open(filename, 'w') as output:
            for verse in versesList:
                output.write(str(verse.returnStringOfEntireVerse()) + '\n')
        print("Finished generating text file called", filename,"with Biblical verses about", userQuestion, sep=" ")
        filelocation= os.path.dirname(os.path.realpath(filename))
        print("The file can be found at:",filelocation,sep=" ")
    elif userChoice =='2':
        print("Saving verses about",  userQuestion, "to a PDF file...", sep=" ")
        print("This feature is not ready yet. Come back later, to check if the developer has already implemented the option to save to a pdf file")

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
        print("Exiting the program")

def menu():
    userInput=""
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

def startProgram():
    if(checkIfFileAlreadyExists("chromedriver.exe")):
        WhatToDo()
    else:
        print("Error, couldn't find chromedriver.exe")
        print("It looks like you haven't downloaded and placed chromedriver executable yet in the folder where this script is located")
        print("Please, download the right chromedriver version corresponding to the current version you have installed of chrome browser and place it")
        print("You can download chromedriver at: https://chromedriver.chromium.org/downloads")
        print("Once you do this try to run this script again after you have done these steps.")

def main():
        print("Welcome to AskTheBible!")
        startProgram()
        print("Thanks for using AskTheBible and remember, the devil finds work for idle hands. So, keep yourself busy!")
        print("The program will now exit")
        exit()

main()