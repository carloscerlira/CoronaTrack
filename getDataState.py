import pandas as pd 
import numpy as np
from datetime import datetime
import json
import requests
from github import Github
from dotenv import load_dotenv
load_dotenv()
import os
branch = os.getenv('branch')

def toUnixTime(date, format):
    t2 = datetime.strptime(date, format)
    t1 = datetime(1970, 1, 1)
    ans = (t2 - t1).total_seconds()*1000
    ans = int(ans)
    return ans

def genRawData():
    sources = {}
    url = lambda metric: f"https://raw.githubusercontent.com/mexicovid19/Mexico-datos/master/datos_abiertos/series_de_tiempo/acumulados/covid19_mex_{metric}.csv"
    metrics = ["confirmed", "deaths"]
    to_spanish = {"confirmed": "confirmados", "deaths": "muertes"}
    for metric in metrics: sources[metric] = url(to_spanish[metric])
    time_series = {metric: pd.read_csv(sources[metric]) for metric in metrics}
    
    def transform_date(date):
        parts = date.split("-")
        year = parts[0][-2:]
        month = str(int(parts[1]))
        day = str(int(parts[2]))
        return f"{month}/{day}/{year}"
    
    for metric in time_series:
        df = time_series[metric]
        df.rename(columns={"Fecha": "date"}, inplace=True)
        df["date"] = time_series[metric]["date"].apply(transform_date)   
        df.set_index("date", inplace=True) 
        df = df.loc["10/1/20":,:]    
        time_series[metric] = df.transpose()
    
    for metric in metrics:
        time_series[f"daily_{metric}"] = time_series[metric].diff(axis=1)
        time_series[f"7MA_daily_{metric}"] = time_series[f"daily_{metric}"].rolling(window=7, axis=1).mean()
    
    sources["iso"] = f"https://raw.githubusercontent.com/carloscerlira/Datasets/master/ISO/Mexico.csv"
    iso_df = pd.read_csv(sources["iso"], index_col="state_name")

    general_df = pd.DataFrame(index=time_series["confirmed"].index)
    for metric in metrics:
        general_df[metric] = time_series[metric].iloc[:,-1]
        general_df[f"daily_{metric}"] = time_series[f"daily_{metric}"].iloc[:,-2]
    
    general_df = general_df.astype(int)
    general_df.sort_values("confirmed", ascending=False, inplace=True) 
    general_df = general_df.applymap(lambda x: "{:,}".format(x))
    
    general_df["country"] = general_df.index
    general_df["iso"] = iso_df["iso"]
    general_df["last_update"] = str(datetime.utcnow())[:-7]
    general_df.dropna(inplace=True)
    return time_series, general_df

time_series, general_df = genRawData()

class countryData:
    def __init__(self, country):
        self.general = general_df.loc[country]
        self.time_series = {metric: time_series[metric].loc[country] for metric in time_series}
        self.preProcessing()
    
    def preProcessing(self):
        def getStart(metric, atleast=1):
            s = self.time_series[metric]
            s.dropna(inplace=True)
            tmp_s = s[s > atleast]
            if len(tmp_s): start = tmp_s.index[0]
            else: start = s.index[0]
            if metric == "7MA_daily_confirmed" and toUnixTime(start, format="%m/%d/%y") < toUnixTime("3/1/20", format="%m/%d/%y"): start = "8/1/20" 
            return start
        
        start = "1/10/21"
        self.time_series = {metric: self.time_series[metric][start:] for metric in self.time_series}
        self.time_series["starts"] = {"confirmed":toUnixTime(start, format="%m/%d/%y")} 

    def to_dict(self):
        res = {
            "general": self.general.to_dict(),
            "time_series": {metric: self.time_series[metric].to_list() for metric in self.time_series if metric != "starts"}
        }
        res["time_series"]["starts"] = self.time_series["starts"]
        return res

def genCountryData(country):
    data = countryData(country)
    return data.to_dict()

# def updateData(access_token):
#     g = Github(access_token)
#     repo = g.get_user().get_repo("CoronaTrack")
    
#     res = general_df.to_json(orient="records")
#     contents = repo.get_contents(f"data/{branch}/general.json")
#     repo.update_file(contents.path, "automatic update", res, contents.sha)
    
#     for country in general_df.index:
#         country_iso = general_df.loc[country]["iso"]
#         country_data = genCountryData(country)
#         res = json.dumps(country_data)
    
#         contents = repo.get_contents(f"data/time_series/{country_iso}.json")
#         repo.update_file(contents.path, "automatic update", res, contents.sha)


def manualUpdate():
    general_df.to_json("data/mexico/general.json", orient="records")
    for country in general_df.index:
        country_iso = general_df.loc[country]["iso"]
        res = genCountryData(country)
        with open("data/mexico/time_series/"+country_iso+".json", "w") as doc:
            json.dump(res, doc)

manualUpdate()