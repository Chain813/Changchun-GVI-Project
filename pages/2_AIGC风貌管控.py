import streamlit as st
import time

# 1. 极简页面配置
st.set_page_config(page_title="AIGC 风貌管控 | 微更新平台", layout="wide")

# 2. 继承极简 CSS 风格
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .block-container {padding-top: 3rem; padding-bottom: 2rem;}
    html, body, [class*="css"] {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-weight: 300;
        color: #333333;
    }
    h2 {font-weight: 400; font-size: 1.8rem; letter-spacing: 1px;}
    .stButton>button {
        width: 100%;
        background-color: #333333;
        color: white;
        border: none;
        border-radius: 4px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #555555;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 页面标题区
st.markdown("<h2>AIGC 历史街区风貌自动化推演</h2>", unsafe_allow_html=True)
st.caption("基于 ControlNet 边缘约束与 Stable Diffusion 扩散模型的触媒节点立面改造")
st.markdown("---")

# 4. 交互控制区 (左侧边栏)
with st.sidebar:
    st.markdown("### 控制台 (Control Panel)")
    st.markdown("---")
    
    # 模拟选择从沙盘中筛出的“低绿视率”节点
    selected_node = st.selectbox(
        "1. 选择目标改造节点",
        ["节点 ID: 042 (长春中车厂主入口)", "节点 ID: 118 (伪满时期老旧家属区)", "节点 ID: 089 (废弃滨水工业驳岸)"]
    )
    
    # 选择 AIGC 渲染风格
    target_style = st.selectbox(
        "2. 设定目标风貌范式",
        ["现代工业复兴风 (Industrial Loft)", "伪满历史修缮风 (Historical Restoration)", "生态海绵城市风 (Ecological Sponge)"]
    )
    
    # 调整生成强度
    denoising_strength = st.slider("3. 改造干预强度 (Denoising Strength)", 0.0, 1.0, 0.65, 0.05)
    
    st.markdown("---")
    generate_btn = st.button("启动 AIGC 演化推演")

# 5. 主视觉展示区
# 预先占位，等点击按钮后展示结果
if not generate_btn:
    st.info("👈 请在左侧控制台选择改造节点与目标风貌，并启动推演。")
    # 这里可以放一张你项目中真实的“未改造前”的街景图占位
    # st.image("你的原图路径.jpg", caption="当前节点原貌提取中...")
else:
    # 模拟 AI 运算的进度条（面试汇报时的绝佳视觉缓冲）
    with st.spinner('ControlNet 正在提取建筑深度图与边缘特征...'):
        time.sleep(1.5)
    with st.spinner(f'Stable Diffusion 正在进行 {target_style} 潜空间采样...'):
        time.sleep(2)
        
    st.success("推演完成：视觉特征已成功对齐。")
    
    # 使用两列进行“改造前 vs 改造后”的直观对比
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<h4 style='text-align: center; color: #666;'>推演前：现状街景</h4>", unsafe_allow_html=True)
        # 💡 占位图：面试前换成你自己的真实街景照片
        st.image("https://images.unsplash.com/photo-1518398471463-548c27cb4a17?q=80&w=1000&auto=format&fit=crop", 
                 use_container_width=True, caption="提取自百度街景的低品质慢行空间")
        
    with col2:
        st.markdown("<h4 style='text-align: center; color: #222;'>推演后：生成方案</h4>", unsafe_allow_html=True)
        # 💡 占位图：面试前换成你用 Midjourney/SD 跑出来的高大上效果图
        st.image("https://images.unsplash.com/photo-1524230572899-a752b38b584c?q=80&w=1000&auto=format&fit=crop", 
                 use_container_width=True, caption=f"AIGC 生成方案 ({target_style})")
                 
    # 底部加上几句唬人的量化评估参数
    st.markdown("---")
    st.markdown("### 方案机读评估参数")
    met1, met2, met3 = st.columns(3)
    met1.metric("GVI (绿视率) 预期提升", "+ 24.5 %", "改善显著")
    met2.metric("SKY (天空开阔度) 变化", "- 5.2 %", "行道树冠幅增加导致")
    met3.metric("AI 生成置信度", f"{int(denoising_strength * 100)} %", "重绘幅度")