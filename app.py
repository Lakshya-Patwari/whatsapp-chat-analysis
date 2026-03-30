import re
import preprocessor,helper
import pandas as pd
import streamlit as st
import plotly.express as px
from wordcloud import WordCloud
import emoji

st.sidebar.title("WhatsApp Chat Analysis")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    data = uploaded_file.getvalue().decode("utf-8")
    df=preprocessor.preprocess(data)
    st.dataframe(df)
    user_list=(df["users"].unique().tolist())
    user_list.sort()
    user_list.insert(0,"Overall")
    
    selected_user=st.sidebar.selectbox("Show analysis wrt",user_list)
    if st.sidebar.button("Show Analysis"):
        num_messages, total_words, media_messages,links=helper.fetch_stats(selected_user,df)
        col1,col2,col3,col4=st.columns(4)
        with col1:
            st.header("Total messages")
            st.title(num_messages)
        with col2:
            st.header("Total words")
            st.title(total_words)
        with col3:
            st.header("Media shared")
            st.title(media_messages)
        with col4:
            st.header("Links shared")
            st.title(links)
        col1,col2=st.columns(2)
        
        user_counts = df["users"].value_counts().reset_index()
        user_counts.columns = ["users", "messages"]
        
        with col1:
            fig = px.bar(user_counts.head(15), x="users", y="messages", labels={"x": "Users", "y": "Message Count"},title="Top 15 active users")
            fig.update_layout(xaxis_tickangle=90)
            fig.update_xaxes(tickmode="linear")
            st.plotly_chart(fig)    
        with col2:
            fig=px.pie(user_counts.head(15),values="messages",names="users" ,title="Message distribution")
            st.plotly_chart(fig)
        st.title("Wordcloud")
        df_wc=helper.create_wordcloud(selected_user,df)
        fig_wc=px.imshow(df_wc)
        fig_wc.update_layout(xaxis={"visible": False}, yaxis={"visible": False})
        st.plotly_chart(fig_wc)
        
        common_df=helper.common_words(selected_user,df)
        fig_common=px.bar(common_df,x="count",y="words",labels={"x":"Count","y":"Words"},title="Most common words")
        
        st.plotly_chart(fig_common) 
        emoji_df=helper.emoji_helper(selected_user,df)
        col1,col2=st.columns(2)
        with col1:
            st.header("Most used emojis")
            st.dataframe(emoji_df)
        with col2:
            fig_emoji=px.pie(emoji_df.head(20),values="count",names="emoji")
            st.plotly_chart(fig_emoji)
    monthly_activity=helper.year_month_activity_map(selected_user,df)
    
    fig_monthly=px.line(monthly_activity,x="year_month",y="messages",labels={"year_month":"Month","messages":"Message Count"},title="Monthly activity")
    st.plotly_chart(fig_monthly)
    
    df["date"]=df["date_time"].dt.date
    datewise_messages=df.groupby("date").count()["messages"].reset_index()
    fig_daily=px.line(datewise_messages,x="date",y="messages",labels={"date":"Date","messages":"Message Count"},title="Daily activity")
    st.plotly_chart(fig_daily)
    col1,col2=st.columns(2)
    with col1:
        df["day_name"]=df["date_time"].dt.day_name()
        day_activity=df.groupby("day_name").count()["messages"].reset_index()
        fig_day=px.bar(day_activity,x="day_name",y="messages",labels={"day_name":"Day","messages":"Message Count"},title="Activity by day")
        st.plotly_chart(fig_day)
    with col2:
        month_activity=df.groupby(["month_num","month"]).count()["messages"].reset_index()
        fig_month=px.bar(month_activity,x="month",y="messages",labels={"month":"Month","messages":"Message Count"},title="Activity by month")
        st.plotly_chart(fig_month)
    hourly_activity=helper.hourly_activity_map(selected_user,df)
    fig_hourly=px.imshow(hourly_activity,title="Activity by hour",labels={"hour":"Hour of the day","messages":"Message Count"},height=800)
    fig_hourly.update_yaxes(
    tickmode="linear"   # 👈 forces every label to show
    )
    st.plotly_chart(fig_hourly)