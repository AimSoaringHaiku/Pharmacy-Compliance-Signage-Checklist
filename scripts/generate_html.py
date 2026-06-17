import csv
import os
import re

# 1. 読み込むCSV（Difyに入れる前の軽いデータでOKです）
csv_path = "生成結果.csv" 
output_dir = "outputs/web_html"
os.makedirs(output_dir, exist_ok=True)

# ====== 追加する完成版HTMLブロック ======
HTML_RENKEI = """
<h3>災害や新興感染症発生時における対応体制（連携強化加算）</h3>
<p>当薬局は、地域の行政機関や医療機関等と連携し、非常時に以下の対応を行う体制を整えています。</p>
<ul>
  <li>都道府県等の要請に応じ、災害や感染症発生時に医薬品の供給や調剤等の対応を実施します。</li>
  <li>第二種協定指定医療機関として、新興感染症発生時における医療提供体制の確保に協力します。</li>
</ul>
"""

HTML_DX = """
<h3>医療DX推進の体制・情報活用について（電子的調剤情報連携体制整備加算）</h3>
<p>当薬局では、医療DXを推進し質の高い医療を提供するため、以下の体制を整備しています。</p>
<ul>
  <li>オンライン資格確認システム等を通じて患者様の診療情報・薬剤情報等を取得し、調剤・服薬指導に活用しています。</li>
  <li>マイナ保険証の利用促進など、医療DXを通じた質の高い医療の提供に取り組んでいます。</li>
  <li>電子処方せんの受付や、電子カルテ情報共有サービス（今後導入予定）を活用する体制を整えています。</li>
</ul>
"""
# ====================================

count = 0

if not os.path.exists(csv_path):
    print(f"⚠️ エラー: '{csv_path}' が見つかりません。")
else:
    with open(csv_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # 列名はスプシに合わせて適宜取得（url, 店舗URLなど）
            url = row.get('url', row.get('店舗URL', ''))
            kasan_list = row.get('kasan_list', row.get('加算届出状況', ''))
            base_html = row.get('web_text', row.get('Webテキスト', ''))
            
            if url:
                # URLからテナント名を抽出
                match = re.search(r'/shop/([a-zA-Z0-9_-]+)/', url)
                if match:
                    tenant_name = match.group(1)
                    file_name = f"{tenant_name}.html"
                    file_path = os.path.join(output_dir, file_name)
                    
                    # ベースのテキストに、加算状況に応じてHTMLを自動合体！
                    final_html = base_html + "\n<hr>\n"
                    
                    if "連携強化加算" in kasan_list:
                        final_html += HTML_RENKEI
                        
                    if "電子的調剤情報連携体制整備加算" in kasan_list:
                        final_html += HTML_DX
                    
                    # UTF-8でHTMLファイルとして書き出し
                    with open(file_path, mode='w', encoding='utf-8') as out_f:
                        out_f.write(final_html)
                    
                    print(f"✅ 保存完了: {file_name} (連携強化加算: {'連携強化加算' in kasan_list})")
                    count += 1

    print("========================================")
    print(f"🎉 全 {count} 店舗のHTML自動合体＆ファイル保存が完了しました！")