'''
Created on Mar 13, 2017

@author: jackwang
'''
import requests
import pprint
from bs4 import BeautifulSoup
from HTMLParser import HTMLParseError
from __init__ import ATC_ALERT_URL
import logging

logging.basicConfig(level=logging.DEBUG)

log = logging.getLogger()
fileHandler = logging.FileHandler("waisum.log")
fileHandler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(fileHandler)

handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)


def getDelayedAirports():
    
    try:
        page = requests.get(ATC_ALERT_URL)
    except requests.exceptions.RequestException as e:
        log.error("Failed to get page. MEG: %s" % e.message)
        return dict()
    
    # parse the html using beautiful soap and store in variable `soup`
    soup = BeautifulSoup(page.content, 'html.parser')  
    #print soup.body
    
    try:
        # Take out the <div> of name and get its value
        ElmDL = soup.find('dl', attrs={'class':'map', 'id':'usmap'})
        #name = name_box.text.strip() # strip() is used to remove starting and trailing  
        # print ElmDL
        # print "--------------"
        ElmDT = ElmDL.find_all_next('dt')
        # print len(ElmDT);
        ElmDD = ElmDL.find_all('dd')
        # print len(ElmDD)
    except HTMLParseError:
        log.error("HTML Parsing failure. MEG: %s" % e.message)
        return dict()
    
    results = dict()
    for JJ in range(len(ElmDT)):
        lineDT = ElmDT[JJ]
        lineDD = ElmDD[JJ]
        textDD = lineDD.getText()
        lineDTa = lineDT.find('a')
        airport = lineDTa['id']
        if 'Departure delays are 15 minutes or less' in textDD:
            pass
        else:
            oneAirpor = dict()
            br = lineDD.find('br')
            if br is not None:
                airport_city_state = br.text
                airport_name = br.previous_element
                oneAirpor['name'] = airport_name.strip()
                oneAirpor['citystate'] = airport_city_state.strip()
                oneAirpor['airportcode'] = airport.upper()
                note = ""
                section = lineDD.find('hr')
                if section is not None:
                    note = section.text
                    note = note[0: -22]
                oneAirpor['status'] = note.strip()
                results[airport] = oneAirpor       
            else:
                log.error("HTML Parsing failure. MEG: No airport, city and state information")
    return(results)

if __name__ == "__main__":
    myResults = getDelayedAirports()
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(myResults)
    
    