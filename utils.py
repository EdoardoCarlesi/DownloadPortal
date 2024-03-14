import random
import string
import pandas as pd
import re
import pickle as pkl
import shutil
import os

def generate_random_string(length):
    """
    Generate a random string of specified length.
    
    Parameters:
        length (int): The length of the random string to generate.
        
    Returns:
        str: The randomly generated string.
    """
    # Define the characters to choose from
    characters = string.ascii_letters + string.digits
    
    # Generate the random string by selecting random characters from the pool
    random_string = ''.join(random.choice(characters) for _ in range(length))
    
    return random_string


def generate_download_link():

    original_link = 'data/test_audio.wav'
    subdir = generate_random_string(8)
    file_name = 'NanowarOfSteel_XX_Years_Of_Steel_FULL_SHOW.wav'
    
    os.mkdir(f'tmp/{subdir}')
    new_link = f'tmp/{subdir}/{file_name}'
    shutil.copy(original_link, new_link)

    return new_link


def random_code_generator():
    
    remove_words = ['is', 'are', 'of', 'the', 'pt']

    songs_csv = 'data/nos_lyrics.csv'
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
    """ """
    
    #codes = generate_codes(500)
    #codes = list(set(codes))
    #print(len(codes))
    #print(codes)
    #pkl.dump(codes, open('data/videocodes.pkl', 'wb'))
    codes = pkl.load(open('data/videocodes.pkl', 'rb'))
    #print(codes)

    codes_df = pd.DataFrame()
    code_used = [0 for i in range(len(codes))]
    used_date = ['00-00-0000' for i in range(len(codes))]
    codes_df['Code'] = codes
    codes_df['Used'] = code_used
    codes_df['Used_date'] = used_date

    print(codes_df.head())
    

    codes_df.to_pickle('data/video_code_df.pkl')



