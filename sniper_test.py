import requests
import json

AK = "W7iTpEM9P3wGO0kuft1fZhdM6YMB9ADr"

# 🎯 随便填一个你认为“绝对有街景”的经纬度 (从你的 Excel 里挑一个没抓到图的点)
lng = 125.3411073   # 替换成测试点的 Lng
lat = 43.9055812   # 替换成测试点的 Lat

url = f"https://api.map.baidu.com/panorama/v2?ak={AK}&width=1024&height=512&location={lng},{lat}&fov=90&heading=0&pitch=0&coordtype=wgs84ll"

print(f"📡 正在向百度发送狙击请求...\n测试坐标: {lng}, {lat}")
response = requests.get(url)

if response.headers.get('Content-Type', '').startswith('image/'):
    print("✅ 成功获取到图片！说明配额够，且这个地方确实有图。此前的漏抓可能是并发太快被踢了。")
else:
    print("❌ 百度拒绝给图！它的真实借口是：")
    try:
        # 强制打印最原始的底裤
        raw_json = response.json()
        print(json.dumps(raw_json, indent=4, ensure_ascii=False))
        
        status = raw_json.get('status')
        if status == 2:
            print("\n🚨 百度官方回复：【找不到相关全景数据】。这说明确实是街景车没开进去，你的直觉和百度的图库存在偏差。")
        elif status == 211 or status == 240:
            print("\n🚨 百度官方回复：【APP SN校验失败 / 服务被禁用】。你可能没有在百度后台勾选开通“全景图V2”的服务权限！")
        elif status == 401 or status == 402:
            print("\n🚨 百度官方回复：【并发量超限】。你被百度的防爬虫机制拦截了！")
    except:
        print(f"⚠️ 无法解析为 JSON，最原始返回文本为：\n{response.text}")