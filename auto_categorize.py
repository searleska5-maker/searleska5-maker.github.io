import os
import re

# 1. 核心專區配置（關鍵字庫精準對應）
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

# 系統與核心保留檔，排除自動分類
EXCLUDE_FILES = {'README.md', 'SUMMARY.md', '_sidebar.md', 'investment.md', 'crypto.md', 'network.md', 'info.md'}

def get_post_info(filepath):
    """精準提取文章一級標題與全文內容"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 尋找 Markdown 的 # 大標題
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if title_match:
        title = title_match.group(1).strip()
    else:
        # 若未找到 # 標題，退回使用檔案名稱
        title = os.path.splitext(os.path.basename(filepath))[0]
    return title, content

def categorize():
    # 讀取倉庫內所有 Markdown 案例文章
    all_files = [f for f in os.listdir('.') if f.endswith('.md') and f not in EXCLUDE_FILES]
    
    category_posts = {cat: [] for cat in CATEGORIES}

    # 依序比對每篇文章內容與關鍵字
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
        
        # 若關鍵字未命中，預設自動歸入投資詐騙專區
        if not matched:
            category_posts['investment.md'].append((title, filename))

    # 自動生成各專區 Markdown 頁面
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
                # 輸出乾淨的標準清單語法，由 index.html 的 CSS 自動提升為醒目大新聞卡片
                lines.append(f"* [{title}]({filename})\n")
        else:
            lines.append("> 💡 目前本專區暫無案例，情報持續更新中...\n")
            
        with open(cat, 'w', encoding='utf-8') as f:
            f.writelines(lines)
            
    print("✅ 全部分類專區與大標題卡片對應已自動生成完畢！")

if __name__ == '__main__':
    categorize()
