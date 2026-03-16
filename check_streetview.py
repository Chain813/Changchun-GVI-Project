import os
import pandas as pd

# 1. 路径配置
EXCEL_PATH = r"C:\Users\23902\ultimateDESIGN\Changchun_Precise_Points.xlsx"
SV_DIR = r"C:\Users\23902\ultimateDESIGN\StreetViews"

# 2. 读取原始坐标表
try:
    df = pd.read_excel(EXCEL_PATH)
except Exception as e:
    print(f"❌ 找不到 Excel: {e}")
    exit()

if 'ID' not in df.columns:
    df['ID'] = df.index + 1

# 3. 扫描本地图库
print("🔍 开始扫描本地街景图库...")
valid_points = []
total_images = 0

for index, row in df.iterrows():
    point_id = int(row['ID'])
    folder_path = os.path.join(SV_DIR, f"Point_{point_id}")
    
    # 检查文件夹存不存在，以及里面有没有 .jpg 文件
    img_count = 0
    if os.path.exists(folder_path):
        img_count = len([f for f in os.listdir(folder_path) if f.endswith('.jpg')])
    
    if img_count > 0:
        valid_points.append(point_id)
        total_images += img_count

# 4. 生成纯净版靶点名单
df_valid = df[df['ID'].isin(valid_points)].copy()
OUTPUT_PATH = r"C:\Users\23902\ultimateDESIGN\Changchun_Valid_Points.xlsx"
df_valid.to_excel(OUTPUT_PATH, index=False)

# 5. 打印体检报告
print("\n" + "="*40)
print(" 🏥 街景数据体检报告")
print("="*40)
print(f"📍 原始规划靶点总数: {len(df)} 个")
print(f"🎯 成功捕获街景靶点: {len(df_valid)} 个 (这就是我们将要输入 AI 的黄金节点！)")
print(f"👻 无数据(物理不可达): {len(df) - len(df_valid)} 个")
print(f"🖼️ 共计可用街景切片: {total_images} 张")
print("="*40)
print(f"💾 有效节点名单已保存至: {OUTPUT_PATH}")