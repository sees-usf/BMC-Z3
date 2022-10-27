from z3 import *
import bmc

""" # Obtain information about the model to check and what to check for.
example = "?"
while example != "y" and example != "n":
  debugMode = input("Would you like to print your counter examples? (y/n): ")
  if debugMode == "y":
    debug = 1
  else:
    debug = 0
    
  example = input("Is your model in the examples folder or in the main src directory? (y/n): ")
  if example == "y":
    model = "examples." + input("Model name (exclude .py): ")
  elif example == "n":
    model = input("Model name (exclude .py): ")
    
path_length = int(input("Provide a path length: "))
property_prob = float(input("Provide a probability to reach: "))
 """
b = bmc.bmc("fsm_2", 4) # BMC initialization runs the SMT-BMC solver