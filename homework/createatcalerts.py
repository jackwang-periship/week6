'''
Created on Jul 7, 2017

@author: jwang02
'''
import pprint
import sys
from pymongo import MongoClient
from waisum.TestAirport import getDelayedAirports


def main():
    myResults = getDelayedAirports()
    
    if len(myResults) is not 0:
        try:
            client = MongoClient(host="localhost", port=27017)
            db = client["atcalerts"]
            
#           STRING_DATA[i] = dict([(str(k), str(v)) for k, v in STRING_DATA[i].items()])
            for k, v in myResults.items():
                db.airports.insert(v)
            print "Successfully inserted document:"
            pp = pprint.PrettyPrinter(indent=4)
            pp.pprint(myResults)
        except Exception as e:
            sys.stderr.write("MongoDB Exception: %s" % e)
            sys.exit(1)
    
    else:
        print "No results!"


if __name__ == "__main__":
    main()
    
