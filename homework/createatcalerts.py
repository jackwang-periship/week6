'''
Created on Jul 7, 2017

@author: jwang02
'''
import pprint
from waisum.TestAirport import getDelayedAirports

myResults = getDelayedAirports()
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(myResults)
