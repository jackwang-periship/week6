'''
Created on Mar 13, 2017

@author: jackwang
'''
import requests
import pprint
from bs4 import BeautifulSoup
#specify the url
from __init__ import ATC_ALERT_URL


def getDelayedAirports():
    
    # query the website and return the html to the variable 'page'
    page = requests.get(ATC_ALERT_URL)
    
    # parse the html using beautiful soap and store in variable `soup`
    soup = BeautifulSoup(page.content, 'html.parser')  
    #print soup.body
     
    # Take out the <div> of name and get its value
    ElmDL = soup.find('dl', attrs={'class':'map', 'id':'usmap'})
    #name = name_box.text.strip() # strip() is used to remove starting and trailing  
    # print ElmDL
    # print "--------------"
    ElmDT = ElmDL.find_all_next('dt')
    # print len(ElmDT);
    ElmDD = ElmDL.find_all('dd')
    # print len(ElmDD)
    
    results = dict()
    for JJ in range(len(ElmDT)):
        lineDT = ElmDT[JJ]
        lineDD = ElmDD[JJ]
        textDD = lineDD.getText()
        lineDTa = lineDT.find('a')
        airport = lineDTa['id']
        # print airport,  textDD
        #offset = lineDT.find("goAirportMap")
        # airport =ElemDT 
        if ('Departure delays are 15 minutes or less' in textDD ):
            pass
        else:
            oneAirpor = dict()
            for br in lineDD.findAll('br'):
                airport_city_state = br.nextSibling
                airport_name = br.previous_element
                oneAirpor['name'] = airport_name.strip()
                oneAirpor['citystate'] =airport_city_state.strip()
    
            notes = list()
            for section in lineDD.findAll('hr'):
                nextNode = section
                note = ""
                while True:
                    nextNode = nextNode.nextSibling
                    if nextNode is None or nextNode.string is None :
                        notes.append(note)
                        break
                    if nextNode.string.find('Click for more info') == -1:
                        note = note + nextNode.string
            oneAirpor['status'] = note
            results[airport.upper()] = oneAirpor       
    
    return(results)

if __name__ == "__main__":
    myResults = getDelayedAirports()
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(myResults)
    
    