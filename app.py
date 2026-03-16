import streamlit as st

# 🌟 强制隐藏侧边栏，设定宽屏模式
st.set_page_config(page_title="系统主页", layout="wide", initial_sidebar_state="collapsed")

# ==========================================
# 🎨 必须带 unsafe_allow_html=True 的全局 CSS
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

    .stApp {
        background-color: #0f172a;
        background-image: linear-gradient(rgba(15, 23, 42, 0.85), rgba(15, 23, 42, 0.95)), 
                          url("https://images.unsplash.com/photo-1519999482648-25049ddd37b1?q=80&w=2500&auto=format&fit=crop");
        background-size: cover; background-position: center; background-attachment: fixed;
    }
    h1, h2, h3, h4, h5, p, li, span, label { color: #f8fafc !important; }

    .glass-panel {
        background: rgba(15, 23, 42, 0.6); backdrop-filter: blur(15px); -webkit-backdrop-filter: blur(15px);
        border-radius: 16px; border: 1px solid rgba(255, 255, 255, 0.15);
        padding: 40px; margin-top: 20px; margin-bottom: 40px; box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
    }

    .module-card {
        background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px; padding: 15px; height: 100%; transition: transform 0.3s ease, background 0.3s ease;
    }
    .module-card:hover {
        transform: translateY(-8px); background: rgba(255, 255, 255, 0.08); border-color: rgba(255, 255, 255, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 🧭 顶部导航栏
# ==========================================
col1, col2, col3, col4 = st.columns(4)
with col1: st.page_link("app.py", label="🏠 系统主页", use_container_width=True)
with col2: st.page_link("pages/1_数字孪生沙盘.py", label="🌳 数字孪生沙盘", use_container_width=True)
with col3: st.page_link("pages/2_AIGC风貌管控.py", label="🎨 风貌管控", use_container_width=True)
with col4: st.page_link("pages/3_交通与人口.py", label="🚥 交通与人口", use_container_width=True)

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
# 🚀 中部：三大子系统入口
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
    st.page_link("pages/2_AIGC风貌管控.py", label="🚀 启动大模型引擎", use_container_width=True)
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

# ==========================================
# 🧬 底部：底层技术架构与全链条路线图 (暴力零缩进修复版)
# ==========================================
st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<div class="glass-panel" style="padding: 30px 40px;">
<h2 style="text-align: center; font-weight: 800; margin-bottom: 5px;">🛠️ 系统底层架构与技术路线</h2>
<p style="text-align: center; color: #94a3b8 !important; font-size: 1rem; margin-bottom: 30px;">Full-Chain Technical Roadmap: From Data Fusion to AI Governance</p>

<div style="border-left: 3px solid #3b82f6; padding-left: 20px; margin-bottom: 25px;">
<h4 style="color: #60a5fa !important; margin-bottom: 10px;">📌 阶段一：多源异构数据底座 (Data Fusion)</h4>
<ul style="color: #cbd5e1; line-height: 1.8;">
<li><b>物理空间数据：</b>整合 OSM 路网、伪满皇宫周边街区建筑拓扑与 POI 数据。</li>
<li><b>视觉感知数据：</b>接入已采集的百度街景图，为后续 CV 识别做好准备。</li>
<li><b>社会情感数据：</b>爬取微博、小红书及大众点评中带有“中车厂区”和“宽城区工业遗产”等关键词的文本。</li>
</ul>
</div>

<div style="border-left: 3px solid #10b981; padding-left: 20px; margin-bottom: 25px;">
<h4 style="color: #34d399 !important; margin-bottom: 10px;">🔬 阶段二：多维度城市空间评估 (Evaluation)</h4>
<ul style="color: #cbd5e1; line-height: 1.8;">
<li><b>视觉感知 (CV)：</b>运用 DeepLabV3+ 语义分割技术，计算绿视率 (GVI)、天空开阔度 (SVF) 及围合度等指标。</li>
<li><b>社会情感 (NLP/LLM)：</b>利用大语言模型 (如 GPT-4o) 进行情感极性分析，识别文本中的“负面情绪点”与“潜在价值点”，并通过热力图进行空间落点识别“吐槽集中区”。</li>
<li><b>空间逻辑 (Space Syntax)：</b>借助 Depthmap+ 或 sDNA 构建穿行度与整合度模型，评估巨大厂区尺度是否导致了城市毛细血管的“梗阻”。</li>
</ul>
</div>

<div style="border-left: 3px solid #f59e0b; padding-left: 20px; margin-bottom: 25px;">
<h4 style="color: #fbbf24 !important; margin-bottom: 10px;">♟️ 阶段三：路网重构与功能置换 (Strategy)</h4>
<ul style="color: #cbd5e1; line-height: 1.8;">
<li><b>路网重构：</b>基于空间句法的高穿行度分析，识别需要打通或加密的断头路，以优化厂区与周边的路网联动。</li>
<li><b>功能置换决策：</b>将大模型的“高情感需求”结论与“空间低可达性”点位结合，提出决策建议，例如将边缘低整合度的厂房改造为创客空间或工业博物馆。</li>
</ul>
</div>

<div style="border-left: 3px solid #ec4899; padding-left: 20px; margin-bottom: 25px;">
<h4 style="color: #f472b6 !important; margin-bottom: 10px;">🎨 阶段四：城市更新风貌重塑 (AIGC Design)</h4>
<ul style="color: #cbd5e1; line-height: 1.8;">
<li><b>精准视觉生成：</b>利用 Stable Diffusion + ControlNet 提取厂房现状轮廓，确保生成方案贴合现状物理结构。</li>
<li><b>多方案推演：</b>输入定制化提示词 (如工业遗产重塑、玻璃与生锈钢铁的融合)，输出多方案的风貌重塑对比图，用于展示功能置换后的视觉效果。</li>
</ul>
</div>

<div style="border-left: 3px solid #8b5cf6; padding-left: 20px;">
<h4 style="color: #a78bfa !important; margin-bottom: 10px;">🤖 阶段五：LLM 模拟社会协同治理 (Governance Simulation)</h4>
<ul style="color: #cbd5e1; line-height: 1.8;">
<li><b>多智能体博弈 (Multi-Agent)：</b>定义代表“政府规划师”、“中车资产方”、“周边居民”与“文创企业”等多个 LLM 智能体角色。</li>
<li><b>冲突分析与修正：</b>将重构与置换方案输入进行模拟博弈，识别实施过程中可能的阻碍 (如噪音担忧、安保问题)，并输出协同修正建议。</li>
</ul>
</div>
</div>
""", unsafe_allow_html=True)