import pandas as pd
from cleaning_tools import *
from nltk.stem import WordNetLemmatizer
import re

train = pd.read_csv("Data/train.csv").drop(columns="location")

original = train.copy()

train["keyword"] = train["keyword"].replace(repl_dict, regex=True)
train["text"] = train["text"].replace(repl_dict, regex=True)

# lowercase
train["text"] = train["text"].apply(lambda x: x.lower())
train["keyword"] = train["keyword"].apply(lambda x: str(x).lower())

# remove white spaces
train["keyword"] = train["keyword"].apply(lambda x: x.strip())

train['text'] = train['text'].apply(lambda x: remove_http(x))

# replace slang
slang_dict = pd.read_csv("Data/twitterSlang.csv")
slang_dict = dict(zip(slang_dict["abbr"], slang_dict["full_word"]))
train["text"] = train["text"].replace(slang_dict)

train["text"] = train["text"].apply(lambda x: remove_stopwords(x))

train['text'] = train['text'].apply(lambda x: text_stemmer(x))

# remove mentions
train["text"] = train["text"].apply(lambda x: re.sub("@[A-Za-z0-9]+","", x))



print()
