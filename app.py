import streamlit as st
import pandas as pd
import utils

def is_code_allowed(input_code):
    """
    Function to check if the input code is in the list of allowed codes.
    """

    df_pkl = 'data/video_code_df.pkl'
    codes_df = pd.read_pickle(df_pkl) 
    print(codes_df.head())

    allowed_codes = list(codes_df['Code'].values)

    if input_code in allowed_codes:
        is_allowed = True
        codes_df = codes_df[codes_df['Code'] != input_code]
        codes_df.to_pickle(df_pkl)
        print(f'Codes updated removing {input_code}, n codes left: {len(codes_df)}')
    else:
        is_allowed = False

    return is_allowed

def generate_download_link(input_code):
    """
    Function to generate a download link based on the input code.
    """
    # In this example, the download link is just a placeholder

    download_link = utils.generate_download_link()

    return f'[DOWNLOAD LINK]({download_link})'

# Streamlit app layout
st.title("XX Years Of Steel")

# User input for code
input_code = st.text_input("Redeem your code:")

# Button to check code and generate download link
if st.button("Check Code"):
    if is_code_allowed(input_code):
        st.success("Valhalleluja! The code worked")
        download_link = generate_download_link(input_code)
        st.markdown(download_link, unsafe_allow_html=True)
    else:
        st.error("Poser, your code did not work.")

