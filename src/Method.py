import math as m
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import statistics as stat
from scipy.stats import norm
import copy
""""The method.py is responsible for both being a calculator of European options, """


#Important Constants
days_in_year=252 #Business days in a stock year.
pi = m.pi

h_stock = .01
h_volatility = .0001
h_rfr = .0001
h_T = .0002
#These few are nudges for the Greeks.

learning_rate = .1 #Small constant used later


#Bell curve function
def N(x):
    #Uses the bell function function from scipy.stats
    return norm.cdf(x)

#European Option Formula. This simply just applies the formula from Black-Scholes to find the European option cost.
def european_option_formula(stock_price, strike, expiration, volatility, rfr, div_yield, call_put):
    #Uses the common form of finding d1 and d2 and then calculating it in terms of d1 and d2
    d1 = (np.log(stock_price/strike)+(rfr-div_yield+(volatility**2)/2)*expiration)/(volatility*m.sqrt(expiration))
    d2 = d1 - volatility * m.sqrt(expiration)
    if call_put != "yes":
        d1 = -d1
        d2 = -d2
    #see later for call vs. put
    std1 = N(d1)
    std2 = N(d2)
    answer = stock_price * m.exp(-div_yield* expiration) * std1 - strike * m.exp(-rfr*expiration) * std2 #uses formula
    if call_put == "yes":
        return answer
    else:
        return -answer
    #If european option is put option, it turns out that the put option is simply the negative of d1 and d2 and then the answer, so used that to write more efficient code.


#The common use CRR method of finding American options. It calculates the hold and exercise advantage at each node and works backwards to find the American option cost.
def american_option_main(stock_price, strike, expiration, volatility, rfr, div_yield, call_put, time_step):
    if call_put == "yes":
        decider = -1
    else:
        decider = 1
    #Noticed that the only difference between call and put option mathematically came down to a -1.
    frequency_step = expiration/time_step #finds how long (part of a year) each time_step is.
    up = m.exp(volatility * m.sqrt(frequency_step))
    down = 1/up
    rnp = (m.exp((rfr -div_yield )*frequency_step) - down)/(up-down)
    reduction = m.exp(-rfr *frequency_step) #important formulas for CRR.
    j = np.arange(time_step + 1)
    prices = stock_price * (up ** (time_step - j)) * (down ** j) #this gives every permutation of up^(1...time_step) and down^(time_step...1) and then multiplies it by stock_prices for a very efficient way of getting the last node.
    values = np.maximum(decider * (strike - prices), 0.0)  #uses the formula for the last node.
    for i in range(time_step - 1, -1, -1): #Using the previous node to calculate the new node using the same logic as the initial step. Then when only 1 value left, that is the option price.
        j = np.arange(i+1)
        prices = stock_price * (up** (i-j)) * (down **j)
        hold = reduction * (rnp * values[:i+1] + (1-rnp) * values[1:i+2]) #new formula that gives you how worth it is to hold the American option.
        exercise = decider * (strike - prices)
        values = np.maximum(hold, exercise)
    return values[0]

#The Theta Method of American Option: American Option Formula where we discretize and optimize by finding when theta = 0 (using gradient ascent) and max points and then taking the maximum point, we take that as our American option.
def american_option_theta(stock_price, strike, expiration, volatility, rfr, div_yield, call_put, time_step, iteration_max):
    frequency_step = expiration / (time_step)
    quantized_expiration = np.arange(frequency_step, expiration + 2 * frequency_step, frequency_step) #includes the first step and one extra at the end to contain the whole interval.
    quantized_expiration_changed = quantized_expiration[0:-1] #deletes the last step at the end and where we will work gradient ascent.
    theta = Theta(stock_price, strike, expiration, volatility, rfr, div_yield, call_put, time_step)
    c = 0
    #Makes sure each gradient ascent does not go over iteration_max, and so let the expiration point does not go below 1 minute and makes sure theta is relevantly large to the actual price.
    while c < iteration_max and 1/(365*24*60) < quantized_expiration_changed[0] < min(expiration, quantized_expiration[1]) and abs(theta) > .001 * european_option_formula(stock_price, strike, quantized_expiration_changed[0], volatility, rfr, div_yield, call_put):
        theta = Theta(stock_price, strike, quantized_expiration_changed[0], volatility, rfr, div_yield, call_put, time_step)
        quantized_expiration_changed[0] = quantized_expiration_changed[0] - theta * frequency_step * learning_rate #Notice that dtheta = -dtime, so there is a minus used instead of a plus. This is gradient ascent step.
        c += 1
    if quantized_expiration_changed[0] < 1/(365*24*60): #making sure that first point does not go above the second or below the "pretty much zero" point otherwise problems occur.
        quantized_expiration_changed[0]= 1/(365 * 24*60)
    for i in range(1, time_step): #The same idea as previously except now looped over every other point.
        c = 0
        theta = Theta(stock_price, strike, quantized_expiration[i], volatility, rfr, div_yield, call_put, time_step)
        j = i-1
        k = i+1
        while c < iteration_max and max(quantized_expiration_changed[j], i/(365*24*60)) < quantized_expiration_changed[i] < min(expiration, quantized_expiration[k]) and abs(theta) > .001 * european_option_formula(stock_price, strike, quantized_expiration_changed[i],volatility, rfr, div_yield, call_put):
            theta = Theta(stock_price, strike, quantized_expiration_changed[i], volatility, rfr, div_yield, call_put, time_step)
            quantized_expiration_changed[i] = quantized_expiration_changed[i] - theta * frequency_step * learning_rate
            c += 1

        boole= max(quantized_expiration_changed[i - 1], i/(365*24*60)) < quantized_expiration_changed[i] < min(expiration, quantized_expiration[i + 1])
        if boole == False:
            if max(quantized_expiration_changed[i - 1], i/(365*24*60)) >= quantized_expiration_changed[i]:
                quantized_expiration_changed[i] = max(quantized_expiration_changed[i - 1], i/(365*24*60))
            else:
                quantized_expiration_changed[i] = min(expiration, quantized_expiration[i+1])
    max_option = european_option_formula(stock_price, strike, quantized_expiration_changed[0], volatility, rfr, div_yield, call_put)
    for i in range(time_step): #This just finds the max number of the options
        compare = european_option_formula(stock_price, strike, quantized_expiration_changed[i], volatility, rfr, div_yield, call_put)
        if max_option < compare:
            max_option = compare
    return max_option #returns it.

#These sets of functions find the Greeks. Theta and Delta are the most important because Theta is a part of another method and Delta has a second derivative Gamma.
#The Greeks are found by using finite difference method with respect to both the stock_price and the nudging constants above. The function "Greeks" calculates all of the Greeks and returns them.
def Delta(stock_price, strike, expiration, volatility, rfr, div_yield, call_put):
    return (european_option_formula(stock_price * (1+h_stock/2), strike, expiration, volatility, rfr, div_yield, call_put) - european_option_formula(stock_price * (1-h_stock/2), strike, expiration, volatility, rfr, div_yield, call_put))/(stock_price * h_stock)
def Theta(stock_price, strike, expiration, volatility, rfr, div_yield, call_put, time_step):
    if time_step <= 1:
        return (european_option_formula(stock_price, strike, expiration * (1 + h_T * expiration / 2), volatility, rfr, div_yield, call_put) - european_option_formula(stock_price, strike, expiration* (1 - h_T * expiration / 2),volatility, rfr, div_yield, call_put)) / (expiration**2 * h_T)
    else:
        frequency_step = expiration/time_step
        return (european_option_formula(stock_price, strike, expiration * (1 + h_T * frequency_step / 2), volatility, rfr, div_yield, call_put) - european_option_formula(stock_price, strike, expiration * (1 - h_T * frequency_step / 2), volatility, rfr, div_yield, call_put)) / (expiration * frequency_step * h_T)
def Greeks(stock_price, strike, expiration, volatility, rfr, div_yield, call_put, time_step):
    delta = Delta(stock_price, strike, expiration, volatility, rfr, div_yield, call_put)
    Gamma = (Delta(stock_price*(1+h_stock/2), strike, expiration, volatility, rfr, div_yield, call_put) - Delta(stock_price*(1-h_stock/2), strike, expiration, volatility, rfr, div_yield, call_put))/(stock_price*h_stock)
    Vega = (european_option_formula(stock_price, strike, expiration, volatility * (1+h_volatility/2), rfr, div_yield, call_put) - european_option_formula(stock_price, strike, expiration, volatility * (1-h_volatility/2), rfr, div_yield, call_put))/(100 * volatility*h_volatility)
    Rho = (european_option_formula(stock_price, strike, expiration, volatility,  (1+h_rfr/2)* rfr, div_yield, call_put) - european_option_formula(stock_price, strike, expiration, volatility, (1-h_rfr/2)* rfr, div_yield, call_put))/(100 * rfr * h_rfr)
    if time_step == 0:
        d1 = (np.log(stock_price / strike) + (rfr - div_yield + (volatility ** 2) / 2) * expiration) / (
                    volatility * expiration)
        d2 = d1 - volatility * m.sqrt(expiration)
        if call_put != "yes":
            d2 = -d2
            d1=-d1
        exponentiad1 = m.exp(-(d1**2)/2)/(m.sqrt(pi*2))
        std1 = N(d1)
        std2 = N(d2)
        if call_put == "yes":
            theta = -stock_price * exponentiad1 * volatility/(2 * m.sqrt(expiration)) + div_yield * stock_price * m.exp(-div_yield* expiration) * std1  - rfr * strike * m.exp(-rfr * expiration) * std2
        else:
            theta = -stock_price * exponentiad1 * volatility/(2 * m.sqrt(expiration)) - div_yield * stock_price * m.exp(-div_yield * expiration) * std1 + rfr * strike * m.exp(-rfr * expiration) * std2
    else:
        theta = Theta(stock_price, strike, expiration, volatility, rfr, div_yield, call_put, time_step)
    return delta, Gamma, Vega, Rho,theta

#User interface section for people wishing to use the calculator with any stock they wish.
if __name__ == '__main__':
    #A lot of the next set of code is just inputting variables and finding values.
    stock = yf.Ticker(input("What stock would you like to analyze?"))
    stock_price = float(str(stock.history(period="1d")[["Close"]]).split()[4]) #Finds the stock price by locating it on the table.
    strike = float(input("What is the strike?"))
    expiration = float(input("What is the expiration (in years)?"))
    historical_or_user = input("Would you like to use historical or implied volatility? (answer historical or implied) ")
    if historical_or_user == "implied":
        volatility = float(input("Please place implied volatility here (in percentage without the sign)?"))/100
    else:
        #this simply follows how historical volatility is calculated and computes the math
        stock_over_time = stock.history(period="252d")['Close'].tolist()
        logreturn = []
        b = np.log(float(stock_over_time[0]))
        for i in range(1, days_in_year):
            a = b
            b = np.log(float(stock_over_time[i]))
            logreturn.append(b-a)
        volatility = stat.stdev(logreturn) * m.sqrt(days_in_year)
    rfr = float(input("Risk-free interest rate (in %)?"))/100
    time_step = float(input("How many time steps would you like to use? (0 for just a European option calculator)"))
    while time_step % 1 != 0 or time_step < 0: #makes sure time_step is a nonnegative integer and loops until it is
        print("Please enter an positive integer (if you want European Option, use 0)")
        time_step = input("How many time steps would you like to use?")
    time_step = int(time_step) #makes time_step int so loops can be done over it if necessary
    call_put = input("Do you want a call option (yes/no, if no, then it becomes a put option)?").lower()
    div_yield = stock.info.get('dividendYield', 0.0)/100 #gets dividend yield from a table using the stock.
    if time_step == 0:
        print(f'The European Option is ${european_option_formula(stock_price, strike, expiration, volatility, rfr, div_yield, call_put)}') #returns the European option using the method above.


    else:
        iteration_max = int(input("How many times max each timestep do you want to do gradient descent?")) #Asks for the max amount of times allowed to do gradient ascent in the Theta Method of American Option.
        max_option = american_option_theta(stock_price, strike, expiration, volatility, rfr, div_yield, call_put, time_step, iteration_max)
        print(f'The American Option is ${max_option} with the Theta method')
        print(f'The American Option is {american_option_main(stock_price, strike, expiration, volatility, rfr, div_yield, call_put, time_step)} with the CRR method.') #Gives both American Options (CRR is more widely accepted)




    want_greeks = input("Do you want the Greeks? (yes/no)").lower() #asks if greeks are wanted
    if want_greeks == "yes":
        (delta, Gamma, Vega, Rho, theta) = Greeks(stock_price, strike, expiration, volatility, rfr, div_yield, call_put, time_step)
        print(f'Delta is {delta}')
        print(f'Gamma is {Gamma}')
        print(f'Vega is {Vega}')
        print(f'Rho is {Rho}')
        print(f'Theta is {theta}')
        #Prints all of the Greeks



