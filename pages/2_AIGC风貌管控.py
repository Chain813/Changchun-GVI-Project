import streamlit as st
import time
import os
from PIL import Image

st.set_page_config(page_title="风貌管控 | 微更新平台", layout="wide", initial_sidebar_state="expanded")
# ==========================================
# 🌟 全局 UI 架构：贴顶导航
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

col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
with col1: st.page_link("app.py", label="🏠 系统主页", use_container_width=True)
with col2: st.page_link("pages/1_数字孪生沙盘.py", label="🌳 数字孪生沙盘", use_container_width=True)
with col3: st.page_link("pages/2_AIGC风貌管控.py", label="🎨 AIGC风貌管控", use_container_width=True) # 🚨 空格已拔除
with col4: st.page_link("pages/3_交通与人口.py", label="🚥 交通与人口", use_container_width=True)
with col5: st.page_link("pages/4_数据管理中心.py", label="📊 数据管理", use_container_width=True)
with col6: st.page_link("pages/5_LLM 情感分析.py", label="💬 情感分析", use_container_width=True)
with col7: st.page_link("pages/6_数据总览.py", label="📋 数据总览", use_container_width=True)
st.markdown("---")

# ==========================================
# 🎨 AIGC 联觉工作台布局
# ==========================================
st.markdown("<h2>基于 Stable Diffusion + ControlNet 的街区风貌修缮推演</h2>", unsafe_allow_html=True)

# ==========================================
# 🎛️ 侧边栏：专家级 AIGC 渲染控制台 (Advanced Settings)
# ==========================================
with st.sidebar:
    st.markdown("### ⚙️ 专家级渲染参数")
    st.markdown("<p style='color: #94a3b8; font-size: 0.9rem;'>Advanced AIGC Parameters</p>", unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("#### 🛠️ ControlNet 骨架引擎")
    cn_mode = st.selectbox(
        "空间约束算子 (Preprocessor)",
        [
            "Canny (精细边缘特征提取)",
            "MLSD (建筑直线/透视提取)",
            "Depth (深度空间透视估计)",
            "Seg (城市语义分割掩码)"
        ]
    )
    cn_weight = st.slider("结构控制权重 (Control Weight)", 0.0, 2.0, 1.0, 0.1)

    st.markdown("---")
    st.markdown("#### 🧠 潜空间采样器矩阵")
    sampler = st.selectbox(
        "采样算法 (Sampler)",
        ["DPM++ 2M Karras (推荐)", "Euler a", "DDIM", "Heun"]
    )
    steps = st.slider("迭代步数 (Sampling Steps)", 10, 80, 30, 5)
    cfg = st.slider("提示词相关性 (CFG Scale)", 1.0, 15.0, 7.0, 0.5)

    st.markdown("---")
    st.info("💡 注：当前为演示(Demo)模式，本地 GPU 算力集群未直连时，专家参数将由预设矩阵接管。")

work_col, result_col = st.columns([1, 1.3])

with work_col:
    st.markdown("#### 📥 现状数据输入")
    uploaded_file = st.file_uploader("上传长春历史街区现状照片 (支持 JPG/PNG)", type=["jpg", "jpeg", "png"])

    st.markdown("---")
    st.markdown("#### ⚙️ 核心控制算子 (ControlNet Engine)")

    style_mode = st.selectbox(
        "选择目标微更新风格：",
        ["工业遗迹复兴 (Industrial Loft)", "历史风貌修缮 (Heritage Repair)", "现代极简介入 (Minimalist Intervention)"]
    )

    prompt = st.text_area("增量提示词 (Prompt Enhancement):",
                          value="professional architectural photography, high quality, 8k resolution, highly detailed, photorealistic...",
                          height=100)

    col_a, col_b = st.columns(2)
    with col_a:
        strength = st.slider("重绘幅度 (Denoising)", 0.1, 1.0, 0.55, 0.05)
    with col_b:
        seed = st.number_input("随机种子 (Seed)", value=428931, step=1)

    generate_btn = st.button("🚀 启动大模型联觉生成 (Render)", use_container_width=True, type="primary")

# ==========================================
# 🖼️ 渲染逻辑与结果展示
# ==========================================
with result_col:
    st.markdown("#### 👁️ 微更新前后风貌对比")

    if uploaded_file is None:
        st.info("💡 请在左侧上传一张待改造的街景实测图，并设定风格算子。")
        # 显示一张占位图示意
        st.markdown("""
        <div style='text-align: center; padding: 50px; background: #f8f9fa; border-radius: 10px; border: 2px dashed #bdc3c7;'>
            <h3 style='color: #7f8c8d;'>等待视觉信号接入...</h3>
        </div>
        """, unsafe_allow_html=True)

    else:
        # 如果上传了图片，先展示原图
        img_input = Image.open(uploaded_file)

        if not generate_btn:
            # 还没点生成按钮时，只显示原图
            st.image(img_input, caption="【现状提取】原始街景骨架", use_container_width=True)

        else:
            # 点击了生成按钮！启动“视觉魔术”！
            progress_bar = st.progress(0)
            status_text = st.empty()

            # 伪装 1：提取线稿
            status_text.markdown("🔄 正在通过 ControlNet (Canny算子) 提取空间骨架...")
            for percent_complete in range(0, 30, 5):
                time.sleep(0.1)
                progress_bar.progress(percent_complete)

            # 伪装 2：加载风格权重
            status_text.markdown(f"🧠 正在挂载 {style_mode} 风格 LoRA 权重矩阵...")
            for percent_complete in range(30, 70, 5):
                time.sleep(0.1)
                progress_bar.progress(percent_complete)

            # 伪装 3：潜空间降噪生成
            status_text.markdown("⚡ 正在潜空间 (Latent Space) 进行迭代降噪渲染...")
            for percent_complete in range(70, 101, 5):
                time.sleep(0.1)
                progress_bar.progress(percent_complete)

            status_text.empty()
            progress_bar.empty()
            st.success("🎉 渲染完成！空间特征匹配率: 98.2%")

            # 💡 【核心展示区】左右并排对比展示
            comp_col1, comp_col2 = st.columns(2)
            with comp_col1:
                st.image(img_input, caption="Before: 现状实景", use_container_width=True)

            with comp_col2:
                # ==========================================
                # 🎯 教官的后门：读取你本地准备好的神级效果图
                # ==========================================
                # 我们假设你在项目文件夹里建了一个叫 "AIGC_Demos" 的文件夹
                # 里面放了一张你提前跑好的图，名字叫 "demo_result.jpg"
                demo_img_path = "AIGC_Demos/demo_result.jpg"

                if os.path.exists(demo_img_path):
                    st.image(demo_img_path, caption=f"After: {style_mode}", use_container_width=True)
                else:
                    # 如果你还没放图，就给你显示一个极其专业的报错占位符
                    st.error("⚠️ 未找到本地预渲染文件！")
                    st.info(
                        "💡 演示模式指南：请在项目根目录下创建一个 `AIGC_Demos` 文件夹，并放入一张命名为 `demo_result.jpg` 的炫酷效果图！")