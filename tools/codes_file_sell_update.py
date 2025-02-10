import os
import pickle

# File path
CODES_FILE_SELL = 'static/videocodes_sell.pkl'


def add_string_to_codes_file_sell(user_string):
    """
    Appends a user-defined string to the CODES_FILE_SELL pickle file.

    Args:
        user_string (str): The string to be added to the file.
    """
    if not isinstance(user_string, str):
        raise ValueError("The provided input must be a string.")

    try:
        # Check if the file exists and load its contents if it does
        if os.path.exists(CODES_FILE_SELL):
            with open(CODES_FILE_SELL, "rb") as file:
                try:
                    data = pickle.load(file)  # Load existing data
                    if not isinstance(data, list):
                        raise ValueError("The content of the file must be a list.")
                except EOFError:
                    data = []  # Initialize as an empty list if the file exists but is empty
        else:
            data = []  # Initialize an empty list if the file doesn't exist

        # Add the new string to the list
        if user_string not in data:  # Avoid duplicates
            data.append(user_string)
        else:
            print(f"The string '{user_string}' already exists in the file.")
            return

        # Write the updated list back to the pickle file
        with open(CODES_FILE_SELL, "wb") as file:
            pickle.dump(data, file)

        print(f"Successfully added to {CODES_FILE_SELL}: {user_string}")
    except Exception as e:
        print(f"An error occurred: {e}")

def show_codes_file_sell_contents():
    """
    Reads and displays the contents of the CODES_FILE_SELL pickle file.
    """
    try:
        # Check if the file exists
        if not os.path.exists(CODES_FILE_SELL):
            print(f"The file '{CODES_FILE_SELL}' does not exist.")
            return

        # Open and load the file contents
        with open(CODES_FILE_SELL, "rb") as file:
            try:
                data = pickle.load(file)  # Load the serialized data
                if not isinstance(data, list):
                    raise ValueError("The content of the file must be a list.")

                # Print the file contents
                print("\nContents of the file:")
                for item in data:
                    print(item)

            except EOFError:
                print(f"The file '{CODES_FILE_SELL}' is empty.")
            except ValueError as ve:
                print(f"Invalid file format: {ve}")

    except Exception as e:
        print(f"An error occurred while reading the file: {e}")

if __name__ == '__main__':

    this_code = 'tiziana-pinessi-special-code'
    add_string_to_codes_file_sell(this_code)
    show_codes_file_sell_contents()