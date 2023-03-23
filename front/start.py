import streamlit as st
import requests
import numpy as np
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
import base64
import multiprocessing
import time

# Define functions:

# Convert Image to Base64
def im_2_b64(image):
    buff = BytesIO()
    image.save(buff, format="PNG")
    img_str = base64.b64encode(buff.getvalue())
    return img_str

# Convert Base64 to Image
def b64_2_img(data):
    buff = BytesIO(base64.b64decode(data))
    return Image.open(buff)

# Check if url is reachable - NEED?
def url_checker(url):
	try:
		#Get Url
		get = requests.get(url)
		# if the request succeeds
		if get.status_code == 200:
			return(f"{url}: is reachable")
		else:
			return(f"{url}: is Not reachable, status_code: {get.status_code}")

	#Exception
	except requests.exceptions.RequestException as e:
        # print URL with Errs
		raise SystemExit(f"{url}: is Not reachable \nErr: {e}")

# Check if url is reachable 2 - NEED?
# Your foo function
def foo(n):
    for i in range(10000 * n):
        response = requests.get(user_url)
        img = Image.open(BytesIO(response.content))
        time.sleep(1)



# Code the page:

st.set_page_config(layout="wide", page_title="Doggos-101", page_icon="https://i.ibb.co/cCRNLwz/doggos-loggos-nb.png")

st.write('## Get breed predictions for a dog')
st.write('Test url1 (working): https://www.purina.co.uk/sites/default/files/2022-07/French-Bulldog.jpg')
st.write('Test url2 (not working): https://www.aspcapetinsurance.com/media/2325/facts-about-maltese-dogs.jpg')

col1, col2 = st.columns([8,8])
with col1:
    uploaded_file = st.file_uploader(label="Upload picture of your 🐶", # image to be fed to api
                                    type=['png'])

with col2:
    user_url = st.text_input('or pass url:')

# col1, col2, col3 = st.columns([3,10,3])

with col1:
    if uploaded_file:
        # To read file as bytes:
        img = Image.open(uploaded_file)
        st.image(img, width=500)

    # elif user_url:
    #     with col2:
    #         with st.spinner("Barking..."):
    #             p = multiprocessing.Process(target=foo, name="Foo", args=(10,))
    #             p.start()
    #             # Wait 10 seconds for foo
    #             time.sleep(10)
    #             # Terminate foo
    #             p.terminate()
    #             st.write('please check your url')
    #             # # Cleanup
    #             # p.join()

        # st.write(url_checker(user_url)) #test_conn_1
        # st.write(urllib.request.urlopen(user_url).getcode()) #test_conn_2
        # response = requests.get(user_url)
        # st.write(f'## response: {response}')
        # img = Image.open(BytesIO(response.content))
        # st.image(img, width=500)

        # st.write('test if url is good', user_url)

    if uploaded_file or user_url:
        pass
        ### Call api to get predictions:
        # img_b64 = im_2_b64(img)
        # new_img = b64_2_img(img_b64)
        # st.image(new_img, width=500)
        ###

        # Check if we have a good response
        # if res.status_code == 200:
            ### Display the predictions
            # st.image(res.content, caption="Image returned from API ☝️")

        # with st.spinner("Barking..."):
        #     st.write('### The closest breeds are: 1, 2, 3')
