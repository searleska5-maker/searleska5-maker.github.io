import os
import re

# 定義分類規則：[分類頁檔名, 匹配關鍵字清單]
CATEGORIES = {
    'investment.md': ['投資', '股票', '期貨', '保證金', '內線', '取引所', '獲利', '文政小判金'],
    'crypto.md': ['加密貨幣', '虛擬幣', '比特幣', '以太幣', '交易所', 'USDT', '提幣', '區塊鏈'],
    'network.md': ['網路', '交友', '詐騙', '簡訊', '求職', '刷單', '兼職', '殺豬盤']
}

# 排除系統與分類檔案
IGNORE_FILES = {
    'README.md', '_sidebar.md', 'about.md', 'investment.md', 
    'crypto.md', 'network.md', 'info.md', 'latest.md', 
    'victims.md', 'withdrawal.md'
}

def extract_title(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line = line.strip()
            if line.startswith('# '):
                return line.replace('# ', '').strip()
    return os.path.splitext(os.path.basename(file_path))[0]

def main():
    md_files = [f for f in os.listdir('.') if f.endswith('.md') and f not in IGNORE_FILES]
    
    cat_posts = {k: [] for k in CATEGORIES}

    for file in md_files:
        title = extract_title(file)
        matched = False
        for cat_file, keywords in CATEGORIES.items():
            if any(kw.lower() in title.lower() for kw in keywords):
                cat_posts[cat_file].append((title, file))
                matched = True
                break
        if not matched:
            # 沒符合的預設放到 network.md
            cat_posts['network.md'].append((title, file))

    titles_map = {
        'investment.md': '# 投資詐騙與黑平台黑幕專區\n\n本專區收錄各類假投資、飆股群組、虛擬交易所黑幕與受害自救指南。\n\n### 📌 最新投資詐騙案例與解析\n',
        'crypto.md': '# 加密貨幣詐騙專區\n\n本專區收錄各類假交易所、偽造空投、黑平台出金問題。\n\n### 📌 案例列表\n',
        'network.md': '# 網路詐騙與交友陷阱專區\n\n本專區收錄各類兼職刷單、交友殺豬盤案例。\n\n### 📌 案例列表\n'
    }

    for cat_file, posts in cat_posts.items():
        if os.path.exists(cat_file):
            header = titles_map.get(cat_file, f"# {cat_file}\n\n")
            links = "\n".join([f"* [{title}]({file})" for title, file in posts])
            with open(cat_file, 'w', encoding='utf-8') as f:
                f.write(header + (links if links else "* 目前尚無文章\n"))

if __name__ == '__main__':
    main()
