from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import pandas as pd
from io import StringIO


# Data Scrapping

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('user-agent=StudentDataProject/1.0 (Educational Capstone Project, contact: camiloochoa@yahoo.com)')
# chrome_options.add_experimental_option('detach', True)

driver = webdriver.Chrome(options=chrome_options)

URL = ('https://www.timeanddate.com/weather/colombia/bogota/historic')

driver.get(URL)

#pauses the information retrieval, both as an etiquette piece and to let the page load the information.
sleep(2)

#dropdown element selection
dropdown = driver.find_element(By.ID, 'month')
selection = Select(dropdown)

#how many options does the dropdown has
months = len(selection.options)

weather_data = []

# harcoded number just for testing, change to months when finished
for month in range(10):
    #load the dropdown on each run
    dropdown = driver.find_element(By.ID, "month")
    selection = Select(dropdown)

    #select month to retrieve
    buffer = selection.options[month]
    date = buffer.text

    print(f'scrapping: {date}')

    selection.select_by_index(month)

    sleep(2)

    #pass html to pandas
    html = StringIO(driver.page_source)
    weather_table = pd.read_html(html, attrs={'class':'zebra'})

    if weather_table:
        df_temps = weather_table[0]
        df_temps['Date'] = date
        weather_data.append(df_temps)


#join all created dataframes
df = pd.concat(weather_data, ignore_index=True)


# Data cleaning

#rename column
df = df.rename(columns={'Unnamed: 0': 'Insight'})

#remove data from last 2 weeks
df = df[df['Date'] != 'Past 2 Weeks']

#remove reported annotations, identified with *
df = df[~df['Insight'].str.contains('\*', na=False)]

#change date to datetime objects
df['Date'] = pd.to_datetime(df['Date'], format='%B %Y')

#sort by date
df = df.sort_values(by='Date').reset_index(drop=True)

#create value and units colums from temperature
temp_split = df['Temperature'].str.split(expand=True)

df['Value'] = temp_split[0].astype(int)
df['Unit'] = temp_split[1]

#drop irrelevant data
bogota_temps = df.drop(['Temperature', 'Humidity', 'Pressure'], axis=1)

print(bogota_temps.head(10))

bogota_temps.to_csv('bogota_temps.csv', index=False)
bogota_temps.to_json('bogota_temps.json', orient='records', indent=4)