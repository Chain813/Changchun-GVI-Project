import streamlit as st
import pandas as pd
import os
import numpy as np
from PIL import Image
import base64
from io import BytesIO

st.set_page_config(page_title="AIGC 风貌管控", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    [data-testid="stHeader"] {display: none !important;}
    [data-testid="stSidebarNav"] {display: none !important;}
    [data-testid="stSidebar"] { display: flex !important; visibility: visible !important; transition: transform 0.3s ease !important; }
    .sidebar-hidden [data-testid="stSidebar"] { display: none !important; }
    .block-container { padding-top: 1rem !important; padding-bottom: 0rem !important;}
    a[data-testid="stPageLink-NavLink"] {
        background-color: rgba(255, 255, 255, 0.1) !important; border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 8px !important; padding: 0.6rem 1rem !important; display: flex !important; justify-content: center !important;
        text-decoration: none !important; transition: all 0.3s ease !important;
    }
    a[data-testid="stPageLink-NavLink"]:hover { background-color: rgba(255, 255, 255, 0.25) !important; border-color: rgba(255, 255, 255, 0.5) !important; transform: translateY(-2px); }
    a[data-testid="stPageLink-NavLink"] p, a[data-testid="stPageLink-NavLink"] span { font-size: 18px !important; font-weight: 600 !important; color: #f8fafc !important; margin: 0 !important; }
    .stApp { background-color: #0f172a; }
    h1, h2, h3, h4, h5, label, .stMarkdown p { color: #f8fafc !important; }
    [data-testid="stSidebar"] { background-color: #1e293b !important; border-right: 1px solid #334155 !important; }
    [data-testid="stSidebar"] * { color: #f8fafc !important; }
    div[data-baseweb="select"] > div, textarea, input, section[data-testid="stFileUploader"] { background-color: #1e293b !important; color: #f8fafc !important; border: 1px solid #475569 !important; }
    [data-testid="stMetricValue"], [data-testid="stMetricLabel"] { color: #f8fafc !important; }
    .upload-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0.02) 100%);
        border: 2px dashed rgba(255, 255, 255, 0.3);
        border-radius: 16px; padding: 80px 40px; text-align: center;
        cursor: pointer; transition: all 0.3s ease;
        margin: 40px 0;
    }
    .upload-card:hover {
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
        border-color: rgba(255, 255, 255, 0.6);
        transform: translateY(-4px);
        box-shadow: 0 8px 32px 0 rgba(255, 255, 255, 0.1);
    }
    .upload-icon { font-size: 80px; margin-bottom: 20px; }
    .upload-title { font-size: 28px; font-weight: 700; color: #f8fafc; margin-bottom: 10px; }
    .upload-desc { font-size: 16px; color: #94a3b8; line-height: 1.8; }
    </style>
    """, unsafe_allow_html=True)

col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
with col1: st.page_link("app.py", label="🏠 系统主页", use_container_width=True)
with col2: st.page_link("pages/1_数字孪生沙盘.py", label="🌳 数字孪生沙盘", use_container_width=True)
with col3: st.page_link("pages/2_AIGC 风貌管控.py", label="🎨 风貌管控", use_container_width=True)
with col4: st.page_link("pages/3_交通与人口.py", label="🚥 交通与人口", use_container_width=True)
with col5: st.page_link("pages/4_数据管理中心.py", label="📊 数据管理", use_container_width=True)
with col6: st.page_link("pages/5_LLM 情感分析.py", label="💬 情感分析", use_container_width=True)
with col7: st.page_link("pages/6_数据总览.py", label="📋 数据总览", use_container_width=True)
st.markdown("---")
st.markdown("<h2>工业遗产风貌 AI 重塑与沉浸式方案推演</h2>", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("#### 🖼️ 建筑类型选择")
    building_type = st.selectbox("选择建筑风貌类型:", [
        "🏭 工业厂房", "🏢 历史建筑", "🏘️ 老旧住宅", "🏪 商业街区"
    ])
    
    st.markdown("#### 🎭 风格迁移模式")
    style_mode = st.radio("生成风格:", [
        "🏛️ 工业遗产保护", "🌿 生态绿色融合", "🎨 现代艺术创意", "🏮 历史文化复兴"
    ], label_visibility="collapsed")
    
    st.markdown("---")
    st.markdown("#### ⚙️ 生成参数")
    guidance_scale = st.slider("提示词相关性 (Guidance Scale)", 1.0, 20.0, 7.5, 0.5)
    num_inference = st.slider("推理步数", 10, 100, 50, 5)
    strength = st.slider("重绘强度 (Strength)", 0.1, 1.0, 0.75, 0.05)

style_prompts = {
    "🏛️ 工业遗产保护": "industrial heritage preservation, red brick and steel structure, historical architecture restoration, high quality, detailed",
    "🌿 生态绿色融合": "green architecture, vertical gardens, eco-friendly design, sustainable building, nature integration, modern",
    "🎨 现代艺术创意": "contemporary art space, creative design, modern architecture, glass and metal, artistic facade",
    "🏮 历史文化复兴": "traditional chinese architecture, cultural heritage, historical style, ornate details, cultural revival"
}

building_contexts = {
    "🏭 工业厂房": "old factory building, industrial structure",
    "🏢 历史建筑": "historical building, heritage site",
    "🏘️ 老旧住宅": "old residential building, apartment complex",
    "🏪 商业街区": "commercial street, retail district"
}

st.markdown("### 📤 上传现状照片")

uploaded_file = st.file_uploader("选择图片文件", type=["jpg", "jpeg", "png"], label_visibility="collapsed")

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    img_array = np.array(image)
    
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 📸 现状照片")
        st.image(image, use_container_width=True)
        st.markdown(f"**尺寸:** {image.size[0]} × {image.size[1]} px")
    
    with col2:
        st.markdown("#### 🎨 AI 生成方案 (模拟)")
        placeholder = st.empty()
        with placeholder.container():
            st.info("""
            ### 🔮 AIGC 生成引擎状态
            
            **当前配置:**
            - 模型：Stable Diffusion XL + ControlNet
            - 风格：""" + style_mode + """
            - 建筑类型：""" + building_type + """
            - Guidance Scale: """ + str(guidance_scale) + """
            - 推理步数：""" + str(num_inference) + """
            - 重绘强度：""" + str(strength) + """
            
            **提示词工程:**
            ```
            Base: """ + building_contexts[building_type] + """
            Style: """ + style_prompts[style_mode] + """
            Control: Canny edge detection + Depth map
            ```
            
            💡 **提示**: 实际部署需连接 Stable Diffusion API 或本地推理服务
            """)
        
        if st.button("🚀 开始生成设计方案", use_container_width=True):
            with st.spinner('⏳ 正在调用 AIGC 引擎生成方案...'):
                progress_bar = st.progress(0)
                for i in range(100):
                    import time
                    time.sleep(0.02)
                    progress_bar.progress(i + 1)
                
                st.success("✅ 方案生成完成!")
                st.markdown("""
                ### 🎯 生成结果说明
                
                基于 ControlNet 的精确轮廓控制，AI 已根据现状建筑结构生成风貌重塑方案:
                
                **设计要点:**
                - ✅ 保留原有建筑主体结构
                - ✅ 立面材质更新为""" + ("红砖工业风" if "工业遗产" in style_mode else "生态绿植墙" if "生态" in style_mode else "现代玻璃幕墙" if "现代艺术" in style_mode else "传统中式元素") + """
                - ✅ 色彩体系协调统一
                - ✅ 细部构造精致化处理
                
                **下一步:**
                1. 下载生成结果
                2. 导出多方案对比图
                3. 生成技术经济指标表
                """)

st.markdown("---")
st.markdown("### 🏛️ 历史工业遗产 AI 重塑案例库")

case_studies = pd.DataFrame({
    "项目名称": ["中车长春老厂房改造", "伪满皇宫缓冲区整治", "宽城区工业遗产更新"],
    "原风貌": ["红砖厂房", "历史街区", "废弃厂区"],
    "改造风格": ["工业遗产公园", "文化保护区", "文创产业园"],
    "AI 匹配度": ["92%", "88%", "95%"],
    "技术路线": ["SD+ControlNet", "SD+LoRA", "SD+Inpainting"]
})

st.dataframe(case_studies, use_container_width=True, hide_index=True)

st.markdown("---")
st.markdown("### 🧠 技术架构说明")

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    #### 🎨 生成模型
    - **Stable Diffusion XL**
    - ControlNet (Canny/Depth)
    - LoRA 风格微调
    - IP-Adapter 参考控制
    """)
with col2:
    st.markdown("""
    #### 🖼️ 图像处理
    - 边缘检测 (Canny)
    - 深度图估计 (MiDaS)
    - 语义分割 (DeepLabV3+)
    - 图像融合 (Blending)
    """)
with col3:
    st.markdown("""
    #### 📊 后处理
    - 多方案对比
    - 指标自动计算
    - 报告生成
    - 成果导出
    """)
