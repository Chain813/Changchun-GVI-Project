import streamlit as st
import pandas as pd
import os
import numpy as np
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go

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
    .status-complete { color: #2ecc71; font-weight: bold; }
    .status-partial { color: #f39c12; font-weight: bold; }
    .status-missing { color: #e74c3c; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

col1, col2, col3, col4, col5, col6 = st.columns(6)
with col1: st.page_link("app.py", label="🏠 系统主页", use_container_width=True)
with col2: st.page_link("pages/1_数字孪生沙盘.py", label="🌳 数字孪生沙盘", use_container_width=True)
with col3: st.page_link("pages/2_AIGC 风貌管控.py", label="🎨 风貌管控", use_container_width=True)
with col4: st.page_link("pages/3_交通与人口.py", label="🚥 交通与人口", use_container_width=True)
with col5: st.page_link("pages/4_数据管理中心.py", label="📊 数据管理", use_container_width=True)
with col6: st.page_link("pages/5_LLM 情感分析.py", label="💬 情感分析", use_container_width=True)
st.markdown("---")
st.markdown("<h2>多源数据资产总览与完整性评估</h2>", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("#### 📊 数据筛选")
    filter_type = st.radio("数据状态:", ["全部", "✅ 已有数据", "⚠️ 部分缺失", "❌ 待采集"], label_visibility="collapsed")

st.markdown("### 📈 数据资产概览")

data_categories = {
    "物理空间数据": {
        "streetview": {"name": "街景图片", "status": "complete", "file": "StreetViews/", "count": "300+ 采样点", "description": "百度街景全景图片，覆盖伪满皇宫周边 150 公顷核心区"},
        "poi": {"name": "POI 数据", "status": "complete", "file": "Changchun_POI_Real.csv", "count": "CSV 文件", "description": "兴趣点数据，包含商业、交通、公共服务等设施"},
        "traffic": {"name": "交通设施", "status": "complete", "file": "Changchun_Traffic_Real.csv", "count": "CSV 文件", "description": "公共交通站点、地铁站、停车场等交通设施数据"},
        "points": {"name": "精确点位", "status": "complete", "file": "Changchun_Precise_Points.xlsx", "count": "Excel 文件", "description": "精确地理坐标采样点位"},
        "valid_points": {"name": "有效点位", "status": "complete", "file": "Changchun_Valid_Points.xlsx", "count": "Excel 文件", "description": "经验证的有效采样点位"}
    },
    "视觉感知数据": {
        "gvi": {"name": "绿视率分析", "status": "complete", "file": "GVI_Results_Analysis.csv", "count": "CSV 文件", "description": "基于 DeepLabV3+ 的绿视率、天空开阔度等指标"},
        "cv_nlp": {"name": "CV+NLP 数据", "status": "partial", "file": "CV_NLP_RawData.csv", "count": "CSV 文件", "description": "计算机视觉与自然语言处理融合数据"}
    },
    "社会情感数据": {
        "weibo": {"name": "微博数据", "status": "missing", "file": "待采集", "count": "-", "description": "微博平台关于工业遗产的讨论文本"},
        "dianping": {"name": "大众点评", "status": "missing", "file": "待采集", "count": "-", "description": "大众点评商户评论与打卡数据"},
        "xiaohongshu": {"name": "小红书", "status": "missing", "file": "待采集", "count": "-", "description": "小红书笔记与标签数据"}
    },
    "分析评估数据": {
        "space_syntax": {"name": "空间句法", "status": "missing", "file": "待生成", "count": "-", "description": "Depthmap+/sDNA 穿行度与整合度分析"},
        "building_info": {"name": "建筑信息", "status": "missing", "file": "待采集", "count": "-", "description": "建筑年代、风貌类型、保护等级等"},
        "land_use": {"name": "土地利用", "status": "missing", "file": "待采集", "count": "-", "description": "用地性质、容积率、建筑密度等"},
        "demographics": {"name": "人口统计", "status": "missing", "file": "待采集", "count": "-", "description": "人口密度、年龄结构、收入水平等"}
    }
}

total_complete = sum(1 for cat in data_categories.values() for item in cat.values() if item["status"] == "complete")
total_partial = sum(1 for cat in data_categories.values() for item in cat.values() if item["status"] == "partial")
total_missing = sum(1 for cat in data_categories.values() for item in cat.values() if item["status"] == "missing")

col1, col2, col3, col4 = st.columns(4)
col1.metric("✅ 已有数据", f"{total_complete} 项")
col2.metric("⚠️ 部分缺失", f"{total_partial} 项")
col3.metric("❌ 待采集", f"{total_missing} 项")
col4.metric("📊 数据完整率", f"{total_complete/(total_complete+total_partial+total_missing)*100:.1f}%")

st.markdown("---")

if filter_type == "全部" or filter_type == "✅ 已有数据":
    st.markdown("### ✅ 已有数据")
    
    for category, items in data_categories.items():
        complete_items = {k: v for k, v in items.items() if v["status"] == "complete"}
        if complete_items:
            st.markdown(f"#### {category}")
            cols = st.columns(len(complete_items))
            for idx, (key, item) in enumerate(complete_items.items()):
                with cols[idx]:
                    st.markdown(f'<div class="data-card">', unsafe_allow_html=True)
                    st.markdown(f"#### {item['name']}")
                    st.info(f"**状态:** 已完成\n\n**文件:** `{item['file']}`\n\n**规模:** {item['count']}")
                    st.markdown(f"*{item['description']}*")
                    st.markdown('</div>', unsafe_allow_html=True)

if filter_type == "全部" or filter_type == "⚠️ 部分缺失":
    st.markdown("### ⚠️ 部分缺失数据")
    
    for category, items in data_categories.items():
        partial_items = {k: v for k, v in items.items() if v["status"] == "partial"}
        if partial_items:
            st.markdown(f"#### {category}")
            cols = st.columns(len(partial_items))
            for idx, (key, item) in enumerate(partial_items.items()):
                with cols[idx]:
                    st.markdown(f'<div class="data-card">', unsafe_allow_html=True)
                    st.markdown(f"#### {item['name']}")
                    st.warning(f"**状态:** 部分缺失\n\n**文件:** `{item['file']}`\n\n**规模:** {item['count']}")
                    st.markdown(f"*{item['description']}*")
                    st.markdown('</div>', unsafe_allow_html=True)

if filter_type == "全部" or filter_type == "❌ 待采集":
    st.markdown("### ❌ 待采集数据")
    
    for category, items in data_categories.items():
        missing_items = {k: v for k, v in items.items() if v["status"] == "missing"}
        if missing_items:
            st.markdown(f"#### {category}")
            cols = st.columns(len(missing_items))
            for idx, (key, item) in enumerate(missing_items.items()):
                with cols[idx]:
                    st.markdown(f'<div class="data-card">', unsafe_allow_html=True)
                    st.markdown(f"#### {item['name']}")
                    st.error(f"**状态:** 待采集\n\n**需求:** 高优先级")
                    st.markdown(f"*{item['description']}*")
                    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown("### 📊 数据完整性可视化")

completeness_data = pd.DataFrame({
    '数据类别': list(data_categories.keys()),
    '已完成': [sum(1 for v in cat.values() if v["status"] == "complete") for cat in data_categories.values()],
    '部分完成': [sum(1 for v in cat.values() if v["status"] == "partial") for cat in data_categories.values()],
    '待采集': [sum(1 for v in cat.values() if v["status"] == "missing") for cat in data_categories.values()]
})

fig = px.bar(completeness_data, x='数据类别', y=['已完成', '部分完成', '待采集'],
             title='各类型数据完整性对比',
             color_discrete_sequence=['#2ecc71', '#f39c12', '#e74c3c'])
fig.update_layout(template="plotly_dark", showlegend=True)
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.markdown("### 📋 数据采集优先级建议")

priority_df = pd.DataFrame({
    "优先级": ["🔴 高", "🔴 高", "🟡 中", "🟡 中", "🟢 低", "🟢 低"],
    "数据类别": ["空间句法分析", "建筑信息数据", "土地利用数据", "人口统计数据", "微博数据", "大众点评/小红书"],
    "用途": ["路网重构决策", "风貌保护规划", "功能置换分析", "活力评估", "社会情感分析", "社会情感分析"],
    "采集难度": ["中等", "较高", "中等", "较高", "高", "高"],
    "建议工具": ["Depthmap+ / sDNA", "实地调研 + 档案查询", "自然资源局数据", "统计局数据", "爬虫 API", "爬虫 API"]
})

st.dataframe(priority_df, use_container_width=True, hide_index=True)

st.markdown("---")
st.markdown("### 🔗 数据血缘关系")

lineage_data = pd.DataFrame({
    "数据名称": ["街景图片", "POI 数据", "交通数据", "精确点位", "绿视率分析", "情感分析数据"],
    "来源": ["百度街景 API", "OpenStreetMap", "百度地图 API", "实地勘测", "DeepLabV3+ 语义分割", "多源社交数据"],
    "处理流程": ["街景采集 → 图片预处理 → CV 分析", "OSM 提取 → 数据清洗 → 格式转换", "API 采集 → 坐标转换 → 分类标注", "GPS 测量 → 坐标校正 → 数据入库", "语义分割 → 指标计算 → 空间聚合", "文本爬取 → NLP 分析 → 情感标注"],
    "应用场景": ["数字孪生沙盘", "交通与人口分析", "交通与人口分析", "所有模块基准", "数字孪生沙盘", "LLM 情感分析"]
})

st.dataframe(lineage_data, use_container_width=True, hide_index=True)

st.markdown("---")
st.markdown("### 💡 数据管理建议")

col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    #### 📌 短期任务 (1-2 周)
    1. **空间句法分析**: 使用 Depthmap+ 对研究区域进行穿行度分析
    2. **建筑信息补充**: 通过地方志、档案馆收集建筑年代信息
    3. **数据标准化**: 统一所有空间数据的坐标系 (WGS-84)
    """)

with col2:
    st.markdown("""
    #### 📌 中期任务 (1-2 月)
    1. **社交数据采集**: 部署微博、点评爬虫，收集公众评价
    2. **土地利用数据**: 申请自然资源局用地规划数据
    3. **人口数据对接**: 对接统计局人口普查数据
    """)
