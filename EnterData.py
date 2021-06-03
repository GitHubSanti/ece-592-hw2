# -*- coding: utf-8 -*-
"""taken from calBMI.py homework1 solutions

this file takes weight and the height from the user and calculates the body mass index.
BMI is calculated from (Weight(kg))/(Height(m))^2
the weight in the input is in pounds (lbs) and the height is in feet 
# """
from Homework2 import dataRecorder

try:
    n = str(input("Name? \n>"))
    w = float(input("Weight? \n>"))
    h = float(input("Height?\n>"))
    record = {"Name" : n, "Weight" : w, "Height" : h}

    dataRecorder("datarecorded.csv",record)

except ValueError:
    print("invalid entry")
except ZeroDivisionError:
    print ("Height can not be zero")
