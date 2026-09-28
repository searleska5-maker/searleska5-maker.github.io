import os
import re
import datetime

BASE_URL = "https://searleska5-maker.github.io/#/"

# 4 大專區分類配置
CATEGORIES = {
    'investment.md': {
        'title': '# 📈 投資詐騙與黑平台',
        'desc': '本專區收錄各類假投資、飆股群組、虛擬交易所黑幕與受害自救指南。',
        'keywords': ['投資', '股票', '期貨', '外匯', '虛擬貨幣', '交易所', 'sothebys', '文政小判', '出金', '保證金', '獲利', '當沖', '高回報']
    },
    'crypto.md': {
        'title': '# 🪙 加密貨幣黑幕',
        'desc': '揭露去中心化假錢包惡意授權、DEX 假合約、高收益質押陷阱與空投騙局。',
        'keywords': ['比特幣', '以太幣', 'USDT', '錢包', '合約', '質押', '空投', 'DEX', '幣安', '授權', '私鑰', '助記詞']
    },
    'network.md': {
        'title': '# 💬 網路交友與兼職',
        'desc': '解析殺豬盤心理話術、家庭代工刷單兼職陷阱、海外高薪求職與人頭戶詐術。',
        'keywords': ['交友', '殺豬盤', '兼職', '代工', '刷單', '求職', '戀愛', '人頭戶', '打工', '家庭代工']
    },
    'info.md': {
        'title': '# 🛠️ 受害自救指南',
        'desc': '黃金通報時間線、銀行圈存止付、筆錄製作要點與防範二次律師追資詐騙。',
        'keywords': ['自救', '報案', '165', '報警', '止付', '圈存', '律師', '追回', '筆錄', '受害自救']
    }
}

# 🚀 嚴格排除系統保留檔、導覽頁與雜頁（絕不進入文章清單）
EXCLUDE_FILES = {
    'README.md', 'SUMMARY.md', '_sidebar.md', 
    'investment.md', 'crypto.md', 'network.md', 'info.md',
    'about.md', 'cases.md', 'experience.md', 'contact.md', 'help.md'
}

# 🚀 標題黑名單：如果抓出來的標題是這些導覽字樣，直接過濾掉
EXCLUDE_TITLES = {
    '關於本站', '關於詐騙觀察筆記', '最新案例', '受害者經驗交流與心得', 
    '無法出金與平台失聯案例', '常見問題', '免責聲明', '首頁'
}

def get_post_info(filepath):
    """四重智慧適配標題"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 規則 1：標準 # 標題
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if title_match:
        return title_match.group(1).strip(), content

    # 規則 2：引號標題「暴雷#被...」
    quote_match = re.search(r'「([^」\n]+)」', content)
    if quote_match:
        clean_title = re.sub(r'<[^>]+>', '', quote_match.group(1)).strip()
        if len(clean_title) > 5:
            return clean_title, content

    # 規則 3：案例名稱
    case_match = re.search(r'案例名稱[：:]\s*([^\n<]+)', content)
    if case_match:
        clean_title = re.sub(r'<[^>]+>', '', case_match.group(1)).strip()
        if len(clean_title) > 3:
            return clean_title, content

    # 規則 4：檔案名稱
    clean_name = os.path.splitext(os.path.basename(filepath))[0].replace('-', ' ').replace('_', ' ')
    return clean_name, content

def generate_sitemap(all_posts):
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    sitemap_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>\n',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n',
        f'  <url><loc>https://searleska5-maker.github.io/</loc><lastmod>{today}</lastmod><priority>1.0</priority></url>\n'
    ]
    for cat in CATEGORIES:
        slug = os.path.splitext(cat)[0]
        sitemap_lines.append(f'  <url><loc>{BASE_URL}{slug}</loc><lastmod>{today}</lastmod><priority>0.8</priority></url>\n')
    for post in all_posts:
        slug = os.path.splitext(post)[0]
        sitemap_lines.append(f'  <url><loc>{BASE_URL}{slug}</loc><lastmod>{today}</lastmod><priority>0.9</priority></url>\n')
    sitemap_lines.append('</urlset>\n')
    
    with open('sitemap.xml', 'w', encoding='utf-8') as f:
        f.writelines(sitemap_lines)

def generate_robots():
    content = "User-agent: *\nAllow: /\nSitemap: https://searleska5-maker.github.io/sitemap.xml\n"
    with open('robots.txt', 'w', encoding='utf-8') as f:
        f.write(content)

def categorize():
    all_files = [f for f in os.listdir('.') if f.endswith('.md') and f not in EXCLUDE_FILES]
    category_posts = {cat: [] for cat in CATEGORIES}
    valid_articles = []

    for filename in all_files:
        title, content = get_post_info(filename)
        
        # 🚀 如果標題在黑名單中，直接跳過，不當作文章收錄
        if title in EXCLUDE_TITLES:
            continue

        matched = False
        # 依照專區關鍵字精準歸類
        for cat, data in CATEGORIES.items():
            for kw in data['keywords']:
                if kw.lower() in content.lower():
                    category_posts[cat].append((title, filename))
                    valid_articles.append(filename)
                    matched = True
                    break
            if matched:
                break
        
        # 🚀 移除先前的「未命中全部丟進投資」的流氓邏輯！未命中文章不再亂塞

    # 生成各專區 Markdown 頁面
    for cat, posts in category_posts.items():
        data = CATEGORIES[cat]
        lines = [
            f"{data['title']}\n\n",
            f"{data['desc']}\n\n",
            "---\n\n",
            "### 📌 最新案例與深度解析\n\n"
        ]
        if posts:
            for title, filename in posts:
                lines.append(f"* [{title}]({filename})\n")
        else:
            lines.append("> 💡 本專區案例持續彙整收錄中，即將更新...\n")
            
        with open(cat, 'w', encoding='utf-8') as f:
            f.writelines(lines)
            
    generate_sitemap(valid_articles)
    generate_robots()
    print("✅ 雜頁與範本已徹底過濾，各專區現在只呈現真正對應的案例！")

if __name__ == '__main__':
    categorize()
