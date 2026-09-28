import os
import re
import datetime

# 網站網址
BASE_URL = "https://searleska5-maker.github.io/"

# 3 大專區分類配置
CATEGORIES = {
    'investment.md': {
        'title': '# 📈 投資詐騙與黑平台',
        'desc': '本專區收錄各類假投資、飆股群組、虛擬交易所黑幕與受害自救指南。',
        'keywords': [
            '投資', '股票', '期貨', '外匯', '虛擬貨幣',
            '交易所', 'sothebys', '文政小判', '出金',
            '保證金', '獲利', '當沖', '高回報'
        ]
    },

    'crypto.md': {
        'title': '# 🪙 加密貨幣黑幕',
        'desc': '揭露去中心化假錢包惡意授權、DEX 假合約、高收益質押陷阱與空投騙局。',
        'keywords': [
            '比特幣', '以太幣', 'USDT', '錢包',
            '合約', '質押', '空投', 'DEX',
            '幣安', '授權', '私鑰', '助記詞'
        ]
    },

    'network.md': {
        'title': '# 💬 網路交友與兼職',
        'desc': '解析殺豬盤心理話術、家庭代工刷單兼職陷阱、海外高薪求職與人頭戶詐術。',
        'keywords': [
            '交友', '殺豬盤', '兼職', '代工',
            '刷單', '求職', '戀愛', '人頭戶',
            '打工', '家庭代工'
        ]
    }
}


# 嚴格排除系統檔案、分類頁與導覽頁
EXCLUDE_FILES = {
    'README.md',
    'SUMMARY.md',
    '_sidebar.md',

    'investment.md',
    'crypto.md',
    'network.md',

    'about.md',
    'cases.md',
    'experience.md',
    'contact.md',
    'help.md'
}


# 標題黑名單
EXCLUDE_TITLES = {
    '關於本站',
    '關於詐騙觀察筆記',
    '最新案例',
    '受害者經驗交流與心得',
    '無法出金與平台失聯案例',
    '常見問題',
    '免責聲明',
    '首頁'
}


def get_post_info(filepath):
    """取得文章標題"""

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 規則 1：標準 Markdown # 標題
    title_match = re.search(
        r'^#\s+(.+)$',
        content,
        re.MULTILINE
    )

    if title_match:
        return title_match.group(1).strip(), content

    # 規則 2：抓取「」中的標題
    quote_match = re.search(
        r'「([^」\n]+)」',
        content
    )

    if quote_match:
        clean_title = re.sub(
            r'<[^>]+>',
            '',
            quote_match.group(1)
        ).strip()

        if len(clean_title) > 5:
            return clean_title, content

    # 規則 3：案例名稱
    case_match = re.search(
        r'案例名稱[：:]\s*([^\n<]+)',
        content
    )

    if case_match:
        clean_title = re.sub(
            r'<[^>]+>',
            '',
            case_match.group(1)
        ).strip()

        if len(clean_title) > 3:
            return clean_title, content

    # 規則 4：使用檔案名稱
    clean_name = (
        os.path.splitext(
            os.path.basename(filepath)
        )[0]
        .replace('-', ' ')
        .replace('_', ' ')
    )

    return clean_name, content


def generate_sitemap():
    """
    只建立網站首頁 Sitemap。

    目前網站使用 Docsify Hash 路由，
    因此不把 #/investment、#/文章 這類網址放進 Sitemap。
    """

    today = datetime.datetime.now().strftime("%Y-%m-%d")

    sitemap_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>\n',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n',
        f'  <url>\n',
        f'    <loc>{BASE_URL}</loc>\n',
        f'    <lastmod>{today}</lastmod>\n',
        f'    <priority>1.0</priority>\n',
        f'  </url>\n',
        '</urlset>\n'
    ]

    with open(
        'sitemap.xml',
        'w',
        encoding='utf-8'
    ) as f:
        f.writelines(sitemap_lines)


def generate_robots():

    content = (
        "User-agent: *\n"
        "Allow: /\n"
        "Sitemap: https://searleska5-maker.github.io/sitemap.xml\n"
    )

    with open(
        'robots.txt',
        'w',
        encoding='utf-8'
    ) as f:
        f.write(content)


def categorize():

    # 找出所有 Markdown 文章
    all_files = [
        f
        for f in os.listdir('.')
        if f.endswith('.md')
        and f not in EXCLUDE_FILES
    ]

    # 建立分類容器
    category_posts = {
        cat: []
        for cat in CATEGORIES
    }

    for filename in all_files:

        title, content = get_post_info(filename)

        # 排除導覽標題
        if title in EXCLUDE_TITLES:
            continue

        matched = False

        # 按照分類關鍵字自動判斷
        for cat, data in CATEGORIES.items():

            for kw in data['keywords']:

                if kw.lower() in content.lower():

                    category_posts[cat].append(
                        (title, filename)
                    )

                    matched = True
                    break

            if matched:
                break

    # 產生 3 個分類頁
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

                lines.append(
                    f"* [{title}]({filename})\n"
                )

        else:

            lines.append(
                "> 💡 本專區案例持續彙整收錄中，即將更新...\n"
            )

        with open(
            cat,
            'w',
            encoding='utf-8'
        ) as f:

            f.writelines(lines)

    # 更新 Sitemap
    generate_sitemap()

    # 更新 robots.txt
    generate_robots()

    print(
        "✅ 自動分類完成！"
        "目前只使用投資詐騙、加密貨幣、"
        "網路交友與兼職 3 個分類。"
    )


if __name__ == '__main__':
    categorize()
