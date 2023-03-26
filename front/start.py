import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import re
import os

# need?
# st.set_option('deprecation.showfileUploaderEncoding', False)

api_url = 'http://localhost:8000'
# TODO:change to docker url once it is running:
# from dotenv import load_dotenv
# load_dotenv()
# url = os.getenv('API_URL')


# Code the page:
#https://wallpapercave.com/dwp2x/wp2941797.png
#https://wallpapercave.com/dwp2x/wp4465167.jpg
#https://i.ibb.co/TYnGjQN/backg.png
st.set_page_config(layout='wide',
                   page_title='Doggos-101',
                   page_icon='https://i.ibb.co/7kk5nbG/doggos-loggos-nb.png',
                   initial_sidebar_state="collapsed")

page_bg_img = '''
<style>
.stApp {
  background-image: url("https://wallpapercave.com/dwp2x/wp2941797.png");
  background-size: cover;
}
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)

response = requests.get('https://i.ibb.co/7kk5nbG/doggos-loggos-nb.png')
img_url = Image.open(BytesIO(response.content))
st.image(img_url, width=100)

st.write('## Get breed predictions for a dog')
st.write('Test url1 (working): https://www.purina.co.uk/sites/default/files/2022-07/French-Bulldog.jpg')
st.write('Test url2 Scotch (working): https://i.ibb.co/qkPPHgR/IMAGE-2023-03-26-01-47-08.jpg')
st.write('Test url3 WestHighland (working): https://i.ibb.co/TT1zCxZ/IMAGE-2023-03-26-01-50-15.jpg')
st.write('Test url4 (not working locally): https://www.aspcapetinsurance.com/media/2325/facts-about-maltese-dogs.jpg')



option = st.selectbox(
    'Would you like to provide a file or a link to a photo of the dog?',
    ('File', 'Link'))

if option == 'File':
    # TODO: limit input to png and jpg
    uploaded_file = st.file_uploader(label='Upload picture of your 🐶', # image to be fed to api
                                    # type=['png, jpg']
                                    )
elif option == 'Link':
    url_with_pic = st.text_input('or pass url:')

img_file, img_url = None, None

if option == 'File' and uploaded_file:
    img_file = Image.open(uploaded_file)
    st.image(img_file, width=500)

if option == 'Link' and url_with_pic:
    # Check format of url (png or jpg):
    if not re.match('(?:([^:/?#]+):)?(?://([^/?#]*))?([^?#]*\.(?:jpg|gif|png))(?:\?([^#]*))?(?:#(.*))?', url_with_pic):
        st.write('Please pass a valid url with an image')
        url_with_pic = None
    else:
        # Check if url is reachable
        try:
            resp_h = requests.head(url_with_pic, timeout=7)
            # Check if url returns an image
            try:
                assert resp_h.headers['Content-Type'][:5] == 'image' # improve for png and jpg?
                response = requests.get(url_with_pic, timeout=7)
                img_url = Image.open(BytesIO(response.content))
                st.image(img_url, width=500)
            except Exception as e:
                st.write('Please pass a valid url with an image')
                url_with_pic = None
        except requests.exceptions.Timeout:
            st.write('Ooops... The request timed out, please check your url or try another')
            url_with_pic = None

# TODO: sometimes we get img of size ... cannot be reshaped into array (-1,224,224,3) - try logo doggos-101
if option == 'Link' and url_with_pic:
    with st.spinner('Barking...'):
        params = {'url_with_pic': url_with_pic}
        res = requests.get(f'{api_url}/predict_url', params=params)
        if res.status_code == 200:
            prediction = res.json()
            st.write(f'{prediction}')
        else:
            st.markdown('**Oops**, something went wrong 😓 Please try again.')

elif option == 'File' and uploaded_file:
    with st.spinner('Barking...'):
        img_bytes = uploaded_file.getvalue()
        files = {'file': BytesIO(img_bytes)}
        res = requests.post(f'{api_url}/predict_file', files=files)
        # st.write(f'{res.status_code}')
        if res.status_code == 200:
            prediction = res.json()
            st.write(f'{prediction}')
        else:
            st.markdown('**Oops**, something went wrong 😓 Please try again.')
