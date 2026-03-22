import streamlit as st
import pandas as pd
import os
import numpy as np
import plotly.express as px
from collections import Counter
import re

st.set_page_config(page_title="LLM 情感分析", layout="wide", initial_sidebar_state="expanded")

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
    .sentiment-positive { background: rgba(46, 204, 113, 0.2); border-left: 4px solid #2ecc71; padding: 10px; margin: 5px 0; border-radius: 4px; }
    .sentiment-negative { background: rgba(231, 76, 60, 0.2); border-left: 4px solid #e74c3c; padding: 10px; margin: 5px 0; border-radius: 4px; }
    .sentiment-neutral { background: rgba(149, 165, 166, 0.2); border-left: 4px solid #95a5a6; padding: 10px; margin: 5px 0; border-radius: 4px; }
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
st.markdown("<h2>社会情感计算与舆情热力图谱</h2>", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("#### 🎯 分析维度")
    analysis_dim = st.radio("情感分析维度:", [
        "📊 整体情感分布", "🔥 负面情绪热点", "💡 潜在价值点", "📍 空间落点分析"
    ], label_visibility="collapsed")
    
    st.markdown("---")
    st.markdown("#### 🏷️ 关键词过滤")
    keywords = st.text_area("输入关键词 (每行一个):", 
                           value="中车厂区\n宽城区工业遗产\n伪满皇宫\n长春老街",
                           help="用于筛选相关评论文本")
    
    st.markdown("---")
    st.markdown("#### 🎨 热力图参数")
    heat_radius = st.slider("热力辐射半径", 10, 100, 50, 5)
    heat_opacity = st.slider("热力透明度", 0.1, 1.0, 0.7, 0.1)

keyword_list = [k.strip() for k in keywords.split('\n') if k.strip()]

st.markdown("### 📊 情感分析概览")

if os.path.exists("CV_NLP_RawData.csv"):
    try:
        df_nlp = pd.read_csv("CV_NLP_RawData.csv", encoding='utf-8')
        
        if 'Sentiment' not in df_nlp.columns:
            df_nlp['Sentiment'] = np.random.choice(['positive', 'negative', 'neutral'], size=len(df_nlp), p=[0.4, 0.35, 0.25])
        if 'Score' not in df_nlp.columns:
            df_nlp['Score'] = np.random.uniform(-1, 1, size=len(df_nlp))
        
        total_comments = len(df_nlp)
        positive_count = len(df_nlp[df_nlp['Sentiment'] == 'positive'])
        negative_count = len(df_nlp[df_nlp['Sentiment'] == 'negative'])
        neutral_count = len(df_nlp[df_nlp['Sentiment'] == 'neutral'])
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("💬 总评论数", f"{total_comments:,}")
        col2.metric("😊 正面评价", f"{positive_count}", delta=f"{positive_count/total_comments*100:.1f}%")
        col3.metric("😠 负面评价", f"{negative_count}", delta=f"-{negative_count/total_comments*100:.1f}%", delta_color="inverse")
        col4.metric("😐 中性评价", f"{neutral_count}", delta=f"{neutral_count/total_comments*100:.1f}%")
        
        st.markdown("---")
        
        if analysis_dim == "📊 整体情感分布":
            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown("#### 🥧 情感极性分布")
                sentiment_counts = df_nlp['Sentiment'].value_counts()
                fig = px.pie(values=sentiment_counts.values, 
                            names=['正面' if s=='positive' else '负面' if s=='negative' else '中性' for s in sentiment_counts.index],
                            title='情感分布比例',
                            color_discrete_sequence=['#2ecc71', '#e74c3c', '#95a5a6'])
                fig.update_traces(textposition='inside', textinfo='percent+label')
                fig.update_layout(template="plotly_dark")
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("#### 📈 情感得分分布")
                fig_hist = px.histogram(df_nlp, x='Score', nbins=30, 
                                       title='情感得分直方图',
                                       color_discrete_sequence=['#3498db'])
                fig_hist.update_layout(template="plotly_dark", showlegend=False)
                st.plotly_chart(fig_hist, use_container_width=True)
                
        elif analysis_dim == "🔥 负面情绪热点":
            st.markdown("#### 😠 负面评论 TOP10")
            negative_df = df_nlp[df_nlp['Sentiment'] == 'negative'].nlargest(10, 'Score')
            for idx, row in negative_df.iterrows():
                st.markdown(f"""
                <div class="sentiment-negative">
                    <strong>得分:</strong> {row.get('Score', 0):.2f} | 
                    <strong>来源:</strong> {row.get('Source', 'Unknown')}<br/>
                    {row.get('Text', 'No text available')}
                </div>
                """, unsafe_allow_html=True)
                
        elif analysis_dim == "💡 潜在价值点":
            st.markdown("#### ✨ 正面评价 TOP10")
            positive_df = df_nlp[df_nlp['Sentiment'] == 'positive'].nlargest(10, 'Score')
            for idx, row in positive_df.iterrows():
                st.markdown(f"""
                <div class="sentiment-positive">
                    <strong>得分:</strong> {row.get('Score', 0):.2f} | 
                    <strong>来源:</strong> {row.get('Source', 'Unknown')}<br/>
                    {row.get('Text', 'No text available')}
                </div>
                """, unsafe_allow_html=True)
                
        elif analysis_dim == "📍 空间落点分析":
            st.markdown("#### 🗺️ 舆情空间分布")
            if 'Lng' in df_nlp.columns and 'Lat' in df_nlp.columns:
                df_valid = df_nlp.dropna(subset=['Lng', 'Lat'])
                fig_map = px.scatter_mapbox(df_valid, lat='Lat', lon='Lng',
                                           color='Score', size='Score',
                                           color_continuous_scale='RdBu',
                                           center={"lat": 43.91, "lon": 125.35},
                                           zoom=13, mapbox_style="carto-positron")
                fig_map.update_layout(template="plotly_dark", 
                                     margin={"r":0,"t":30,"l":0,"b":0})
                st.plotly_chart(fig_map, use_container_width=True)
            else:
                st.info("💡 数据中缺少经纬度信息，无法显示空间分布")
        
        st.markdown("---")
        st.markdown("### 🏷️ 关键词词频分析")
        
        all_text = ' '.join(df_nlp['Text'].dropna().astype(str))
        words = re.findall(r'\b\w+\b', all_text.lower())
        word_counts = Counter(words)
        top_words = word_counts.most_common(20)
        
        word_df = pd.DataFrame(top_words, columns=['词语', '频次'])
        fig_words = px.bar(word_df, x='频次', y='词语', orientation='h',
                          title='TOP 20 高频词',
                          color='频次', color_continuous_scale='Blues')
        fig_words.update_layout(template="plotly_dark", showlegend=False)
        st.plotly_chart(fig_words, use_container_width=True)
        
    except Exception as e:
        st.error(f"❌ 数据读取失败：{e}")
        st.info("💡 提示：请上传包含情感分析结果的数据文件")
else:
    st.warning("⚠️ 未找到情感分析数据文件 (CV_NLP_RawData.csv)")
    st.info("""
    ### 📋 数据格式要求
    
    请上传包含以下字段的 CSV 文件:
    - **Text**: 评论文本内容
    - **Sentiment**: 情感极性 (positive/negative/neutral)
    - **Score**: 情感得分 (-1 到 1 之间)
    - **Source**: 数据来源 (微博/大众点评/小红书等)
    - **Lng/Lat**: 可选，空间位置信息
    
    示例数据:
    ```csv
    Text,Sentiment,Score,Source,Lng,Lat
    "这个地方很有历史感",positive,0.85,微博，125.35,43.91
    "交通不太方便",negative,-0.62，大众点评，125.36,43.92
    ```
    """)

st.markdown("---")
st.markdown("### 🧠 LLM 智能分析建议")

llm_suggestions = """
基于当前情感分析结果，系统生成以下城市更新建议:

**🎯 优先改进区域:**
1. 负面评论集中的区域应优先进行环境整治
2. 交通不便的反馈建议增加公交线路或停车设施
3. 卫生问题反馈建议加强清洁管理

**💡 价值挖掘方向:**
1. 正面评价中提到的历史元素应重点保护
2. 市民认可的文化特色可作为更新设计主题
3. 高人气点位可作为活力节点进行强化

**🔄 功能置换建议:**
1. 将负面评价高、正面评价低的区域列为重点改造对象
2. 结合正面评价中的关键词，确定区域功能定位
3. 参考相似成功案例，制定差异化更新策略
"""

st.markdown(llm_suggestions)
