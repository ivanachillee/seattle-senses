import urllib
import requests
from bs4 import BeautifulSoup
import time

#Load neighbourhood list from Seattle Senses notebook
nhood_list = ['Alki', 'Arbor Heights', 'Atlantic', 'Ballard', 'Belltown',
       'Bitter Lake', 'Brighton', 'Broadview', 'Broadway', 'Bryant',
       'Capitol Hill', 'Cedar Park', 'Central Business District',
       'Columbia City', 'Crown Hill', 'Dunlap', 'Eastlake',
       'Fairmount Park', 'Fauntleroy', 'First Hill', 'Fremont',
       'Gatewood', 'Genesee', 'Georgetown', 'Green Lake', 'Greenwood',
       'Haller Lake', 'Harrison/Denny-Blaine', 'High Point',
       'Highland Park', 'Holly Park', 'Industrial District', 'Interbay',
       'International District', 'Laurelhurst', 'Leschi',
       'Licton Springs', 'Lower Queen Anne', 'Madison Park', 'Madrona',
       'Magnolia', 'Maple Leaf', 'Mathews Beach', 'Meadowbrook', 'Minor',
       'Montlake', 'Mount Baker', 'North Admiral',
       'North Beach/Blue Ridge', 'North Beacon Hill',
       'North College Park', 'North Delridge', 'Olympic Hills',
       'Phinney Ridge', 'Pike Place Market', 'Pinehurst',
       'Pioneer Square', 'Portage Bay', 'Queen Anne', 'Rainier Beach',
       'Ravenna', 'Riverview', 'Roosevelt', 'Roxhill', 'Seaview',
       'Seward Park', 'South Beacon Hill', 'South Delridge',
       'South Lake Union', 'South Park', 'Stevens', 'The Junction',
       'University District', 'Victory Heights', 'View Ridge',
       'Wallingford', 'Wedgewood', 'Westlake', 'Windermere',
       'Yesler Terrace']

#Requests Configuration
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
headers = {"user-agent" : USER_AGENT}

print("======================================================")
#Parsing the coordinates
for i in range(len(nhood_list)):

    neigh_og = nhood_list[i] #vis purposes

    neighbourhood = nhood_list[i]
    neighbourhood = neighbourhood.replace(' ', '_') #align with wikipedia url structure


    url = f"https://en.wikipedia.org/wiki/{neighbourhood},_Seattle"
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text,
                         "html.parser")

    a = soup.find_all("span", {"class": "geo-dec"})

    try:
        coords = a[0].text
    except:
        coords = "Unavailable"

    if coords=="Unavailable":
        c1 = "Unavailable"
        c2 = "Unavailable"
    else:
        coords = coords.split(" ")

        #reordered for geojson point() formatting
        c1 = coords[1]
        c2 = coords[0]
        def corrector(cf):
            try:
                cf = cf.replace("°","")
                cf = cf.replace("W","")
                cf = float(cf)*-1
            except:
                cf = cf.replace("°","")
                cf = cf.replace("N","")
                cf = float(cf)

            return cf

        c1 = corrector(c1)
        c2 = corrector(c2)
    #geojson formatting
    output = '''
    {
      "properties": {
        "Neighbourhood": "'''+neigh_og+'''"
      },
      "id": "'''+str(i)+'''",
      "geometry": {
        "type": "Point",
        "coordinates": [
          '''+str(c1)+''', '''+str(c2)+'''
        ]
      },

      "type": "Feature"
    },
    '''
    print(output)

print("======================================================")
