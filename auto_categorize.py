import os
import re
import datetime

BASE_URL = "https://searleska5-maker.github.io/#/"

# 4 大專區分類配置與關鍵字庫
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

EXCLUDE_FILES = {'README.md', 'SUMMARY.md', '_sidebar.md', 'investment.md', 'crypto.md', 'network.md', 'info.md'}

def get_post_info(filepath):
    """精準提取文章一級標題與全文內容"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if title_match:
        title = title_match.group(1).strip()
    else:
        # 若未找到 # 大標題，搜尋引號開頭標題或檔名
        quote_match = re.search(r'「([^」]+)」', content)
        title = quote_match.group(1).strip() if quote_match else os.path.splitext(os.path.basename(filepath))[0]
    return title, content

def generate_sitemap(all_posts):
    """為 Google SEO 生成專屬 sitemap.xml"""
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
    print("✅ sitemap.xml 已同步生成！")

def generate_robots():
    """生成利於 Googlebot 抓取的 robots.txt"""
    content = "User-agent: *\nAllow: /\nSitemap: https://searleska5-maker.github.io/sitemap.xml\n"
    with open('robots.txt', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ robots.txt 已同步生成！")

def categorize():
    all_files = [f for f in os.listdir('.') if f.endswith('.md') and f not in EXCLUDE_FILES]
    category_posts = {cat: [] for cat in CATEGORIES}

    for filename in all_files:
        title, content = get_post_info(filename)
        matched = False
        for cat, data in CATEGORIES.items():
            for kw in data['keywords']:
                if kw.lower() in content.lower():
                    category_posts[cat].append((title, filename))
                    matched = True
                    break
            if matched:
                break
        if not matched:
            category_posts['investment.md'].append((title, filename))

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
            lines.append("> 💡 目前本專區暫無案例，情報持續更新中...\n")
            
        with open(cat, 'w', encoding='utf-8') as f:
            f.writelines(lines)
            
    generate_sitemap(all_files)
    generate_robots()
    print("✅ 全部分類專區、Sitemap 與 SEO 配置已自動更新完成！")

if __name__ == '__main__':
    categorize()
