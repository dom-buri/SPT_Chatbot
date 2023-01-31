# coding=utf-8

import logging
import csv
import re
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, KeyboardButton,ReplyKeyboardMarkup, Bot, ForceReply,ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters, ConversationHandler
import time

# Insert Token
path = ""

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

register_user, run_2, run_3 = range(3)

bot = Bot(token=TOKEN)

users, COs, buddyDict, ISOs = {}, {}, {}, {}

currentRunning = {"AI99": {}, "AILO": {}, "AITC": {}, "AIAD": {}, "AICD": {}, "AIAV": {}, "AIAL": {}, "AIAR": {}, "AIAU": {}, "AIOF": {}, "AITF": {},
                  "HQ99": {}, "HQ1": {}, "HQ2": {}, "HQ3": {}, "HQ4": {}, "HQ5": {},"HQ6": {}, "HQ7": {},
                  "2399": {}, "23A": {}, "23B": {}, "23C": {}, "23H": {},
                  "2499": {}, "24K": {}, "24C": {}, "24D": {}, "24G": {}, "24S": {},
                  "211": {}, "212": {}, "213": {}, "214": {}, "21H": {}, "21A": {}, "21B": {}, "21C": {},
                  "SS99": {}, "SS1": {}, "SS2": {}, "SS3": {}, "SS4": {}, "SS5": {},"SS6": {}, "SS7": {}}

def send_message_job(context):
    print("Reminder Job Exceuted")
    job_send_reminder()
    print("Reminder Job Completed")
        
def job_send_reminder():
    for unit, runners in currentRunning.items():
        for runner in runners:
            bot.send_message(chat_id=runner, text='Hello! Just checking in to check whether you have completed your SPT. If u are still doing SPT, please ignore this message, else click on /complete')
    return None

def loadData():
    global users, COs, ISO
    reader = csv.reader(open(path + 'Runners.csv', 'r'))
    for row in reader:
        if row != []:
            id, first_name, office, unit = row
            users[str(id)] = [first_name, office, unit]
            
    reader = csv.reader(open(path + 'COs.csv', 'r'))
    for row in reader:
        if row != []:
            id, first_name, office, unit = row
            COs[str(id)] = [first_name, office, unit]
    
    reader = csv.reader(open(path + 'ISO.csv', 'r'))
    for row in reader:
        if row != []:
            ISOs[str(row[0])] = [row[1], row[2]]
    print(users)

def deEmojify(text):
    regrex_pattern = re.compile(pattern="["
                                u"\U0001F600-\U0001F64F"
                                u"\U0001F300-\U0001F5FF"
                                u"\U0001F680-\U0001F6FF"
                                u"\U0001F1E0-\U0001F1FF"
                                "]+", flags=re.UNICODE)
    return regrex_pattern.sub(r'', text)

def userExists(user_id):
    user_id = str(user_id)
    if user_id in users or user_id in COs or user_id in ISOs:
        return True
    return False
    
def addUser(user_id, first_name, office, role, unit):
    if role == "CO":
        COs[user_id] = [first_name, office, unit]
        with open('COs.csv', 'w') as f:
            for key in COs.keys():
                f.write("%s,%s,%s,%s\n"%(key, COs[key][0], COs[key][1], COs[key][2]))
    else:
        users[user_id] = [first_name, office, unit]
        with open('Runners.csv', 'w') as f:
            for key in users.keys():
                f.write("%s,%s,%s,%s\n"%(key, users[key][0], users[key][1], users[key][2]))     

def start(update, context):
    user_id = update.message.chat['id']
    first_name = deEmojify(update.message.chat['first_name'])
    #first_name = update.message.chat['first_name']

    if userExists(user_id):
        update.message.reply_text("Hey! "+ first_name + ", welcome back to AI SPT Chatbot")
        update.message.reply_text("To start a new SPT, enter /run")
        return ConversationHandler.END
    else:
        update.message.reply_text("Hey! " + first_name + ", welcome to AI SPT Chatbot")
        update.message.reply_text("You should have been given a registration key by your commanders")
        update.message.reply_text("To register, please enter the registeration key:")
        return register_user
    
def run(update, context):
    user_id = update.message.chat['id']
    global buddyDict
    if users[str(user_id)][2] == "SS":
        buddyDict[user_id] = ["", ""]
        keyboard = [[], []]
        keyboard[0].append(InlineKeyboardButton("Stadium", callback_data= "WORKOUT_Stadium"))
        keyboard[0].append(InlineKeyboardButton("Gym", callback_data= "WORKOUT_Gym"))
        keyboard[1].append(InlineKeyboardButton("MPH", callback_data= "WORKOUT_MPH"))
        keyboard[1].append(InlineKeyboardButton("Parade Square", callback_data= "WORKOUT_ParadeSquare"))
        update.message.reply_text("Where will you be doing your SPT?")
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('Please choose:', reply_markup = reply_markup)
        return ConversationHandler.END
    first_name = deEmojify(update.message.chat['first_name'])
    #first_name = update.message.chat['first_name']

    update.message.reply_text("Hey! " + first_name + ", to start your workout, please enter your buddy's name")
    return run_2

def run_2_func(update: Update, _: CallbackContext) -> int:
    global buddyDict
    user_id = update.message.chat['id']
    response = update.message.text
    buddyDict[user_id] = [response]
    update.message.reply_text("Please enter your buddy's HP Number")
    return run_3
    
def run_3_func(update: Update, _: CallbackContext) -> int:
    global buddyDict
    user_id = update.message.chat['id']
    response = update.message.text
    if not response.isdigit() or len(response) != 8:
        update.message.reply_text("Sorry! Invalid phone number, please enter /run to start a new SPT")
        return ConversationHandler.END
    buddyDict[user_id].append(response)
    keyboard = [[], []]
    keyboard[0].append(InlineKeyboardButton("Camp Stadium", callback_data= "WORKOUT_Stadium"))
    keyboard[0].append(InlineKeyboardButton("Perimeter", callback_data= "WORKOUT_Perimeter"))
    keyboard[1].append(InlineKeyboardButton("Out of Camp", callback_data= "WORKOUT_OutOfCamp"))
    keyboard[1].append(InlineKeyboardButton("Gym", callback_data= "WORKOUT_Gym"))
    keyboard[1].append(InlineKeyboardButton("Pool", callback_data= "WORKOUT_Pool"))
    update.message.reply_text("Where will you be doing your SPT?")
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose:', reply_markup = reply_markup)
    return ConversationHandler.END
    
def notifyCO(user_id, first_name):
    buddyName = buddyDict[user_id][0]
    buddyContact = buddyDict[user_id][1]
    if len(buddyContact) >= 3:
        lastThreeNums = buddyContact[-3:]
    else:
        lastThreeNums = buddyContact
    place = buddyDict[user_id][2]
    userOffice = users[str(user_id)][1]
    userUnit = users[str(user_id)][2]
    for key, value in COs.items():
        if value[1] == userOffice and value[2] == userUnit:
            if userUnit == "SS":
                bot.send_message(chat_id = key, text=first_name + " from " + userOffice + " has completed his self declaration safety checks and is going for SPT at " + place)
            else:
                bot.send_message(chat_id = key, text=first_name + " from " + userOffice + " has completed his self declaration safety checks and is going for SPT with " + buddyName + " and his contact number is XXXX X" + lastThreeNums + " at " + place)
    for ISO in ISOs:
        if ISOs[ISO][1] == userUnit:
            if userUnit == "SS":
                bot.send_message(chat_id = ISO, text=first_name + " from " + userOffice + " has completed his self declaration safety checks and is going for SPT at " + place)
            else:
                bot.send_message(chat_id = ISO, text=first_name + " from " + userOffice + " has completed his self declaration safety checks and is going for SPT with " + buddyName + " and his contact number is XXXX X" + lastThreeNums + " at " + place)
    bot.send_message(chat_id = user_id, text="Thank you! The relevant parties have been notified!")
    bot.send_message(chat_id = user_id, text="You are now able to start your SPT!")
    masekdNum = "XXXX X" + lastThreeNums
    currentRunning[userUnit + userOffice][user_id] = [first_name, buddyName, masekdNum, place, time.strftime("%X")]
    bot.send_message(chat_id = user_id, text="Once you have completed your run, please enter /complete")  

def registerUser(update: Update, _: CallbackContext) -> int:
    response = update.message.text
    if response == "AIKey":
        update.message.reply_text("Registration Key accepted")
        registerUserUnit(update, "Runner", "AI")
        return ConversationHandler.END
    elif response == "HQKey":
        update.message.reply_text("Registration Key accepted")
        registerUserUnit(update, "Runner", "HQ")
        return ConversationHandler.END
    elif response == "23Key":
        update.message.reply_text("Registration Key accepted")
        registerUserUnit(update, "Runner", "23")
        return ConversationHandler.END
    elif response == "24Key":
        update.message.reply_text("Registration Key accepted")
        registerUserUnit(update, "Runner", "24")
        return ConversationHandler.END
    elif response == "AICOKey":
        update.message.reply_text("Registration Key accepted")
        registerUserUnit(update, "CO", "AI")
        return ConversationHandler.END
    elif response == "HQCOKey":
        update.message.reply_text("Registration Key accepted")
        registerUserUnit(update, "CO", "HQ")
        return ConversationHandler.END
    elif response == "23COKey":
        update.message.reply_text("Registration Key accepted")
        registerUserUnit(update, "CO", "23")
        return ConversationHandler.END
    elif response == "24COKey":
        update.message.reply_text("Registration Key accepted")
        registerUserUnit(update, "CO", "24")
        return ConversationHandler.END
    elif response == "AIISOKey":
        update.message.reply_text("Thank you! You are now registered as ISO")
        registerUserUnit(update, "ISO", "AI")
        return ConversationHandler.END
    elif response == "HQFSOKey":
        update.message.reply_text("Thank you! You are now registered as FSO")
        registerUserUnit(update, "ISO", "HQ")
        return ConversationHandler.END
    elif response == "23FSOKey":
        update.message.reply_text("Thank you! You are now registered as FSO")
        registerUserUnit(update, "ISO", "23")
        return ConversationHandler.END
    elif response == "24FSOKey":
        update.message.reply_text("Thank you! You are now registered as FSO")
        registerUserUnit(update, "ISO", "24")
        return ConversationHandler.END
    elif response == "21Key":
        update.message.reply_text("Registration Key accepted")
        registerUserUnit(update, "Runner", "21")
        return ConversationHandler.END
    elif response == "21COKey":
        update.message.reply_text("Registration Key accepted")
        registerUserUnit(update, "CO", "21")
        return ConversationHandler.END
    elif response == "21ISOKey":
        update.message.reply_text("Thank you! You are now registered as ISO")
        registerUserUnit(update, "ISO", "21")
        return ConversationHandler.END
    elif response == "SSKey":
        update.message.reply_text("Registration Key accepted")
        registerUserUnit(update, "Runner", "SS")
        return ConversationHandler.END
    elif response == "SSCOKey":
        update.message.reply_text("Registration Key accepted")
        registerUserUnit(update, "CO", "SS")
        return ConversationHandler.END
    elif response == "SSISOKey":
        update.message.reply_text("Thank you! You are now registered as ISO")
        registerUserUnit(update, "ISO", "SS")
        return ConversationHandler.END
    else:
        update.message.reply_text("Invalid Registration Key. Please enter a registration key again.")
    
def registerUserUnit(update, role, unit):
    if role == "ISO":
        user_id = update.message.chat['id']
        first_name = deEmojify(update.message.chat['first_name'])
        #first_name = update.message.chat['first_name']
        with open('ISO.csv', 'w') as f:
            f.write("%s,%s,%s\n"%(user_id, first_name, unit))   
        ISOs[str(user_id)] = [first_name, unit]
        return ConversationHandler.END
        
    if unit == "AI":
        keyboard = [[], []]
        keyboard[0].append(InlineKeyboardButton("99", callback_data= "REGISTER_AI_99_" + role))
        keyboard[0].append(InlineKeyboardButton("LO", callback_data= "REGISTER_AI_MO_" + role))
        keyboard[0].append(InlineKeyboardButton("TC", callback_data= "REGISTER_AI_TC_" + role))
        keyboard[0].append(InlineKeyboardButton("AD", callback_data= "REGISTER_AI_AD_" + role))
        keyboard[0].append(InlineKeyboardButton("CD", callback_data= "REGISTER_AI_CD_" + role))
        keyboard[1].append(InlineKeyboardButton("AV", callback_data= "REGISTER_AI_AV_" + role))
        keyboard[1].append(InlineKeyboardButton("AL", callback_data= "REGISTER_AI_AL_" + role))
        keyboard[1].append(InlineKeyboardButton("AR", callback_data= "REGISTER_AI_AR_" + role))
        keyboard[1].append(InlineKeyboardButton("AU", callback_data= "REGISTER_AI_AU_" + role))
        keyboard[1].append(InlineKeyboardButton("OF", callback_data= "REGISTER_AI_OF_" + role))
        keyboard[1].append(InlineKeyboardButton("TF", callback_data= "REGISTER_AI_TF_" + role))
        update.message.reply_text("To register, please state which department are you from?")
    elif unit == "HQ":
        keyboard = [[]]
        keyboard[0].append(InlineKeyboardButton("99", callback_data= "REGISTER_HQ_99_" + role))
        keyboard[0].append(InlineKeyboardButton("1", callback_data= "REGISTER_HQ_1_" + role))
        keyboard[0].append(InlineKeyboardButton("2", callback_data= "REGISTER_HQ_2_" + role))
        keyboard[0].append(InlineKeyboardButton("3", callback_data= "REGISTER_HQ_3_" + role))
        keyboard[0].append(InlineKeyboardButton("4", callback_data= "REGISTER_HQ_4_" + role))
        keyboard[0].append(InlineKeyboardButton("5", callback_data= "REGISTER_HQ_5_" + role))
        keyboard[0].append(InlineKeyboardButton("6", callback_data= "REGISTER_HQ_6_" + role))
        keyboard[0].append(InlineKeyboardButton("7", callback_data= "REGISTER_HQ_7_" + role))
        update.message.reply_text("To register, please state which department are you from?")
    elif unit == "23":
        keyboard = [[]]
        keyboard[0].append(InlineKeyboardButton("99", callback_data= "REGISTER_23_99_" + role))
        keyboard[0].append(InlineKeyboardButton("A", callback_data= "REGISTER_23_A_" + role))
        keyboard[0].append(InlineKeyboardButton("B", callback_data= "REGISTER_23_B_" + role))
        keyboard[0].append(InlineKeyboardButton("C", callback_data= "REGISTER_23_C_" + role))
        keyboard[0].append(InlineKeyboardButton("H", callback_data= "REGISTER_23_H_" + role))
        update.message.reply_text("To register, please state which battery are you from?")
    elif unit == "24":
        keyboard = [[]]
        keyboard[0].append(InlineKeyboardButton("99", callback_data= "REGISTER_24_99_" + role))
        keyboard[0].append(InlineKeyboardButton("K", callback_data= "REGISTER_24_K_" + role))
        keyboard[0].append(InlineKeyboardButton("C", callback_data= "REGISTER_24_C_" + role))
        keyboard[0].append(InlineKeyboardButton("D", callback_data= "REGISTER_24_D_" + role))
        keyboard[0].append(InlineKeyboardButton("G", callback_data= "REGISTER_24_G_" + role))
        keyboard[0].append(InlineKeyboardButton("S", callback_data= "REGISTER_24_S_" + role))
        update.message.reply_text("To register, please state which battery are you from?")  
    elif unit == "21":
        keyboard = [[]]
        keyboard[0].append(InlineKeyboardButton("1", callback_data= "REGISTER_21_1_" + role))
        keyboard[0].append(InlineKeyboardButton("2", callback_data= "REGISTER_21_2_" + role))
        keyboard[0].append(InlineKeyboardButton("3", callback_data= "REGISTER_21_3_" + role))
        keyboard[0].append(InlineKeyboardButton("4", callback_data= "REGISTER_21_4_" + role))
        keyboard[0].append(InlineKeyboardButton("H", callback_data= "REGISTER_21_H_" + role))
        keyboard[0].append(InlineKeyboardButton("A", callback_data= "REGISTER_21_A_" + role))
        keyboard[0].append(InlineKeyboardButton("B", callback_data= "REGISTER_21_B_" + role))
        keyboard[0].append(InlineKeyboardButton("C", callback_data= "REGISTER_21_C_" + role))
        update.message.reply_text("To register, please state which battery are you from?")  
    elif unit == "SS":
        keyboard = [[]]
        keyboard[0].append(InlineKeyboardButton("99", callback_data= "REGISTER_SS_99_" + role))
        keyboard[0].append(InlineKeyboardButton("1", callback_data= "REGISTER_SS_1_" + role))
        keyboard[0].append(InlineKeyboardButton("2", callback_data= "REGISTER_SS_2_" + role))
        keyboard[0].append(InlineKeyboardButton("3", callback_data= "REGISTER_SS_3_" + role))
        keyboard[0].append(InlineKeyboardButton("4", callback_data= "REGISTER_SS_4_" + role))
        keyboard[0].append(InlineKeyboardButton("5", callback_data= "REGISTER_SS_5_" + role))
        keyboard[0].append(InlineKeyboardButton("6", callback_data= "REGISTER_SS_6_" + role))
        keyboard[0].append(InlineKeyboardButton("7", callback_data= "REGISTER_SS_7_" + role))
        update.message.reply_text("To register, please state which department are you from?")


    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose:', reply_markup = reply_markup)

def help(update, context):
    update.message.reply_text('Help!')

def echo(update, context):
    update.message.reply_text(update.message.text)

def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)
    
def cancel(update: Update, _: CallbackContext) -> int:
    update.message.reply_text(
        'Bye!', reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

def button(update: Update, context: CallbackContext) -> None:
    user_id = str(update.callback_query.message.chat['id'])
    first_name = deEmojify(update.callback_query.message.chat['first_name'])
    #first_name = update.callback_query.message.chat['first_name']
    query = update.callback_query
    cleaned_response = query.data.split("_")
    if cleaned_response[0] == "REGISTER":
        unit = cleaned_response[1]
        office = cleaned_response[2]
        role = cleaned_response[3]
        query.edit_message_text(text="Selected option: " + office)
        first_name = str(update.callback_query.message.chat['first_name'])
        first_name = deEmojify(first_name)
        addUser(user_id, first_name, office, role, unit)
        bot.send_message(chat_id = user_id, text="Thank you, you are now registered under " + office + " .")
        if user_id in users:
            bot.send_message(chat_id = user_id, text="To start a SPT, enter /run")
        else:
            bot.send_message(chat_id = user_id, text="You will be notified when a user starts a SPT.")
        print("New user registered id: "+ user_id +" Name: " + first_name)
    elif cleaned_response[0] == "SAFETY1":
        userOffice = users[str(user_id)][1]
        userUnit = users[str(user_id)][2]
        buddyName = buddyDict[int(user_id)][0]
        buddyContact = buddyDict[int(user_id)][1]
        if len(buddyContact) >= 3:
            lastThreeNums = buddyContact[-3:]
        else:
            lastThreeNums = buddyContact
        place = buddyDict[int(user_id)][2]
        masekdNum = "XXXX X" + lastThreeNums
        yesOrNo = cleaned_response[1]
        query.edit_message_text(text="Selected option: " + yesOrNo)
        if yesOrNo == "NO":
            keyboard = [[]]
            keyboard[0].append(InlineKeyboardButton("Yes", callback_data= "SAFETY2_YES"))
            keyboard[0].append(InlineKeyboardButton("No", callback_data= "SAFETY2_NO"))
            bot.send_message(chat_id = user_id, text="Have you ever experienced a diagnosis of/treatment for high blood pressure (BP), or a resting BP of 160/90 mmHg or higher within the past 6 months?")
            reply_markup = InlineKeyboardMarkup(keyboard)
            bot.send_message(chat_id = user_id, text='Please choose:', reply_markup = reply_markup)
        else:
            with open("Logs/" + userUnit + 'Log.csv', 'a') as f:
                f.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n"%(first_name, userOffice, buddyName, masekdNum, place, time.strftime("%X"), "", "Y", "", "", "", "", "", "", "", "", ""))  
            bot.send_message(chat_id = user_id, text="Please contact your superior for permission as this selection is a “No GO” criteria.")
            for ISO in ISOs:
                if ISOs[ISO][1] == userUnit:
                    bot.send_message(chat_id = ISO, text=first_name + " has done his self declaration, however, he has selected a 'NO GO' criteria")
            for key, value in COs.items():
                if value[1] == userOffice and value[2] == userUnit:
                    bot.send_message(chat_id = key, text=first_name + " has done his self declaration, however, he has selected a 'NO GO' criteria")
            return ConversationHandler.END
    elif cleaned_response[0] == "SAFETY2":
        userOffice = users[str(user_id)][1]
        userUnit = users[str(user_id)][2]
        buddyName = buddyDict[int(user_id)][0]
        buddyContact = buddyDict[int(user_id)][1]
        if len(buddyContact) >= 3:
            lastThreeNums = buddyContact[-3:]
        else:
            lastThreeNums = buddyContact
        place = buddyDict[int(user_id)][2]
        masekdNum = "XXXX X" + lastThreeNums
        yesOrNo = cleaned_response[1]
        query.edit_message_text(text="Selected option: " + yesOrNo)
        if yesOrNo == "NO":
            keyboard = [[]]
            keyboard[0].append(InlineKeyboardButton("Yes", callback_data= "SAFETY4_YES"))
            keyboard[0].append(InlineKeyboardButton("No", callback_data= "SAFETY4_NO"))
            bot.send_message(chat_id = user_id, text="Have you ever experienced dizziness or light-headedness during physical activity or shortness of breath at rest within the past 6 months?")
            reply_markup = InlineKeyboardMarkup(keyboard)
            bot.send_message(chat_id = user_id, text='Please choose:', reply_markup = reply_markup)
        else:
            with open("Logs/" + userUnit + 'Log.csv', 'a') as f:
                f.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n"%(first_name, userOffice, buddyName, masekdNum, place, time.strftime("%X"), "", "N", "Y", "", "", "", "", "", "", "", ""))  
            bot.send_message(chat_id = user_id, text="Please contact your superior for permission as this selection is a “No GO” criteria.")
            for ISO in ISOs:
                if ISOs[ISO][1] == userUnit:
                    bot.send_message(chat_id = ISO, text=first_name + " has done his self declaration, however, he has selected a 'NO GO' criteria")

            for key, value in COs.items():
                if value[1] == userOffice and value[2] == userUnit:
                    bot.send_message(chat_id = key, text=first_name + " has done his self declaration, however, he has selected a 'NO GO' criteria")
            return ConversationHandler.END
    elif cleaned_response[0] == "SAFETY4":
        userOffice = users[str(user_id)][1]
        userUnit = users[str(user_id)][2]
        buddyName = buddyDict[int(user_id)][0]
        buddyContact = buddyDict[int(user_id)][1]
        if len(buddyContact) >= 3:
            lastThreeNums = buddyContact[-3:]
        else:
            lastThreeNums = buddyContact
        place = buddyDict[int(user_id)][2]
        masekdNum = "XXXX X" + lastThreeNums
        yesOrNo = cleaned_response[1]
        query.edit_message_text(text="Selected option: " + yesOrNo)
        if yesOrNo == "NO":
            keyboard = [[]]
            keyboard[0].append(InlineKeyboardButton("Yes", callback_data= "SAFETY6_YES"))
            keyboard[0].append(InlineKeyboardButton("No", callback_data= "SAFETY6_NO"))
            bot.send_message(chat_id = user_id, text="Have you ever experienced loss of consciousness/fainting for any reason or experienced concussion within the past 6 months?")
            reply_markup = InlineKeyboardMarkup(keyboard)
            bot.send_message(chat_id = user_id, text='Please choose:', reply_markup = reply_markup)
        else:
            with open("Logs/" + userUnit + 'Log.csv', 'a') as f:
                f.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n"%(first_name, userOffice, buddyName, masekdNum, place, time.strftime("%X"), "", "N", "N", "Y", "", "", "", "", "", "", ""))  
            bot.send_message(chat_id = user_id, text="Please contact your superior for permission as this selection is a “No GO” criteria.")
            for ISO in ISOs:
                if ISOs[ISO][1] == userUnit:
                    bot.send_message(chat_id = ISO, text=first_name + " has done his self declaration, however, he has selected a 'NO GO' criteria")
            for key, value in COs.items():
                if value[1] == userOffice and value[2] == userUnit:
                    bot.send_message(chat_id = key, text=first_name + " has done his self declaration, however, he has selected a 'NO GO' criteria")
            return ConversationHandler.END
    elif cleaned_response[0] == "SAFETY6":
        userOffice = users[str(user_id)][1]
        userUnit = users[str(user_id)][2]
        buddyName = buddyDict[int(user_id)][0]
        buddyContact = buddyDict[int(user_id)][1]
        if len(buddyContact) >= 3:
            lastThreeNums = buddyContact[-3:]
        else:
            lastThreeNums = buddyContact
        place = buddyDict[int(user_id)][2]
        masekdNum = "XXXX X" + lastThreeNums
        yesOrNo = cleaned_response[1]
        query.edit_message_text(text="Selected option: " + yesOrNo)
        if yesOrNo == "NO":
            keyboard = [[]]
            keyboard[0].append(InlineKeyboardButton("Yes", callback_data= "SAFETY7_YES"))
            keyboard[0].append(InlineKeyboardButton("No", callback_data= "SAFETY7_NO"))
            bot.send_message(chat_id = user_id, text="Do you currently have pain or swelling in any part of your body (e.g. from an injury, acute flare-up of arthritis, or back pain) that affects your ability to be physically active?")
            reply_markup = InlineKeyboardMarkup(keyboard)
            bot.send_message(chat_id = user_id, text='Please choose:', reply_markup = reply_markup)
        else:
            with open("Logs/" + userUnit + 'Log.csv', 'a') as f:
                f.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n"%(first_name, userOffice, buddyName, masekdNum, place, time.strftime("%X"), "", "N", "N", "N", "Y", "", "", "", "", "", ""))  
            bot.send_message(chat_id = user_id, text="Please contact your superior for permission as this selection is a “No GO” criteria.")
            for ISO in ISOs:
                if ISOs[ISO][1] == userUnit:
                    bot.send_message(chat_id = ISO, text=first_name + " has done his self declaration, however, he has selected a 'NO GO' criteria")
            for key, value in COs.items():
                if value[1] == userOffice and value[2] == userUnit:
                    bot.send_message(chat_id = key, text=first_name + " has done his self declaration, however, he has selected a 'NO GO' criteria")
            return ConversationHandler.END
    elif cleaned_response[0] == "SAFETY7":
        userOffice = users[str(user_id)][1]
        userUnit = users[str(user_id)][2]
        buddyName = buddyDict[int(user_id)][0]
        buddyContact = buddyDict[int(user_id)][1]
        if len(buddyContact) >= 3:
            lastThreeNums = buddyContact[-3:]
        else:
            lastThreeNums = buddyContact
        place = buddyDict[int(user_id)][2]
        masekdNum = "XXXX X" + lastThreeNums
        yesOrNo = cleaned_response[1]
        query.edit_message_text(text="Selected option: " + yesOrNo)
        if yesOrNo == "NO":
            keyboard = [[]]
            keyboard[0].append(InlineKeyboardButton("Yes", callback_data= "SAFETY9_YES"))
            keyboard[0].append(InlineKeyboardButton("No", callback_data= "SAFETY9_NO"))
            bot.send_message(chat_id = user_id, text="Has a healthcare provider told you that you should avoid or modify certain types of physical activity or do you have any other medical or physical conditions (such as diabetes, cancer, osteoporosis, ashma, spinal cord injury) that may affect your ability to be physically active?")
            reply_markup = InlineKeyboardMarkup(keyboard)
            bot.send_message(chat_id = user_id, text='Please choose:', reply_markup = reply_markup)
        else:
            with open("Logs/" + userUnit + 'Log.csv', 'a') as f:
                f.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n"%(first_name, userOffice, buddyName, masekdNum, place, time.strftime("%X"), "", "N", "N", "N", "N", "Y", "", "", "", "", ""))  
            bot.send_message(chat_id = user_id, text="Please contact your superior for permission as this selection is a “No GO” criteria.")
            for ISO in ISOs:
                if ISOs[ISO][1] == userUnit:
                    bot.send_message(chat_id = ISO, text=first_name + " has done his self declaration, however, he has selected a 'NO GO' criteria")
            for key, value in COs.items():
                if value[1] == userOffice and value[2] == userUnit:
                    bot.send_message(chat_id = key, text=first_name + " has done his self declaration, however, he has selected a 'NO GO' criteria")
            return ConversationHandler.END
    elif cleaned_response[0] == "SAFETY9":
        userOffice = users[str(user_id)][1]
        userUnit = users[str(user_id)][2]
        buddyName = buddyDict[int(user_id)][0]
        buddyContact = buddyDict[int(user_id)][1]
        if len(buddyContact) >= 3:
            lastThreeNums = buddyContact[-3:]
        else:
            lastThreeNums = buddyContact
        place = buddyDict[int(user_id)][2]
        masekdNum = "XXXX X" + lastThreeNums
        yesOrNo = cleaned_response[1]
        query.edit_message_text(text="Selected option: " + yesOrNo)
        if yesOrNo == "NO":
            keyboard = [[]]
            keyboard[0].append(InlineKeyboardButton("Yes", callback_data= "SAFETY10_YES"))
            keyboard[0].append(InlineKeyboardButton("No", callback_data= "SAFETY10_NO"))
            bot.send_message(chat_id = user_id, text="Have you drank beyond the point of thirst and have at least 7 hours of uninterrupted rest?")
            reply_markup = InlineKeyboardMarkup(keyboard)
            bot.send_message(chat_id = user_id, text='Please choose:', reply_markup = reply_markup)
        else:
            with open("Logs/" + userUnit + 'Log.csv', 'a') as f:
                f.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n"%(first_name, userOffice, buddyName, masekdNum, place, time.strftime("%X"), "", "N", "N", "N", "N", "N", "Y", "", "", "", ""))  
            bot.send_message(chat_id = user_id, text="Please contact your superior for permission as this selection is a “No GO” criteria.")
            for ISO in ISOs:
                if ISOs[ISO][1] == userUnit:
                    bot.send_message(chat_id = ISO, text=first_name + " has done his self declaration, however, he has selected a 'NO GO' criteria")

            for key, value in COs.items():
                if value[1] == userOffice and value[2] == userUnit:
                    bot.send_message(chat_id = key, text=first_name + " has done his self declaration, however, he has selected a 'NO GO' criteria")
            return ConversationHandler.END
    elif cleaned_response[0] == "SAFETY10":
        userOffice = users[str(user_id)][1]
        userUnit = users[str(user_id)][2]
        buddyName = buddyDict[int(user_id)][0]
        buddyContact = buddyDict[int(user_id)][1]
        if len(buddyContact) >= 3:
            lastThreeNums = buddyContact[-3:]
        else:
            lastThreeNums = buddyContact
        place = buddyDict[int(user_id)][2]
        masekdNum = "XXXX X" + lastThreeNums
        yesOrNo = cleaned_response[1]
        query.edit_message_text(text="Selected option: " + yesOrNo)
        if yesOrNo == "YES":
            keyboard = [[]]
            keyboard[0].append(InlineKeyboardButton("Yes", callback_data= "SAFETY13_YES"))
            keyboard[0].append(InlineKeyboardButton("No", callback_data= "SAFETY13_NO"))
            bot.send_message(chat_id = user_id, text="Do you have any medical excuse, pre-existing medical condition or injury that prevents you from taking part in the activity or are you feeling unwell? For example, flu, diarrhea or vomitting in the past 24 hours?")
            reply_markup = InlineKeyboardMarkup(keyboard)
            bot.send_message(chat_id = user_id, text='Please choose:', reply_markup = reply_markup)
        else:
            with open("Logs/" + userUnit + 'Log.csv', 'a') as f:
                f.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n"%(first_name, userOffice, buddyName, masekdNum, place, time.strftime("%X"), "", "N", "N", "N", "N", "N", "N", "N", "", "", ""))  
            bot.send_message(chat_id = user_id, text="Please contact your superior for permission as this selection is a “No GO” criteria.")
            for ISO in ISOs:
                if ISOs[ISO][1] == userUnit:
                    bot.send_message(chat_id = ISO, text=first_name + " has done his self declaration, however, he has selected a 'NO GO' criteria")
            for key, value in COs.items():
                if value[1] == userOffice and value[2] == userUnit:
                    bot.send_message(chat_id = key, text=first_name + " has done his self declaration, however, he has selected a 'NO GO' criteria")
            return ConversationHandler.END
    elif cleaned_response[0] == "SAFETY13":
        userOffice = users[str(user_id)][1]
        userUnit = users[str(user_id)][2]
        buddyName = buddyDict[int(user_id)][0]
        buddyContact = buddyDict[int(user_id)][1]
        if len(buddyContact) >= 3:
            lastThreeNums = buddyContact[-3:]
        else:
            lastThreeNums = buddyContact
        place = buddyDict[int(user_id)][2]
        masekdNum = "XXXX X" + lastThreeNums
        yesOrNo = cleaned_response[1]
        query.edit_message_text(text="Selected option: " + yesOrNo)
        if yesOrNo == "NO":
            keyboard = [[]]
            keyboard[0].append(InlineKeyboardButton("Yes", callback_data= "SAFETY15_YES"))
            keyboard[0].append(InlineKeyboardButton("No", callback_data= "SAFETY15_NO"))
            bot.send_message(chat_id = user_id, text="Is your temperature 37.5°C or higher or do you have underlying medical conditions that require medical aid for you to train safely? For example, Asthmatic personnel.")
            reply_markup = InlineKeyboardMarkup(keyboard)
            bot.send_message(chat_id = user_id, text='Please choose:', reply_markup = reply_markup)
        else:
            with open("Logs/" + userUnit + 'Log.csv', 'a') as f:
                f.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n"%(first_name, userOffice, buddyName, masekdNum, place, time.strftime("%X"), "", "N", "N", "N", "N", "N", "N", "Y", "Y", "", ""))  
            bot.send_message(chat_id = user_id, text="Please contact your superior for permission as this selection is a “No GO” criteria.")
            for ISO in ISOs:
                if ISOs[ISO][1] == userUnit:
                    bot.send_message(chat_id = ISO, text=first_name + " has done his self declaration, however, he has selected a 'NO GO' criteria")
            for key, value in COs.items():
                if value[1] == userOffice and value[2] == userUnit:
                    bot.send_message(chat_id = key, text=first_name + " has done his self declaration, however, he has selected a 'NO GO' criteria")
            return ConversationHandler.END
    elif cleaned_response[0] == "SAFETY15":
        userOffice = users[str(user_id)][1]
        userUnit = users[str(user_id)][2]
        buddyName = buddyDict[int(user_id)][0]
        buddyContact = buddyDict[int(user_id)][1]
        if len(buddyContact) >= 3:
            lastThreeNums = buddyContact[-3:]
        else:
            lastThreeNums = buddyContact
        place = buddyDict[int(user_id)][2]
        masekdNum = "XXXX X" + lastThreeNums
        yesOrNo = cleaned_response[1]
        query.edit_message_text(text="Selected option: " + yesOrNo)
        if yesOrNo == "YES":
            with open("Logs/" + userUnit + 'Log.csv', 'a') as f:
                f.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n"%(first_name, userOffice, buddyName, masekdNum, place, time.strftime("%X"), "", "N", "N", "N", "N", "N", "N", "Y", "N", "Y", ""))  
            bot.send_message(chat_id = user_id, text="Please contact your superior for permission as this selection is a “No GO” criteria.")
            for ISO in ISOs:
                if ISOs[ISO][1] == userUnit:
                    bot.send_message(chat_id = ISO, text=first_name + " has done his self declaration, however, he has selected a 'NO GO' criteria")
            for key, value in COs.items():
                if value[1] == userOffice and value[2] == userUnit:
                    bot.send_message(chat_id = key, text=first_name + " has done his self declaration, however, he has selected a 'NO GO' criteria")
            return ConversationHandler.END
        notifyCO(int(user_id), first_name)
    elif cleaned_response[0] == "WORKOUT":
        place = cleaned_response[1]
        if place == "OutOfCamp":
            place = "Out of Camp"
        buddyDict[int(user_id)].append(place)
        query.edit_message_text(text="Selected option: " + place)
        bot.send_message(chat_id = user_id, text="Before starting your workout, please complete a self declaration safety checks")
        keyboard = [[]]
        keyboard[0].append(InlineKeyboardButton("Yes", callback_data= "SAFETY1_YES"))
        keyboard[0].append(InlineKeyboardButton("No", callback_data= "SAFETY1_NO"))
        bot.send_message(chat_id = user_id, text="Have you ever experienced a diagnosis of/treatment for heart disease or stroke, or pain/discomfort/pressure in your chest during activities of daily living or during your physical activity within the past 6 months?")
        reply_markup = InlineKeyboardMarkup(keyboard)
        bot.send_message(chat_id = user_id, text='Please choose:', reply_markup = reply_markup)
    elif cleaned_response[0] == "COMPLETED":
        yesOrNo = cleaned_response[1]
        query.edit_message_text(text="Selected option: " + yesOrNo)
        userOffice = users[str(user_id)][1]
        userUnit = users[str(user_id)][2]
        buddyName = buddyDict[int(user_id)][0]
        buddyContact = buddyDict[int(user_id)][1]
        if len(buddyContact) >= 3:
            lastThreeNums = buddyContact[-3:]
        else:
            lastThreeNums = buddyContact
        place = buddyDict[int(user_id)][2]
        masekdNum = "XXXX X" + lastThreeNums
        for key, value in COs.items():
            if value[1] == userOffice and value[2] == userUnit:
                if yesOrNo == "YES": 
                    bot.send_message(chat_id = key, text=first_name + " from " + userOffice + " has completed his SPT and is feeling well.")
                else:
                    bot.send_message(chat_id = key, text=first_name + " from " + userOffice + " has completed his SPT and is not feeling well.")
        if yesOrNo == "YES":
            with open("Logs/" + userUnit + 'Log.csv', 'a') as f:
                f.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n"%(first_name, userOffice, buddyName, masekdNum, place, currentRunning[userUnit + userOffice][int(user_id)][4], time.strftime("%X"), "N", "N", "N", "N", "N", "N", "N", "N", "Y", "Y"))  
            for ISO in ISOs:
                if ISOs[ISO][1] == userUnit:
                    bot.send_message(chat_id = ISO, text=first_name + " from " + userOffice + " has completed his SPT and is feeling well.")
        else:
            with open("Logs/" + userUnit + 'Log.csv', 'a') as f:
                f.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n"%(first_name, userOffice, buddyName, masekdNum, place, currentRunning[userUnit + userOffice][int(user_id)][4], time.strftime("%X"), "N", "N", "N", "N", "N", "N", "N", "N", "Y", "N"))  
            for ISO in ISOs:
                if ISOs[ISO][1] == userUnit:
                    bot.send_message(chat_id = ISO, text=first_name + " from " + userOffice + " has completed his SPT and is not feeling well.")
            bot.send_message(chat_id = user_id, text="Please go and report sick.")

        bot.send_message(chat_id = user_id, text="Thank you! The relevant parties have been notified!")
        print(first_name + " has completed his SPT")
        bot.send_message(chat_id = user_id, text="To start a new SPT, enter /run")
        currentRunning[userUnit + userOffice].pop(int(user_id))
        return ConversationHandler.END
        
def complete(update, context):
    keyboard = [[]]
    keyboard[0].append(InlineKeyboardButton("Yes", callback_data= "COMPLETED_YES"))
    keyboard[0].append(InlineKeyboardButton("No", callback_data= "COMPLETED_NO"))
    update.message.reply_text('Are you feeling well?')
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose:', reply_markup = reply_markup)
    
def check(update, context):
    user_id = str(update.message.chat['id'])
    if user_id not in COs and user_id not in ISOs:
        update.message.reply_text('Sorry! You do not have the permission for this command.')
        return ConversationHandler.END
    
    if user_id in COs:
        office = COs[user_id][1]
        unit = COs[user_id][2]
        runners = currentRunning[unit + office]
        if runners == {}:
            update.message.reply_text("No one is currently doing SPT")
        else:  
            filename = unit + office + "Current.csv"
            Genpath = path + 'GenResult/' + filename
            with open(Genpath, 'w') as outfile:
                writer = csv.writer(outfile)
                writer.writerow(["Name", "Unit", "Buddy Name", "Buddy HP Number", "Location", "Start Time"])
                for key, value in runners.items():
                    value.insert(1, office)
                    writer.writerow(value)
            bot.send_document(chat_id=user_id, document=open(Genpath, 'rb'))
    else:
        filename = "ISOCurrent.csv"
        Genpath = path + 'GenResult/' + filename
        with open(Genpath, 'w') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(["Name", "Unit", "Buddy Name", "Buddy HP Number", "Location", "Start Time"])
            for office, value in currentRunning.items():
                if office[0:2] == ISOs[user_id][1]:
                    for userID, runInfo in value.items():
                        runInfo.insert(1, office[2:])
                        writer.writerow(runInfo)
        bot.send_document(chat_id=user_id, document=open(Genpath, 'rb'))

def reset(update, context):
    user_id = str(update.message.chat['id'])
    if user_id in users:
        users.pop(user_id)
        with open('Runners.csv', 'w') as f:
            for key in users.keys():
                f.write("%s,%s,%s,%s\n"%(key, users[key][0], users[key][1], users[key][2]))  
        update.message.reply_text('Account sucessfully reseted.')
        update.message.reply_text('Please register your self again by entering /start')
    elif user_id in COs:
        COs.pop(user_id)
        with open('COs.csv', 'w') as f:
            for key in COs.keys():
                f.write("%s,%s,%s,%s\n"%(key, COs[key][0], COs[key][1], COs[key][2]))
        update.message.reply_text('Account sucessfully reseted.')
        update.message.reply_text('Please register your self again by entering /start')
    elif user_id in ISOs:
        ISOs.pop(user_id)
        with open('ISO.csv', 'w') as f:
            for key in ISOs.keys():
                f.write("%s\n"%(key, ISOs[key][0], ISOs[key][1]))   
        update.message.reply_text('Account sucessfully reseted.')
        update.message.reply_text('Please register your self again by entering /start')
    else:
        print(user_id + " facing error resetting account.")
        update.message.reply_text('Error encountered, please try again /start.')
        
def log(update, context):
    user_id = str(update.message.chat['id'])
    if user_id not in COs and user_id not in ISO:
        update.message.reply_text('Sorry! You do not have the permission for this command.')
        return ConversationHandler.END
    if user_id in COs:
        userUnit = COs[str(user_id)][2]
    else:
        userUnit = ISOs[str(user_id)][1]
    Genpath = path + 'Logs/' + userUnit + "Log.csv"
    bot.send_document(chat_id=user_id, document=open(Genpath, 'rb'))

def clear(update, context):   
    user_id = str(update.message.chat['id'])
    if user_id not in COs:
        update.message.reply_text('Sorry! You do not have the permission for this command.')
        return ConversationHandler.END
    userUnit = users[str(user_id)][2]
    Genpath = path + 'Logs/' + userUnit + "Log.csv"
    with open(Genpath, 'w') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(["Name", "Office", "Buddy Name", "Buddy HP Number", "Location", "Start Time", "End Time", "Safety Q1", "Safety Q2", "Safety Q3", "Safety Q4", "Safety Q5", "Safety Q6", "Safety Q7", "Safety Q8", "Safety Q9", "Feeling Well After SPT"])
    bot.send_message(chat_id = user_id, text = userUnit + " Logs has been sucessfully cleared.")
    print(userUnit + " Logs cleared.")

def main():
    loadData()
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    start_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            register_user: [MessageHandler(Filters.text, registerUser)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    run_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('run', run)],
        states={
            run_2: [MessageHandler(Filters.text, run_2_func)],
            run_3: [MessageHandler(Filters.text, run_3_func)]

        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    complete_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('complete', complete)],
        states={

        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    checkRunner_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('check', check)],
        states={

        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    log_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('log', log)],
        states={

        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    clear_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('clear', clear)],
        states={

        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dp.add_handler(start_conv_handler)
    dp.add_handler(run_conv_handler)
    dp.add_handler(complete_conv_handler)
    dp.add_handler(checkRunner_conv_handler)
    dp.add_handler(log_conv_handler)
    dp.add_handler(clear_conv_handler)
    dp.add_handler(CommandHandler("reset", reset))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_handler(CallbackQueryHandler(button))
    #job_queue.run_repeating(send_message_job, interval=3600.0, first=0.0)
    #dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
