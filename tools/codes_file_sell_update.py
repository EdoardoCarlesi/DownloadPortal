import os

# File path (one code per line, read by xxyears/codes.py)
CODES_FILE_SELL = 'xxyears/data/videocodes_sell.txt'


def read_codes_file_sell():
    if not os.path.exists(CODES_FILE_SELL):
        return []
    with open(CODES_FILE_SELL, encoding='utf8') as file:
        return [line.strip() for line in file if line.strip()]


def add_string_to_codes_file_sell(user_string):
    """
    Appends a user-defined code to the CODES_FILE_SELL text file.

    Args:
        user_string (str): The code to be added to the file.
    """
    if not isinstance(user_string, str) or not user_string.strip() or any(c.isspace() for c in user_string):
        raise ValueError("The provided input must be a non-empty string without whitespace.")

    try:
        data = read_codes_file_sell()

        if user_string in data:  # Avoid duplicates
            print(f"The string '{user_string}' already exists in the file.")
            return

        with open(CODES_FILE_SELL, "a", encoding='utf8') as file:
            file.write(user_string + '\n')

        print(f"Successfully added to {CODES_FILE_SELL}: {user_string}")
    except Exception as e:
        print(f"An error occurred: {e}")

def show_codes_file_sell_contents():
    """
    Reads and displays the contents of the CODES_FILE_SELL text file.
    """
    if not os.path.exists(CODES_FILE_SELL):
        print(f"The file '{CODES_FILE_SELL}' does not exist.")
        return

    print("\nContents of the file:")
    for item in read_codes_file_sell():
        print(item)

if __name__ == '__main__':

    this_code = 'tiziana-pinessi-special-code'
    add_string_to_codes_file_sell(this_code)
    show_codes_file_sell_contents()
