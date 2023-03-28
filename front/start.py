import streamlit as st
import requests
import pandas as pd
from PIL import Image
from io import BytesIO
import re
from funcs.kennel_club_UK_descriptions import get_description

# API_URL = 'http://localhost:8000' # local
# API_URL = 'https://doggos-101-m7gv5bfljq-ew.a.run.app/'
API_URL = 'https://doggos-101selection-m7gv5bfljq-ew.a.run.app/' # new

#select background:
#https://wallpapercave.com/dwp2x/wp2941797.png
#https://wallpapercave.com/dwp2x/wp4465167.jpg
#https://i.ibb.co/TYnGjQN/backg.png
st.set_page_config(layout='wide',
                   page_title='Doggos-101',
                   page_icon='https://i.ibb.co/7kk5nbG/doggos-loggos-nb.png',
                   initial_sidebar_state="collapsed")

# add gradient background
page_bg_img = '''
<style>
.stApp {
  background-image: url("https://wallpapercave.com/dwp2x/wp2941797.png");
  background-size: cover;
}
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)

# print our logo?
response = requests.get('https://i.ibb.co/7kk5nbG/doggos-loggos-nb.png')
logo = Image.open(BytesIO(response.content))
st.image(logo, width=100)

# set css for tables:
# https://discuss.streamlit.io/t/unable-to-center-table-cell-values-with-pandas-style-need-input-to-see-if-this-is-even-possible-with-streamlit/31852
# th_props = [
#   ('font-size', '14px'),
#   ('text-align', 'left'),
#   ('font-weight', 'bold'),
#   ('color', '#123C69'),
#   #('background-color', '#eeeeef'),
#   ('border','1px solid #AD9EA1'),
#   #('padding','12px 35px')
# ]

# td_props = [
#   ('font-size', '14px'),
#   ('text-align', 'center'),
# ]

# cell_hover_props = [  # for row hover use <tr> instead of <td>
#     ('background-color', '#EEE2CD')
# ]

# headers_props = [
#     ('text-align','center'),
#     ('font-size','1.1em')
# ]
# #dict(selector='th:not(.index_name)',props=headers_props)

# styles = [
#     dict(selector="th", props=th_props),
#     dict(selector="td", props=td_props),
#     dict(selector="td:hover", props=cell_hover_props),
#     # dict(selector='th.col_heading',props=headers_props),
#     dict(selector='th.col_heading.level0', props=headers_props),
#     dict(selector='th.col_heading.level1', props=td_props)
# ]

#_______________________________________________________________________________
# Code the page:

st.write('## Get breed predictions for a dog')

# temporal for testing
# st.write('Test url1 (working): https://www.purina.co.uk/sites/default/files/2022-07/French-Bulldog.jpg')
# st.write('Test url2 Scotch (working): https://i.ibb.co/qkPPHgR/IMAGE-2023-03-26-01-47-08.jpg')
st.write('Test url3 WestHighland (working): https://i.ibb.co/TT1zCxZ/IMAGE-2023-03-26-01-50-15.jpg')
# st.write('Test url4 (not working locally): https://www.aspcapetinsurance.com/media/2325/facts-about-maltese-dogs.jpg')

left_co, cent_co, last_co = st.columns(3)

with left_co:
    option = st.radio('Would you like to provide a file or a link to a photo of the dog?', ('File', 'Link'))

if option == 'File':
    uploaded_file = st.file_uploader(label='Upload picture of your 🐶',
                                    type=['png','jpeg', 'jpg']
                                    )
elif option == 'Link':
    url_with_pic = st.text_input('Pass url containing picture of your 🐶:')

img_file, img_url = None, None

if option == 'File' and uploaded_file:
    img_file = Image.open(uploaded_file)
    left_co, cent_co,last_co = st.columns(3)
    with cent_co:
        st.image(img_file, use_column_width=True)

if option == 'Link' and url_with_pic:
    # Check format of url (png or jpg):
    if not re.match('(?:([^:/?#]+):)?(?://([^/?#]*))?([^?#]*\.(?:jpg|png))(?:\?([^#]*))?(?:#(.*))?', url_with_pic):
        st.write('Please pass a valid url')
        url_with_pic = None
    else:
        # Check if url is reachable
        try:
            resp_h = requests.head(url_with_pic, timeout=7)
            # Check if url returns an image
            try:
                assert resp_h.headers['Content-Type'][:5] == 'image'
                response = requests.get(url_with_pic, timeout=7)
                img_url = Image.open(BytesIO(response.content))
                left_co, cent_co,last_co = st.columns(3)
                with cent_co:
                    st.image(img_url, use_column_width=True)
            except Exception as e:
                st.write('Please pass a valid url with an image')
                url_with_pic = None
        except requests.exceptions.Timeout:
            st.write('Ooops... The request timed out, please check your url or try another')
            url_with_pic = None

# TODO: sometimes we get img of size ... cannot be reshaped into array (-1,224,224,3) - try logo doggos-101
if option == 'Link' and url_with_pic:
    with cent_co:
        with st.spinner('Barking...'):
            params = {'url_with_pic': url_with_pic}
            res = requests.get(f'{API_URL}/predict_url', params=params)
            if res.status_code == 200:
                prediction, prediction_og, good_response = res.json(), res.json(), True
                prediction['score'].update((key, re.sub(r'\.(\w{2}).*', r'.\1',
                    str(value * 100))+' %') for key, value in prediction['score'].items())
                df = pd.DataFrame.from_dict(prediction)
                df.prediction = df.prediction.str.replace('_', ' ')
                st.table(df)

                #####
                THREASHOLD = 0.9
                EX_URL = 'https://www.purina.co.uk/sites/default/files/2022-07/French-Bulldog.jpg'

                response1 = requests.get('https://i.ibb.co/qkPPHgR/IMAGE-2023-03-26-01-47-08.jpg', timeout=7) #tmp
                ex1_url = Image.open(BytesIO(response1.content))
                response1 = requests.get(EX_URL, timeout=7)
                ex2_url = Image.open(BytesIO(response1.content))
                response1 = requests.get(EX_URL, timeout=7)
                ex3_url = Image.open(BytesIO(response1.content))
                ######

            else:
                st.markdown(f'### **Oops**, Bad response 💩 Please try again')

    # testing example images START
    if good_response:
        #### test descriptions
        desc = get_description('data/uk_kc_characteristics.csv', species_name='West_Highland_white_terrier')
        st.table(desc)

        # st.write(prediction_og)
        # st.write(type(prediction_og['score']['first']))
        left_co, cent_co,last_co = st.columns(3)
        with cent_co:
            st.markdown('### Here are examples of predicted breeds:')

        left_co, cent_co,last_co = st.columns(3)
        with cent_co:
            # if st.checkbox('Show some examples of predicted breeds'):
                if prediction_og['score']['first'] < THREASHOLD:
                    with left_co:
                        st.image(ex1_url, use_column_width=True, caption=f'''{prediction['prediction']['first']}, {prediction['score']['first']} match''')
                    with cent_co:
                        st.image(ex2_url, use_column_width=True, caption=f'''{prediction['prediction']['second']}, {prediction['score']['second']} match''')
                    with last_co:
                        st.image(ex3_url, use_column_width=True, caption=f'''{prediction['prediction']['third']}, {prediction['score']['third']} match''')

    # testing example images END

elif option == 'File' and uploaded_file:
    with cent_co:
        with st.spinner('Barking...'):
            img_bytes = uploaded_file.getvalue()
            files = {'file': BytesIO(img_bytes)}
            res = requests.post(f'{API_URL}/predict_file', files=files)
            if res.status_code == 200:
                prediction = res.json()
                prediction['score'].update((key, re.sub(r'\.(\w{2}).*', r'.\1', str(value * 100))+' %') for key, value in prediction['score'].items())
                df = pd.DataFrame.from_dict(prediction)
                df.prediction = df.prediction.str.replace('_', ' ')
                st.table(df)
            else:
                st.markdown(f'### **Oops**, Bad response 💩 Please try again')
