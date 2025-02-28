"""
Author: Witten Yeh
Date: 2025-02-26 08:28:19
LastEditors: Witten Yeh
LastEditTime: 2025-02-27 20:43:50
"""

from playwright.sync_api import sync_playwright

def create_browser():
    playwright = sync_playwright().start()
    
    # 创建浏览器实例（Chromium）
    browser = playwright.chromium.launch(
        headless=False,  # 设置为True则不显示浏览器窗口
        args=[
            '--disable-blink-features=AutomationControlled',
            '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36'
        ]
    )
    
    # 创建浏览器上下文（支持多标签页独立配置）
    context = browser.new_context()
    return playwright, browser, context

def search_keys(required_keys, optional_keys, context):
    # 创建新页面
    page = context.new_page()
    
    # 导航到必应
    page.goto('https://www.bing.com')
    
    # 定位搜索框并输入内容
    search_box = page.locator('#sb_form_q')
    search_box.click()  # 确保焦点在搜索框
    
    # 构建查询字符串
    query_str = ' '.join(required_keys + optional_keys)
    
    # 输入内容并回车（使用更可靠的fill + press组合）
    search_box.fill(query_str)
    search_box.press("Enter")
    
    # 等待页面加载（显式等待结果区域）
    page.wait_for_selector('.b_results', timeout=10000)  # 10秒超时

if __name__ == "__main__":
    playwright, browser, context = create_browser()
    try:
        search_keys(
            required_keys=["中国天楹"], 
            optional_keys=["AI", "智能"], 
            context=context
        )
        input("Press Enter to exit...")  # 保持浏览器打开用于调试
    finally:
        # 关闭资源
        context.close()
        browser.close()
        playwright.stop()
