import json
import numpy as np
import requests
import wrapper
import calculator

#insert a list in one straight line
n = input("Please insert a list here >>> ")
input_ = json.loads(n)
five_price = wrapper.call_api(input_) #get a list of five price array from wrapper.py
checked_error = calculator.detect_error(five_price) #check if error is more than 3
remove_outlier = calculator.filter_data(checked_error)  #filter outlier data
get_median = calculator.cal_median(remove_outlier)  #calculate median
print(get_median)
