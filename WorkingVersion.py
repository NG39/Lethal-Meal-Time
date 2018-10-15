import logging

import random

from flask import Flask, render_template

from flask_ask import Ask, statement, question, session, convert_errors


app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

#dictionaries
dictfood = {"apples":["",0.285,"the cyanide in the seeds", 0.16],
            "oranges":["", 157.14,"vitamin C poisoning",0.13 ],
            "bananas":["", 6.86,"hyperkalemia or excess potassium in blood", 0.12],
            "chocolates":["",1.214,"excess theobromine",0.180],
            "almonds":["raw",0.214,"cyanide poisoning", 0.0012],
           "cherries":["seeds of", 0.0285, "cyanide poisoning", 0.005]}
foodkeys = list(dictfood.keys())

drinks = {'vodka' : ['shots of ',0.186,"alcohol poisoning"],'whisky' : ['shots of ',0.186,"alcohol poisoning"],
          'coffee' : ['cups of ',1.714,"caffeine overdose."], 'water':['glasses of ',0.23,"hyponatremia or too little salt in blood"] ,
          'espresso' : ['shots of ',2.557,"caffeine overdose."],'tequila' : ['shots of ',0.186,"alcohol poisoning"]}
drinkkeys = list(drinks.keys())




#start of program
@ask.launch
def start():

    welcome_msg = "Welcome to Lethal Meal Time. What would be your last supper?"

    return question(welcome_msg)

@ask.intent("KgFIntent", convert = {"kg":float, "food":str})
def foodanswer(food, kg):
    session.attributes['kg'] = kg
    if food[-1]=="y":
        food = food[:-1]+"ies"
    if food[-1] !="s":
        food = food + "s"
    print(food)
    
    if food in foodkeys:
        session.attributes['var'] = food
        msg = "What is your weight in kilograms?"

    else:
        print(session.attributes.keys())
        
        suggestion = random.randint(0,len(foodkeys)-1)
        msg = "Sorry I don't have the data for %s. You can try asking me about %s" %(food, foodkeys[suggestion])
    return question(msg)
 
    
    
@ask.intent("QFIntent", convert = {"food":str, "quantity":int})
def foodanswer(food, quantity):
    session.attributes['quantity'] = quantity
    if food[-1]=="y":
        food = food[:-1]+"ies"
    if food[-1] !="s":
        food = food + "s"
    print(food)
    
    if food in foodkeys:
        session.attributes['var'] = food
        msg = "What is your weight in kilograms?"

    else:
            
        suggestion = random.randint(0,len(foodkeys)-1)
        msg = "Sorry I don't have the data for %s. You can try asking me about %s" %(food, foodkeys[suggestion])
    return question(msg)



@ask.intent("FIntent", convert={'food': str})
def foodanswer(food):
    if food[-1]=="y":
        food = food[:-1]+"ies"
    if food[-1] !="s":
        food = food + "s"
    print(food)
    if food in foodkeys:
        session.attributes['var'] = food
        msg = "What is your weight in kilograms?"
        
    else:
        suggestion = random.randint(0,len(foodkeys)-1)
        msg = "Sorry I don't have the data for %s. You can try asking me about %s" %(food, foodkeys[suggestion])
    return question(msg)
    
    
   
@ask.intent("DIntent", convert = {"drink":str})


def drinkanswer(drink):
    if drink in drinks.keys():
        session.attributes['var'] = drink
        msg = "What is your weight in kilograms?"

    else:
        suggestion = random.randint(0,len(drinkkeys)-1)
        msg = "Sorry I don't have the data for %s. You can try asking me about %s" %(drink, drinkkeys[suggestion])
    return question(msg)

  
    


@ask.intent("WIntent", convert={'number': int})
def checkweight(number):

    
    if number<=10:
        message = "That is too light. Can you add a couple more kilograms?"
        return question(message)
    
    if session.attributes["var"] in foodkeys:
        food = session.attributes['var']
        dose = int(round(number * dictfood[food][1]))
        endmessage  = " %d %s %s will be deadly for you. Death due to %s . " %(dose, dictfood[food][0], food, dictfood[food][2])
       
        if "quantity" in session.attributes.keys():
            quantity = session.attributes["quantity"]
            dose1 = dose - quantity
            if dose1<=0:
                endmessage = "Do you really need %d %s? You should reconsider your life choices." % (quantity, food)
            else:
                endmessage  = " You need around %d more %s for it to be deadly. Death due to %s . " %(dose1, food, dictfood[food][2])
                   
        if "kg" in session.attributes.keys():
            kg = session.attributes["kg"]
            quantity = int(kg/dictfood[food][3])
            dose1 = dose - quantity
            if dose1 <= 0:
                endmessage = "Do you really need %s kilograms of  %s? You should reconsider your life choices." % (str(kg), food)
            else:
                #rewrite to print kilograms
                totalkg = dose1*dictfood[food][3]
                kgtolethal = round(totalkg)
                endmessage  = " You need around  %d kg more of %s for it to be deadly. Death due to %s ." %(kgtolethal, food, dictfood[food][2])
            
            

    else:
        drink = session.attributes['var']
        dose = int(round(number*drinks[drink][1]))
        endmessage = "You will need to drink %d %s %s before you die. Death due to %s . " % (dose,drinks[drink][0], drink,drinks[drink][2])
    endmessage =endmessage +" You can ask me again for another item."
    return question(endmessage)
        


if __name__ == '__main__':

    app.run(debug=True)


