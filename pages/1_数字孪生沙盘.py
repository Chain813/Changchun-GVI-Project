import streamlit as st
import pandas as pd
import pydeck as pdk
import os

st.set_page_config(page_title="数字孪生沙盘 | 街区更新", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .block-container {padding-top: 2rem; padding-bottom: 0rem;}
    html, body, [class*="css"] {font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-weight: 300;}
    </style>
    """, unsafe_allow_html=True)


@st.cache_data
def load_and_merge_data():
    points_file = "Changchun_Precise_Points.xlsx"
    gvi_file = "GVI_Results_Analysis.csv"

    if not os.path.exists(points_file):
        points_file = "../" + points_file
        gvi_file = "../" + gvi_file

    if not os.path.exists(points_file):
        return None, None

    df_points = pd.read_excel(points_file)
    center_lng = float(df_points['Lng'].mean())
    center_lat = float(df_points['Lat'].mean())

    if os.path.exists(gvi_file):
        df_gvi = pd.read_csv(gvi_file)
        if not df_gvi.empty:
            df_gvi['ID'] = df_gvi['Folder'].str.replace('Point_', '').astype(int)
            df_gvi_avg = df_gvi.groupby('ID')['GVI'].mean().reset_index()
            merged_df = pd.merge(df_points, df_gvi_avg, on='ID', how='left')
        else:
            merged_df = df_points.copy()
            merged_df['GVI'] = None
    else:
        merged_df = df_points.copy()
        merged_df['GVI'] = None

    df_valid = merged_df.dropna(subset=['GVI']).copy()
    if not df_valid.empty:
        max_gvi = df_valid['GVI'].max()
        min_gvi = df_valid['GVI'].min()

        def get_enhanced_color(x):
            ratio = (x - min_gvi) / (max_gvi - min_gvi + 0.1)
            r = int(240 - ratio * (240 - 34))
            g = int(220 + ratio * (139 - 220))
            b = int(200 - ratio * (200 - 34))
            return [r, g, b, 230]

        merged_df['fill_color'] = merged_df['GVI'].apply(
            lambda x: get_enhanced_color(x) if pd.notnull(x) else [200, 200, 200, 50]
        )
    else:
        merged_df['fill_color'] = pd.Series([[200, 200, 200, 50]] * len(merged_df))

    return merged_df, (center_lng, center_lat)


df, map_center = load_and_merge_data()

if df is None:
    st.info("💡 请确保目录下存在基础坐标文件 Changchun_Precise_Points.xlsx。")
    st.stop()

df_done = df.dropna(subset=['GVI'])
df_pending = df[df['GVI'].isna()]

with st.sidebar:
    st.markdown("### 数字孪生·古今共振")
    st.markdown("---")
    st.markdown("#### 👁️ 空间视角控制")
    view_mode = st.radio("选择观测模式：", ["🦅 鸟瞰视角", "🗺️ 上帝视角", "🚶 漫游视角"], label_visibility="collapsed")
    st.markdown("---")
    if not df_done.empty:
        min_val = float(df_done['GVI'].min())
        max_val = float(df_done['GVI'].max())
        gvi_range = st.slider("过滤绿视率 (GVI) 区间：", min_val, max_val, (min_val, max_val), 0.1)
        df_done_filtered = df_done[(df_done['GVI'] >= gvi_range[0]) & (df_done['GVI'] <= gvi_range[1])]
    else:
        df_done_filtered = pd.DataFrame()
    st.markdown("---")
    st.metric("总采样点规划", f"{len(df)} 个")
    st.metric("深度学习推演进度", f"{len(df_done)} 个")

st.markdown("### 基于 CV 的街道绿视率 (GVI) 空间聚类诊断")

if "鸟瞰" in view_mode:
    v_pitch, v_bearing, v_zoom = 45, -15, 14.5
elif "上帝" in view_mode:
    v_pitch, v_bearing, v_zoom = 0, 0, 14
else:
    v_pitch, v_bearing, v_zoom = 60, 45, 15.5

layers_to_render = []

if not df_pending.empty:
    layers_to_render.append(pdk.Layer('ScatterplotLayer', data=df_pending, get_position='[Lng, Lat]', get_radius=15,
                                      get_fill_color='fill_color', pickable=False))

if not df_done_filtered.empty:
    layers_to_render.append(pdk.Layer(
        'ColumnLayer', data=df_done_filtered, get_position='[Lng, Lat]', get_elevation='GVI',
        elevation_scale=30, radius=18, coverage=0.85, extruded=True, wireframe=True,
        get_fill_color='fill_color', get_line_color=[255, 255, 255, 64],  # 🌟 25% 透明描边
        lineWidthMinPixels=1, pickable=True, auto_highlight=True
    ))

view_state = pdk.ViewState(longitude=map_center[0], latitude=map_center[1], zoom=v_zoom, pitch=v_pitch,
                           bearing=v_bearing)

r = pdk.Deck(layers=layers_to_render, initial_view_state=view_state, map_style='light',
             tooltip={"html": "<b>GVI:</b> {GVI}%"})
st.pydeck_chart(r, use_container_width=True)