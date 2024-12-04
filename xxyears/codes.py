import pickle as pkl
import random 
import numpy as np

CODES_FILE_ORIGINAL = 'xxyears/static/videocodes.pkl'
CODES_FILE_SELL = 'xxyears/static/videocodes_sell.pkl'

def get_codes():

    codes_original = pkl.load(open(CODES_FILE_ORIGINAL, 'rb'))
    codes_sell = pkl.load(open(CODES_FILE_SELL, 'rb'))
    return codes_original, codes_sell

def draw_random_sell_code():
    
    co, cs = get_codes()
    n_cs = random.randint(0, len(cs))

    return cs[n_cs]


def draw_random_code():
    
    co, cs = get_codes()
    n_co = random.randint(0, len(co))
    n_cs = random.randint(0, len(cs))
    n_rand = random.randint(0, 10)

    if n_rand > 5:
        return co[n_co]
    else:
        return cs[n_cs]

def is_code_valid(code):
    
    co, cs = get_codes()

    if (code in co) or (code in cs):
        return True
    else:
        return False

def is_code_sell(code):

    co, cs = get_codes()

    if code in cs:
        return True
    else:
        return False

def remove_code_from_list(code):
    
    co, cs = get_codes()
    print(f'Removing code {code} from the database.')

    if code in cs:
        print(len(cs), ' len first')
        icd = np.where(np.array(cs) == code)[0][0]
        del cs[icd]
        print(len(cs), ' len after')
        print('Updating codes file...')
        pkl.dump(cs, open(CODES_FILE_SELL, 'wb'))
        print('Done')

    elif code in co:
        print(len(co), ' len first')
        icd = np.where(np.array(co) == code)[0][0]
        del co[icd]
        print(len(co), ' len after')
        print('Updating codes file...')
        pkl.dump(co, open(CODES_FILE_ORIGINAL, 'wb'))
        print('Done')

if __name__ == '__main__':

    this_code = draw_random_code()
    print(is_code_valid(this_code))
    #remove_code_from_list(this_code)
