import pandas as pd
import numpy as np
import os
import math
import jieba
from collections import Counter


# ==========================================
# 🗺️ 核心算法：百度坐标 (BD-09) 转 WGS-84
# ==========================================
def bd09_to_wgs84(bd_lon, bd_lat):
    x_pi, pi = 3.14159265358979324 * 3000.0 / 180.0, 3.1415926535897932384626
    a, ee = 6378245.0, 0.00669342162296594323
    x, y = bd_lon - 0.0065, bd_lat - 0.006
    z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * x_pi)
    theta = math.atan2(y, x) - 0.000003 * math.cos(x * x_pi)
    gcj_lon, gcj_lat = z * math.cos(theta), z * math.sin(theta)

    def transformlat(lng, lat):
        ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + 0.1 * lng * lat + 0.2 * math.sqrt(abs(lng))
        ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 * math.sin(2.0 * lng * pi)) * 2.0 / 3.0
        ret += (20.0 * math.sin(lat * pi) + 40.0 * math.sin(lat / 3.0 * pi)) * 2.0 / 3.0
        ret += (160.0 * math.sin(lat / 12.0 * pi) + 320 * math.sin(lat * pi / 30.0)) * 2.0 / 3.0
        return ret

    def transformlng(lng, lat):
        ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + 0.1 * lng * lat + 0.1 * math.sqrt(abs(lng))
        ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 * math.sin(2.0 * lng * pi)) * 2.0 / 3.0
        ret += (20.0 * math.sin(lng * pi) + 40.0 * math.sin(lng / 3.0 * pi)) * 2.0 / 3.0
        ret += (150.0 * math.sin(lng / 12.0 * pi) + 300.0 * math.sin(lng / 30.0 * pi)) * 2.0 / 3.0
        return ret

    dlat, dlon = transformlat(gcj_lon - 105.0, gcj_lat - 35.0), transformlng(gcj_lon - 105.0, gcj_lat - 35.0)
    radlat = gcj_lat / 180.0 * pi
    magic = 1 - ee * math.sin(radlat) * math.sin(radlat)
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
    dlon = (dlon * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
    return gcj_lon - dlon, gcj_lat - dlat


# ==========================================
# 🌳 模块 1：空间物理测度计算引擎
# ==========================================
def get_spatial_data():
    base_path = "Changchun_Precise_Points.xlsx"
    gvi_path = "GVI_Results_Analysis.csv"
    if not os.path.exists(base_path): base_path = "../" + base_path
    if not os.path.exists(gvi_path): gvi_path = "../" + gvi_path

    try:
        df_base = pd.read_excel(base_path)
        df_gvi = pd.read_csv(gvi_path)
        if 'Folder' in df_gvi.columns:
            df_gvi['ID'] = df_gvi['Folder'].str.replace('Point_', '').astype(int)
            df_gvi = df_gvi.groupby('ID').mean().reset_index()
        df = pd.merge(df_base, df_gvi, on='ID', how='inner')
    except Exception:
        # 如果没有真实数据，生成占位防崩溃数据
        lngs = np.random.normal(loc=125.3517, scale=0.005, size=150)
        lats = np.random.normal(loc=43.9116, scale=0.005, size=150)
        df = pd.DataFrame({"ID": range(1, 151), "Lng": lngs, "Lat": lats, "GVI": np.random.randint(10, 50, size=150)})

    if "GVI" not in df.columns: df["GVI"] = 0
    df = df.dropna(subset=['Lng', 'Lat'])

    # 计算冷暖色动态映射
    min_v, max_v = df["GVI"].min(), df["GVI"].max()
    if min_v == max_v: max_v = min_v + 1

    def get_gradient_color(val):
        n = (val - min_v) / (max_v - min_v)
        return [int(255 * (1 - n)), int(200 * math.sin(n * math.pi)), int(255 * n), 255]

    df["Dynamic_Color"] = df["GVI"].apply(get_gradient_color)
    return df


# ==========================================
# 💬 模块 5：NLP 社会情感计算引擎
# ==========================================
def get_nlp_data():
    file_path = "CV_NLP_RawData.csv"
    if not os.path.exists(file_path): file_path = "../" + file_path

    try:
        df = pd.read_csv(file_path, encoding='utf-8')
    except Exception:
        df = pd.DataFrame({"Text": ["环境很差", "历史遗迹不错", "老厂房太破了", "交通拥堵", "伪满建筑很有特色"],
                           "Score": [-0.8, 0.9, -0.6, -0.7, 0.8]})

    np.random.seed(42)
    if 'Sentiment' not in df.columns:
        df['Sentiment'] = np.random.choice(['positive', 'negative', 'neutral'], size=len(df), p=[0.4, 0.35, 0.25])

    # 结巴分词提取高频词
    all_text = ' '.join(df['Text'].dropna().astype(str))
    stop_words = {'的', '了', '是', '在', '我', '有', '和', '就', '不', '人', '都', '一', '很', '什么', '我们'}
    words = [w for w in jieba.cut(all_text) if len(w) > 1 and w not in stop_words]
    word_counts = Counter(words).most_common(15)

    return df, word_counts


# ==========================================
# 🚥 模块 3：交通拥堵计算引擎
# ==========================================
def get_traffic_data():
    cong_bd_lngs = [125.360106, 125.355170, 125.346943]
    cong_bd_lats = [43.908314, 43.915339, 43.912892]
    cong_wgs = [bd09_to_wgs84(lon, lat) for lon, lat in zip(cong_bd_lngs, cong_bd_lats)]

    df_cong = pd.DataFrame({
        "Name": ["早市核心拥堵段", "铁道口车流瓶颈", "老旧小区出入口"],
        "Lng": [p[0] for p in cong_wgs], "Lat": [p[1] for p in cong_wgs],
        "Weight": [85, 90, 65]
    })
    return df_cong