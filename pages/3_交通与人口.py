import streamlit as st
import pandas as pd
import pydeck as pdk
import os

st.set_page_config(page_title="交通与人口 | 微更新平台", layout="wide")

st.markdown("<h2>历史街区真实商业活力测度 (POI)</h2>", unsafe_allow_html=True)
st.markdown("---")


@st.cache_data
def load_real_poi():
    f = "Changchun_POI_Real.csv"
    if not os.path.exists(f): f = "../" + f
    return pd.read_csv(f) if os.path.exists(f) else None


@st.cache_data
def load_base_points():
    f = "Changchun_Precise_Points.xlsx"
    if not os.path.exists(f): f = "../" + f
    return pd.read_excel(f) if os.path.exists(f) else None


df_poi, df_base = load_real_poi(), load_base_points()

if df_poi is not None:
    with st.sidebar:
        st.markdown("#### 👁️ 视角控制")
        v_m = st.radio("模式", ["鸟瞰", "上帝", "漫游"], label_visibility="collapsed")
        st.markdown("---")
        # 🌟 默认半径调小到 50
        h_r = st.slider("聚合网格半径 (米)", 20, 150, 50, 10)
        e_s = st.slider("高度拉伸", 0.5, 10.0, 3.0, 0.5)

    c_lng, c_lat = (df_base['Lng'].mean(), df_base['Lat'].mean()) if df_base is not None else (125.315, 43.902)

    params = {"鸟瞰": (50, 15, 14), "上帝": (0, 0, 14), "漫游": (60, 45, 15.5)}
    v_pitch, v_bearing, v_zoom = params[v_m]

    layer = pdk.Layer(
        "HexagonLayer", data=df_poi, get_position=["Lng", "Lat"], radius=h_r,
        elevation_scale=e_s, elevation_range=[0, 300], extruded=True, coverage=0.88,
        wireframe=True, opacity=0.85, pickable=True,
        get_line_color=[255, 255, 255, 64],  # 🌟 统一 25% 透明描边
        color_range=[[241, 238, 246, 180], [208, 209, 230, 180], [166, 189, 219, 180], [116, 169, 207, 180],
                     [43, 140, 190, 180], [4, 90, 141, 180]]
    )

    st.pydeck_chart(pdk.Deck(
        layers=[layer],
        initial_view_state=pdk.ViewState(longitude=c_lng, latitude=c_lat, zoom=v_zoom, pitch=v_pitch,
                                         bearing=v_bearing),
        map_style="light", tooltip={"text": "POI数量: {elevationValue}"}
    ), use_container_width=True)
else:
    st.warning("请先运行 get_poi.py 抓取数据。")