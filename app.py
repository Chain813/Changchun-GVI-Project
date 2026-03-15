import streamlit as st

st.set_page_config(
    page_title="城市微更新智能决策平台",
    layout="centered",
    initial_sidebar_state="expanded"
)

# 极致纯净的 CSS 排版
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .block-container {padding-top: 4rem; padding-bottom: 2rem; max-width: 800px;}
    html, body, [class*="css"]  {
        font-family: 'Helvetica Neue', Helvetica, Arial, 'Microsoft YaHei', sans-serif;
        font-weight: 300;
        color: #333333;
    }
    h1 {font-weight: 400; font-size: 2.2rem; letter-spacing: 2px; margin-bottom: 0.5rem;}
    h3 {font-weight: 300; font-size: 1.2rem; color: #666666; margin-bottom: 2rem;}
    hr {margin-top: 2rem; margin-bottom: 2rem; border-top: 1px solid #EAEAEA;}
    </style>
    """, unsafe_allow_html=True)

st.sidebar.markdown("### 🧭 系统导航")
st.sidebar.caption("注：点击下方链接进入相应模块")

st.markdown("<h1>长春中车街区 | 城市微更新决策平台</h1>", unsafe_allow_html=True)
st.markdown("<h3>AI 赋能下的历史街区空间品质提升与多模态感知研究</h3>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

st.markdown("""
本平台旨在打破传统城乡规划的主观经验壁垒，引入计算机视觉 (CV)、生成式人工智能 (AIGC) 与多源城市大数据。
通过构建定量化、可视化的多模态感知矩阵，为历史街区的空间微更新、风貌管控与活力激发提供科学的决策支持。
""")
st.write("")

# 🌟 核心改造：使用 st.page_link 让模块可以直接点击跳转！
col1, col2 = st.columns(2)

with col1:
    st.page_link("pages/1_数字孪生沙盘.py", label="**模块 01 / 数字孪生沙盘**", icon="📍")
    st.caption("基于 DeepLabV3 的街区绿视率连续空间测度与 3D 可视化诊断，精准定位生态脆弱点。")
    st.write("")
    st.page_link("pages/3_交通与人口.py", label="**模块 03 / 交通与人口分布**", icon="🚶")
    st.caption("融合多源 POI 与 LBS 数据，剖析历史街区的活力潮汐与慢行网络空间阻抗。")

with col2:
    st.page_link("pages/2_AIGC风貌管控.py", label="**模块 02 / AIGC 风貌管控**", icon="🎨")
    st.caption("基于 ControlNet 与 Stable Diffusion 模型，自动化推演工业风或伪满风的立面改造。")
    st.write("")
    st.markdown("**📊 模块 04 / 综合效益评估**")
    st.caption("*(模型标定与研发中)* 微更新方案的碳汇测算与社会经济效益预估。")

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<div style='text-align: center; color: #999999; font-size: 0.8rem;'>© 2026 深圳大学建筑与城市规划学院 准研究生研发构建</div>", unsafe_allow_html=True)