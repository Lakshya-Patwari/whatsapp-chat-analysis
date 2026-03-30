import re
import pandas as pd
def preprocess(data):
  
    pattern=r"(\d{1,2}/\d{1,2}/\d{1,2},\s\d{1,2}:\d{1,2}\s[AP]M\s-\s)"
    data =re.split(pattern,data)[1:]
    date=data[0::2]
    message=data[1::2]
    df=pd.DataFrame({"date_time":date,"user_message":message})
    df["date_time"]=pd.to_datetime(df["date_time"],format="%m/%d/%y, %I:%M %p - ")

    users=[]
    messages=[]

    for msg in df["user_message"]:
        entry=re.split(r"([^:]+?):\s",msg)
        if len(entry)>1:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append("group_notification")
            messages.append(entry[0])
    df["users"]=users
    df["messages"]=messages
    df.drop(columns={"user_message"},inplace = True)

    df["year"]=df["date_time"].dt.year
    df["month"]=df["date_time"].dt.month_name()
    df["day"]=df["date_time"].dt.day
    df["hour"]=df["date_time"].dt.hour
    df["minute"]=df["date_time"].dt.minute
    df["month_num"]=df["date_time"].dt.month
    
    return df