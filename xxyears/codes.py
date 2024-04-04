import pickle as pkl
import random 
import numpy as np

CODES_FILE = 'xxyears/static/videocodes.pkl'

def get_codes():
    codes = pkl.load(open(CODES_FILE, 'rb'))
    return codes

def draw_random_code():
    codes = get_codes()
    n_rand = random.randint(0, len(codes))
    return codes[n_rand]

def is_code_valid(code):
    codes = get_codes()

    if code in codes:
        return True
    else:
        return False

def remove_code_from_list(code):
    codes = get_codes()
    print(f'Removing code {code} from the database.')

    if code in codes:
        print(len(codes), ' len first')
        icd = np.where(np.array(codes) == code)[0][0]
        del codes[icd]
        print(len(codes), ' len after')
        print('Updating codes file...')
        #pkl.dump(codes, open(CODES_FILE, 'wb'))
        print('Done')

if __name__ == '__main__':

    this_code = draw_random_code()
    print(is_code_valid(this_code))
    remove_code_from_list(this_code)
