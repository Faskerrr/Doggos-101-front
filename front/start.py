import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import re

# TODO: add a choice between file and url. In current version if both file and url are passed predicts from url

# need?
# st.set_option('deprecation.showfileUploaderEncoding', False)

# url = os.getenv('API_URL')

# Code the page:

st.set_page_config(layout='wide', page_title='Doggos-101', page_icon='https://i.ibb.co/cCRNLwz/doggos-loggos-nb.png')

st.write('## Get breed predictions for a dog')
st.write('Test url1 (working): https://www.purina.co.uk/sites/default/files/2022-07/French-Bulldog.jpg')
st.write('Test url2 Scotch (working): https://i.ibb.co/qkPPHgR/IMAGE-2023-03-26-01-47-08.jpg')
st.write('Test url3 WestHighland (working): https://i.ibb.co/TT1zCxZ/IMAGE-2023-03-26-01-50-15.jpg')
st.write('Test url4 (not working locally): https://www.aspcapetinsurance.com/media/2325/facts-about-maltese-dogs.jpg')

col1, col2, col3 = st.columns([8,1,8])
# TODO: limit input to png and jpg
with col1:
    uploaded_file = st.file_uploader(label='Upload picture of your 🐶', # image to be fed to api
                                    # type=['png, jpg']
                                    )

with col3:
    url_with_pic = st.text_input('or pass url:')

img_file, img_url = None, None

with col1:
    if uploaded_file:
        img_file = Image.open(uploaded_file)
        with st.spinner('Barking...'):
            st.image(img_file, width=500)

with col3:
    if url_with_pic:
        with st.spinner('Barking...'):
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
# TODO: change URL to custom
if url_with_pic:
    with st.spinner('Barking...'):
        params = {'url_with_pic': url_with_pic}
        res = requests.get('http://localhost:8000/predict_url', params=params)
        if res.status_code == 200:
            prediction = res.json()
            st.write(f'{prediction}')
        else:
            st.markdown('**Oops**, something went wrong 😓 Please try again.')

elif uploaded_file:
    with st.spinner('Barking...'):
        img_bytes = uploaded_file.getvalue()
        files = {'file': BytesIO(img_bytes)}
        res = requests.post(f'http://localhost:8000/predict_file', files=files)
        # st.write(f'{res.status_code}')
        if res.status_code == 200:
            prediction = res.json()
            st.write(f'{prediction}')
            # breeds_pred = json.loads(res.content)['prediction']
            # score_pred = json.loads(res.content)['score']
            # st.write(f'{breeds_pred}')
            # st.write(f'{score_pred}')
        else:
            st.markdown('**Oops**, something went wrong 😓 Please try again.')
