import csv
import os
import re

csv_path = "生成結果.csv"
output_dir = "outputs/web_html"
os.makedirs(output_dir, exist_ok=True)

count = 0
if not os.path.exists(csv_path):
    print(f"⚠️ エラー: '{csv_path}' が見つかりません。アップロードを確認してください。")
else:
    with open(csv_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # 列名はスプシに合わせて柔軟に取得
            url = row.get('url', row.get('店舗URL', ''))
            # GASで生成したHTMLの列名（適宜合わせています）
            html_content = row.get('更新後Webテキスト（完成版HTML）', row.get('完成版HTML', row.get('Webテキスト', '')))
            
            if url and html_content and html_content.strip():
                match = re.search(r'/shop/([a-zA-Z0-9_-]+)/', url)
                if match:
                    tenant_name = match.group(1)
                    file_name = f"{tenant_name}.html"
                    file_path = os.path.join(output_dir, file_name)
                    
                    # 個別HTMLファイルとして保存
                    with open(file_path, mode='w', encoding='utf-8') as out_f:
                        out_f.write(html_content)
                    print(f"✅ 保存完了: {file_name}")
                    count += 1
    print("========================================")
    print(f"🎉 全 {count} 店舗のHTMLファイル保存が完了しました！")
