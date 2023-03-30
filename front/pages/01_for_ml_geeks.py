import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import requests
from io import BytesIO

st.set_page_config(layout='wide',
                   page_title='Doggos-101/Geeks',
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

# LOGO
response = requests.get('https://i.ibb.co/7kk5nbG/doggos-loggos-nb.png')
logo = Image.open(BytesIO(response.content))
st.image(logo, width=100)


# WELCOME MESSAGE
st.markdown("""
            # :feet: Welcome to section for geeks :feet:

            ### Here are summaries and visualizations of Doggos-101's performance""")


# DATA
res = requests.get('https://d3i71xaburhd42.cloudfront.net/b5e3beb791cc17cdaf131d5cca6ceb796226d832/2-Figure1-1.png')
img = Image.open(BytesIO(res.content))

st.header(":file_folder: About the dataset")
with st.expander("See details"):
    _, col_text, col_img, _ = st.columns([0.2,2,2,0.2])
    col_text.markdown("""
                ##### Context:
                - **The Stanford Dogs dataset contains images of 120 breeds of dogs from around the world.**
                - **This dataset has been built using images and annotation from ImageNet.**

                #####
                ##### Content:
                - **Number of classes: 120**
                - **Number of images: 20,580**

                #####
                ##### **Source:**
                - https://www.kaggle.com/datasets/miljan/stanford-dogs-dataset-traintest
                - http://vision.stanford.edu/aditya86/ImageNetDogs/
                """)
    col_img.image(img, caption="Source: https://bit.ly/3G1yblS", width=500)


# MODEL
st.header(":computer: About the model")
with st.expander("See details"):
    st.markdown("""
                ### Multiclass image classification using Transfer learning:
                - **Use pretrained models (*Inception_V3* and *Resnet50*)**
                - **Use data augmentation**
                - **Modify the dense layers to meet the purpose of our task.**""")


    _, col_models,_ = st.columns([0.2,4,0.2])
    image_models = Image.open("./data/Models.png")
    col_models.image(image_models)

# CLASSIFICATION REPORT
# add the classification report
st.header(":pencil: Classification report")
with st.expander("See details"):
    _, col_tab = st.columns([0.5,4])

    report = pd.read_csv("./data/classification_report.csv")
    report[["precision","recall","f1-score","support"]] = report[["precision","recall","f1-score","support"]].round(decimals=3)

    fig_report = go.Figure(layout=go.Layout(height=800, width=1000),
                        data=[go.Table(
                            header=dict(values=list(report.columns),
                            fill_color='#214660',
                            font_color= 'white',
                            align='right'),
                            cells=dict(values=[report[column] for column in report.columns],
                            fill_color='#fbf3f6',
                            align='right'))]
                        )
    fig_report.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)', 'paper_bgcolor': 'rgba(0,0,0,0)'}, margin=dict(l=20, r=20, t=20, b=20))
    col_tab.write(fig_report)


# HORIZONTAL BAR CHARTS
st.header(":dog: Most- and least- recognized breeds ")
with st.expander("See details"):
    # add containers laid out as side-by-side columns
    col1, col2 = st.columns(2)

    # add a horizontal bar chart for the least recognized breeds
    least_recognized_breeds = report.sort_values(by="recall")[report.recall < 0.6]
    least_recognized_breeds = least_recognized_breeds.rename(columns = {'index':'breeds'})

    fig1= px.bar(least_recognized_breeds, x="recall", y="breeds", orientation="h",
                hover_data=['precision', 'f1-score'], height=400, width=650, color="recall",
                color_continuous_scale="pubu", range_color=[0.5,1], template='simple_white')
    fig1.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)', 'paper_bgcolor': 'rgba(0,0,0,0)'})

    col1.subheader("The least recognized breeds")
    col1.write(fig1)

    # add a horizontal bar chart for the top recognized breeds
    top_recognized_breeds = report.sort_values(by="recall")[report.recall > 0.98]
    top_recognized_breeds = top_recognized_breeds.rename(columns = {'index':'breeds'})

    fig2 = px.bar(top_recognized_breeds, x="recall", y="breeds", orientation="h",
                hover_data=['precision', 'f1-score'], height=400, width=650, color="recall",
                color_continuous_scale="pubu", range_color=[0.5,1], template='simple_white')
    fig2.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)', 'paper_bgcolor': 'rgba(0,0,0,0)'})

    col2.subheader("The most recognized breeds")
    col2.write(fig2)

    st.subheader("Examples of two least recognized breeds")
    _, col_dog1, col_dog2, _ = st.columns([2,2,2,1])

    dog1 = Image.open("./data/dog1.png")
    col_dog1.image(dog1, caption="Eskimo dog", width=300)

    dog2 = Image.open("./data/dog2.png")
    col_dog2.image(dog2, caption="Siberian husky", width=300)

# CONFUSION MATRIX
st.header(":nerd_face: Confusion matrix")
with st.expander("See the table"):
    # add the confusion matrix table
    cm = pd.read_csv("./data/confusion_matrix.csv", index_col=0)
    st.dataframe(data=cm.style.highlight_max(axis=0, color="#c46464"), width=2000, height=1000)

with st.expander("See the figure"):
    # add the confusion matrix figure
    fig3, ax = plt.subplots(figsize=(30,30))
    sns.set_style(style="darkgrid")
    sns.heatmap(cm, ax=ax, annot=True)
    st.write(fig3)

    # image = Image.open("./data/confusion_matrix.png")
    # st.image(image)


# ACTIVATION IMAGES
st.header(":frame_with_picture: Activation images after some convolutional layers")
with st.expander("See the effects of 12 kernels of the first convolutional layer"):
    _, col_img1, col_img2, _ = st.columns([0.5,2,2,0.5])
    image1 = Image.open("./data/activation_img1.png")
    col_img1.image(image1, width=500)
    image2 = Image.open("./data/activation_img2.png")
    col_img2.image(image2, width=500)

with st.expander("See the effects of all kernels of some convolutional layers"):
    _, col_img, _ = st.columns([1,4,1])
    image3 = Image.open("./data/activation_img3.png")
    col_img.image(image3)
    image4 = Image.open("./data/activation_img4.png")
    col_img.image(image4)
    image5 = Image.open("./data/activation_img5.png")
    col_img.image(image5)
    image6 = Image.open("./data/activation_img6.png")
    col_img.image(image6)
