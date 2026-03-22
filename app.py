import streamlit as st

# 🌟 强制隐藏侧边栏，设定宽屏模式
st.set_page_config(page_title="系统主页", layout="wide", initial_sidebar_state="collapsed")

# ==========================================
# 🎨 必须使用 unsafe_allow_html=True 的全局 CSS
# ==========================================
st.markdown("""
    <style>
    [data-testid="stHeader"] {display: none !important;}
    [data-testid="stSidebarNav"] {display: none !important;}
    [data-testid="stSidebar"] {display: none !important;}
    [data-testid="collapsedControl"] {display: none !important;}

    .block-container { padding-top: 1rem !important; padding-bottom: 2rem !important; max-width: 1400px; }

    a[data-testid="stPageLink-NavLink"] {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 8px !important;
        padding: 0.6rem 1rem !important;
        display: flex !important;
        justify-content: center !important;
        text-decoration: none !important;
        transition: all 0.3s ease !important;
    }

    a[data-testid="stPageLink-NavLink"]:hover {
        background-color: rgba(255, 255, 255, 0.25) !important;
        border-color: rgba(255, 255, 255, 0.5) !important;
        transform: translateY(-2px);
    }

    a[data-testid="stPageLink-NavLink"] p, a[data-testid="stPageLink-NavLink"] span {
        font-size: 18px !important;
        font-weight: 600 !important;
        color: #f8fafc !important;
        margin: 0 !important;
    }

    .stApp { background-color: #0f172a; }
    h1, h2, h3, h4, h5, label, .stMarkdown p { color: #f8fafc !important; }

    .glass-panel {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 40px;
        margin: 20px 0;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    }

    .module-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 25px;
        transition: all 0.3s ease;
        cursor: pointer;
        margin-bottom: 20px;
    }

    .module-card:hover {
        background: rgba(255, 255, 255, 0.08);
        border-color: rgba(255, 255, 255, 0.3);
        transform: translateY(-4px);
        box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.4);
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 🧭 顶部导航栏
# ==========================================
col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
with col1: st.page_link("app.py", label="🏠 系统主页", use_container_width=True)
with col2: st.page_link("pages/1_数字孪生沙盘.py", label="🌳 数字孪生沙盘", use_container_width=True)
with col3: st.page_link("pages/2_AIGC风貌管控.py", label="🎨 风貌管控", use_container_width=True)
with col4: st.page_link("pages/3_交通与人口.py", label="🚥 交通与人口", use_container_width=True)
with col5: st.page_link("pages/4_数据管理中心.py", label="📊 数据管理", use_container_width=True)
with col6: st.page_link("pages/5_LLM 情感分析.py", label="💬 情感分析", use_container_width=True)
with col7: st.page_link("pages/6_数据总览.py", label="📋 数据总览", use_container_width=True)

# ==========================================
# 🏠 顶部主视觉区
# ==========================================
st.markdown("""
<div class="glass-panel">
    <h1 style="text-align: center; font-size: 3rem; margin-bottom: 10px; font-weight: 800; text-shadow: 0 2px 4px rgba(0,0,0,0.5);">
        🏙️ 长春伪满皇宫周边街区：多模态微更新决策平台
    </h1>
    <p style="text-align: center; font-size: 1.2rem; color: #94a3b8 !important;">
        Multi-modal Micro-renewal Decision Support System for Historic Districts
    </p>
    <hr style="border-color: rgba(255,255,255,0.1); margin: 30px 0;">
    <p style="font-size: 1.15rem; line-height: 1.8; text-align: center;">
        欢迎进入系统！本平台整合了 <b>空间数字孪生 (Digital Twin)</b>、<b>计算机视觉 (CV)</b> 与 <b>生成式大模型 (AIGC)</b> 技术。<br>
        旨在通过多源城市数据的跨尺度耦合，为历史工业街区的城市设计与微更新提供数据支撑与空间决策辅助。
    </p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 🚀 中部：五大子系统入口
# ==========================================
st.markdown("### 🧭 核心子系统导览 (点击进入)")
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown('<div class="module-card">', unsafe_allow_html=True)
    st.image("https://images.unsplash.com/photo-1524661135-423995f22d0b?q=80&w=800&auto=format&fit=crop",
             use_container_width=True)
    st.markdown("#### 🌳 模块 1：数字孪生沙盘")
    st.markdown(
        "<p style='color:#cbd5e1 !important; font-size:0.95rem; height: 45px;'>基于 DeepLabV3 的大规模绿视率 (GVI) 自动化测度与 3D 高精度落位。</p>",
        unsafe_allow_html=True)
    st.page_link("pages/1_数字孪生沙盘.py", label="🚀 启动数字沙盘", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="module-card">', unsafe_allow_html=True)
    st.image("https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?q=80&w=800&auto=format&fit=crop",
             use_container_width=True)
    st.markdown("#### 🎨 模块 2：AIGC 风貌管控")
    st.markdown(
        "<p style='color:#cbd5e1 !important; font-size:0.95rem; height: 45px;'>基于 Stable Diffusion + ControlNet 的工业遗产风貌修缮与沉浸式推演。</p>",
        unsafe_allow_html=True)
    st.page_link("pages/2_AIGC 风貌管控.py", label="🎨 启动风貌管控", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with c3:
    st.markdown('<div class="module-card">', unsafe_allow_html=True)
    st.image("https://images.unsplash.com/photo-1519501025264-65ba15a82390?q=80&w=800&auto=format&fit=crop",
             use_container_width=True)
    st.markdown("#### 🚥 模块 3：交通与人口")
    st.markdown(
        "<p style='color:#cbd5e1 !important; font-size:0.95rem; height: 45px;'>商业活力潮汐聚类与多模态公共交通路网的高通量空间耦合分析。</p>",
        unsafe_allow_html=True)
    st.page_link("pages/3_交通与人口.py", label="🚀 启动交通探针", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
c4, c5 = st.columns(2)

with c4:
    st.markdown('<div class="module-card">', unsafe_allow_html=True)
    st.image("https://images.unsplash.com/photo-1551288049-bebda4e38f71?q=80&w=800&auto=format&fit=crop",
             use_container_width=True)
    st.markdown("#### 📊 模块 4：数据管理中心")
    st.markdown(
        "<p style='color:#cbd5e1 !important; font-size:0.95rem; height: 45px;'>多源数据融合管理、上传更新与可视化分析的一站式平台。</p>",
        unsafe_allow_html=True)
    st.page_link("pages/4_数据管理中心.py", label="🚀 进入数据中心", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with c5:
    st.markdown('<div class="module-card">', unsafe_allow_html=True)
    st.image("https://images.unsplash.com/photo-1529156069898-49953e39b3ac?q=80&w=800&auto=format&fit=crop",
             use_container_width=True)
    st.markdown("#### 💬 模块 5：LLM 情感分析")
    st.markdown(
        "<p style='color:#cbd5e1 !important; font-size:0.95rem; height: 45px;'>基于大模型的社会情感计算、舆情热力图与智能决策建议。</p>",
        unsafe_allow_html=True)
    st.page_link("pages/5_LLM 情感分析.py", label="🚀 启动情感分析", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
