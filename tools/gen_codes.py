import random
import string
import pandas as pd
import re
import pickle as pkl
import shutil
import os
import ftplib
import ftputil

   
def random_code_generator():
    
    remove_words = ['is', 'are', 'of', 'the', 'pt']

    songs_csv = '../data/nos_lyrics.csv'
    songs_df = pd.read_csv(songs_csv)
    titles = songs_df['Title']

    title_words = []

    for title in titles:
        for word in title.split(' '):
            word = word.lower()
            word = re.sub(r'[^a-z]', '', word)

            if word not in remove_words and len(word) > 3:
                title_words.append(word)

    title_words = list(set(title_words))
    
    code = ''
    indexes = random.sample(range(0, len(title_words)), 3)
    
    for ind in indexes:
         w = title_words[ind]
         code = f'{code}{w}-'

    num = random.randint(0, 10000)
    code = code + str(num)

    return code


def generate_codes(num):

    codes = []
    for i in range(0, num):
        code = random_code_generator()
        codes.append(code)

    return codes


if __name__ == '__main__':
    """ Generate a series of codes to be redeemed """
    
    codes = generate_codes(1000)
    pkl.dump(codes, open('../data/videocodes_sell.pkl', 'wb'))
    
