import streamlit as st
import pandas as pd
from urlextract import URLExtract
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import emoji

def fetch_stats(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    num_messages = df['message'].shape[0]
    words = []
    for message in df['message']:
        words.extend(message.split())

    # Media
    media = df[df['message'] == '<Media omitted>\n'].shape[0]

    # Links
    extractor = URLExtract()
    link = []
    for message in df['message']:
        link.extend(extractor.find_urls(message))

    return num_messages, len(words), media, len(link)

def most_bussy_user(df):
    x =  df['user'].value_counts().head(6)
    y = round(df['user'].value_counts().head(6)/df.shape[0]*100,2).reset_index().rename(columns={'user':'Name', 'count':'Percentage'})
    return x, y

# Word Cloud
def create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = df[df['message'] != '<Media omitted>\n']

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()
    def remove_stop_words(message):
        y=[]
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=400, height=300, background_color='white', min_font_size=10)
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

def remove_stopwords(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = df[df['message'] != '<Media omitted>\n']

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    
    most_common_df =  pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def handling_emoji(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if emoji.is_emoji(c)])
    most_common_emoji = pd.DataFrame(Counter(emojis).most_common(), columns=['Emoji', 'Count'])
    return most_common_emoji.head(10)

def monthly_timeline(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['month','month_num', 'year']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + '-' + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline

def date_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    day_timeline = df.groupby(df['only_date']).count().reset_index()
    return day_timeline

def activity_map_day(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    day7_timeline = df.groupby(['day_name']).count()['message'].reset_index()
    return day7_timeline

def activity_map_month(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    month_map = df['month'].value_counts()
    return month_map

def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    user_heatmap = df.pivot_table(index = 'day_name', columns='period', values='message', aggfunc = 'count').fillna(0)
    return user_heatmap
    
    