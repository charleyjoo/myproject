import wget
import os

import zipfile
import pandas as pd

import matplotlib.pyplot as plt
import seaborn; seaborn.set()

def download_if_needed(URL, filename):
    """
    Download from URL TO FILENAME UNLESS FILENAME ALREADY EXISTS
    """
    if os.path.exists(filename):
        print(filename, "already exists.")
        return
    else:
        print("Downloading...")
        wget.download(URL)

def get_pronto_data():
    """
    Download pronto data, unless already downloaded
    """
    download_if_needed('https://s3.amazonaws.com/pronto-data/open_data_year_one.zip','open_data_year_one.zip')


def get_trip_data():
    """
    Fetch pronto data (if needed) and extract trip data from the zip file
    """
    get_pronto_data()
    zf = zipfile.ZipFile('open_data_year_one.zip')
    file_handle = zf.open('2015_trip_data.csv')
    return pd.read_csv(file_handle)


def get_weather_data():
    """
    Get weather data from the zip file
    """
    get_pronto_data()
    zf = zipfile.ZipFile('open_data_year_one.zip')
    file_handle = zf.open('2015_weather_data.csv')
    return pd.read_csv(file_handle)

def get_trip_and_weather():
    trip = get_trip_data()
    weather = get_weather_data()
    date = pd.DatetimeIndex(trip['starttime'])
    trips_by_date = trip.pivot_table('trip_id',aggfunc='count',index=date.date,columns='usertype')
    weather = weather.set_index('Date')
    weather.index = pd.DatetimeIndex(weather.index)
    weather = weather.iloc[:-1]
    return weather.join(trips_by_date)

def plot_daily_totals():
    data = get_trip_and_weather()
    fig, ax = plt.subplots(2,figsize=(14,6),sharex = True)
    data['Annual Member'].plot(ax = ax[0], title='Annual Member')
    data['Short-Term Pass Holder'].plot(ax = ax[1], title='Short-Term Pass Holder')
    fig.savefig('trips_by_day.png')
