from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time
import random


def build_stealth_browser():
    print("🛡️ 正在挂载隐形迷彩...")
    chrome_options = Options()
    # ⚠️ 调试阶段千万别开无头模式（--headless），你要亲眼看着浏览器怎么动！

    # 伪装成一个极其普通的 Windows 10 用户
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    chrome_options.add_argument(f'user-agent={user_agent}')

    # 禁用一些可能暴露爬虫身份的自动化标记
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    # 启动浏览器装甲车
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # 抹除 WebDriver 的指纹（高级隐身）
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"""
    })

    return driver


def deep_dive_scroll(driver, target_url, scroll_times=5):
    print(f"🚁 空降目标区域：{target_url}")
    driver.get(target_url)

    # 给网页一点加载初始内容的时间
    time.sleep(3)

    print("⬇️ 开始执行战术下潜...")
    for i in range(scroll_times):
        print(f"   -> 第 {i + 1} 次下潜")
        # 随机滚动一段距离（模拟人手滑鼠标）
        scroll_step = random.uniform(0.5, 0.9)
        driver.execute_script(f"window.scrollTo(0, document.body.scrollHeight * {scroll_step});")

        # ⚠️ 极其关键：每次滚动后必须随机休息 2~4 秒！太快会被当场击毙！
        time.sleep(random.uniform(2.0, 4.0))

    return driver.page_source


def extract_intel(html_source):
    print("🔍 启动 BeautifulSoup 情报提取引擎...")
    soup = BeautifulSoup(html_source, 'html.parser')

    intel_data = []

    # ⚠️ 这里的 'div' 和 'card-wrap' 是举例，你需要根据真实网页 F12 看到的标签去改
    cards = soup.find_all('div', class_='card-wrap')

    for card in cards:
        try:
            # 提取文本内容
            text_element = card.find('p', class_='txt')
            content = text_element.text.strip() if text_element else ""

            if content:
                intel_data.append({"Content": content})
        except Exception as e:
            continue

    print(f"✅ 提取成功，共获得 {len(intel_data)} 条有效情报。")
    return intel_data


if __name__ == "__main__":
    # 1. 目标 URL (你可以换成微博搜索“长春中车厂”的 URL)
    TARGET = "https://s.weibo.com/weibo?q=%E9%95%BF%E6%98%A5%E4%B8%AD%E8%BD%A6%E5%8E%82"

    # 2. 组装战车
    driver = build_stealth_browser()

    try:
        # 3. 突入阵地并滚动获取源码 (设置滚动 3 次练练手)
        html = deep_dive_scroll(driver, TARGET, scroll_times=3)

        # 4. 解析情报
        data = extract_intel(html)

        # 5. 导出战果
        if data:
            df = pd.DataFrame(data)
            df.to_csv("CV_NLP_RawData.csv", index=False, encoding='utf-8-sig')
            print("🎉 战报已保存至 CV_NLP_RawData.csv！")

    finally:
        # 6. 销毁装甲车，清理痕迹
        print("💥 任务结束，正在销毁装甲车...")
        driver.quit()