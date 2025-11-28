import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(layout="wide", page_title="Gapminder 互動儀表板", page_icon="🌍")

# 標題
st.title("🌍 Gapminder 互動式儀表板 ")
st.markdown("---")

df = px.data.gapminder()
unique_years = df['year'].unique()

selected_year = st.slider(
    '請選擇年份 (Year Slider):',
    min_value=int(unique_years.min()),
    max_value=int(unique_years.max()),
    value=int(unique_years.max()),
    step=int(np.diff(unique_years)[0]), # 確保步長是年份之間的間隔
    format='%d'
)

st.markdown("---")

dff = df[df['year'] == selected_year]

col1, col2 = st.columns(2)

# 左側：散佈圖 
with col1:
    st.subheader(f"人均GDP vs. 預期壽命 ({selected_year}年)")
    
    fig_scatter = px.scatter(
        dff, 
        x="gdpPercap", 
        y="lifeExp", 
        size="pop",
        color="continent",
        hover_name="country",
        log_x=True,
        size_max=60,
        labels={
            "gdpPercap": "人均GDP (對數)", 
            "lifeExp": "預期壽命 (年)",
            "pop": "人口數"
        },
        height=550
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

# 右側：旭日圖 
with col2:
    st.subheader(f"各大洲與國家人口分佈 ({selected_year}年)")

    fig_sunburst = px.sunburst(
        dff, 
        path=['continent', 'country'], 
        values='pop',
        color='continent',
        height=550
    )
    st.plotly_chart(fig_sunburst, use_container_width=True)
