import streamlit as st
import pandas as pd
import preprocessing, helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Whatsapp Chat Analyser")
file = st.sidebar.file_uploader("Upload your file here")


if file is not None:
    bytes_data = file.getvalue()
    data = bytes_data.decode('utf-8')
    df = preprocessing.preprocess(data)


    # fetch list of users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,'Overall')
    selected_user = st.sidebar.selectbox('Show overall analysis', user_list)

    if st.sidebar.button("Show analysis"):
        st.title("Top Statistics")
        num_messages, words, media, link = helper.fetch_stats(selected_user, df)
        col1, col2, col3, col4 = st.columns(4)

        # Total number of messges
        with col1:
            st.header("Total Message")
            st.title(num_messages)
        
        # Total number of words
        with col2:
            st.header("Total Words")
            st.title(words)

        # Total media
        with col3:
            st.header("Media Shared")
            st.title(media)

        # Total links
        with col4:
            st.header("Link Shared")
            st.title(link)
        
        # find the bussiest user from the chat
        if selected_user == 'Overall':
            x,y = helper.most_bussy_user(df)
            col1, col2 = st.columns(2)
            with col1:
                st.title("Most Bussy Users")
                name = x.index
                count = x.values
                plt.figure(figsize=(8,5))
                plt.bar(name, count, color='red')
                plt.xticks(rotation = 'vertical')
                st.pyplot(plt)

            with col2:
                st.title("User %")
                st.dataframe(y)

            # Word Cloud
            
        st.title("Word Cloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        plt.figure(figsize=(8,4))
        plt.axis('off')
        plt.imshow(df_wc)
        st.pyplot(plt)

        

        most_commom_df = helper.remove_stopwords(selected_user, df)
    
        st.title('Most Commom Words')
        fig, ax = plt.subplots()
        ax.barh(most_commom_df[0], most_commom_df[1], color='purple')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)


        # Most common emoji
        most_common_emoji = helper.handling_emoji(selected_user, df)
        st.title("Emoji Analysis")
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(most_common_emoji)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(most_common_emoji['Count'].head(), labels=most_common_emoji['Emoji'].head(), autopct="%0.2f")
            
            st.pyplot(fig)
        
        # Timeline Monthly
        timeline = helper.monthly_timeline(selected_user, df)
        st.title("Monthly Timeline")
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'])
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)

        # Timeline Day
        day_timeline = helper.activity_map_day(selected_user, df)
        col1, col2 = st.columns(2)
        st.title("Activity Map")
        with col1:
            st.title('Most bussy day')
            fig, ax = plt.subplots()
            ax.bar(day_timeline['day_name'], day_timeline['message'], color='green')
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig)
        month_map = helper.activity_map_month(selected_user, df)
        with col2:
            st.title('Most bussy month')
            fig, ax = plt.subplots()
            ax.bar(month_map.index, month_map.values, color='red')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        st.title("Weakly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        # Timeline Daily
        date_timeline = helper.date_timeline(selected_user, df)
        st.title('Daily Timeline')
        plt.figure(figsize=(18,10))
        fig, ax = plt.subplots()
        ax.plot(date_timeline['only_date'], date_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        