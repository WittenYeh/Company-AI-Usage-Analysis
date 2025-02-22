'''
Autor: Witten Yeh
Date: 2025-02-21 21:36:22
LastEditors: Witten Yeh
LastEditTime: 2025-02-22 13:39:14
Description: 
'''

from playwright.sync_api import sync_playwright
from urllib.parse import quote
import time

def web_content_collector(required_keyword, optional_keyword, max_pages):
    with sync_playwright() as p:
        # open browser
        browser = p.chromium.launch(channel="msedge", headless=True, args=['--headless=new'])
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59"
        )
        page = context.new_page()
        
        # build searching query
        query = ' '.join([f'"{kw}"' for kw in required_keyword])
        if optional_keyword:
            query += " (" + " OR ".join(optional_keyword) + ")"
            
            
        
        # execute bing searching
        page.goto(f"https://www.bing.com/search?q={quote(query)}", timeout=6000)
        
        # maybe need to accept cookies
        try:
            page.click("#bnp_btn_accept", timeout=3000)
        except:
            pass
        
        collected_urls = []
        current_page = 1
        while len(collected_urls) < max_pages:
            # extract all target webpages of current searing page
            page.wait_for_selector("ol#b_results li.b_algo")
            search_results = page.query_selector_all("ol#b_results li.b_algo")

            for search_result in search_results:
                try:
                    link = search_result.query_selector("h2 a")
                    href = link.get_attribute("href")
                    if href and href not in collected_urls:
                        collected_urls.append(href)
                        print("found ")
                        if len(collected_urls) >= max_pages:
                            break
                except:
                    continue

            # Bing next page operation (each page display 10 search results)
            if len(collected_urls) < max_pages:
                try:
                    current_page += 1
                    page.goto(f"https://www.bing.com/search?q={quote(query)}&first={10*(current_page-1)+1}")
                    page.wait_for_load_state("networkidle")
                except:
                    break

        # validate and collect web contents
        valid_web_contents = []
        for url in collected_urls[:max_pages]:
            try:
                page.goto(url, timeout=20000)
                content = page.inner_text("body")
                
                # check for keywords
                required_check = all(kw in content for kw in required_keyword)
                optional_check = any(kw in content for kw in optional_keyword) if optional_keyword else True
                
                if required_check and optional_check:
                    valid_web_contents.append({
                        "url": url,
                        "content": content
                    })
            except:
                continue

        browser.close()
        
        return valid_web_contents

def save_to_html(web_content, path):
    pass

def web_search(company_name: str, display: bool = True):
    valid_web_content = web_content_collector(
        required_keyword=[company_name],
        optional_keyword=["AI", "智能"],
        max_pages=10
    )

    if display:
        for idx, item in enumerate(valid_web_content, 1):
            print(str(idx) + "th searching result of company ", company_name)
            print("url: " + item['url'])
            print("web content: " + item['web_content'])
    
    return valid_web_content
            
def save_search_result(results):
    pass

# test
if __name__ == "__main__":
    web_search(company_name="中国天楹", display=True)
    