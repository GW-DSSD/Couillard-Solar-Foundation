import pandas as pd


df = pd.read_csv('Dataset/data.csv').drop(['Unnamed: 0'],axis=1)

df['Image URL'] = df['Image URL'].apply(lambda x: x if pd.isna(x) else [x,'https://unsplash.it/g/500/350'])



df.to_csv('Dataset/multi_image_data.csv')
