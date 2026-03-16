import streamlit as st

st.set_page_config(page_title="长春历史街区微更新决策平台", layout="wide")

# ==========================================
# 🌟 全局 UI 架构：贴顶导航与去侧边栏
# ==========================================
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    /* 🌟 修复：将顶部压缩回调到 3.5rem，避开系统透明护罩！ */
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
    </style>
    """, unsafe_allow_html=True)

# 顶部导航
col1, col2, col3, col4 = st.columns(4)
with col1: st.page_link("app.py", label="系统主页", use_container_width=True)
with col2: st.page_link("pages/1_数字孪生沙盘.py", label="数字孪生沙盘", use_container_width=True)
with col3: st.page_link("pages/2_AIGC风貌管控.py", label="风貌管控", use_container_width=True)
with col4: st.page_link("pages/3_交通与人口.py", label="交通与人口", use_container_width=True)
st.markdown("---")

# ==========================================
# 🏠 主页欢迎大屏
# ==========================================
st.title("🏙️ 长春中车厂历史街区：多模态微更新决策平台")
st.markdown("""
### 欢迎进入系统 (Welcome to the System)
本系统集成了 **空间数字孪生 (Digital Twin)**、**计算机视觉 (CV)** 与 **生成式大模型 (AIGC)** 技术。
请通过顶部导航栏进入各子模块：

* **🌳 模块 1：数字孪生沙盘** —— 基于 DeepLabV3 的大规模绿视率 (GVI) 自动化测度与三维空间落位。
* **🎨 模块 2：AIGC 风貌管控** —— 基于 Stable Diffusion + ControlNet 的历史风貌修缮与推演。
* **🚥 模块 3：交通与人口** —— 商业活力 POI 潮汐与多模态公共交通路网的耦合分析。
""")