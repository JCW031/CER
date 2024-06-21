import streamlit as st
import pandas as pd
import time
import matplotlib.pyplot as plt
from io import BytesIO

#데이터 크롤링 함수
def get_exchange_rate_data(currency_code, last_page_num):
    df = pd.DataFrame()
    
    for page_num in range(1, last_page_num+1):
        url = f"https://finance.naver.com/marketindex/exchangeDailyQuote.naver?marketindexCd=FX_{currency_code}KRW&page={page_num}"
        
        # 표 table 일때 pandas로 사용 가능
        dfs = pd.read_html(url, header=1, encoding='cp949') 
        
        # 통화 코드가 잘못 지정됐거나 마지막 페이지의 경우 for 문을 빠져나옴
        if dfs[0].empty:
            if page_num == 1:
                print(f"통화 코드({currency_code})가 잘못 지정됐습니다.")
            else:
                print(f"{page_num}가 마지막 페이지입니다.")
            break
            
        # page별로 가져온 DataFrame 데이터 연결
        df = pd.concat([df, dfs[0]], ignore_index=True)
        time.sleep(0.1) # 0.1초간 멈춤
        
    return df

# -----------------------------------------


def exchange_main(): 
    st.subheader('Exchange Rate Search Engine')
    currency_name_dict = {'USA': 'USD', 'EU': 'EUR', 'JAP': 'JPY'}

    # 콤보 상자 작성
    currency_name = st.selectbox('Select currency', currency_name_dict.keys())
    click = st.button('Fetch currency data')

    if click:
        select_currency_code = currency_name_dict[currency_name]
        last_page = 20

        # 환율코드 크롤링
        df_exchange = get_exchange_rate_data(select_currency_code, last_page)
        
        # 원하는 열만 선택
        df_exchange = df_exchange[['날짜', '매매기준율', '사실 때', '파실 때', '보내실 때', '받으실 때']]
        
        # 날짜를 인덱스로 설정
        df_exchange = df_exchange.set_index('날짜')
        
        # 환율 데이터 표시
        st.dataframe(df_exchange)

        # 차트 그리기 (선 그래프, 판다스)
        df_exchange_2 = df_exchange.copy()
        df_exchange_2.index = pd.to_datetime(df_exchange_2.index)
        
        fig, ax = plt.subplots(figsize=(15, 5))
        df_exchange_2['매매기준율'].plot(ax=ax, grid=True)
        ax.set_ylabel(f'won/{select_currency_code}')
        ax.set_title('Exchange Rate Graph', fontsize=20)
        
        # Streamlit을 통해 차트 표시
        st.pyplot(fig)

        # 파일 다운로드
        st.subheader('Currency Data Download')
        csv_data = df_exchange.to_csv(index=False, encoding='utf-8-sig')
        excel_data = BytesIO()
        df_exchange.to_excel(excel_data, index=False)
        excel_data.seek(0)  # 파일을 읽기 전에 버퍼 위치를 처음으로 설정
        
        # 2개의 새로단을 구성
        col1, col2 = st.columns(2)
        with col1:
            st.download_button('CSV file download', csv_data, file_name='today_currency_exchange_rate.csv', mime='text/csv')
        with col2:
            st.download_button('Excel file download', data=excel_data, file_name='today_currency_exchange_rate.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

if __name__=='__name__':
    exchange_main()