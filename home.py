import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import subprocess as sp
import os
import pyjokes
import random
import tkinter
from tkinter import *
from PIL import Image, ImageTk
from tkinter import BOTH
import pyautogui
import json
import sqlite3
from plyer import notification
import time

#-----------------------------------------------------------------

engine=pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)
newVoiceRate = 180
engine.setProperty('rate',newVoiceRate);
conn = sqlite3.connect('assignment_data.db') #connecting to the database
cur = conn.cursor() #saving it in cur
cur.execute('''SELECT * FROM ass_data''')
user_data = cur.fetchall()
#-----------------------------------------------------------------

def speak(audio):
    # string to speaker
    engine.say(audio)
    engine.runAndWait()

def time(): #reads out the current time
    Time=datetime.datetime.now().strftime("%H:%M:%S")
    speak("Now the time is")
    speak(Time)

def date(): #speaks out current year
    year=datetime.datetime.now().year #extracts year from now and saves it in integer format 
    speak("you are in year")
    speak(year)


def wishme():
    speak("Welcome back!")
    hour = datetime.datetime.now().hour
    if hour >=6 and hour <=12:
        speak("Good morning")
    elif hour >=12 and hour <18:
        speak("Good afternoon")
    elif hour >=18 and hour <=24:
        speak("Good evening")
    time()
    date()
    speak("Purple is at your service. How can I help you?")

def listening():
    # microphone to string output
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening to speaker......")
        r.pause_threshold = 1
        r.phrase_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing the command...")
        query = r.recognize_google(audio, language = 'en-in')
        print(f"user said : {query}\n")

    except Exception as e:
        # speak("I beg your pardon")
        return "None"

    return query


def joke():
    speak(pyjokes.get_joke())
'''
def sendemail(to,content):
    server=smtplib.SMTP('smtp.gmail.com',587)#portnumber 587
    server.ehlo()
    server.starttls()# these two lines will check smtp connection
    server.login("mail","password")
    server.sendmail("mail",to,content)
    server.close()
'''

def screenshot():
    img = pyautogui.screenshot()
    img.save("D:\sss.png")

def tm(str):
    pr="Notepad.exe"
    fname="text_files/todolist1.txt"
    if 'show'  in str:
        speak("ok")
        sp.Popen([pr,fname])


    #if 'close' in str:
        #sp.terminate(fname)

    if 'add' in str:
        speak("Noting down")
        f1 = open('text_files/todolist.txt','a')
        q1 = listening().lower()
        f1.write(q1)
        f1.write("\n")
        speak("Anything else u want me to add?")
        q2 = listening().lower()
        if 'yes' in q2:
            speak("Noting down!")
            q3 = listening().lower()
            f1.write(q3)
            f1.write("\n")

        if 'no' in q2:
            speak("Your to do list has been successfully updated!!")

    if 'update' in str:
        speak("Noting down!")
        q4 = listening().lower()
        if 'important' in q4:
            open("text_files/todolist1.txt", "a").write(q4)
            open("text_files/todolist1.txt", "a").write("\n" + open("text_files/todolist.txt").read())
        speak("Updated the todo list according to the need!")

    if 'manage' in str:
        speak("Just a min, i am analyzing the tasks to give the best possible sequence")
        f=open("text_files/todolist1.txt",'r')
        Lines = f.readlines()
        i=0;
        for line in f:
            i=i+1
        nol=i
        c=0
        mon=[]
        tue=[]
        wed=[]
        thu=[]
        fri=[]
        for line in Lines:
            c=c+1
            if (c%5) == 1:
                mon.append(line)
            elif (c%5) == 2:
                tue.append(line)
            elif (c%5) == 3:
                wed.append(line)
            elif (c%5) == 4:
                thu.append(line)
            elif (c%5) == 0:
                fri.append(line)
        speak('On monday u can')
        for l in mon:
            speak(l)
        speak('On tuesday u can')
        for l in tue:
            speak(l)
        speak('on wednesday u can')
        for l in wed:
            speak(l)
        speak('on thursday u can')
        for l in thu:
            speak(l)
        speak('on friday u can')
        for l in fri:
            speak(l)



def deadline_notify():
    format="%d-%m-%Y"
    dt_now=datetime.datetime.now()
    print(dt_now)
    for i in user_data:
        dt=datetime.datetime.strptime(i[2],format)
        diff=abs((dt-dt_now).days)
        if(diff<=1 and i[1]!="no"):
            notification.notify(
                title="Submit your Assignment",
                message="Course: "+i[1]+"\nDue date: "+i[2],
                app_icon="assets/noti_icon.ico",
                timeout=15
        )

def deadline_view():
    speak("Mam here are your deadlines")
    for i in user_data:
        if(i[3]=="no"):
            format="%d-%m-%Y"
            dt=datetime.datetime.strptime(i[2],format)
            d =dt.day
            m=dt.month
            speak("course name "+i[1])
            speak("deadline")
            dt_obj = datetime.datetime.strptime(str(m), "%m")
            full_month_name = dt_obj.strftime("%B")
            speak(d)
            speak(full_month_name)

def mark_view():
    speak("Mam in which course you want me to show your marks")
    m=listening().lower()
    print(m)
    f=0
    for i in user_data:
        if(i[1]==m):
            speak("marks awarded")
            speak(i[4])
            f=1
    if(f==0):
        speak("Still marks are not awarded for course ")
    


#-----------------------------------------------------------------

#main window
root = tkinter.Tk()
root.title('purple')
root.iconbitmap('assets/logo.ico')
root.geometry('850x650')
root.resizable(0,0)
#-----------------------------------------------------------------

# Create a photoimage object of the image in the path
image1 = Image.open("assets/background.png")
test = ImageTk.PhotoImage(image1)
label1 = tkinter.Label(image=test)
label1.image = test
label1.place(x=-160, y=0) # Position image

#-----------------------------------------------------------------
#action performed when button is clicked
def my_command():
    wishme()
    while True:
        query = listening().lower()
        tm(query)
        if 'wikipedia' in query:
            speak('searching in wikipedia!')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query,sentences=2)
            speak("According to wikipedia")
            print(results)
            speak(results)
        elif 'google' in query:
            webbrowser.Chrome("letsplay.com")
        elif 'nice' in query:
            speak("Great as usual.")
            speak("So,How may i help you today?")
        elif 'sweet' in query:
            speak("I am feeling shy now")
        elif 'thanks' in query:
            speak("Anything for you!")
        elif 'shut' in query:
            speak("Sure! Have a great day ahead!")
            quit()
            break
        elif "jokes" in query:
            joke()
        elif "screenshot" in query:
            screenshot()
            speak("screenshot is saved in D drive successfully")
        elif "play song" in query:
            songs_dir = "songs"
            songs= os.listdir(songs_dir)
            k=0
            num=[]
            for i in songs:
                k=k+1
                num.append(k)
            r=random.choice(num)
            os.startfile(os.path.join(songs_dir,songs[r-1]))
        elif "remember that" in query:
            speak("what should I remmber?")
            data=listening()
            speak("You said me to remember"+data)
            remember=open("data.txt","w")
            remember.write(data)
            remember.close()
        elif "do you know anything" in query:
            remember=open("data.txt","r")
            speak("you said me to remember"+remember.read())
        elif "deadlines" in query:
            deadline_view()
        elif "marks" in query:
            mark_view()
        elif "notify" in query:
            deadline_notify()
        elif "send email" in query:
            speak("what you want me to send?")
            data=listening()
            speak("To whom do you want to send?")
            data1=listening()
            speak("sending the mail")
            speak("sent successfully")

#-----------------------------------------------------------------

#button
click_btn= ImageTk.PhotoImage(file='assets/micro.png')
img_label= tkinter.Label(image=click_btn)
#Let us create a dummy button and pass the image
button= tkinter.Button(root, image=click_btn,command= my_command,borderwidth=10,relief="raised",activebackground="#932ce8")
button.pack()
button.place(x=60,y=220)
#text= tkinter.Label(root, text= "")
#text.pack(pady=30)
#-----------------------------------------------------------------

root.mainloop()

   