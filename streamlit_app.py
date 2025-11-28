import streamlit as st
import pandas as pd
import plotly.express as px
# import numpy as np # 移除 numpy 依賴，使用列表計算步長

# ----------------------------------------------------
# 📌 頁面設定與資料載入
# ----------------------------------------------------
# 設定頁面標題和佈局
st.set_page_config(layout="wide", page_title="Gapminder 互動儀表板", page_icon="🌍")

# 標題
st.title("🌍 Gapminder 互動式儀表板")
st.markdown("---")

# 資料讀取：使用 Plotly 官方標準內建的 Gapminder 資料集
df = px.data.gapminder()
unique_years = df['year'].unique().tolist() # 將年份轉換為列表
year_step = unique_years[1] - unique_years[0] if len(unique_years) > 1 else 5 # 簡化步長計算

# ----------------------------------------------------
# 📌 區域 1: 年份滑桿 (位於最上方)
# ----------------------------------------------------
# 使用 Streamlit 的 slider widget 獲取選定的年份
selected_year = st.slider(
    '請選擇年份 (Year Slider):',
    min_value=int(df['year'].min()),
    max_value=int(df['year'].max()),
    value=int(df['year'].max()),
    step=int(year_step), # 使用簡化後的步長
    format='%d'
)

st.markdown("---")

# ----------------------------------------------------
# 📌 數據篩選
# ----------------------------------------------------
# 根據選擇的年份篩選數據
dff = df[df['year'] == selected_year]

# ----------------------------------------------------
# 📌 區域 2: 圖表容器 (左右並排)
# ----------------------------------------------------
# 使用 Streamlit 的 st.columns 實現左右佈局
col1, col2 = st.columns(2)

# --- 左側：散佈圖 (Scatter Plot) ---
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
    # 使用 st.plotly_chart 顯示 Plotly 圖表
    st.plotly_chart(fig_scatter, use_container_width=True)

# --- 右側：旭日圖 (Sunburst Chart) ---
with col2:
    st.subheader(f"各大洲與國家人口分佈 ({selected_year}年)")

    fig_sunburst = px.sunburst(
        dff, 
        path=['continent', 'country'], # 階層：大洲 -> 國家
        values='pop',
        color='continent',
        height=550
    )
    # 使用 st.plotly_chart 顯示 Plotly 圖表
    st.plotly_chart(fig_sunburst, use_container_width=True)
