import streamlit as st
import pandas as pd
import pydeck as pdk
import os

st.set_page_config(page_title="数字孪生沙盘 | 微更新平台", layout="wide")
# 🌟 核心修复：强制侧边栏在子页面加载时就是展开的
st.set_page_config(page_title="子模块", layout="wide", initial_sidebar_state="expanded")

# ==========================================
# 🌟 全局 UI 架构：巨幕地图与极致排版
# ==========================================
st.markdown("""
    <style>
    /* 1. 炸毁顶栏 (没问题，继续炸) */
    [data-testid="stHeader"] {display: none !important;}
    
    /* 2. 只炸毁侧边栏里面的“页面导航菜单”，保留侧边栏本身用来放滑块 */
    [data-testid="stSidebarNav"] {display: none !important;}
    
    /* 3. 强制显示侧边栏，防止它被意外收起 */
    [data-testid="stSidebar"] {
        display: flex !important;
        visibility: visible !important;
    }

    /* 2. 极致贴顶 */
    .block-container { padding-top: 1rem !important; padding-bottom: 0rem !important;}

    /* 3. 完美的悬浮导航栏 */
    a[data-testid="stPageLink-NavLink"] {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 8px !important; padding: 0.6rem 1rem !important;
        display: flex !important; justify-content: center !important;
        text-decoration: none !important; transition: all 0.3s ease !important;
    }
    a[data-testid="stPageLink-NavLink"]:hover {
        background-color: rgba(255, 255, 255, 0.25) !important;
        border-color: rgba(255, 255, 255, 0.5) !important; transform: translateY(-2px);
    }
    a[data-testid="stPageLink-NavLink"] p, a[data-testid="stPageLink-NavLink"] span {
        font-size: 18px !important; font-weight: 600 !important; color: #f8fafc !important; margin: 0 !important;
    }

    /* 4. 全局暗黑模式 */
    .stApp { background-color: #0f172a; }
    h1, h2, h3, h4, h5, label, .stMarkdown p { color: #f8fafc !important; }

    /* 🌟 5. 核心修复：侧边栏暴力变白！ */
    [data-testid="stSidebar"] { background-color: #1e293b !important; border-right: 1px solid #334155 !important; }
    /* 用 * 号强行让侧边栏里所有的字（滑块数值、勾选框等）全部变成极光白！ */
    [data-testid="stSidebar"] * { color: #f8fafc !important; }

    /* 6. 其他组件暗黑化 */
    div[data-baseweb="select"] > div, textarea, input, section[data-testid="stFileUploader"] {
        background-color: #1e293b !important; color: #f8fafc !important; border: 1px solid #475569 !important;
    }
    [data-testid="stMetricValue"], [data-testid="stMetricLabel"] { color: #f8fafc !important; }

    /* 7. 地图巨幕高度 */
    [data-testid="stDeckGlJsonChart"] { height: 75vh !important; min-height: 650px !important; }
    </style>
    """, unsafe_allow_html=True)
# 顶部导航
col1, col2, col3, col4 = st.columns(4)
with col1: st.page_link("app.py", label="系统主页", use_container_width=True)
with col2: st.page_link("pages/1_数字孪生沙盘.py", label="数字孪生沙盘", use_container_width=True)
with col3: st.page_link("pages/2_AIGC风貌管控.py", label="风貌管控", use_container_width=True)
with col4: st.page_link("pages/3_交通与人口.py", label="交通与人口", use_container_width=True)
st.markdown("---")

st.markdown("<h2>多模态数字孪生：深度学习绿视率 (GVI) 空间落位</h2>", unsafe_allow_html=True)


# ==========================================
# 1. 挂载数据 (底表 + GVI结果)
# ==========================================
@st.cache_data
def load_and_merge_data():
    base_path = "Changchun_Precise_Points.xlsx"
    gvi_path = "GVI_Results_Analysis.csv"
    if not os.path.exists(base_path): base_path = "../" + base_path
    if not os.path.exists(gvi_path): gvi_path = "../" + gvi_path

    try:
        df_base = pd.read_excel(base_path)
        df_gvi = pd.read_csv(gvi_path)
        # 提取点位 ID 并合并 GVI 数据
        df_gvi['ID'] = df_gvi['Folder'].str.replace('Point_', '').astype(int)
        df_gvi_avg = df_gvi.groupby('ID')['GVI'].mean().reset_index()
        df_merged = pd.merge(df_base, df_gvi_avg, on='ID', how='inner')
        return df_merged
    except:
        return None


df_merged = load_and_merge_data()

# ==========================================
# 2. 侧边栏控制
# ==========================================
with st.sidebar:
    st.markdown("#### 👁️ 视角控制")
    v_m = st.radio("模式", ["🦅 鸟瞰视角", "🗺️ 上帝视角", "🚶 漫游视角"], label_visibility="collapsed")
    st.markdown("---")
    st.markdown("#### 📊 图层参数")
    col_radius = st.slider("GVI 柱体半径 (米)", 5, 50, 15, 5)
    col_elev = st.slider("GVI 高度拉伸倍数", 1, 20, 8, 1)

# ==========================================
# 3. 构建 4:1 巨幕沙盘
# ==========================================
if df_merged is None or df_merged.empty:
    st.warning("⚠️ 尚未生成 GVI 分析数据，请先运行 CV 测度代码。")
else:
    c_lng, c_lat = df_merged['Lng'].mean(), df_merged['Lat'].mean()
    params = {"🦅 鸟瞰视角": (50, 15, 14.5), "🗺️ 上帝视角": (0, 0, 14), "🚶 漫游视角": (60, 45, 15.5)}
    v_pitch, v_bearing, v_zoom = params[v_m]

    layer_gvi = pdk.Layer(
        "ColumnLayer",
        data=df_merged,
        get_position=["Lng", "Lat"],
        get_elevation="GVI",
        elevation_scale=col_elev,
        radius=col_radius,
        get_fill_color="[255 - (GVI * 2.5), 200 + (GVI * 1.5), 100, 200]",  # 动态渐变绿
        pickable=True,
        auto_highlight=True,
        extruded=True
    )

    map_col, data_col = st.columns([4, 1])

    with map_col:
        r = pdk.Deck(
            layers=[layer_gvi],
            initial_view_state=pdk.ViewState(longitude=c_lng, latitude=c_lat, zoom=v_zoom, pitch=v_pitch,
                                             bearing=v_bearing),
            map_style="light",
            tooltip={"html": "<b>节点 ID:</b> {ID} <br/> <b>综合绿视率 (GVI):</b> {GVI}%",
                     "style": {"backgroundColor": "white", "color": "#333"}}
        )
        st.pydeck_chart(r, use_container_width=True)

    with data_col:
        st.markdown("### 📊 绿视率体检报告")
        st.markdown("---")
        with st.container():
            st.metric("🎯 成功解析街景节点", f"{len(df_merged)} 个")
        st.markdown("<br>", unsafe_allow_html=True)
        with st.container():
            st.metric("🌿 街区平均绿视率", f"{df_merged['GVI'].mean():.1f}%", "整体生态评价")
        st.markdown("<br>", unsafe_allow_html=True)
        with st.container():
            st.metric("👑 最高绿视率节点", f"{df_merged['GVI'].max():.1f}%",
                      f"位于节点 {df_merged.loc[df_merged['GVI'].idxmax(), 'ID']}")