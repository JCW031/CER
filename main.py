import streamlit as st
from PIL import Image
import exchange_rate
# import exchange_main 

st.title('Hi')
st.header('My love')
st.sidebar.header('Log in')
user_id = st.sidebar.text_input('아이디 입력', value='', max_chars=15)
user_password = st.sidebar.text_input('패스워드 입력', value='', type='password')

if user_id == 'violetta' and user_password == '1234':
    st.sidebar.header('Cj Portfolio')
    # options = ['', '진주 귀걸이를 한 소녀', '별이 빛나는 밤', '절규', '생명의 나무', '월하정인']
    # user_opt = st.sidebar.selectbox('좋아하는 작품은?', options, index=0)
    # st.sidebar.write('**선택한 그림은', user_opt)

    menu = st.sidebar.radio('메뉴 선택',['환율 조회','부동산 조회(EDA)','인공지능 옟측/분류'], index= None)
    if menu == '환율 조회': 
        exchange_rate.exchange_main()
        st.sidebar.write('환율 조회')
    elif menu == '부동산 조회(EDA)':
        st.sidebar.write('부동산 조회(EDA)')   
    elif menu == '인공지능 옟측/분류':
        st.sidebar.write('인공지능 옟측/분류')
    else:
        st.sidebar.write('메뉴를 선택해주세요')
        

    # 메인 화면
    st.subheader('How are you?')
    
