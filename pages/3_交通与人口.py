import streamlit as st
import pandas as pd
import pydeck as pdk
import os

st.set_page_config(page_title="交通与人口 | 微更新平台", layout="wide")

# ==========================================
# 🌟 UI 架构：巨幕地图与 3.5rem 安全贴顶
# ==========================================
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    .block-container {
        padding-top: 3.5rem !important; 
        padding-bottom: 0rem !important;
    }
    button[data-testid="stBaseButton-secondary"] {
        height: 3rem !important;
        padding: 0.5rem 1rem !important;
        border-radius: 8px !important;
    }
    div[data-testid="stHorizontalBlock"] a {
        font-size: 18px !important;
        font-weight: 600 !important;
        text-decoration: none !important;
    }
    [data-testid="stDeckGlJsonChart"] {
        height: 75vh !important; 
        min-height: 650px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 顶部导航
col1, col2, col3, col4 = st.columns(4)
with col1: st.page_link("app.py", label="系统主页", use_container_width=True)
with col2: st.page_link("pages/1_数字孪生沙盘.py", label="数字孪生沙盘", use_container_width=True)
with col3: st.page_link("pages/2_AIGC风貌管控.py", label="风貌管控", use_container_width=True)
with col4: st.page_link("pages/3_交通与人口.py", label="交通与人口", use_container_width=True)
st.markdown("---")

st.markdown("<h2>历史街区交通枢纽与商业活力耦合分析</h2>", unsafe_allow_html=True)


# ==========================================
# 1. 数据加载与底层格式统一
# ==========================================
@st.cache_data
def load_data(filename):
    if not os.path.exists(filename):
        filename = "../" + filename
    return pd.read_csv(filename) if os.path.exists(filename) else None


@st.cache_data
def load_base_points():
    f = "Changchun_Precise_Points.xlsx"
    if not os.path.exists(f): f = "../" + f
    return pd.read_excel(f) if os.path.exists(f) else None


df_poi = load_data("Changchun_POI_Real.csv")
df_traffic = load_data("Changchun_Traffic_Real.csv")
df_base = load_base_points()

# 🌟 核心升级：强行让 POI 数据和 Traffic 数据具备相同的字段，完美适配雷达！
if df_poi is not None and 'Type' in df_poi.columns:
    df_poi['Category'] = df_poi['Type']  # 把 Type 映射成 Category

if df_traffic is not None:
    def classify_and_color(row):
        text = str(row.get('Name', '')) + str(row.get('Type', ''))
        if '地铁' in text or '轻轨' in text:
            return pd.Series(['轻轨站或地铁站', [231, 76, 60, 220]])
        elif '铁路' in text or '火车站' in text or '长春站' in text:
            return pd.Series(['铁路及铁路站', [142, 68, 173, 220]])
        elif '公交' in text or '客运' in text:
            return pd.Series(['公交站', [46, 204, 113, 220]])
        elif '停车' in text:
            return pd.Series(['停车场', [52, 152, 219, 220]])
        else:
            return pd.Series(['其他交通设施', [149, 165, 166, 200]])


    df_traffic[['Category', 'Color']] = df_traffic.apply(classify_and_color, axis=1)

# ==========================================
# 2. 侧边栏控制台 (新增微观 POI 开关)
# ==========================================
with st.sidebar:
    st.markdown("#### 👁️ 视角控制")
    v_m = st.radio("模式", ["🦅 鸟瞰视角", "🗺️ 上帝视角", "🚶 漫游视角"], label_visibility="collapsed")
    st.markdown("---")

    st.markdown("#### 📊 商业活力图层")
    show_hex = st.checkbox("🔮 开启宏观蜂窝柱 (密度聚合)", value=True)
    if show_hex:
        h_r = st.slider("蜂窝网格半径 (米)", 20, 150, 50, 10)
        e_s = st.slider("活力高度拉伸倍数", 0.5, 10.0, 3.0, 0.5)

    # 🌟 核心升级：增加微观 POI 散点开关
    show_poi_raw = st.checkbox("🔍 透视微观商铺点 (显示名称)", value=False)

    st.markdown("---")
    show_traffic = st.checkbox("🚥 开启交通枢纽脉冲点", value=True)
    if show_traffic and df_traffic is not None:
        t_r = st.slider("交通节点光晕半径", 5, 60, 15, 5)

# ==========================================
# 3. 构建 3D 复合图层
# ==========================================
c_lng, c_lat = (df_base['Lng'].mean(), df_base['Lat'].mean()) if df_base is not None else (125.315, 43.902)
params = {"🦅 鸟瞰视角": (50, 15, 14.5), "🗺️ 上帝视角": (0, 0, 14), "🚶 漫游视角": (60, 45, 15.5)}
v_pitch, v_bearing, v_zoom = params[v_m]

layers_to_render = []

# 图层 1：宏观蜂窝柱 (没有名字，只有高度)
if df_poi is not None and show_hex:
    layer_hex = pdk.Layer(
        "HexagonLayer", data=df_poi, get_position=["Lng", "Lat"], radius=h_r,
        elevation_scale=e_s, elevation_range=[0, 300], extruded=True, coverage=0.88,
        wireframe=True, opacity=0.75, pickable=True,  # 降低一点透明度，方便看底下的点
        color_range=[[241, 238, 246, 180], [208, 209, 230, 180], [166, 189, 219, 180], [116, 169, 207, 180],
                     [43, 140, 190, 180], [4, 90, 141, 180]]
    )
    layers_to_render.append(layer_hex)

# 🌟 图层 2：微观商铺散点 (赛博朋克高亮版！)
if df_poi is not None and show_poi_raw:
    layer_poi_raw = pdk.Layer(
        "ScatterplotLayer", data=df_poi, get_position=["Lng", "Lat"],
        get_radius=12,  # 稍微放大一点点半径，增强存在感
        get_fill_color=[255, 20, 147, 240],   # 🔴 极度显眼的荧光洋红 (Deep Pink)
        get_line_color=[255, 255, 255, 255],  # ⚪ 纯白高亮描边，让点位更加锐利
        lineWidthMinPixels=2, pickable=True, auto_highlight=True
    )
    layers_to_render.append(layer_poi_raw)

# 图层 3：交通脉冲点
if df_traffic is not None and show_traffic:
    layer_traffic = pdk.Layer(
        "ScatterplotLayer", data=df_traffic, get_position=["Lng", "Lat"], get_radius=t_r,
        get_fill_color="Color", get_line_color=[255, 255, 255, 200], lineWidthMinPixels=1, pickable=True,
        auto_highlight=True
    )
    layers_to_render.append(layer_traffic)

# ==========================================
# 4. 🚀 大一统雷达探针 (完全兼容三种图层)
# ==========================================
radar_tooltip = {
    "html": """
    <div style="font-family: 'Helvetica Neue', Arial, sans-serif; padding: 5px;">
        <h4 style="margin: 0 0 8px 0; color: #2c3e50; font-size: 14px;">📡 空间雷达探针扫描</h4>
        <div style="font-size: 13px; line-height: 1.6; color: #34495e;">
            <span style="color: #7f8c8d;">节点名称 (Name)：</span><b>{Name}</b><br/>
            <span style="color: #7f8c8d;">节点业态 (Category)：</span><b style="color: #8e44ad;">{Category}</b><br/>
            <span style="color: #7f8c8d;">密度聚合量 (Density)：</span><b style="color: #e74c3c; font-size: 16px;">{elevationValue}</b>
        </div>
    </div>
    """,
    "style": {"backgroundColor": "rgba(255, 255, 255, 0.95)", "border": "1px solid #bdc3c7", "borderRadius": "8px"}
}

if not layers_to_render:
    st.info("💡 请在左侧边栏至少开启一个数据图层。")
else:
    map_col, data_col = st.columns([4, 1])

    with map_col:
        r = pdk.Deck(layers=layers_to_render,
                     initial_view_state=pdk.ViewState(longitude=c_lng, latitude=c_lat, zoom=v_zoom, pitch=v_pitch,
                                                      bearing=v_bearing), map_style="light", tooltip=radar_tooltip)
        st.pydeck_chart(r, use_container_width=True)

    with data_col:
        st.markdown("### 📊 空间特征洞察")
        st.markdown("---")
        if df_traffic is not None and df_poi is not None:
            counts = df_traffic['Category'].value_counts()
            with st.container(): st.metric("🛍️ 活跃商业 POI", f"{len(df_poi)} 个", "活力底座")
            st.markdown("<br>", unsafe_allow_html=True)
            with st.container(): st.metric("🚌 公交网络节点", f"{counts.get('公交站', 0)} 个", "高频覆盖")
            st.markdown("<br>", unsafe_allow_html=True)
            with st.container(): st.metric("🚇 轨交/铁路枢纽",
                                           f"{counts.get('轻轨站或地铁站', 0) + counts.get('铁路及铁路站', 0)} 个",
                                           "城市大动脉")
            st.markdown("<br>", unsafe_allow_html=True)
            with st.container(): st.metric("🅿️ 静态停车设施", f"{counts.get('停车场', 0)} 个", "机动车承载力")