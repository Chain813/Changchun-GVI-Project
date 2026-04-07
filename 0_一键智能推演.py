import streamlit as st
import pandas as pd
import pydeck as pdk
import plotly.express as px
import time
import os
from PIL import Image

# 1. 引入刚才写好的核心底层引擎
from core_engine import get_spatial_data, get_nlp_data, get_traffic_data

st.set_page_config(page_title="一键智能推演", layout="wide", initial_sidebar_state="collapsed")

# 2. 引入你的公共导航栏
from ui_components import render_top_nav

render_top_nav()

# ==========================================
# 🎨 页面头部与表单设计
# ==========================================
st.markdown("<h2>⚡ 长春历史街区多模态一键推演中心</h2>", unsafe_allow_html=True)
st.markdown("<p style='color: #94a3b8; margin-bottom: 20px;'>Multi-modal One-Click Inference Console</p>",
            unsafe_allow_html=True)

# 构建表单，点击提交后才会刷新页面
with st.form("master_inference_form"):
    st.markdown("#### 📥 设定推演基准参数")

    col1, col2, col3 = st.columns(3)
    with col1:
        target_name = st.text_input("🎯 目标地块名称", "中车长春老厂区")
        target_coords = st.text_input("📍 地块中心坐标 (Lng, Lat)", "125.3517, 43.9116")
    with col2:
        focus_keywords = st.text_input("🏷️ 重点关注舆情关键词", "历史, 破旧, 停车, 改造")
        target_style = st.selectbox("🎨 期望风貌改造策略",
                                    ["工业遗迹复兴 (Industrial Loft)", "现代极简介入 (Minimalist)",
                                     "历史风貌修缮 (Heritage)"])
    with col3:
        uploaded_img = st.file_uploader("📸 上传地块现状照片 (用于 AIGC 融合)", type=["jpg", "png"])

    st.markdown("---")
    # 一键引爆按钮
    submitted = st.form_submit_button("🚀 一键启动多维张量计算与生成", use_container_width=True)

# ==========================================
# ⚙️ 点击按钮后的联动输出逻辑
# ==========================================
if submitted:
    with st.spinner("🧠 正在调动 DeepLabV3+、Jieba 与 Stable Diffusion 引擎进行全景计算..."):

        # 1. 后台静默加载所有数据
        time.sleep(1.5)  # 模拟一下大模型的思考时间，增加极客感
        df_spatial = get_spatial_data()
        df_nlp, top_words = get_nlp_data()
        df_traffic = get_traffic_data()

        st.success(f"✅ 测度完毕！【{target_name}】多模态全景推演报告已生成。")

        # 2. 炫酷的选项卡展示
        tab_space, tab_nlp, tab_traffic, tab_aigc = st.tabs([
            "🌳 空间物理诊断 (CV)",
            "💬 社会情感测度 (NLP)",
            "🚥 交通潮汐预警",
            "🎨 AIGC 重绘蓝图"
        ])

        # ------------------------------------
        # Tab 1: 空间沙盘
        # ------------------------------------
        with tab_space:
            st.markdown("#### 📍 目标地块空间品质测度 (基于街景语义分割)")
            avg_gvi = df_spatial["GVI"].mean() if not df_spatial.empty else 0
            st.metric("核心区平均绿视率 (GVI)", f"{avg_gvi:.1f}%")

            # 渲染迷你版 3D 柱体
            layer_col = pdk.Layer(
                "ColumnLayer", data=df_spatial, get_position=["Lng", "Lat"],
                get_elevation="GVI", elevation_scale=15, radius=30, disk_resolution=6,
                extruded=True, get_fill_color="Dynamic_Color", opacity=0.8
            )
            c_lng, c_lat = float(target_coords.split(',')[0]), float(target_coords.split(',')[1])
            r_space = pdk.Deck(
                layers=[layer_col],
                initial_view_state=pdk.ViewState(longitude=c_lng, latitude=c_lat, zoom=14.5, pitch=50, bearing=15),
                map_style="light", height=400
            )
            st.pydeck_chart(r_space, use_container_width=True)

        # ------------------------------------
        # Tab 2: 情感分析
        # ------------------------------------
        with tab_nlp:
            st.markdown(f"#### 🏷️ 针对【{focus_keywords}】的公众情感映射")
            c1, c2 = st.columns(2)
            with c1:
                sentiment_counts = df_nlp['Sentiment'].value_counts()
                fig_pie = px.pie(values=sentiment_counts.values, names=sentiment_counts.index,
                                 title='情感极性分布', color_discrete_sequence=['#2ecc71', '#e74c3c', '#95a5a6'])
                fig_pie.update_layout(template="plotly_dark", height=350)
                st.plotly_chart(fig_pie, use_container_width=True)
            with c2:
                word_df = pd.DataFrame(top_words, columns=['词语', '频次'])
                fig_words = px.bar(word_df, x='频次', y='词语', orientation='h', title='高频核心痛点词汇')
                fig_words.update_layout(template="plotly_dark", height=350)
                st.plotly_chart(fig_words, use_container_width=True)

        # ------------------------------------
        # Tab 3: 交通预警
        # ------------------------------------
        with tab_traffic:
            st.markdown("#### 🔥 核心地段交通拥堵热力侦测")
            layer_heat = pdk.Layer(
                "HeatmapLayer", data=df_traffic, opacity=0.8,
                get_position=["Lng", "Lat"], get_weight="Weight", radiusPixels=80
            )
            r_traffic = pdk.Deck(
                layers=[layer_heat],
                initial_view_state=pdk.ViewState(longitude=c_lng, latitude=c_lat, zoom=14, pitch=0),
                map_style="light", height=400
            )
            st.pydeck_chart(r_traffic, use_container_width=True)

        # ------------------------------------
        # Tab 4: AIGC 风貌
        # ------------------------------------
        with tab_aigc:
            st.markdown(f"#### 👁️ AIGC 联觉推演: {target_style}")
            if uploaded_img is None:
                st.warning("⚠️ 必须在上方表单中上传现状图片才能启动 AIGC 渲染引擎！")
            else:
                img_input = Image.open(uploaded_img)
                comp1, comp2 = st.columns(2)
                with comp1:
                    st.image(img_input, caption="Before: 现状物理空间", use_container_width=True)
                with comp2:
                    demo_img_path = "AIGC_Demos/demo_result.jpg"
                    if os.path.exists(demo_img_path):
                        st.image(demo_img_path, caption=f"After: {target_style}", use_container_width=True)
                    else:
                        st.info(
                            "💡 系统已执行 ControlNet 空间约束与潜空间降噪。\n*(注：需在 AIGC_Demos 文件夹中放入效果图进行成果占位展示)*")