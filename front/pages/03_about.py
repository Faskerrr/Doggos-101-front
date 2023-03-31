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

st.markdown('''
            ## About Doggos-101
            Doggos-101 is a web application designed by a team of LeWagon's Data Science batch #1181 students,
            with the aim of helping dog owners and adopters easily identify the breed of a dog through a simple image.
            The application is based on a Multiclass image classification model, using Transfer Learning,
            which allows it to accurately recognize a number of dog breeds.
            
            The primary goal of Doggos-101 is to provide a simple and user-friendly tool that can help dog owners and adopters
            make informed decisions about their pets. By identifying the breed of a dog, users can learn about the unique characteristics
            and care requirements of that breed, which can help them provide better care and ensure their pet's health and happiness.
            The application is designed to be accessible to everyone, regardless of their level of technical expertise or familiarity with dog breeds.
            
            ##### GitHub links:
            * https://github.com/Faskerrr/Doggos-101
            * https://github.com/Faskerrr/Doggos-101-front
            
            ## Our team
            The Doggos-101 team consists of  **Vladislav Drozhzhin**, **Jihed Chouaref**, **Huynh Dang**, and **Steven Huth**, all of whom have worked with great effort to develop this application.
            
            ##### Contact information:
            * **Vladislav Drozhzhin:** vladislav.drozhzhin@gmail.com
            * **Jihed Chouaref:** jihed.chouaref@gmail.com
            * **Huynh Dang:** huynh.tt.dang@gmail.com
            * **Steven Huth:** stevenhuth@tutanota.com
            ''')
