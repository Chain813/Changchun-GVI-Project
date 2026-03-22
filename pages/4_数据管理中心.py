import streamlit as st
import pandas as pd
import os
import numpy as np
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="数据管理中心", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    [data-testid="stHeader"] {display: none !important;}
    [data-testid="stSidebarNav"] {display: none !important;}
    [data-testid="stSidebar"] { display: flex !important; visibility: visible !important; }
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
    .sidebar-toggle-btn {
        position: fixed; top: 70px; left: 10px; z-index: 9999;
        background: rgba(255, 255, 255, 0.15); border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 8px; padding: 8px 12px; cursor: pointer; transition: all 0.3s ease;
        color: #f8fafc; font-size: 20px; backdrop-filter: blur(10px);
    }
    .sidebar-toggle-btn:hover { background: rgba(255, 255, 255, 0.25); }
    .data-card {
        background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px; padding: 20px; margin-bottom: 20px;
        transition: all 0.3s ease;
    }
    .data-card:hover { background: rgba(255, 255, 255, 0.08); border-color: rgba(255, 255, 255, 0.3); }
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
st.markdown("<h2>多源数据融合管理中心</h2>", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("#### 📂 数据类型")
    data_type = st.radio("选择数据类型:", [
        "🏪 POI 数据", "🚥 交通数据", "📍 精确点位", "📊 CV 分析结果", "💬 情感分析数据"
    ], label_visibility="collapsed")

st.markdown("### 📊 数据概览")

data_files = {
    "🏪 POI 数据": "Changchun_POI_Real.csv",
    "🚥 交通数据": "Changchun_Traffic_Real.csv",
    "📍 精确点位": "Changchun_Precise_Points.xlsx",
    "📊 CV 分析结果": "GVI_Results_Analysis.csv",
    "💬 情感分析数据": "CV_NLP_RawData.csv"
}

selected_file = data_files[data_type]

if os.path.exists(selected_file):
    try:
        if selected_file.endswith('.csv'):
            df = pd.read_csv(selected_file, encoding='utf-8')
        else:
            df = pd.read_excel(selected_file)
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("📊 总记录数", f"{len(df):,}")
        col2.metric("📐 字段数量", f"{len(df.columns)}")
        col3.metric("💾 文件大小", f"{os.path.getsize(selected_file) / 1024:.1f} KB")
        col4.metric("✅ 数据状态", "正常")
        
        st.markdown("---")
        st.markdown("### 📋 数据预览")
        st.dataframe(df.head(10), use_container_width=True)
        
        st.markdown("---")
        st.markdown("### 📊 数据质量分析")
        missing_data = df.isnull().sum()
        missing_percent = (missing_data / len(df) * 100).round(2)
        quality_df = pd.DataFrame({
            '字段': missing_data.index,
            '缺失值': missing_data.values,
            '缺失率 (%)': missing_percent.values
        })
        st.dataframe(quality_df, use_container_width=True, hide_index=True)
        
    except Exception as e:
        st.error(f"❌ 数据读取失败：{e}")
else:
    st.warning(f"⚠️ 文件不存在：{selected_file}")

st.markdown("---")
st.markdown("### 📤 数据上传与更新")

upload_col1, upload_col2 = st.columns(2)
with upload_col1:
    st.markdown("#### 🆕 上传新数据")
    uploaded_file = st.file_uploader("选择文件上传", type=['csv', 'xlsx'], key="upload")
    if uploaded_file is not None:
        save_name = st.text_input("保存文件名:", value=uploaded_file.name)
        if st.button("💾 保存数据"):
            with open(save_name, 'wb') as f:
                f.write(uploaded_file.getvalue())
            st.success(f"✅ 数据已保存至 {save_name}")

with upload_col2:
    st.markdown("#### 🗑️ 数据管理")
    if st.button("🗑️ 删除选定数据文件"):
        if os.path.exists(selected_file):
            os.remove(selected_file)
            st.success(f"✅ 已删除 {selected_file}")
        else:
            st.warning("⚠️ 文件不存在")

st.markdown("---")
st.markdown("### 📈 数据可视化分析")

if os.path.exists(selected_file):
    try:
        if selected_file.endswith('.csv'):
            df = pd.read_csv(selected_file, encoding='utf-8')
        else:
            df = pd.read_excel(selected_file)
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if len(numeric_cols) > 0:
            viz_type = st.selectbox("选择图表类型:", ["📊 柱状图", "📈 折线图", "🔵 散点图", "🥧 饼图"])
            
            x_col = st.selectbox("X 轴:", df.columns, key="x")
            y_col = st.selectbox("Y 轴:", numeric_cols, key="y")
            
            if viz_type == "📊 柱状图":
                fig = px.bar(df, x=x_col, y=y_col, title=f"{y_col} vs {x_col}")
                fig.update_layout(template="plotly_dark")
                st.plotly_chart(fig, use_container_width=True)
            elif viz_type == "📈 折线图":
                fig = px.line(df, x=x_col, y=y_col, title=f"{y_col} vs {x_col}")
                fig.update_layout(template="plotly_dark")
                st.plotly_chart(fig, use_container_width=True)
            elif viz_type == "🔵 散点图":
                if len(numeric_cols) > 1:
                    color_col = st.selectbox("颜色:", numeric_cols, key="color")
                    fig = px.scatter(df, x=x_col, y=y_col, color=color_col, title=f"{y_col} vs {x_col}")
                    fig.update_layout(template="plotly_dark")
                    st.plotly_chart(fig, use_container_width=True)
            elif viz_type == "🥧 饼图":
                fig = px.pie(df, names=x_col, values=y_col, title=f"{y_col} Distribution")
                fig.update_layout(template="plotly_dark")
                st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"❌ 可视化失败：{e}")

st.markdown("---")
st.markdown("### 🧬 数据血缘关系")

data_lineage = pd.DataFrame({
    "数据名称": ["POI 数据", "交通数据", "精确点位", "街景图片", "CV 分析结果", "情感分析数据"],
    "来源": ["OpenStreetMap", "百度地图 API", "实地勘测", "百度街景 API", "DeepLabV3+/Segformer", "微博/大众点评爬虫"],
    "用途": ["商业设施分析", "交通路网分析", "空间定位基准", "视觉感知数据", "绿视率等指标计算", "社会情感分析"],
    "更新频率": ["季度", "月度", "年度", "季度", "实时", "周度"]
})

st.dataframe(data_lineage, use_container_width=True, hide_index=True)
