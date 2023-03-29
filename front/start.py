import streamlit as st
import requests
import pandas as pd
from PIL import Image
from io import BytesIO
import re
import sys
import os
import glob

# for deployment
path_tmp = os.path.dirname(__file__)
module_path = os.path.join(path_tmp, 'funcs')
sys.path.insert(0, module_path)

from kennel_club_UK_descriptions import get_description, clean_description_data

# for local testing
# from funcs.kennel_club_UK_descriptions import get_description


# API_URL = 'http://localhost:8000' # local
# API_URL = 'https://doggos-101-m7gv5bfljq-ew.a.run.app/'
# API_URL = 'https://doggos-101selection-m7gv5bfljq-ew.a.run.app/' # new
API_URL = 'https://doggos-101-m7gv5bfljq-ew.a.run.app' # latest

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

# print our logo? https://i.ibb.co/7kk5nbG/doggos-loggos-nb.png https://i.ibb.co/pzS26yL/doggos-loggos-nb-txt.png
response = requests.get('https://i.ibb.co/n7zX33C/doggos-loggos-nb-txt.png')
logo = Image.open(BytesIO(response.content))
st.image(logo, width=275)

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

# preload names of example images:
ex_names = [i[:-7].lower() for i in os.listdir('example_images/')]
rename_ex = pd.DataFrame({'col1': os.listdir('example_images/')}, index=ex_names)

# temporal for testing
# st.write('Test url1 (working): https://www.purina.co.uk/sites/default/files/2022-07/French-Bulldog.jpg')
# st.write('Test url2 Scotch (working): https://i.ibb.co/qkPPHgR/IMAGE-2023-03-26-01-47-08.jpg')
# st.write('Test url3 WestHighland (working): https://i.ibb.co/TT1zCxZ/IMAGE-2023-03-26-01-50-15.jpg')
# st.write('Test url4 (not working locally): https://www.aspcapetinsurance.com/media/2325/facts-about-maltese-dogs.jpg')
# st.write('Test url4 (png): https://i.ibb.co/6bMDVSb/1.png')

left_co, cent_co, last_co = st.columns(3)

with left_co:
    option = st.radio('Would you like to provide a file or a link to a photo of the dog?', ('File', 'Link'))

if option == 'File':
    uploaded_file = st.file_uploader(label='Upload picture of your 🐶',
                                    type=['png', 'jpeg', 'jpg']
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
                prediction, prediction_og = res.json(), res.json()
                prediction['score'] = {key: value for key, value in prediction['score'].items() if value > 0}
                prediction['prediction'] = {key: value for key, value in prediction['prediction'].items() if key in prediction['score'].keys()}
                prediction['score'].update((key, re.sub(r'\.(\w{2}).*', r'.\1',
                    str(value * 100))+'%') for key, value in prediction['score'].items())
                df = pd.DataFrame.from_dict(prediction)
                df.prediction = df.prediction.str.replace('_', ' ').str.title()
                hdf = df.assign(hack='').set_index('hack')
                st.table(hdf)
            else:
                st.markdown(f'### **Oops**, Bad response 💩 Please try again')

    if res.status_code == 200:

        ex1_png = glob.glob(f'''example_images/{rename_ex.loc[prediction_og['prediction']['first'].lower(), 'col1']}''')
        ex2_png = glob.glob(f'''example_images/{rename_ex.loc[prediction_og['prediction']['second'].lower(), 'col1']}''')
        ex3_png = glob.glob(f'''example_images/{rename_ex.loc[prediction_og['prediction']['third'].lower(), 'col1']}''')

        # Use that to display references from url's:

        # response1 = requests.get('https://i.ibb.co/qkPPHgR/IMAGE-2023-03-26-01-47-08.jpg', timeout=7) #tmp
        # ex1_url = Image.open(BytesIO(response1.content))

        if prediction_og['score']['first'] > 0 and prediction_og['score']['second'] > 0 and prediction_og['score']['third'] > 0:

            left_co, cent_co,last_co = st.columns((5, 8, 1))
            with cent_co:
                st.markdown('### Predicted breeds look like:')

            left_co, cent_co,last_co = st.columns(3)
            with left_co:
                st.image(ex1_png, use_column_width=True, caption=f'''{df.loc['first', 'prediction']}, {prediction['score']['first']} match''')
            with cent_co:
                st.image(ex2_png, use_column_width=True, caption=f'''{df.loc['second', 'prediction']}, {prediction['score']['second']} match''')
            with last_co:
                st.image(ex3_png, use_column_width=True, caption=f'''{df.loc['third', 'prediction']}, {prediction['score']['third']} match''')

            left_co, cent_co,last_co = st.columns((5, 8, 1))
            with cent_co:
                st.markdown('### Some facts on these breeds:')

            st.table(get_description('data/uk_kc_characteristics.csv', species_name=prediction_og['prediction']['first']))
            st.table(get_description('data/uk_kc_characteristics.csv', species_name=prediction_og['prediction']['second']))
            st.table(get_description('data/uk_kc_characteristics.csv', species_name=prediction_og['prediction']['third']))

        elif prediction_og['score']['first'] > 0 and prediction_og['score']['second'] > 0:

            left_co, cent_co,last_co = st.columns((5, 8, 1))
            with cent_co:
                st.markdown('### Predicted breeds look like:')

            col_1, col_2, col_3, col_4 = st.columns((2, 4, 4, 2))
            with col_2:
                st.image(ex1_png, use_column_width=True, caption=f'''{df.loc['first', 'prediction']}, {prediction['score']['first']} match''')
            with col_3:
                st.image(ex2_png, use_column_width=True, caption=f'''{df.loc['second', 'prediction']}, {prediction['score']['second']} match''')

            left_co, cent_co,last_co = st.columns((5, 8, 1))
            with cent_co:
                st.markdown('### Some facts on these breeds:')

            st.table(get_description('data/uk_kc_characteristics.csv', species_name=prediction_og['prediction']['first']))
            st.table(get_description('data/uk_kc_characteristics.csv', species_name=prediction_og['prediction']['second']))

        else:

            left_co, cent_co,last_co = st.columns((5, 8, 1))
            with cent_co:
                st.markdown('### Predicted breeds look like:')

            left_co, cent_co,last_co = st.columns(3)
            with cent_co:
                st.image(ex1_png, use_column_width=True, caption=f'''{df.loc['first', 'prediction']}, {prediction['score']['first']} match''')

            left_co, cent_co,last_co = st.columns((5, 8, 1))
            with cent_co:
                st.markdown('### Some facts on these breeds:')

            st.table(get_description('data/uk_kc_characteristics.csv', species_name=prediction_og['prediction']['first']))


elif option == 'File' and uploaded_file:
    with cent_co:
        with st.spinner('Barking...'):
            img_bytes = uploaded_file.getvalue()
            files = {'file': BytesIO(img_bytes)}
            res = requests.post(f'{API_URL}/predict_file', files=files)
            if res.status_code == 200:
                prediction, prediction_og = res.json(), res.json()
                prediction['score'] = {key: value for key, value in prediction['score'].items() if value > 0}
                prediction['prediction'] = {key: value for key, value in prediction['prediction'].items() if key in prediction['score'].keys()}
                prediction['score'].update((key, re.sub(r'\.(\w{2}).*', r'.\1',
                    str(value * 100))+'%') for key, value in prediction['score'].items())
                df = pd.DataFrame.from_dict(prediction)
                df.prediction = df.prediction.str.replace('_', ' ').str.title()
                hdf = df.assign(hack='').set_index('hack')
                st.table(hdf)
            else:
                st.markdown(f'### **Oops**, Bad response 💩 Please try again')

    if res.status_code == 200:

        ex1_png = glob.glob(f'''example_images/{rename_ex.loc[prediction_og['prediction']['first'].lower(), 'col1']}''')
        ex2_png = glob.glob(f'''example_images/{rename_ex.loc[prediction_og['prediction']['second'].lower(), 'col1']}''')
        ex3_png = glob.glob(f'''example_images/{rename_ex.loc[prediction_og['prediction']['third'].lower(), 'col1']}''')

        # Use that to display references from url's:

        # response1 = requests.get('https://i.ibb.co/qkPPHgR/IMAGE-2023-03-26-01-47-08.jpg', timeout=7) #tmp
        # ex1_url = Image.open(BytesIO(response1.content))

        if prediction_og['score']['first'] > 0 and prediction_og['score']['second'] > 0 and prediction_og['score']['third'] > 0:

            left_co, cent_co,last_co = st.columns((5, 8, 1))
            with cent_co:
                st.markdown('### Predicted breeds look like:')

            left_co, cent_co,last_co = st.columns(3)
            with left_co:
                st.image(ex1_png, use_column_width=True, caption=f'''{df.loc['first', 'prediction']}, {prediction['score']['first']} match''')
            with cent_co:
                st.image(ex2_png, use_column_width=True, caption=f'''{df.loc['second', 'prediction']}, {prediction['score']['second']} match''')
            with last_co:
                st.image(ex3_png, use_column_width=True, caption=f'''{df.loc['third', 'prediction']}, {prediction['score']['third']} match''')

            left_co, cent_co,last_co = st.columns((5, 8, 1))
            with cent_co:
                st.markdown('### Some facts on these breeds:')

            st.table(get_description('data/uk_kc_characteristics.csv', species_name=prediction_og['prediction']['first']))
            st.table(get_description('data/uk_kc_characteristics.csv', species_name=prediction_og['prediction']['second']))
            st.table(get_description('data/uk_kc_characteristics.csv', species_name=prediction_og['prediction']['third']))

        elif prediction_og['score']['first'] > 0 and prediction_og['score']['second'] > 0:

            left_co, cent_co,last_co = st.columns((5, 8, 1))
            with cent_co:
                st.markdown('### Predicted breeds look like:')

            col_1, col_2, col_3, col_4 = st.columns((2, 4, 4, 2))
            with col_2:
                st.image(ex1_png, use_column_width=True, caption=f'''{df.loc['first', 'prediction']}, {prediction['score']['first']} match''')
            with col_3:
                st.image(ex2_png, use_column_width=True, caption=f'''{df.loc['second', 'prediction']}, {prediction['score']['second']} match''')

            left_co, cent_co,last_co = st.columns((5, 8, 1))
            with cent_co:
                st.markdown('### Some facts on these breeds:')

            st.table(get_description('data/uk_kc_characteristics.csv', species_name=prediction_og['prediction']['first']))
            st.table(get_description('data/uk_kc_characteristics.csv', species_name=prediction_og['prediction']['second']))

        else:
          ###
            description_data = pd.read_csv(description_data_path, index_col='breed_name')
            clean_data = clean_description_data(description_data)
            st.wirte(f'''this is decsription raw:
            {description_data}''')
            st.wirte(f'''this is decsription clean:
            {clean_data}''')
          ###
            left_co, cent_co,last_co = st.columns((5, 8, 1))
            with cent_co:
                st.markdown('### Predicted breeds look like:')

            left_co, cent_co,last_co = st.columns(3)
            with cent_co:
                st.image(ex1_png, use_column_width=True, caption=f'''{df.loc['first', 'prediction']}, {prediction['score']['first']} match''')

            left_co, cent_co,last_co = st.columns((5, 8, 1))
            with cent_co:
                st.markdown('### Some facts on these breeds:')

            st.table(get_description('data/uk_kc_characteristics.csv', species_name=prediction_og['prediction']['first']))
