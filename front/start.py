import streamlit as st
import requests
import numpy as np
from PIL import Image
from io import BytesIO
import re

from Functions.funcs import im_2_b64, b64_2_img

# Code the page:

st.set_page_config(layout="wide", page_title="Doggos-101", page_icon="https://i.ibb.co/cCRNLwz/doggos-loggos-nb.png")

st.write('## Get breed predictions for a dog')
st.write('Test url1 (working): https://www.purina.co.uk/sites/default/files/2022-07/French-Bulldog.jpg')
st.write('Test url2 (not working): https://www.aspcapetinsurance.com/media/2325/facts-about-maltese-dogs.jpg')

col1, col2, col3 = st.columns([8,1,8])
with col1:
    uploaded_file = st.file_uploader(label="Upload picture of your 🐶", # image to be fed to api
                                    type=['png'])

with col3:
    user_url = st.text_input('or pass url:')

img_file, img_url = None, None

with col1:
    if uploaded_file:
        img_file = Image.open(uploaded_file)
        with st.spinner("Barking..."):
            st.image(img_file, width=500)

with col3:
    if user_url:
        with st.spinner("Barking..."):
            # Check format of url (png or jpg):
            if not re.match('(?:([^:/?#]+):)?(?://([^/?#]*))?([^?#]*\.(?:jpg|gif|png))(?:\?([^#]*))?(?:#(.*))?', user_url):
                st.write('Please pass a valid url with an image')
                user_url = None
            else:
                # Check if url is reachable
                try:
                    resp_h = requests.head(user_url, timeout=7)
                    # Check if url returns an image
                    try:
                        assert resp_h.headers['Content-Type'][:5] == 'image' # improve for png and jpg?
                        response = requests.get(user_url, timeout=7)
                        img_url = Image.open(BytesIO(response.content))
                        st.image(img_url, width=500)
                    except Exception as e:
                        st.write('Please pass a valid url with an image')
                        user_url = None
                except requests.exceptions.Timeout:
                    st.write('The request timed out, please check your url or try another')
                    user_url = None

# TODO: deal with case when both file and url are provided
if uploaded_file or user_url:
    img = img_file or img_url
    st.write('api will get:')
    st.image(img, width=500)
    ### Call api to get predictions:

    ###

    # Check if we have a good response
    # if res.status_code == 200:
        ### Display the predictions
        # st.image(res.content, caption="Image returned from API ☝️")

    # with st.spinner("Barking..."):
    #     st.write('### The closest breeds are: 1, 2, 3')

# TODO: try functions from Davy
######## Convert to bytes and decode
    # img_b64 = im_2_b64(img)
    # new_img = b64_2_img(img_b64)
    # st.image(new_img, width=500)
