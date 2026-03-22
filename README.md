# 长春伪满皇宫周边街区：多模态微更新决策平台

## 🏙️ 项目简介

本平台整合了**空间数字孪生 (Digital Twin)**、**计算机视觉 (CV)** 与**生成式大模型 (AIGC)** 技术，旨在通过多源城市数据的跨尺度耦合，为历史工业街区的城市设计与微更新提供数据支撑与空间决策辅助。

## 🚀 核心功能模块

### 1. 🌳 数字孪生沙盘
- 基于 DeepLabV3+ 的大规模绿视率 (GVI) 自动化测度
- 四维空间指标：绿视率、天空开阔度、围合度、视觉杂乱度
- 3D 高精度落位与多视角可视化

### 2. 🎨 AIGC 风貌管控
- 基于 Stable Diffusion + ControlNet 的工业遗产风貌修缮
- 多风格迁移：工业遗产保护、生态绿色融合、现代艺术创意、历史文化复兴
- 沉浸式方案推演与对比

### 3. 🚥 交通与人口
- 商业活力潮汐聚类分析
- 多模态公共交通路网耦合分析
- 24H 人口动态推演

### 4. 📊 数据管理中心
- 多源数据融合管理 (POI、交通、精确点位等)
- 数据上传、更新与可视化分析
- 数据质量监控

### 5. 💬 LLM 情感分析
- 社会情感计算与舆情热力图
- 负面情绪热点识别
- LLM 智能决策建议生成

## 📦 安装说明

### 环境要求
- Python 3.8+
- Windows 10/11

### 快速开始

1. **创建虚拟环境**
```bash
python -m venv venv
venv\Scripts\activate
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **启动应用**
```bash
streamlit run app.py
```

或者双击运行 `run.bat` 文件

## 📁 项目结构

```
ultimateDESIGN/
├── app.py                      # 主入口
├── pages/
│   ├── 1_数字孪生沙盘.py        # 数字孪生模块
│   ├── 2_AIGC 风貌管控.py       # AIGC 风貌模块
│   ├── 3_交通与人口.py          # 交通分析模块
│   ├── 4_数据管理中心.py        # 数据管理模块
│   └── 5_LLM 情感分析.py        # 情感分析模块
├── StreetViews/                # 街景图片数据
├── *.csv                       # 各类数据文件
├── run_deeplabv3.py           # CV 推理引擎
├── cv_semantic_engine.py      # Segformer 语义分割引擎
└── requirements.txt           # 依赖清单
```

## 🛠️ 技术架构

### 数据层
- OSM 路网数据
- POI 兴趣点数据
- 百度街景数据
- 微博/点评社交数据

### 算法层
- DeepLabV3+ 语义分割
- Segformer 城市语义理解
- Stable Diffusion 图像生成
- LLM 情感分析

### 应用层
- Streamlit Web 界面
- PyDeck 3D 可视化
- Plotly 数据分析图表

## 📊 数据说明

- **Changchun_POI_Real.csv**: 长春 POI 数据
- **Changchun_Traffic_Real.csv**: 交通设施数据
- **Changchun_Precise_Points.xlsx**: 精确采样点位
- **GVI_Results_Analysis.csv**: 绿视率分析结果
- **CV_NLP_RawData.csv**: 情感分析原始数据

## 🎯 使用场景

1. **城市规划师**: 评估街区空间品质，识别微更新靶点
2. **设计师**: 生成风貌重塑方案，进行多方案对比
3. **研究者**: 分析社会情感分布，理解市民需求
4. **管理者**: 监控交通活力，制定管理策略

## 📝 注意事项

- 首次运行 CV 推理引擎需要下载预训练模型
- AIGC 功能需要配置 Stable Diffusion API 或本地部署
- 情感分析需要预先爬取并处理社交数据

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request 来改进本项目！

## 📄 许可证

本项目仅供学术研究与教学使用。

## 📧 联系方式

如有问题或合作意向，请联系项目负责人。
