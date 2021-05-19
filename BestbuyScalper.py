from selenium import webdriver
from selenium.webdriver.support.ui import Select
from requests_html import HTMLSession, AsyncHTMLSession
from selenium.webdriver.common.by import By
import time
import smtplib, ssl
import phonenumbers
from phonenumbers import carrier
import PySimpleGUI as sg
import phonenumbers
import sys
sys.setrecursionlimit(10**9)


# carrier: to know the name of 
# service provider of that phone number
from phonenumbers import carrier

contactCheck = False
urlCheck = False
loginCheck = False

bestBuyemailAdress = "PLACEHOLDER"
bestBuypassword = "PLACEHOLDER"



''' ---------------------------------------- / DIVIDER \ ---------------------------------------- '''

'''
Sets up the messaging part of the script
'''


'''
For the senderemail you need to set it to a email with no verification, no 2fa.
Everything has to be disabled so the bot can login to it.
'''

sender_email = "PLACEHOLDER"
password = "PLACEHOLDER"


port = 465
smtp_server = "smtp.gmail.com"
receiver_email = "PLACEHOLDER"


message = """\
Subject: BestBuy

Your order has been placed in your Cart

https://www.bestbuy.com/cart"""



''' ---------------------------------------- / DIVIDER \ ---------------------------------------- '''

'''
Creates the First Window for BestBuy Email and Password
'''


def askLogin():
    global bestBuyemailAdress, bestBuypassword
    
    sg.theme('dark grey 3')

    # Define the window's contents
    layout = [[sg.Text("BestBuy Login Information")],
              [sg.Text('Email', size=(20, 1)), sg.InputText('')],
              [sg.Text('Password', size=(20, 1)), sg.InputText('')],
              [sg.Button('Submit')]]

    # Create the window
    window = sg.Window('BestBuy Scalper', layout)

    # Display and interact with the Window using an Event Loop
    while True:
        event, values = window.read()
        # See if user wants to quit or window was closed
        if event == 'Submit':
            try:
                bestBuyemailAdress = str(values[0])
                bestBuypassword = str(values[1])
                
                print("Information Recieved")
                break
            except:
                print("Please fill all statements")

        if event == sg.WINDOW_CLOSED:
            break
        
    # Finish up by removing from the screen
    window.close()



''' ---------------------------------------- / DIVIDER \ ---------------------------------------- '''

'''
Creates the Second Window for Phonenumber and carrier

We need the carrier because im to cheap
to pay a website to ping the number
and find it automatically

A phone is basically an email, and so different
carriers have different ends to it
'''


def askContact():
    global receiver_email
    
    layout = [[sg.Text('Phone-Number / Email', size=(20, 1)), sg.InputText('')],
              [sg.Radio('Sprint', 1, size=(10, 1), enable_events=True, key='R1'), sg.Radio('AT&T',1, size=(10, 1), enable_events=True, key='R2')],
              [sg.Radio('Verizon',1, size=(10, 1), enable_events=True, key='R3'), sg.Radio('Email',1, size=(10, 1), enable_events=True, key='R4')],
              [sg.Button('Submit')]]



    window = sg.Window('Contact Information', layout)

    while True:             # Event Loop
        event, values = window.read()
        if event in (None, 'Submit'):
            phoneNumber = values[0]
            
            if values["R1"] == True:
                receiver_email = phoneNumber + "@messaging.sprintpcs.com"
            elif values["R2"] == True:
                receiver_email = phoneNumber + "@mms.att.net"
            elif values["R3"] == True:
                receiver_email = phoneNumber + "@vtext.com"
            else:
                receiver_email = phoneNumber

            break
        
    window.close()



''' ---------------------------------------- / DIVIDER \ ---------------------------------------- '''

'''
Gets the website the user wants
'''


def askWebsite():
    global skuID, base_url
    
    sg.theme('dark grey 3')

    # Define the window's contents
    layout = [[sg.Text("Bestbuy Item Information")],
              [sg.Text('URL', size=(20, 1)), sg.InputText('')],
              [sg.Button('Submit')]]

    # Create the window
    window = sg.Window('BestBuy Scalper', layout)

    # Display and interact with the Window using an Event Loop
    while True:
        event, values = window.read()
        # See if user wants to quit or window was closed
        if event == 'Submit':
            try:
                base_url = str(values[0])

                skuID = base_url.split("=")[1]
                
                print("Information Recieved")
                break
            except:
                print("Please enter a valid Bestbuy URL")

        if event == sg.WINDOW_CLOSED:
            break
        
    # Finish up by removing from the screen
    window.close()



''' ---------------------------------------- / DIVIDER \ ---------------------------------------- '''

'''
GLOBAL VARIABLES
'''


buy_btn = "PLACEHOLDER"
session = HTMLSession()
r = "PLACEHOLDER" # We globalize it so when the item is found Available
                  # The script doesnt reload the page



''' ---------------------------------------- / DIVIDER \ ---------------------------------------- '''

'''
PROGRAM and INFORMATION TESTER
'''


def programTest():
    global contactCheck, urlCheck, loginCheck
    
    
    ''' ---------------------------------------- / DIVIDER \ ------------------------------------ '''
    

    if contactCheck == False:    
        print("\n---------- / TESTING \ ----------")
        print("--- Testing Messaging         ---\n")

        print("PLEASE ALLOW UP TO 30 SECONDS IN DELAY")
        print("PLEASE HOLD\n")

        if sender_email == "PLACEHOLDER" or password == "PLACEHOLDER":
            print("Please setup the SENDER EMAIL and PASSWORD in the begining of the script/nThis is located around LINE 40")

        try:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message)

            layout = [[sg.Text('Did you recieve a message?', size=(20, 1))],
                      [sg.Radio('Yes', 1, size=(10, 1), enable_events=True, key='R1'), sg.Radio('No',1, size=(10, 1), enable_events=True, key='R2')],
                      [sg.Button('Submit')]]



            window = sg.Window('PROGRAM TESTING', layout)

            while True:             # Event Loop
                event, values = window.read()
                if event in (None, 'Submit'):
                    
                    if values["R1"] == True:
                        print("MESSAGING SUCCEEDED")
                        contactCheck = True
                    elif values["R2"] == True:
                        print("ERROR: FAILED TO SEND MESSAGE BUT PASSED CHECK")
                        window.close()
                        time.sleep(3)
                        sys.exit()
                    else:
                        print("ERROR: PROGRAM TESTING FOR MESSAGING, PASSED WITHOUT ASKING IF SENT")
                        window.close()
                        
                    break
                if event == sg.WINDOW_CLOSED:
                    break
                
            window.close()
                
        except:
            print("MESSAGING FAILED")
            print("Please Re-Try")
            print("RESTARTING")
            time.sleep(3)
            askContact()

            #Recursion ------------------------------------------------------------------------------
            programTest()



    ''' ---------------------------------------- / DIVIDER \ ------------------------------------ '''
    

    if urlCheck == False:
        print("\n---------- / TESTING \ ----------")
        print("--- Testing URL               ---\n")

        print("PLEASE HOLD\n")

        try:
            r = session.get(base_url) # This allows us to reload every 1 Second
                                      # if it is found to be unavailable

            
            buy_btn = r.html.find('button[data-sku-id="'+ skuID +'"]', first=True)
            if buy_btn.text == "Sold Out" or buy_btn.text == "Add to Cart":
                print("URL SUCCEEDED")
                urlCheck = True
            else:
                print("ERROR: URL FAILED")
                print("Please Re-Try")
                print("RESTARTING")
                time.sleep(3)
                askWebsite()
                
                #Recursion --------------------------------------------------------------------------
                programTest()
        except:
            print("ERROR: URL FAILED")
            print("Please Re-Try")
            print("RESTARTING")
            time.sleep(3)
            askWebsite()
            
            #Recursion ------------------------------------------------------------------------------
            programTest()


    ''' ---------------------------------------- / DIVIDER \ ------------------------------------ '''


    if loginCheck == False:
        print("\n---------- / TESTING \ ----------")
        print("--- Testing Login Info        ---\n")

        print("PLEASE HOLD\n")

        try:

            layout = [[sg.Text('Is this Information Correct?', size=(20, 1))],
                      [sg.Text('Email: ' + bestBuyemailAdress, size=(50, 1))],
                      [sg.Text('Password: ' + bestBuypassword, size=(50, 1))],
                      [sg.Radio('Yes', 1, size=(10, 1), enable_events=True, key='R1'), sg.Radio('No',1, size=(10, 1), enable_events=True, key='R2')],
                      [sg.Button('Submit')]]



            window = sg.Window('PROGRAM TESTING', layout)

            while True:             # Event Loop
                event, values = window.read()
                if event in (None, 'Submit'):
                    
                    if values["R1"] == True:
                        print("LOGIN SUCCEEDED")
                        loginCheck = True
                    elif values["R2"] == True:
                        print("ERROR: WRONG LOGIN INFORMATION")
                        window.close()
                        time.sleep(3)
                        sys.exit()
                    else:
                        print("ERROR: PROGRAM TESTING FOR LOGIN, PASSED WITHOUT ASKING IF CORRECT")
                        window.close()
                    break
                
            window.close()
                
            #Recursion ----------------------------------------------------------------------------------
            programTest()

        except:
            print("LOGIN FAILED")
            print("Please Re-Try")
            print("RESTARTING")
            time.sleep(3)
            askLogin()

            #Recursion ----------------------------------------------------------------------------------
            programTest()
            



''' ---------------------------------------- / DIVIDER \ ---------------------------------------- '''

'''
Once the item is made available
it adds it to your cart and signs you in
with the email and password provided

At the end it will send you a message
to the provided phonenumber
'''


def perform_purchase(url):

    print("ITEM AVAILABLE")
    
    # Opens Item URL
    driver = webdriver.Chrome()
    driver.get(url)
    
    try:

        try:
            driver.find_element(By.XPATH, '//button[text()="Add to Cart"]').click()
        except:
            time.sleep(1)
            driver.find_element(By.XPATH, '//button[text()="Add to Cart"]').click()

        #time.sleep(0.5)

        # Checkout
        checkout_url = 'https://www.bestbuy.com/cart'
        driver.get(checkout_url)

        try:
            time.sleep(0.5)
            driver.find_element(By.XPATH, '//button[text()="Checkout"]').click()
        except:
            time.sleep(1)
            driver.find_element(By.XPATH, '//button[text()="Checkout"]').click()


        time.sleep(1)
        url = driver.current_url
        driver.get(url)


        try:
            time.sleep(0.5)
            # Logs in
            driver.find_element_by_id('fld-e').send_keys(bestBuyemailAdress)
            driver.find_element_by_id('fld-p1').send_keys(bestBuypassword)
        except:
            time.sleep(1)
            # Logs in
            driver.find_element_by_id('fld-e').send_keys(bestBuyemailAdress)
            driver.find_element_by_id('fld-p1').send_keys(bestBuypassword)


        try:
            time.sleep(0.5)
            driver.find_element(By.XPATH, '//button[text()="Sign In"]').click()
        except:
            time.sleep(1)
            driver.find_element(By.XPATH, '//button[text()="Sign In"]').click()

        
        time.sleep(5)



        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)

        
    except:
        print("---ATTEMPT FAILED---")
        driver.close()
        main()
    



''' ---------------------------------------- / DIVIDER \ ---------------------------------------- '''

'''
Checks if sold out, reloads the main script

When available, add the unit to cart

When complete, keep the webpage up fo r15 minutes
to allow us the 15 minute reserve time when having
the checkout page open
'''


def main():
    global buy_btn, r

    r = session.get(base_url) # This allows us to reload every 1 Second
                              # if it is found to be unavailable

    
    buy_btn = r.html.find('button[data-sku-id="'+ skuID +'"]', first=True)  

    
    while buy_btn.text == "Sold Out":
        print("OUT OF STOCK")
        
        time.sleep(1)
        
        r = session.get(base_url) # This allows us to reload every 1 Second
                                  # if it is found to be unavailable
    
        buy_btn = r.html.find('button[data-sku-id="'+ skuID +'"]', first=True)
        

    perform_purchase(base_url)


    

    print("FINISHED")
    print("Waiting for the 15 minute reserve")
    time.sleep(900)
    driver.close()



''' ---------------------------------------- / DIVIDER \ ---------------------------------------- '''



askLogin()
askContact()
askWebsite()

programTest()

print("FINISHED TESTING")


main()
