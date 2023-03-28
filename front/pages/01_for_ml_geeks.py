import streamlit as st

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


st.markdown('*welcome to section for geeks*')
