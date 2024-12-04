
from ftplib import FTP
import json
import schedule 
import time
import random
import string
import logging


#TIME_RENAME = 240 
TIME_RENAME = 1 #short for testing


def rename_file_on_ftp(server, username, password, current_filename, new_filename, directory="/"):
    """
    Connects to an FTP server and renames a file.

    Args:
        server (str): The FTP server address.
        username (str): The username for the FTP login.
        password (str): The password for the FTP login.
        current_filename (str): The current name of the file on the FTP server.
        new_filename (str): The new name to assign to the file.
        directory (str): The directory containing the file (default is root "/").

    Returns:
        str: Success message if the operation is successful.
    """

    # Configure the logger
    logger = logging.getLogger('my_app_logger')
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler = logging.FileHandler('log/file_ftp_rename.log')
    file_handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(file_handler)

    # Example usage


    try:
        # Connect to the FTP server
        ftp = FTP(server)
        ftp.login(user=username, passwd=password)
        message = f"Connected to FTP server: {server}"
        print(message)
        logger.info(message) 

        # Change to the specified directory
        if directory != "/":
            ftp.cwd(directory)
            message = f"Changed to directory: {directory}"
            print(message)
            logger.info(message) 

        # Rename the file
        ftp.rename(current_filename, new_filename)
        message = f"Renamed '{current_filename}' to '{new_filename}'"
        print(message)
        logger.info(message) 

        # Close the connection
        ftp.quit()
        return True

    except Exception as e:
        message = f"Error: {e}"
        logger.error(message) 
        print(message)
        return False 


def generate_random_string(length=10):
    """
    Generates a random string of specified length.

    Args:
        length (int): Length of the random string. Default is 10.

    Returns:
        str: Randomly generated string.
    """
    characters = string.ascii_letters + string.digits  # Include letters and digits
    return ''.join(random.choice(characters) for _ in range(length))


def dump_to_json(variable, file_path):
    """
    Dumps a Python variable to a JSON file.

    Args:
        variable (any): The Python variable to be serialized into JSON.
        file_path (str): The path of the JSON file to write to.

    Returns:
        str: Success message if the operation is successful.
    """
    try:
        with open(file_path, 'w') as json_file:
            json.dump(variable, json_file, indent=4)  # Pretty print with 4 spaces
        return f"Successfully wrote variable to {file_path}"
    except Exception as e:
        return f"Error: {e}"


def change_fname(file_path='json/video_filename.json', new_file_root='discoMetal'):
 
    rand_str = generate_random_string(8)

    with open('json/.ftp_credentials.json') as file:
        credentials = json.load(file)
    
    with open(file_path) as file:
        filename = json.load(file)
    
    password = credentials['password']   
    username = credentials['username']   
    server = credentials['server']   
    current = filename['filename']
    rand_str = generate_random_string()
    new = f'{new_file_root}_{rand_str}.mp4'
    directory = '/www.nanowar.it/XX_YEARS_OF_STEEL/FULL_VIDEO/'
    renamed = rename_file_on_ftp(server, username, password, current, new, directory)

    if renamed:
        filename['filename'] = new
        dump_to_json(filename, file_path)


def change_fnames(file_path='json/video_filenames.json', new_file_root='LiveAlcatraz_Part'):
 
    rand_str = generate_random_string(8)
    new_file_root = 'LiveAlcatraz_Part'
    file_format = 'mp4'

    with open('json/.ftp_credentials.json') as file:
        credentials = json.load(file)
    
    with open(file_path) as file:
        filename = json.load(file)
    
    ftp.cwd(ftp_path)
                
    password = credentials['password']   
    username = credentials['username']   
    server = credentials['server']   
    ftp = FTP(server)
    ftp.login(user=username, passwd=password)
        
    ftp_path = 'www.nanowar.it/XX_YEARS_OF_STEEL/FULL_VIDEO/'
    http_path = 'http://www.nanowar.it/XX_YEARS_OF_STEEL/FULL_VIDEO/'

    # Change to the specified directory
    ftp.cwd(ftp_path)

    files = ftp.nlst()
    mp4_files = [file for file in sorted(files) if file.endswith('.mp4')]


    current1 = filename['filename1']
    current2 = filename['filename2']
    current3 = filename['filename3']
    
    rand_str1 = generate_random_string()
    rand_str2 = generate_random_string()
    rand_str3 = generate_random_string()

    new1 = f'{new_file_root}1_{rand_str1}.{file_format}'
    new2 = f'{new_file_root}2_{rand_str2}.{file_format}'
    new3 = f'{new_file_root}3_{rand_str3}.{file_format}'
    
    directory = '/www.nanowar.it/XX_YEARS_OF_STEEL/FULL_VIDEO/'
    
    rename_file_on_ftp(server, username, password, current1, new1, directory)
    rename_file_on_ftp(server, username, password, current2, new2, directory)
    rename_file_on_ftp(server, username, password, current3, new3, directory)

    filename['filename1'] = new1
    filename['filename2'] = new2
    filename['filename3'] = new3

    dump_to_json(filename, file_path)



if __name__ == '__main__':

    print("Scheduler running! Started at: ", time.time())
    schedule.every(TIME_RENAME).minutes.do(change_fnames)

    while True:
        schedule.run_pending()
        time.sleep(1)

