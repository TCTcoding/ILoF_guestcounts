from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd

date = '20201229'
url = 'https://inlieuof.fun/episodes.html'

page = urlopen(url).read()
soup = BeautifulSoup(page)  #makes the html soup
table = soup.find("tbody")  #pulls the table
data=[]  #empty list to store table data in
rows = table.find_all('tr')  #all the table rows is a list
for row in rows:
    cols = row.find_all('td')  #td = table data = each cell in table
    cols = [ele.text.strip().replace('\xa0',' ') for ele in cols]  #cleans the talbe data '\xa0' is an html element/sapce?
    data.append(cols)  #data finishes as a lists of the table rows (where each row is a list of the columns)
    
episodeID, dates, guests = [], [], []
for i in data:
    episodeID.append(i[0].split(' ')[0])  #custome way to pull the data given the table/text formating
    dates.append(i[0].split('\n')[1])  # above
    guests.append(i[1].split('\n')[0].replace('Guests: ',''))  # above
data = pd.DataFrame({'episodeID':episodeID, 'date':dates, 'guests':guests}) 
data['date'] = pd.to_datetime(data['date'])
# data['episodeID'] = pd.to_numeric(data['episodeID'])
data['guest_n'] = data.guests.str.count(',') + 1  #count of guests in episode
data['guests'] = data.guests.str.split(', ')  #turns the guests column into a list of guests
data = data.guests.apply(pd.Series)\
    .merge(data, left_index=True,right_index=True)\
    .melt(id_vars=['episodeID', 'date', 'guest_n', 'guests'], value_name='guest')\
    .drop('variable',axis=1)\
    .dropna(axis=0,subset=['guest'])  
    ## guests turns into columns for each element in the longest list in this column through "apply(pd.Series)"
    ## these new columns are then merged with the previous data (note there is "empty" guests spots because of the different number of guests across the shows)
    ## melt to preserve the "ids" ('episodeID', 'date', guest_n) for each of the guest entries
    ## drop the variables column (because these are the meaningless column numbers maded during the pd.Series step)
    ## lastly, the pd.Series step added "empty" values because not all shows had the same number of guests, so drop all rows where the guest is 'NaN'
data.sort_values(by='date',ascending=False, inplace=True)
data.to_csv('guest_list_{}.csv'.format(date), index=False)
data['guest'].value_counts().to_csv('guest_counts_{}.csv'.format(date))
