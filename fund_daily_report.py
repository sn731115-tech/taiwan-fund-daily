import requests
from bs4 import BeautifulSoup
from datetime import datetime
import csv
import os
import time

FUNDS = [
    {"name": "安聯台灣科技",     "code": "acdd04"},
    {"name": "統一奔騰",         "code": "acps10"},
    {"name": "復華全方位",       "code": "acfh15"},
    {"name": "路博邁台灣5G",     "code": "acnb01"},
    {"name": "施羅德台灣樂活中小", "code": "aces10"},
]

CSV_FILE = "fund_daily_history.csv"

def get_fund_data(code):
    url = f"https://www.moneydj.com/funddj/ya/yp010000.djhtm?a={code}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        # 抓取最新淨值、漲跌、漲跌幅
        row = soup.find('td', string=lambda t: t and '最新值' in t)
        if row:
            tr = row.find_parent('tr')
            tds = tr.find_all('td')
            if len(tds) >= 4:
                nav = tds[1].get_text(strip=True).replace('台幣', '').strip()
                change = tds[2].get_text(strip=True)
                pct = tds[3].get_text(strip=True)
                return nav, change, pct
    except:
        pass
    return "N/A", "N/A", "N/A"

def save_to_csv(data):
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["日期", "基金名稱", "最新淨值", "今日漲跌", "漲跌幅"])
        writer.writerows(data)

def main():
    today = datetime.now().strftime("%Y-%m-%d %H:%M")
    print(f"🕖 {today} 台灣基金每日快報")
    print("=" * 50)
    
    report_data = []
    for fund in FUNDS:
        time.sleep(1)
        nav, change, pct = get_fund_data(fund["code"])
        print(f"• {fund['name']:<18} 淨值: {nav:>8}  漲跌: {change:>8}  {pct}")
        report_data.append([today.split()[0], fund["name"], nav, change, pct])
    
    save_to_csv(report_data)
    print(f"\n✅ 今日資料已記錄！共 {len(FUNDS)} 檔基金")

if __name__ == "__main__":
    main()
