import pandas as pd 
import numpy as np 
from datetime import datetime
import json
import requests
from github import Github

def toUnixTime(date, format):
    t2 = datetime.strptime(date, format)
    t1 = datetime(1970, 1, 1)
    ans = (t2 - t1).total_seconds()*1000
    ans = int(ans)
    return ans

def genRawData():
    sources = {}
    data = {}

    url = lambda metric: f'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_{metric}_global.csv' 
    metrics = ['confirmed', 'recovered', 'deaths'] 
    for metric in metrics: sources[metric] = url(metric)
    time_series = {metric: pd.read_csv(sources[metric]) for metric in metrics}

    for metric in time_series:
        df = time_series[metric]
        gb = df.groupby('Country/Region')
        df = gb.sum()
        df = df.loc[:,'1/22/20':] 
        time_series[metric] = df

    time_series['infected'] = time_series['confirmed']-time_series['recovered']-time_series['deaths']

    for metric in time_series:
        time_series[metric].loc['World'] = time_series[metric].sum()

    for metric in metrics:
        time_series[f'daily_{metric}'] = time_series[metric].diff(axis=1)
        time_series[f'7MA_daily_{metric}'] = time_series[f'daily_{metric}'].rolling(window=7, axis=1).mean()

    sources['iso'] = 'https://raw.githubusercontent.com/lukes/ISO-3166-Countries-with-Regional-Codes/master/all/all.csv'
    iso = pd.read_csv(sources['iso'], index_col='name')
    rename = {
        "Bolivia (Plurinational State of)": "Bolivia",
        "Brunei Darussalam": "Brunei",
        "Côte d'Ivoire": "Cote d'Ivoire",
        "Iran (Islamic Republic of)": "Iran",
        "Korea, Republic of": "Korea, South",
        "Taiwan, Province of China": "Taiwan*",
        "United States of America": "US",
        "Russian Federation":"Russia",
        "Venezuela (Bolivarian Republic of)": "Venezuela",
        "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
        "Moldova, Republic of": "Moldova",
        "Viet Nam": "Vietnam",
        "Tanzania, United Republic of": "Tanzania",
        "Palestine, State of": "West Bank and Gaza",
        "Syrian Arab Republic": "Syria",
        "Lao People's Democratic Republic": "Laos",
        "Myanmar":"Burma",
        "Congo, Democratic Republic of the": "Congo (Kinshasa)",
        "Congo": "Congo (Brazzaville)"
    }
    iso.rename(index=rename, inplace=True)
    iso.loc['Kosovo'] = 'XK'
    iso.loc['Namibia'] = 'NA'
    iso.loc['World'] = 'WD'

    general = pd.DataFrame(index=time_series['confirmed'].index)

    for metric in metrics:
        general[metric] = time_series[metric].iloc[:,-1]
        general[f'daily_{metric}'] = time_series[f'daily_{metric}'].iloc[:,-1]

    general = general.astype(int)
    general.sort_values('confirmed', ascending=False, inplace=True) 
    general = general.applymap(lambda x: '{:,}'.format(x))

    general['country'] = general.index
    general['iso'] = iso['alpha-2']
    general['region'] = iso['region']
    general['last_update'] = str(datetime.utcnow())[:-7]

    no_match = general[general['iso'].isnull()].index
    for metric in time_series:
        time_series[metric].drop(index=no_match, inplace=True)
    general.drop(index=no_match, inplace=True)
    
    return time_series, general

time_series, general = genRawData()

def genCountryData(country):
    class countryData:
        def __init__(self, country):
            self.general = general.loc[country]
            self.time_series = {metric: time_series[metric].loc[country] for metric in time_series}
            self.preProcessing()
        
        def preProcessing(self):
            def getStart(atleast=1):
                s = self.time_series['confirmed']
                s = s['1/29/20':]
                start = s.index[0]
                s = s[s > atleast]
                if len(s): start = s.index[0]
                return start
                
            start = getStart(100)
            self.time_series = {metric: self.time_series[metric][start:] for metric in self.time_series}
            self.general['start'] = toUnixTime(start, format="%m/%d/%y")

        def to_dict(self):
            res = {
                'general': self.general.to_dict(),
                'time_series': {metric: self.time_series[metric].to_list() for metric in self.time_series}
            }
            return res

    data = countryData(country)
    return data.to_dict()

def updateData(user, passoword):
    g = Github(user, passoword)
    repo = g.get_user().get_repo("CoronaTrack")
    
    for country in general.index:
        country_iso = general.loc[country]['iso']
        country_data = genCountryData(country)
        res = json.dumps(country_data)
    
        contents = repo.get_contents(f"data/time_series/{country_iso}.json")
        repo.update_file(contents.path, "automatic update", res, contents.sha)

    res = general.to_json(orient='records')
    contents = repo.get_contents(f"data/general.json")
    repo.update_file(contents.path, "automatic update", res, contents.sha)