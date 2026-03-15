import streamlit as st
import pandas as pd
import pydeck as pdk
import os

# --- 1. 极简风页面配置与 CSS 注入 ---
st.set_page_config(page_title="数字孪生沙盘 | 街区更新", layout="wide", initial_sidebar_state="expanded")

# 隐藏默认菜单，优化字体和排版
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .block-container {padding-top: 2rem; padding-bottom: 0rem;}
    h1, h2, h3, h4 {font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-weight: 300;}
    </style>
    """, unsafe_allow_html=True)

# --- 2. 侧边栏：极简信息与视角交互 ---
with st.sidebar:
    st.markdown("### 数字孪生·古今共振")
    st.caption("AI赋能下的伪满皇宫周边街区更新")
    st.markdown("---")
    
    # 🌟 核心交互：视角控制器
    st.markdown("#### 👁️ 空间视角控制")
    view_mode = st.radio(
        "选择沙盘观测模式：",
        ["🦅 鸟瞰视角 (3D倾斜)", "🗺️ 上帝视角 (2D平面)", "🚶 漫游视角 (低空沉浸)"],
        label_visibility="collapsed"
    )
    st.markdown("---")
    st.markdown("#### 📊 实时数据感知")
    metric_placeholder = st.empty() # 预留给后面的数据统计

# --- 3. 数据加载与融合 ---
@st.cache_data
def load_and_merge_data():
    # ⚠️ 确保这里的文件名和你刚才生成的最新 Excel 一致！
    points_file = "Changchun_Precise_Points.xlsx" 
    gvi_file = "GVI_Results_Analysis.csv"
    
    if not os.path.exists(points_file) or not os.path.exists(gvi_file):
        return None
        
    df_points = pd.read_excel(points_file)
    df_gvi = pd.read_csv(gvi_file)
    
    # 清洗并匹配 ID
    df_gvi['ID'] = df_gvi['Folder'].str.replace('Point_', '').astype(int)
    df_gvi_avg = df_gvi.groupby('ID')['GVI'].mean().reset_index()
    return pd.merge(df_points, df_gvi_avg, on='ID', how='inner')

df = load_and_merge_data()

# --- 4. 主视觉与交互渲染 ---
if df is not None:
    # 更新侧边栏的数据面板
    with metric_placeholder.container():
        st.metric("感知节点总数", f"{len(df)} 个")
        st.metric("街区平均绿视率", f"{df['GVI'].mean():.1f} %")

    # 主界面标题 (极简留白)
    st.markdown("### 基于 CV 的街道绿视率 (GVI) 空间聚类诊断")
    st.caption("注：较高的绿色柱体代表环境品质较好的慢行空间；低矮的暖灰色柱体提示亟待微更新的触媒节点。")
    
    # 🌟 高级色彩映射：从沙灰色(低) 到 翡翠绿(高)
    # x 取值 0~100。x=0 时接近 [240, 220, 200] (沙灰)；x=100 时接近 [40, 200, 100] (鲜绿)
    df['fill_color'] = df['GVI'].apply(lambda x: [
        int(240 - (x * 2)),      # R
        int(200 + (x * 0.2)),    # G
        int(200 - (x * 1)),      # B
        220                      # 透明度
    ])
    
    # 动态设定视角参数
    if "鸟瞰" in view_mode:
        v_pitch, v_bearing, v_zoom = 45, -15, 14.5
    elif "上帝" in view_mode:
        v_pitch, v_bearing, v_zoom = 0, 0, 14
    else: # 漫游
        v_pitch, v_bearing, v_zoom = 60, 45, 15.5

    # PyDeck 3D 柱状图层
    layer = pdk.Layer(
        'ColumnLayer',
        data=df,
        get_position='[Lng, Lat]',
        get_elevation='GVI',
        elevation_scale=8, # 柱子高度缩放，极简风不宜太夸张
        radius=12,         # 柱子粗细
        get_fill_color='fill_color',
        pickable=True,
        auto_highlight=True,
    )

    # 初始化视角 (移除花哨的过渡动画，确保 100% 稳定运行)
    view_state = pdk.ViewState(
        longitude=df['Lng'].mean(),
        latitude=df['Lat'].mean(),
        zoom=v_zoom,
        pitch=v_pitch,
        bearing=v_bearing
    )
    
    # 渲染地图 (更换为极简浅色底图)
    r = pdk.Deck(
        layers=[layer], 
        initial_view_state=view_state, 
        map_style='light', # 🌟 核心：改成极简白底地图
        tooltip={"html": "<b>节点 ID:</b> {ID} <br/> <b>GVI 测度:</b> {GVI}%", "style": {"backgroundColor": "white", "color": "#333", "fontFamily": "sans-serif"}}
    )
    
    # 渲染高度设为 600px，让视觉更开阔
    st.pydeck_chart(r, use_container_width=True)

else:
    st.info("💡 请先完成数据采集与推理，确保目录下存在坐标 Excel 与测度结果 CSV。")