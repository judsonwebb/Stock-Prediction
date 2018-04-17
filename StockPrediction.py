"""
Stock market prediction using Markov chains.

"""

import comp140_module3 as stocks
from collections import defaultdict
import random
### Model
    

def markov_chain(data, order):
    """
    This function creates an nth order Markov chain given n and a list of data.
    """
    the_chain=defaultdict(dict)
    count=0
    for each in data:
        count += 1
        if count > order:
            the_tuple = get_tuple(data, order,count)
            the_chain[the_tuple]=defaultdict(int)
            
    count = 0
    for each in data:
        count += 1
        if count > order:
            the_tuple = get_tuple(data, order,count)
            division = get_division(data,list(the_tuple),order)
            the_chain[the_tuple][each]+=1.0/division
    return the_chain
    
        

        
def get_tuple(data, order,count):
    """
    Creates a tuple dictionary key given data, an order, and a count.
    """
    a_list =[]
    for each in range(order):
        a_list.append(data[count-order-1+each])	
    return tuple(a_list)



### Predict
def get_division(data, a_list,order):
    """
    returns an increment divisor for a value returned by a key given data and the key.
    """
    count=0
    divisor =0
    for each in data:
        another_list =[]
        count += 1
        if count > order:
            for each in range(order):
                another_list.append(data[count-order-1+each])	
            if a_list==another_list:
                divisor+=1
    return divisor
            
            
            
            
            
            


def predict(model, last, num):
    """
    Predicts the next num values given model and the last values.
    """
    dictionary = defaultdict(dict,model)
    new_last = list(last)

    returned_list = []
    count =0
    while count<num:
        count+=1
        dictionary[tuple(new_last)]=defaultdict(int,dictionary[tuple(new_last)])
        if (len(model)==0) :
            returned_list.append(random.randint(0,3))
        elif not(dictionary[tuple(new_last)][0]+dictionary[tuple(new_last)][1]+dictionary[tuple(new_last)][2]+dictionary[tuple(new_last)][3]+dictionary[tuple(new_last)][4]+dictionary[tuple(new_last)][5]==1):
            returned_list.append(random.randint(0,3))
        else:
            
            check = random.random()
            if (check < dictionary[tuple(new_last)][1])and(check>0):
                returned_list.append(1)
            elif (check>0)and(check < (dictionary[tuple(new_last)][(1)]+dictionary[tuple(new_last)][2])):
                returned_list.append(2)
            elif (check>0) and (check < (dictionary[tuple(new_last)][1]+dictionary[tuple(new_last)][2]+dictionary[tuple(new_last)][3])):
                returned_list.append(3)
            elif (check>0) and (check < (dictionary[tuple(new_last)][1]+dictionary[tuple(new_last)][2]+dictionary[tuple(new_last)][3]+dictionary[tuple(new_last)][4])):
                returned_list.append(4)
            elif (check>0) and (check < (dictionary[tuple(new_last)][1]+dictionary[tuple(new_last)][2]+dictionary[tuple(new_last)][3]+dictionary[tuple(new_last)][4]+dictionary[tuple(new_last)][5])):
                returned_list.append(5)
            elif (check>0) and (check < 1):
                returned_list.append(0)
        new_last.pop(0)
        new_last.append(returned_list[len(returned_list)-1])
    return returned_list



def mse(result, expected):
    """
    Calculates the mean squared error between the sequences 
    result and expected.
    """
    #Assumes result and expected are the same length.
    comp_sum=0
    for each in range(len(expected)):
        comp_sum+=((expected[each]-result[each])**2)/(1.0*len(expected))
    return comp_sum


### Experiment

def run_experiment(train, order, test, future, actual, trials):
    """
    Runs an experiment that predicts the future of the test
    data given the training data.  Returns the average 
    mean squared error over the number of trials.
    
    train  - training data
    order  - order of the markov model to use
    test   - "order" days of testing data
    future - number of days to predict
    actual - actual results for next "future" days
    trials - number of trials to run
    """
    trial_runs=[]
    for each in range(trials):
        model = markov_chain(train,order)
        #Problem probably here.
        expected = predict(model, test, future)
        trial_runs.append(mse(actual, expected))
    comp_sum= 0
    for each in trial_runs:
        comp_sum+=each/(1.0*len(trial_runs))
        print comp_sum
    return comp_sum
    


### Application
def run():
    """
    You do not need to modify any code in this function.  You should
    feel free to look it over and understand it, though.
    
    # Get the supported stock symbols
    symbols = stocks.get_supported_symbols()
    
    # Get stock data and process it

    # Training data
    changes = {}
    bins = {}
    for symbol in symbols:
        prices = stocks.get_historical_prices(symbol)
        changes[symbol] = stocks.compute_daily_change(prices)
        bins[symbol] = stocks.bin_daily_changes(changes[symbol])

    # Test data
    testchanges = {}
    testbins = {}
    for symbol in symbols:        
        testprices = stocks.get_test_prices(symbol)
        testchanges[symbol] = stocks.compute_daily_change(testprices)
        testbins[symbol] = stocks.bin_daily_changes(testchanges[symbol])

    # Display data
    #   Comment these 2 lines out if you don't want to see the plots
    stocks.plot_daily_change(changes)
    stocks.plot_bin_histogram(bins)

    # Run experiments
    orders = [1, 3, 5, 7, 9]
    ntrials = 500
    days = 5

    for symbol in symbols:
        print symbol
        print "===="
        print "Actual:", testbins[symbol][-days:]
        for order in orders:
            error = run_experiment(bins[symbol], order,
                                   testbins[symbol][-order-days:-days], days, 
                                   testbins[symbol][-days:], ntrials)
            print "Order", order, ":", error
        print            
    """
