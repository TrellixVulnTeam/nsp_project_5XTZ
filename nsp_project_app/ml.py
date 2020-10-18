import pandas as pd
import pandas as pd
import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
import math
import time
import re
import os
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
stopwords = set(stopwords.words('english'))
from sklearn.metrics import pairwise_distances
from collections import Counter

global postId
def add(image,data,user):

    postId = []
    #print(ob,'--------------------------------------')
    df=pd.DataFrame(data)
    df_user=pd.DataFrame(user)


    print('--------------aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
    #df2=pd.DataFrame(image)

    print(df_user,'-----------------------------first')
    print(df)
    #df_user=df_user.to_csv(r'C:\Users\Ankesh\Desktop\user.csv', index=False)
    #df=df.to_csv(r'C:\Users\Ankesh\Desktop\data.csv', index=False)
    #df_user1=df_user.to_csv('user.csv', index=False)
    #df1=df.to_csv('data.csv', index=False)
    #df=df1.copy()
    #df_user=df_user1.copy()
    df['text'] = df['post_title'] + df['Text'] + df['TechnicalField'] + df['NonTechnicalField']

    def tokenization_and_stemming(text):

        text = re.sub(r"[^a-zA-Z]", " ", text)
        tokens = word_tokenize(text)
        stemmer = SnowballStemmer("english")
        clean_tokens = []
        for word in tokens:
            clean_tok = stemmer.stem(word).lower().strip()
            if clean_tok not in stopwords:
                clean_tokens.append(clean_tok)

        return clean_tokens

    from sklearn.feature_extraction.text import TfidfVectorizer
    tf = TfidfVectorizer(analyzer='word',ngram_range=(1, 3),min_df=0, stop_words='english',tokenizer=tokenization_and_stemming)
    tfidf_matrix = tf.fit_transform(df['text'])

    log_id = df_user['username'].to_list()
    username = df['username'].to_list()
    match_index = [key for key, val in enumerate(username) if val in set(log_id)]
    id_user = match_index[0]


    def text_to_vector(text):
        word = re.compile(r'\w+')
        words = word.findall(text)

        return Counter(words)

    def get_result(id_user, content_a, content_b, model):

        text1 = content_a
        text2 = content_b
        vector1 = text_to_vector(str(text1))
        vector2 = text_to_vector(str(text2))



    lis = []
    postId_u = []
    def tfidf_model(id_user,num_results):

        pairwise_dist = pairwise_distances(tfidf_matrix,tfidf_matrix[id_user])
        indices = np.argsort(pairwise_dist.flatten())[0:num_results]
        pdists  = np.sort(pairwise_dist.flatten())[0:num_results]
        user_id = df['username'][id_user]
        df_indices = list(df.index[indices])

        for i in range(0,len(indices)):
            # we will pass 1. doc_id, 2. title1, 3. title2, url, model
            get_result(indices[i], df['text'].loc[df_indices[0]], df['text'].loc[df_indices[i]], 'tfidf')

            #print('Text:',df['text'].loc[df_indices[i]])
            us = df["username"].loc[df_indices[i]]
           # us2 = df["username"].loc[df_indices[i]]
            pos= df["post_title"].loc[df_indices[i]]
            tec = df["TechnicalField"].loc[df_indices[i]]
            Ntec = df["NonTechnicalField"].loc[df_indices[i]]
            tex = df["Text"].loc[df_indices[i]]
            creat=df['CreatedDate'].loc[df_indices[i]]
            updat=df['UpdateDate'].loc[df_indices[i]]
            like=df['LikeCount'].loc[df_indices[i]]
            unlik=df['UnLikeCount'].loc[df_indices[i]]
            inst=df['Institute_user_post'].loc[df_indices[i]]
            city=df['city_Name'].loc[df_indices[i]]
            cruser=df['CreatedDate_user'].loc[df_indices[i]]
            up=df['UpdateDate_user'].loc[df_indices[i]]
            tex2=df['text'].loc[df_indices[i]]
            posId = df['Id'].loc[df_indices[i]]
           # Id.append((df['Id']))
            lis.append(( posId,us,pos,tec,Ntec,tex))
        rec = pd.DataFrame(lis,columns = ['Id','username', 'post_title','TechnicalField','NonTechnicalField','Text'])
        rec = rec.drop([0])
        rec =rec[rec.username != user_id]
        postId_u = rec['Id'].values
        return postId_u
    x = tfidf_model(id_user ,20)
    postId.append((x))
    return postId
    #    postId.append(posted_u[:])


        #postId= rec['Id'].to_list()
        #return postId
#    postId_u = tfidf_model(id_user,10)
    #return tfidf_model(id_user,10)
        #postId_u=tfidf_model(id_user, 10)



#print("ohhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh____1_____Yeeeaaaaaaahhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")
#print(add())
