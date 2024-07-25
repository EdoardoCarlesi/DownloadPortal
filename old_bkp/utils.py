import random
import string
import pandas as pd
import re
import pickle as pkl
import shutil
import os
import ftplib
import ftputil


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


def get_files_directories(session):

    dirlisting = []
    
    session.retrlines('LIST',callback=dirlisting.append)
    
    files = []
    directories = []
    
    for l in dirlisting:
        lastspace = l.rindex(' ')
        file_name = l[lastspace+1:]
        if l[0] == 'd':
            directories.append(file_name)
        elif l[0] == '-':
            files.append(file_name)
            
    return files,directories
    

def copy_file_ftp(base_path, tmp_path, old_link, new_link):

    usr = os.getenv('ARUBA_USR')
    pwd = os.getenv('ARUBA_PWD')
    #session = ftplib.FTP('ftp.nanowar.it', usr, pwd)
    session = ftputil.FTPHost('ftp.nanowar.it', usr, pwd)
    print(session.listdir(session.curdir))
    session.chdir(base_path)
    session.mkdir(tmp_path)

    with session.open(old_link, "rb") as source:
        with session.open(new_link, "wb") as target:
            session.copyfileobj(source, target)
    #files, dirs = get_files_directories(session)
    #print(files, dirs)
        
    #with session.transfercmd(f'RETR {old_link}') as source_file:
    #    print(old_link, new_link)
    #source_file = open('short.wav', 'rb')
    #session.storbinary(f'STOR {new_link}', source_file)

    #session.retrbinary(f'RETR {f}')

    #print(f'FILE {old_link} copied to {new_link}')

def generate_download_link():

    form = '.wav'
    url_base = 'www.nanowar.it/XX_YEARS_OF_STEEL'
    old_link = f'short{form}'
    tmp_str = generate_random_string(8)
    file_name = 'Nanowar_Of_Steel_XX_Years_Of_Steel_FULL_SHOW'
    tmp_path = f'TMP/{tmp_str}'
    new_link = f'{tmp_path}/{file_name}{form}'
    copy_file_ftp(url_base, tmp_path, old_link, new_link)
    
    download_link = f'http://{url_base}/{tmp_path}/{file_name}{form}'
    
    return download_link

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
    
    """
    codes_df = pd.DataFrame()
    code_used = [0 for i in range(len(codes))]
    used_date = ['00-00-0000' for i in range(len(codes))]
    codes_df['Code'] = codes
    codes_df['Used'] = code_used
    codes_df['Used_date'] = used_date

    print(codes_df.head())
    codes_df.to_pickle('data/video_code_df.pkl')
    """

    generate_download_link()


