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
    {"name": "統一台灣動力基金", "code": "acps23"},
]

CSV_FILE = "fund_daily_history.csv"

def get_fund_data(code):
    url = f"https://www.moneydj.com/funddj/ya/yp010000.djhtm?a={code}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.text, 'html.parser')
        
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

def generate_report():
    today = datetime.now().strftime("%Y-%m-%d %H:%M")
    report = f"🕖 **{today} 台灣基金每日快報**\n"
    report += "=" * 45 + "\n\n"
    
    for fund in FUNDS:
        time.sleep(1)
        nav, change, pct = get_fund_data(fund["code"])
        report += f"• **{fund['name']}**\n   淨值: {nav}   漲跌: {change}   {pct}\n\n"
    
    save_to_csv([[today.split()[0], f["name"], *get_fund_data(f["code"])] for f in FUNDS])
    report += f"✅ 共 {len(FUNDS)} 檔基金 | 資料來源：MoneyDJ"
    return report

if __name__ == "__main__":
    report_text = generate_report()
    print(report_text)
    with open("daily_report.txt", "w", encoding="utf-8") as f:
        f.write(report_text)
