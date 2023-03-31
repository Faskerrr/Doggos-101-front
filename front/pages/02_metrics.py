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
response = requests.get('https://i.ibb.co/n7zX33C/doggos-loggos-nb-txt.png')
logo = Image.open(BytesIO(response.content))
st.image(logo, width=275)


# WELCOME MESSAGE
st.markdown("""
            # :feet: Welcome to metrics :feet:

            ### Here you can find the performance metrics of our model""")


# CLASSIFICATION REPORT
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
