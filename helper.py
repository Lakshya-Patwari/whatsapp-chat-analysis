import re
import pandas as pd
from urlextract import URLExtract

from wordcloud import WordCloud
import emoji
extractor=URLExtract()
def fetch_stats(selected_user,df):
    if selected_user =="Overall":
        pass  
    else:
        df=df[df["users"]==selected_user]
    total_messages=df.shape[0]
    words=[]
    for message in df["messages"]:
        words.extend(message.split())
    media_messages=df[df["messages"]=="<Media omitted>\n"].shape[0]
    urls=extractor.find_urls(df["messages"].str.cat(sep=""))
    return total_messages, len(words),media_messages,len(urls)
def create_wordcloud(selected_user,df):
    if selected_user !="Overall":
       df=df[df["users"]==selected_user]
    df=df[df["messages"]!="<Media omitted>\n"]
    urls=extractor.find_urls(df["messages"].str.cat(sep=""))
    for url in urls:
        df=df[~df["messages"].str.contains(url)]
    wc=WordCloud(width=1000,height=1000,min_font_size=10,background_color="white")
    df_wc=wc.generate(df["messages"].str.cat(sep=" "))
    return df_wc
def common_words(selected_user,df):
    if selected_user !="Overall":
       df=df[df["users"]==selected_user]
    df=df[df["messages"]!="<Media omitted>\n"]
    urls=extractor.find_urls(df["messages"].str.cat(sep=""))
    for url in urls:
        df=df[~df["messages"].str.contains(url)]
    words=[]
    for message in df["messages"]:
        words.extend(message.split())
    words=pd.DataFrame({"words":words})
    a=words.value_counts().head(20).reset_index()
    a.columns=["words","count"]
    return a
def emoji_helper(selected_user,df):
    if selected_user !="Overall":
       df=df[df["users"]==selected_user]
    emojis=[]
    for message in df["messages"]:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
    return pd.DataFrame({"emoji":emojis}).value_counts().reset_index()
def year_month_activity_map(selected_user,df):
    if selected_user !="Overall":
       df=df[df["users"]==selected_user]
   
    year_month_list=df.groupby(["year","month_num","month"]).count()["messages"].reset_index()
    year_month_list["year_month"]=year_month_list["year"].astype(str)+"-"+year_month_list["month"]
    
    return year_month_list
def daily_activity_map(selected_user,df):
    if selected_user !="Overall":
       df=df[df["users"]==selected_user]
    df["date"]=df["date_time"].dt.date
    datewise_messages=df.groupby("date").count()["messages"].reset_index()
    return datewise_messages
def hourly_activity_map(selected_user,df):
    if selected_user !="Overall":
       df=df[df["users"]==selected_user]
    df["hour"]=df["date_time"].dt.hour
    df["day_name"]=df["date_time"].dt.day_name()
    
    hourly_messages=df.pivot_table(index="hour",columns="day_name",values="messages",aggfunc="count")
    return hourly_messages