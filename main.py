import requests
import I2C_LCD_driver
import time
import string
from datetime import datetime
from datetime import date
mylcd = I2C_LCD_driver.lcd()
import config
#EVERYTHING BELOW CAN BE CHANGED IN config.py!!! CHANGING THIS DIRECTLY FROM HERE WILL OVERWRITE config.py!!!
#replace with your username
username = config.username
usernamemagi = config.usernamemagi
#replace with how much time you want in between switching
waittime = config.waittime
#set to False if you dont want printing in the console
printornot = config.printornot
#replace this with the custom price value you want(like trx, bch, etc)
customexv = config.customexv
#change to false if you do not want to donate
allowdonate = config.allowdonate
#replace with donation amount
donateamount = config.donateamount
#replace with who you want to donate to
donateperson = config.donateperson
print("config.py loaded")
old=0
turns = 14

def refresh():
    mylcd.lcd_display_string("                ",1,0)
    mylcd.lcd_display_string("                ",2,0)
    
isapidown = False
now = datetime.now()
date = now.strftime("%m-%d-%Y")
current_time = now.strftime("%I:%M %p")
print("Thank you for using j727s's 16x02 Duino Coin monitor")
ducoapi = True
xmgapi = True
while True:
    try:
        print(turns)
        now = datetime.now()
        date = now.strftime("%m-%d-%Y")
        current_time = now.strftime("%I:%M %p")
        turns = turns +1
        if turns == 15:
            turns = 1
            print("Date: "+date+" Time: "+current_time)
            if allowdonate == True:        
                url = "https://server.duinocoin.com/transaction?username="+str(username)+"&password="+str(config.ducopassword)+"&recipient="+donateperson+"&amount="+str(donateamount)+"&memo=automatic donation from my python script"
                payload = {}
                headers= {}
                response = requests.request("GET", url, headers=headers, data = payload)
                data = response.json()
                print(data)
                connection = str(data["success"])
                print("Donation success: "+connection)
            else:
                print("Skipping donation")
        time.sleep(1)
        url = "https://server.duinocoin.com/v2/users/"+username
        payload = {}
        headers= {}
        response = requests.request("GET", url, headers=headers, data = payload)
        data = response.json()
        connection = str(data["success"])
        if not connection == "True":
            ducoapi = False
        else:
            ducoapi = True
        balance = str(data["result"]["balance"]["balance"])
        price = str(data["result"]["prices"]["max"])
        stakeamt = str(data["result"]["balance"]["stake_amount"])
        customex = str(data["result"]["prices"][customexv])
        customexsci = ("{:.16f}".format(float(customex)))
        #if not float(old) == float(customexsci):
        #    print("Changed from "+str(old)+" to "+str(customexsci))
        old=customexsci
        mylcd.lcd_display_string(balance,1,0)
        if printornot == True:
            print(balance)
            print(price)
            print(stakeamt)
            print(customexsci)
        refresh()
        mylcd.lcd_display_string(price,1,0)
        mylcd.lcd_display_string("Date: "+date,1,0)
        mylcd.lcd_display_string("Time: "+current_time,2,0)
        time.sleep(waittime)
        refresh()
        mylcd.lcd_display_string("DUCO Segment ",1,0)
        time.sleep(waittime)
        refresh()
        mylcd.lcd_display_string("Balance: ",1,0)
        mylcd.lcd_display_string(balance,2,0)
        time.sleep(waittime)
        refresh()
        mylcd.lcd_display_string("Exchange Price: ",1,0)
        mylcd.lcd_display_string(price,2,0)
        time.sleep(waittime)
        refresh()
        #mylcd.lcd_display_string(customexv.upper()+" Price: ",1,0)
        #mylcd.lcd_display_string(customexsci,2,0)
        #time.sleep(waittime)
        refresh()
        mylcd.lcd_display_string("1 USD to DUCO: ",1,0)
        mylcd.lcd_display_string(str(float(1)/float(price)),2,0)
        time.sleep(waittime)
        refresh()
        mylcd.lcd_display_string("Balance to USD: ",1,0)
        mylcd.lcd_display_string(str(float(price)*float(balance)),2,0)
        time.sleep(waittime)
        refresh()
        mylcd.lcd_display_string("Stake amount: ",1,0)
        mylcd.lcd_display_string(stakeamt,2,0)
        time.sleep(waittime)
        refresh()
        url = "https://magi.duinocoin.com/users/"+usernamemagi
        payload = {}
        headers= {}
        response = requests.request("GET", url, headers=headers, data = payload)
        data = response.json()
        connection = str(data["success"])
        if not connection == "True":
            xmgapi = False
        else:
            xmgapi = True
        balance = str(data["result"]["balance"]["balance"])
        price = str(data["result"]["price"]["max"])
        stakeamt = str(data["result"]["balance"]["staked_balance"])
        mylcd.lcd_display_string("XMG Segment ",1,0)
        time.sleep(waittime)
        refresh()
        mylcd.lcd_display_string("Balance: ",1,0)
        mylcd.lcd_display_string(balance,2,0)
        time.sleep(waittime)
        refresh()
        mylcd.lcd_display_string("Stake amount: ",1,0)
        mylcd.lcd_display_string(stakeamt,2,0)
        time.sleep(waittime)
        refresh()
        mylcd.lcd_display_string("Exchange Price: ",1,0)
        mylcd.lcd_display_string(price,2,0)
        time.sleep(waittime)
        refresh()
        mylcd.lcd_display_string("1 USD to XMG: ",1,0)
        mylcd.lcd_display_string(str(float(1)/float(price)),2,0)
        time.sleep(waittime)
        refresh()
        mylcd.lcd_display_string("Balance to USD: ",1,0)
        mylcd.lcd_display_string(str(float(price)*float(balance)),2,0)
        time.sleep(waittime)
        if isapidown == True:
            isapidown = False
            print("Connection OK! Date: "+date+" Time: "+current_time)
    except Exception:
        refresh()
        #print("API down! Date: "+date+" Time: "+current_time)
        if ducoapi == False:
            print("Failed to connect to Duino Coin API! Date: " +date+ " Time: " +current_time)
            mylcd.lcd_display_string("Duino Coin API ",1,0)
            mylcd.lcd_display_string("Down ",2,0)
        elif xmgapi == False:
            print("Failed to connect to Magi Coin API! Date: " +date+ " Time: " +current_time)
            mylcd.lcd_display_string("Magi API ",1,0)
            mylcd.lcd_display_string("Down ",2,0)
        else:
            print("Failed to connect to internet! Date: " +date+ " Time: " +current_time)
            mylcd.lcd_display_string("Internet ",1,0)
            mylcd.lcd_display_string("Connection Down ",2,0)
        
        isapidown = True
        time.sleep(60)
        refresh()
        pass
