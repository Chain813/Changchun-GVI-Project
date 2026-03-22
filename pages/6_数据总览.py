import streamlit as st
import pandas as pd
import os
import plotly.express as px

st.set_page_config(page_title="数据总览", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    [data-testid="stHeader"] {display: none !important;}
    [data-testid="stSidebarNav"] {display: none !important;}
    [data-testid="stSidebar"] { display: flex !important; visibility: visible !important; }
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
with col3: st.page_link("pages/2_AIGC风貌管控.py", label="🎨 风貌管控", use_container_width=True)
with col4: st.page_link("pages/3_交通与人口.py", label="🚥 交通与人口", use_container_width=True)
with col5: st.page_link("pages/4_数据管理中心.py", label="📊 数据管理", use_container_width=True)
with col6: st.page_link("pages/5_LLM 情感分析.py", label="💬 情感分析", use_container_width=True)
with col7: st.page_link("pages/6_数据总览.py", label="📋 数据总览", use_container_width=True)
st.markdown("---")
st.markdown("<h2>多源数据资产总览与完整性评估</h2>", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("#### 📊 数据筛选")
    filter_type = st.radio("数据状态", ["全部", "✅ 已有数据", "⚠️ 部分缺失", "❌ 待采集"], label_visibility="collapsed")

st.markdown("### 📈 数据资产概览")

data_categories = {
    "物理空间数据": {
        "streetview": {"name": "街景图片", "status": "complete", "file": "StreetViews/", "count": "300+ 采样点",
                       "description": "百度街景全景图片，覆盖伪满皇宫周边核心区"},
        "poi": {"name": "POI 数据", "status": "complete", "file": "Changchun_POI_Real.csv", "count": "CSV 文件",
                "description": "兴趣点数据，包含商业、交通等设施"},
        "traffic": {"name": "交通设施", "status": "complete", "file": "Changchun_Traffic_Real.csv", "count": "CSV 文件",
                    "description": "公共交通站点、停车场等"},
        "points": {"name": "精确点位", "status": "complete", "file": "Changchun_Precise_Points.xlsx",
                   "count": "Excel 文件", "description": "精确地理坐标采样点位"}
    },
    "视觉感知数据": {
        "gvi": {"name": "绿视率分析", "status": "complete", "file": "GVI_Results_Analysis.csv", "count": "CSV 文件",
                "description": "基于 DeepLabV3+ 的指标测度"},
        "cv_nlp": {"name": "CV+NLP 数据", "status": "partial", "file": "CV_NLP_RawData.csv", "count": "CSV 文件",
                   "description": "视觉与情感融合分析数据"}
    },
    "社会情感数据": {
        "weibo": {"name": "微博数据", "status": "missing", "file": "待采集", "count": "-",
                  "description": "公众讨论文本"},
        "dianping": {"name": "大众点评", "status": "missing", "file": "待采集", "count": "-",
                     "description": "商户评论与打卡数据"}
    }
}

total_complete = sum(1 for cat in data_categories.values() for item in cat.values() if item["status"] == "complete")
total_partial = sum(1 for cat in data_categories.values() for item in cat.values() if item["status"] == "partial")
total_missing = sum(1 for cat in data_categories.values() for item in cat.values() if item["status"] == "missing")

col1, col2, col3, col4 = st.columns(4)
col1.metric("✅ 已有数据", f"{total_complete} 项")
col2.metric("⚠️ 部分缺失", f"{total_partial} 项")
col3.metric("❌ 待采集", f"{total_missing} 项")
col4.metric("📊 数据完整率", f"{total_complete / (total_complete + total_partial + total_missing) * 100:.1f}%")

st.markdown("---")

for category, items in data_categories.items():
    filtered_items = {k: v for k, v in items.items() if filter_type == "全部" or
                      (filter_type == "✅ 已有数据" and v["status"] == "complete") or
                      (filter_type == "⚠️ 部分缺失" and v["status"] == "partial") or
                      (filter_type == "❌ 待采集" and v["status"] == "missing")}

    if filtered_items:
        st.markdown(f"#### {category}")
        cols = st.columns(len(filtered_items))
        for idx, (key, item) in enumerate(filtered_items.items()):
            with cols[idx]:
                st.markdown(f'<div class="data-card">', unsafe_allow_html=True)
                st.markdown(f"#### {item['name']}")

                status_icon = "✅ 已完成" if item["status"] == "complete" else "⚠️ 部分缺失" if item[
                                                                                                   "status"] == "partial" else "❌ 待采集"
                st.info(f"**状态:** {status_icon}\n\n**文件:** `{item['file']}`\n\n**规模:** {item['count']}")
                st.markdown(f"*{item['description']}*")
                st.markdown('</div>', unsafe_allow_html=True)