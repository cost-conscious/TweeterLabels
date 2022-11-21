import pandas as pd
from cleaning_tools import *


train = pd.read_csv("train.csv").drop(columns="location")
original = train.copy()

train["keyword"] = train["keyword"].replace(repl_dict, regex=True)
train["text"] = train["text"].replace(repl_dict, regex=True)

train["text"] = train["text"].apply(lambda x: x.lower())
train["keyword"] = train["keyword"].apply(lambda x: str(x).lower())

train["text"] = train["text"].apply(lambda x: x.lower())
train["keyword"] = train["keyword"].apply(lambda x: x.strip())

train['text'] = train['text'].apply(lambda x: remove_http(x))

train["text"] = train["text"].apply(lambda x: remove_stopwords(x))

train['text'] = train['text'].apply(lambda x: text_stemmer(x))

print()