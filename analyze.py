from classify import analysis
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import plotly.express as px
import json

# with open('tokenizer/tokenizer2_mix.pickle', 'rb') as handle:
#     tokenizer = pickle.load(handle)
# best_model = keras.models.load_model("model/best_model5_mix_suff.hdf5")

df = pd.read_csv("data/vax_tweets_sentiment.csv" ,header=0)

all_vax = ['covaxin', 'sinopharm', 'sinovac', 'moderna', 'pfizer', 'biontech', 'oxford', 'astrazeneca', 'sputnik']

def filtered_input_vax(vax):
    positive = vax[(vax['sentiment'] == 'Positive') | (vax['sentiment'] == 'positive')].sort_values(by='date').reset_index()
    negative = vax[(vax['sentiment'] == 'Negative') | (vax['sentiment'] == 'negative')].sort_values(by='date').reset_index()
    neutral = vax[(vax['sentiment'] == 'Neutral') | (vax['sentiment'] == 'neutral')].sort_values(by='date').reset_index()
    return positive, negative, neutral

# def filtered_input_vax_base_on_tweets_timeline(df, vax):
def filtered_input_vax_base_on_tweets_timeline(vax):
    # drop Nan values.
    df = pd.read_csv("data/vax_tweets_sentiment.csv" ,header=0)
    df = df.dropna()

    # set string vax to list vax that has one value.
    vax = [vax]

    # Create a new dataframe
    filter_data = pd.DataFrame()

    # filter text that contain the vaccine name
    for input_vax in vax:
        filter_data = filter_data.append(df[df['orig_text'].str.lower().str.contains(input_vax)])
    
    # delete the input vaccine in all vaccine.
    other_vax = list(set(all_vax)-set(vax))

     # filter out the other vaccine
    for not_input_vax in other_vax:
        filter_data = filter_data[~filter_data['orig_text'].str.lower().str.contains(not_input_vax)]
    filter_data = filter_data.drop_duplicates()

    # filter to positive negative and neutral. All value sort by date and reset the index.
    positive, negative, neutral = filtered_input_vax(filter_data)

    # filter timeline by using group by date and sentiment then create value tweets with count and reset datetime.
    timeline_pos = positive.groupby(['date', 'sentiment']).agg(**{'tweets': ('id', 'count')}).reset_index()
    timeline_neg = negative.groupby(['date', 'sentiment']).agg(**{'tweets': ('id', 'count')}).reset_index()
    timeline_neu = neutral.groupby(['date', 'sentiment']).agg(**{'tweets': ('id', 'count')}).reset_index()

    # set date arg to datetime.
    # timeline_pos["date"] = pd.to_datetime(timeline_pos["date"])
    # timeline_neg["date"] = pd.to_datetime(timeline_neg["date"])
    # timeline_neu["date"] = pd.to_datetime(timeline_neu["date"])

    pos_data_list = []
    neg_data_list = []
    neu_data_list = []

    pos_data_list.append(timeline_pos['tweets'].values.tolist())
    pos_data_list.append(timeline_pos["date"].values.tolist())

    neg_data_list.append(timeline_neg['tweets'].values.tolist())
    neg_data_list.append(timeline_neg["date"].values.tolist())

    neu_data_list.append(timeline_neu['tweets'].values.tolist())
    neu_data_list.append(timeline_neu["date"].values.tolist())


    # # plot graph
    # plt.plot(timeline_pos['date'], timeline_pos['tweets'], label="Positive")
    # plt.plot(timeline_neg['date'], timeline_neg['tweets'], label="Negative")
    # plt.plot(timeline_neu['date'], timeline_neu['tweets'], label="Neutral")

    # # set label x and y
    # plt.xlabel("time")
    # plt.ylabel("tweets")

    # # show label
    # plt.legend()

    # # auto fomating in date form
    # plt.gcf().autofmt_xdate()

    # # let x label rotation 45 degree
    # plt.xticks(rotation=45)

    # # show graph
    # plt.show()

    new_json = {'positive':pos_data_list,
                'negative':neg_data_list,
                'neutral':neu_data_list
                }
    json_data_sentiment = json.dumps(new_json)
    return  json_data_sentiment

def filtered_all_base_on_tweets_timeline(df):

    df = df.dropna()

    # filter to positive negative and neutral. All value sort by date and reset the index.
    positive, negative, neutral = filtered_input_vax(df)

    # filter timeline by using group by date and sentiment then create value tweets with count and reset datetime.
    timeline_pos = positive.groupby(['date', 'sentiment']).agg(**{'tweets': ('id', 'count')}).reset_index()
    timeline_neg = negative.groupby(['date', 'sentiment']).agg(**{'tweets': ('id', 'count')}).reset_index()
    timeline_neu = neutral.groupby(['date', 'sentiment']).agg(**{'tweets': ('id', 'count')}).reset_index()

    # set date arg to datetime.
    # timeline_pos["date"] = pd.to_datetime(timeline_pos["date"])
    # timeline_neg["date"] = pd.to_datetime(timeline_neg["date"])
    # timeline_neu["date"] = pd.to_datetime(timeline_neu["date"])

    
    pos_data_list = []
    neg_data_list = []
    neu_data_list = []

    pos_data_list.append(timeline_pos['tweets'].values.tolist())
    pos_data_list.append(timeline_pos["date"].values.tolist())

    neg_data_list.append(timeline_neg['tweets'].values.tolist())
    neg_data_list.append(timeline_neg["date"].values.tolist())

    neu_data_list.append(timeline_neu['tweets'].values.tolist())
    neu_data_list.append(timeline_neu["date"].values.tolist())

    # # plot graph
    # plt.plot(timeline_pos['date'], timeline_pos['tweets'], label="Positive")
    # plt.plot(timeline_neg['date'], timeline_neg['tweets'], label="Negative")
    # plt.plot(timeline_neu['date'], timeline_neu['tweets'], label="Neutral")

    # # set label x and y
    # plt.xlabel("time")
    # plt.ylabel("tweets")

    # # show label
    # plt.legend()

    # # auto fomating in date form
    # plt.gcf().autofmt_xdate()

    # # let x label rotation 45 degree
    # plt.xticks(rotation=45)

    # # show graph
    # plt.show()

    new_json = {'positive':pos_data_list,
                'negative':neg_data_list,
                'neutral':neu_data_list
                }
    json_data_sentiment = json.dumps(new_json)
    return  json_data_sentiment

# covaxin = filtered_input_vax_base_on_tweets_timeline('sinovac')
# all_data = filtered_all_base_on_tweets_timeline(df)