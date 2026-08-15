import numpy as np
import matplotlib.pyplot as plt
import Method as M
import time as t
#The idea of this code is comparing Theta American Option Formula vs. CRR amongst different stats that we would think to have the most effect.
#The Theta American Option Formula is in-nature with the European Option Formula, and therefore, the Theta American Option Formula will get tested on the things that
#most make the CRR different from the regular European Option Formula. These are the different plots (and then of course there is the runtime).
run_plot_one = input("Generate plot for accuracy with different moneyness (S/K)? (yes/no)")
run_plot_two = input("Generate plot for accuracy with different dividend yields? (yes/no)")
run_plot_three = input("Generate plot to see the difference in times per number of timesteps? (yes/no)")
run_plot_four = input("Generate plot to see difference when increasing expiration? (yes/no)")
run_plot_five = input("Generate plot to see time difference per timestep for both? (yes/no)")
#Plots 1-4 are pretty much the same code but very slightly different (testing different parameters).
#They create a call and a put section and then run it changing one of the variables and then plot the graph with a legend.
#Time_step is reduced to a smaller number because of how easily it can get out of hand for y_values_Theta, but multiplied by 100 for CRR to get a more accurate answer.
if run_plot_one == "yes":
    iteration_max = 10000
    x_values = []
    y_values_Theta_yes = []
    y_values_Theta_no = []
    y_values_CRR_yes = []
    y_values_CRR_no = []
    for j in range(2):
        if j == 1:
            call_put = "no"
        else:
            call_put = "yes"
        for i in range(30):
            stock_price = 100
            strike = 50+5*i
            expiration = .5
            volatility = .3
            rfr = .03
            div_yield = .005
            time_step = 20
            if j == 0:
                x_values.append(stock_price/strike)
            if j ==0:
                y_values_Theta_yes.append(M.american_option_theta(stock_price, strike, expiration, volatility, rfr, div_yield, call_put, time_step, iteration_max))
                y_values_CRR_yes.append(M.american_option_main(stock_price, strike, expiration, volatility, rfr, div_yield, call_put, time_step*100))
            else:
                y_values_Theta_no.append( M.american_option_theta(stock_price, strike, expiration, volatility, rfr, div_yield, call_put,time_step, iteration_max))
                y_values_CRR_no.append(M.american_option_main(stock_price, strike, expiration, volatility, rfr, div_yield, call_put,time_step*100))
            #y_values_exercise.append(M.american_option_exercise(stock_price, strike, expiration, volatility, rfr, div_yield, call_put, time_step))
            print(j,i) #Lets you know how far in the process it is.
    x_array = np.array(x_values)
    y_array_Theta_call = np.array(y_values_Theta_yes)
    y_array_Theta_put = np.array(y_values_Theta_no)
    y_array_CRR_call = np.array(y_values_CRR_yes)
    y_array_CRR_put = np.array(y_values_CRR_no)
    if 0 in y_array_CRR_call: #This part of the code checks to see if there are any zeros in the y_array_CRR because then the error would not be defined. We write these points as zeros and hope they do not happen often.
        error = []
        for i in range(len(y_array_CRR_call)):
            if y_array_CRR_call[i] != 0:
                error.append(100*(abs(y_array_Theta_call[i] - y_array_CRR_call[i]))/abs(y_array_CRR_call[i]))
            else:
                error.append(0)
        error_call = np.array(error)
    else:
        error_call = 100*(abs(y_array_Theta_call - y_array_CRR_call))/abs(y_array_CRR_call)
    if 0 in y_array_CRR_put:
        error = []
        for i in range(len(y_array_CRR_put)):
            if y_array_CRR_put[i] != 0:
                error.append(100*(abs(y_array_Theta_put[i] - y_array_CRR_put[i]))/abs(y_array_CRR_put[i]))
            else:
                error.append(0)
        error_put = np.array(error)
    else:
        error_put = (100*abs(y_array_Theta_put - y_array_CRR_put))/y_array_CRR_put
    fig0, ax0 = plt.subplots()
    ax0.plot(x_array, error_call, color="red", linestyle='--', label = "Call Error %")
    ax0.plot(x_array, error_put, color="blue", linestyle='--', label = "Put Error %")
    ax0.set_xlabel('Moneyness (Stock Price)/Strike')
    ax0.set_ylabel('Relative Error % from CRR')
    plt.legend()
    ax0.set_yscale("log") #This scale is in logarithm because of big of a difference it is to be in call/put.
    plt.legend()
    plt.show()
    print("Plot 1 Complete") #Remember to close the plot to continue the code.
if run_plot_two == "yes": #Same code except now we barely change dividend yield.
    iteration_max = 10000
    x_values = []
    y_values_Theta_yes = []
    y_values_Theta_no =[]
    y_values_CRR_yes = []
    y_values_CRR_no = []
    for j in range(2):
        if j == 1:
            call_put = "no"
        else:
            call_put = "yes"
        for i in range(11):
            stock_price = 100
            strike = 110
            expiration = .5
            volatility = .3
            rfr = .03
            div_yield = .01 * i
            time_step = 20
            if j == 0:
                x_values.append(div_yield * 100)
            if j ==0:
                y_values_Theta_yes.append(M.american_option_theta(stock_price, strike, expiration, volatility, rfr, div_yield, call_put, time_step, iteration_max))
                y_values_CRR_yes.append(M.american_option_main(stock_price, strike, expiration, volatility, rfr, div_yield, call_put, time_step*100))
            else:
                y_values_Theta_no.append( M.american_option_theta(stock_price, strike, expiration, volatility, rfr, div_yield, call_put,time_step, iteration_max))
                y_values_CRR_no.append(M.american_option_main(stock_price, strike, expiration, volatility, rfr, div_yield, call_put,time_step*100))
            #y_values_exercise.append(M.american_option_exercise(stock_price, strike, expiration, volatility, rfr, div_yield, call_put, time_step))
            print(j,i)
    x_array = np.array(x_values)
    y_array_Theta_call = np.array(y_values_Theta_yes)
    y_array_Theta_put = np.array(y_values_Theta_no)
    y_array_CRR_call = np.array(y_values_CRR_yes)
    y_array_CRR_put = np.array(y_values_CRR_no)
    if 0 in y_array_CRR_call:
        error = []
        for i in range(len(y_array_CRR_call)):
            if y_array_CRR_call[i] != 0:
                error.append(100*(abs(y_array_Theta_call[i] - y_array_CRR_call[i]))/abs(y_array_CRR_call[i]))
            else:
                error.append(0)
        error_call = np.array(error)
    else:
        error_call = 100*(abs(y_array_Theta_call - y_array_CRR_call))/abs(y_array_CRR_call)
    if 0 in y_array_CRR_put:
        error = []
        for i in range(len(y_array_CRR_put)):
            if y_array_CRR_put[i] != 0:
                error.append(100*(abs(y_array_Theta_put[i] - y_array_CRR_put[i]))/abs(y_array_CRR_put[i]))
            else:
                error.append(0)
        error_put = np.array(error)
    else:
        error_put = (100*abs(y_array_Theta_put - y_array_CRR_put))/y_array_CRR_put
    fig1, ax1 = plt.subplots()
    ax1.plot(x_array, error_call, color="red", linestyle='--', label = "Call Error %")
    ax1.plot(x_array, error_put, color="blue", linestyle='--', label = "Put Error %")
    ax1.set_xlabel('Dividend yield (in %)')
    ax1.set_ylabel('Relative Error % from CRR')
    #plt.scatter(x_values, y_values_exercise, c='green', label = "Main dots")
    plt.legend()
    plt.show()
    print("Plot 2 complete")
if run_plot_three == "yes":
    iteration_max = 10000
    x_values = []
    y_values_Theta_yes = []
    y_values_Theta_no =[]
    y_values_CRR_yes = []
    y_values_CRR_no = []
    #y_values_exercise = []
    for j in range(2):
        if j == 1:
            call_put = "no"
        else:
            call_put = "yes"
        for i in range(11):
            stock_price = 100
            strike = 110
            expiration = .5
            volatility = .3
            rfr = .01*i
            div_yield = .005
            time_step = 20
            if j == 0:
                x_values.append(rfr * 100)
            if j ==0:
                y_values_Theta_yes.append(M.american_option_theta(stock_price, strike, expiration, volatility, rfr, div_yield, call_put, time_step, iteration_max))
                y_values_CRR_yes.append(M.american_option_main(stock_price, strike, expiration, volatility, rfr, div_yield, call_put, time_step*100))
            else:
                y_values_Theta_no.append( M.american_option_theta(stock_price, strike, expiration, volatility, rfr, div_yield, call_put,time_step, iteration_max))
                y_values_CRR_no.append(M.american_option_main(stock_price, strike, expiration, volatility, rfr, div_yield, call_put,time_step*100))
            #y_values_exercise.append(M.american_option_exercise(stock_price, strike, expiration, volatility, rfr, div_yield, call_put, time_step))
            print(j,i)
    x_array = np.array(x_values)
    y_array_Theta_call = np.array(y_values_Theta_yes)
    y_array_Theta_put = np.array(y_values_Theta_no)
    y_array_CRR_call = np.array(y_values_CRR_yes)
    y_array_CRR_put = np.array(y_values_CRR_no)
    if 0 in y_array_CRR_call:
        error = []
        for i in range(len(y_array_CRR_call)):
            if y_array_CRR_call[i] != 0:
                error.append(100*(abs(y_array_Theta_call[i] - y_array_CRR_call[i]))/abs(y_array_CRR_call[i]))
            else:
                error.append(0)
        error_call = np.array(error)
    else:
        error_call = 100*(abs(y_array_Theta_call - y_array_CRR_call))/abs(y_array_CRR_call)
    if 0 in y_array_CRR_put:
        error = []
        for i in range(len(y_array_CRR_put)):
            if y_array_CRR_put[i] != 0:
                error.append(100*(abs(y_array_Theta_put[i] - y_array_CRR_put[i]))/abs(y_array_CRR_put[i]))
            else:
                error.append(0)
        error_put = np.array(error)
    else:
        error_put = (100*abs(y_array_Theta_put - y_array_CRR_put))/abs(y_array_CRR_put)
    fig2, ax2 = plt.subplots()
    ax2.plot(x_array, error_call, color="red", linestyle='--', label = "Call Error %")
    ax2.plot(x_array, error_put, color="blue", linestyle='--', label = "Put Error %")
    ax2.set_xlabel('Risk Free Interest Rate (in %)')
    ax2.set_ylabel('Relative Error % from CRR')
    #plt.scatter(x_values, y_values_exercise, c='green', label = "Main dots")
    plt.legend()
    plt.show()
    print("Plot 3 Complete")
if run_plot_four == "yes":
    iteration_max = 10000
    x_values = []
    y_values_Theta_yes = []
    y_values_Theta_no = []
    y_values_CRR_yes = []
    y_values_CRR_no = []
    #y_values_exercise = []
    for j in range(2):
        if j == 1:
            call_put = "no"
        else:
            call_put = "yes"
        for i in range(1,16):
            stock_price = 100
            strike = 110
            expiration = .1*i
            volatility = .3
            rfr = .03
            div_yield = .005
            time_step = 20
            if j == 0:
                x_values.append(expiration)
            if j ==0:
                y_values_Theta_yes.append(M.american_option_theta(stock_price, strike, expiration, volatility, rfr, div_yield, call_put, time_step, iteration_max))
                y_values_CRR_yes.append(M.american_option_main(stock_price, strike, expiration, volatility, rfr, div_yield, call_put, time_step*100))
            else:
                y_values_Theta_no.append( M.american_option_theta(stock_price, strike, expiration, volatility, rfr, div_yield, call_put,time_step, iteration_max))
                y_values_CRR_no.append(M.american_option_main(stock_price, strike, expiration, volatility, rfr, div_yield, call_put,time_step*100))
            #y_values_exercise.append(M.american_option_exercise(stock_price, strike, expiration, volatility, rfr, div_yield, call_put, time_step))
            print(j,i)
    x_array = np.array(x_values)
    y_array_Theta_call = np.array(y_values_Theta_yes)
    y_array_Theta_put = np.array(y_values_Theta_no)
    y_array_CRR_call = np.array(y_values_CRR_yes)
    y_array_CRR_put = np.array(y_values_CRR_no)
    if 0 in y_array_CRR_call:
        error = []
        for i in range(len(y_array_CRR_call)):
            if y_array_CRR_call[i] != 0:
                error.append(100*(abs(y_array_Theta_call[i] - y_array_CRR_call[i]))/abs(y_array_CRR_call[i]))
            else:
                error.append(0)
        error_call = np.array(error)
    else:
        error_call = 100*(abs(y_array_Theta_call - y_array_CRR_call))/abs(y_array_CRR_call)
    if 0 in y_array_CRR_put:
        error = []
        for i in range(len(y_array_CRR_put)):
            if y_array_CRR_put[i] != 0:
                error.append(100*(abs(y_array_Theta_put[i] - y_array_CRR_put[i]))/abs(y_array_CRR_put[i]))
            else:
                error.append(0)
        error_put = np.array(error)
    else:
        error_put = (100*abs(y_array_Theta_put - y_array_CRR_put))/abs(y_array_CRR_put)
    fig3, ax3 = plt.subplots()
    ax3.plot(x_array, error_call, color="red", linestyle='--', label = "Call Error %")
    ax3.plot(x_array, error_put, color="blue", linestyle='--', label = "Put Error %")
    ax3.set_xlabel('Years')
    ax3.set_ylabel('Relative Error % from CRR')
    #plt.scatter(x_values, y_values_exercise, c='green', label = "Main dots")
    plt.legend()
    plt.show()
    print("Plot 4 complete")
if run_plot_five == "yes": #Plot 5 is the most different from the rest. This plot takes a long time to do with high i because how long the Theta American Option takes with many timesteps (an extra timestep can be another 10,000 calculations).
    iteration_max = 10000
    x_values = []
    y_values_Theta_yes = []
    y_values_Theta_no = []
    y_values_CRR_yes = []
    y_values_CRR_no = []
    # y_values_exercise = []
    time_step = 10
    for j in range(2):
        if j == 1:
            call_put = "no"
            time_step = 10
        else:
            call_put = "yes"
        for i in range(4):
            stock_price = 100
            strike = 110
            expiration = 1
            volatility = .3
            rfr = .03
            div_yield = .005

            if j == 0:
                x_values.append(time_step)
            if j == 0: #the main difference is here, where we calculate the result 10 times and average how long it took for these results to happen.
                set_of_times_theta = []
                set_of_times_CRR = []
                for k in range(10):
                    start_time1 = t.perf_counter() #Starts timer
                    M.american_option_theta(stock_price, strike, expiration, volatility, rfr, div_yield, call_put,time_step, iteration_max)
                    end_time1 = t.perf_counter() #ends timer after Theta option.
                    start_time2 = t.perf_counter()
                    M.american_option_main(stock_price, strike, expiration, volatility, rfr, div_yield, call_put,time_step)
                    end_time2 = t.perf_counter()
                    set_of_times_theta.append(end_time1 - start_time1)
                    set_of_times_CRR.append(end_time2 - start_time2)
                y_values_Theta_yes.append(sum(set_of_times_theta)/10) #Averages and appends for graphing data.
                y_values_CRR_yes.append(sum(set_of_times_CRR)/10)
            else:
                set_of_times_theta = []
                set_of_times_CRR = []
                for k in range(10):
                    start_time1 = t.perf_counter()
                    M.american_option_theta(stock_price, strike, expiration, volatility, rfr, div_yield, call_put,time_step, iteration_max)
                    end_time1 = t.perf_counter()
                    start_time2 = t.perf_counter()
                    M.american_option_main(stock_price, strike, expiration, volatility, rfr, div_yield, call_put,time_step)
                    end_time2 = t.perf_counter()
                    set_of_times_theta.append(end_time1 - start_time1)
                    set_of_times_CRR.append(end_time2 - start_time2)
                y_values_Theta_no.append(sum(set_of_times_theta) / 10)
                y_values_CRR_no.append(sum(set_of_times_CRR) / 10)
            if i % 2 == 0:
                time_step = time_step * 5
            else:
                time_step = time_step * 2
            # y_values_exercise.append(M.american_option_exercise(stock_price, strike, expiration, volatility, rfr, div_yield, call_put, time_step))
            print(j, i)
    x_array = np.array(x_values)
    y_array_Theta_call = np.array(y_values_Theta_yes)
    y_array_Theta_put = np.array(y_values_Theta_no)
    y_array_CRR_call = np.array(y_values_CRR_yes)
    y_array_CRR_put = np.array(y_values_CRR_no)
    if 0 in y_array_CRR_call:
        runtime_error = []
        for i in range(len(y_array_CRR_call)):
            if y_array_CRR_call[i] != 0:
                runtime_error.append(100 * (abs(y_array_Theta_call[i] - y_array_CRR_call[i])) / abs(y_array_CRR_call[i]))
            else:
                runtime_error.append(0)
        runtime_error_call = np.array(runtime_error)
    else:
        runtime_error_call = 100 * (abs(y_array_Theta_call - y_array_CRR_call)) /abs( y_array_CRR_call)
    if 0 in y_array_CRR_put:
        runtime_error = []
        for i in range(len(y_array_CRR_put)):
            if y_array_CRR_put[i] != 0:
                runtime_error.append(100 * (abs(y_array_Theta_put[i] - y_array_CRR_put[i])) / abs(y_array_CRR_put[i]))
            else:
                runtime_error.append(0)
        runtime_error_put = np.array(runtime_error)
    else:
        runtime_error_put = (100 * abs(y_array_Theta_put - y_array_CRR_put)) / abs(y_array_CRR_put)
    fig4, ax4 = plt.subplots()
    ax4.plot(x_array, runtime_error_call, color="red", linestyle='--', label="Call Error %")
    ax4.plot(x_array, runtime_error_put, color="blue", linestyle='--', label="Put Error %")
    ax4.set_xlabel('# of Timesteps')
    ax4.set_ylabel('Relative % Runtime Error from CRR comparison')
    plt.legend()
    # plt.scatter(x_values, y_values_exercise, c='green', label = "Main dots")
    plt.show()
    print("Plot 5 complete")

#plt.scatter(x_values, y_values_exercise, c='green', label = "Main dots")
#Plot 3 Comparing Time of all three (Iteration

print("Done")