import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


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


st.markdown('# *Welcome to section for geeks*')


# add the classification report
report = pd.read_csv("./data/classification_report.csv")
st.title("Classification report")
st.write(report)


# add a horizontal bar chart for the least recognized breeds
recall_threshold = 0.6
least_recognized_breeds = report.sort_values(by="recall")[report.recall < recall_threshold]
least_recognized_breeds = least_recognized_breeds.rename(columns = {'index':'breeds'})
fig1= px.bar(least_recognized_breeds, x="recall", y="breeds", orientation="h", title="The least recognized breeds",color_discrete_sequence=["#4C4C4C"],)

st.write(fig1)


# add a horizontal bar chart for the top recognized breeds
recall_threshold = 0.97
top_recognized_breeds = report.sort_values(by="recall")[report.recall > recall_threshold]
top_recognized_breeds = top_recognized_breeds.rename(columns = {'index':'breeds'})
fig2 = px.bar(top_recognized_breeds, x="recall", y="breeds", orientation="h", title="The top recognized breeds",color_discrete_sequence=["#4A1B1B"])

st.write(fig2)



# add the confusion matrix
cm = pd.read_csv("./data/confustion_matrix.csv", index_col=0)
st.title("Confusion matrix")
st.write(cm)

# plt.figure(figsize=(50,50))
# matrix = sns.heatmap(cm, annot=True)
# st.write(matrix)
fig3, ax = plt.subplots(figsize=(30,30))
sns.heatmap(cm, ax=ax, annot=True)
st.write(fig3)
