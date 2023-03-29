import streamlit as st
import requests
import pandas as pd
from PIL import Image
from io import BytesIO
import re
import sys
import os
import glob

##########################IGNORE THIS TON OF CODE#################IT IS SUPPOSED TO BE IMPORTED FROM THE FUNCS DIR BUT STREAMLIT ACTS######
def clean_description_data(description_data):
    description_data['class'] = description_data['class'].map(str.capitalize)
    description_data['size_of_garden'] = description_data['size_of_garden'].map(lambda x: x.replace('/ medium', ''))
    description_data['town_or_country'] = description_data['town_or_country'].map({'Either': 'Yes', 'Country': 'No'})
    description_data['exercise'] = description_data['exercise'].map(lambda x: x.replace('per day', '').replace('Up to', '~').replace('More than', '>').replace('minutes', 'mins'))
    description_data['lifespan'] = description_data['lifespan'].map(lambda x: x.replace('Over', '>').replace('Under', '<'))

    description_data.drop(columns = ['Position', 'vulnerable_native_breed'], inplace = True)
    description_data.index.name = None

    description_data.columns = ['Class', 'Size', 'Daily exercise', 'Home', 'Grooming', 'Fur length', 'Fur loss', 'Lifespan', 'City', 'Garden']
    return description_data[['Class', 'Size', 'Lifespan', 'Daily exercise', 'Home', 'Garden', 'City', 'Fur length', 'Fur loss', 'Grooming']]

def clean_name(name):
    ''' converts dog name to match the names used by the kennel club UK'''
    name = name.replace('-and-', ' & ')
    name = name.replace('_', ' ')
    name = name.replace('-', ' ')
    name = ' '.join(map(str.capitalize,name.split(' ')))

    correction_dict = {
        'Greater': 'Great',
        'Short Haired': 'Shorthaired',
        'Long Haired': 'Longhaired',
        'Bullterrier': 'Bull Terrier',
        'Scotch': 'Scottish',
        'Saint': 'St.',
        'Bull Mastiff': 'Bullmastiff',
        'Great Pyrenees': 'Pyrenean Mountain Dog',
        'Standard Schnauzer': 'Schnauzer',
        'Japanese Spaniel': 'Japanese Chin',
        'Boston Bull': 'Boston Terrier',
        'Brabancon Griffon': 'Griffon Bruxellois',
        'Haired': '',
        'Mexican': 'Mex',
        'Pekinese': 'Pekingese',
        'Basset': 'Basset Hound',
        'Bull Dog': 'Bulldog',
        'Schnauzer Standard': 'Schnauzer',
        'Blenheim Spaniel': 'King Charles Spaniel'
    }
    for word, correction in correction_dict.items():
        name = name.replace(word, correction)
    return name


def find_exact_kennel_entries(description_data, name):
    ''' returns all kennel_club UK entries with indexes that contain ALL words of species_name (order doesn't matter)
    e.g. Standard Poodle is going to be recognized as Poodle (Standard)'''
    index_in_kennel_data = description_data.index.map(lambda kennel_entry: all(word in kennel_entry for word in name.split()))
    return description_data[index_in_kennel_data]


def find_approximate_kennel_entries(description_data, name):
    ''' # returns kennel_club UK entries with indexes that contains ONE word of species_name ; common words like "dog" or "hound" are ignored'''
    ignore_list = ['Dog', 'English', 'Terrier', 'American', 'Spaniel', 'Haired', 'Wire', 'Japanese', 'Hound', 'Scottish']
    for word in ignore_list:
        name = name.replace(word, '')
    index_in_kennel_data = description_data.index.map(lambda kennel_entry: any(word in kennel_entry for word in name.split()))
    return description_data[index_in_kennel_data]


def remove_exceptions(descriptions, name):
    ''' hard coding for unwanted matches that were not removed automatically;
    if the dog name matches a key of exceptions, the corresponding row of
    from description is dropped '''
    exceptions_dict = {'Collie': 'Border Collie'}
    if name in exceptions_dict.keys():
        corrected_descriptions = descriptions.drop(exceptions_dict[name], axis=0)
        return corrected_descriptions
    return descriptions


def get_description(description_data_path, species_name:str):
    ''' takes the name of a dog breed and looks for corresponding entries in the kennel club UK data
    returns a DataFrame with all matching entries
    First, checks for exact matches
    If no exact matches are found, looks for matches that contain all words of species_name
    If there are still no matches, looks for entries that contain any word of species_name
    '''
    description_data = pd.read_csv(description_data_path, index_col='breed_name')
    description_data = clean_description_data(description_data)
    cleaned_name = clean_name(species_name)
    if cleaned_name in description_data.index:
        descriptions = description_data.loc[[cleaned_name],:]
    elif not find_exact_kennel_entries(description_data, cleaned_name).empty:
        descriptions = find_exact_kennel_entries(description_data, cleaned_name)
    else:
        descriptions = find_approximate_kennel_entries(description_data, cleaned_name)
    return remove_exceptions(descriptions, cleaned_name)
    # .style is necessary so that the output shows the "<br>" introduced in
    #  clean_description_data as linebreaks in the dataframe
###################################END IGNORING###################################################

# for deployment
# path_tmp = os.path.dirname(__file__)
# module_path = os.path.join(path_tmp, 'funcs')
# sys.path.insert(0, module_path)

# from kennel_club_UK_descriptions import get_description

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
