import csv
import os
import re

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

dashboard_data = []
count = 0

if not os.path.exists(csv_path):
    print(f"⚠️ エラー: '{csv_path}' が見つかりません。")
else:
    with open(csv_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            url = row.get('url', row.get('店舗URL', ''))
            kasan_list = row.get('kasan_list', row.get('加算届出状況', ''))
            base_html = row.get('web_text', row.get('Webテキスト', ''))
            
            if url:
                match = re.search(r'/shop/([a-zA-Z0-9_-]+)/', url)
                if match:
                    tenant_name = match.group(1)
                    file_name = f"{tenant_name}.html"
                    file_path = os.path.join(output_dir, file_name)
                    
                    final_html = base_html + "\n<hr>\n"
                    has_renkei = "連携強化加算" in kasan_list
                    has_dx = "電子的調剤情報連携体制整備加算" in kasan_list
                    
                    if has_renkei: final_html += HTML_RENKEI
                    if has_dx: final_html += HTML_DX
                        
                    with open(file_path, mode='w', encoding='utf-8') as out_f:
                        out_f.write(final_html)
                    
                    # 💡加算リストの「／」をHTMLの改行「<br>」に変換して見やすくする
                    kasan_formatted = kasan_list.replace("／", "<br>").replace(" ", "")

                    dashboard_data.append({
                        "name": tenant_name,
                        "file": file_name,
                        "kasan_list": kasan_formatted,
                        "has_renkei": has_renkei,
                        "has_dx": has_dx
                    })
                    count += 1

    # ====== 新・目次（ダッシュボード） 白地＆シンプル版 ======
    index_html = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<title>薬局コンプライアンス更新案件（加算対応）</title>
<style>
  body { font-family: sans-serif; font-size: 11px; margin: 10px; background-color: #fff; }
  h1 { font-size: 16px; margin: 0 0 10px 0; color: #333; }
  table { width: 100%; border-collapse: collapse; }
  th, td { border: 1px solid #ccc; padding: 6px; text-align: left; vertical-align: top; }
  th { background-color: #f5f5f5; white-space: nowrap; }
  .kasan-list { font-size: 10px; color: #555; line-height: 1.4; }
  .status-high { color: #d32f2f; font-weight: bold; } /* 赤字 */
  .status-low { color: #f57c00; font-weight: bold; } /* オレンジ字 */
  .status-ok { color: #388e3c; } /* 緑字 */
  a { color: #0066cc; text-decoration: none; font-weight: bold; }
  a:hover { text-decoration: underline; }
</style>
</head>
<body>
  <h1>更新案件一覧（連携強化加算・医療DX加算）</h1>
  <table>
    <thead>
      <tr>
        <th>店舗ID</th>
        <th>更新後ページ</th>
        <th>取得している加算一覧</th>
        <th>対応ステータス</th>
      </tr>
    </thead>
    <tbody>
"""
    for d in dashboard_data:
        # 💡アイコンと短い文字だけのステータス判定
        status_html = ""
        if d['has_renkei']:
            status_html += '<span class="status-high">⚠️連携強化(追加済)</span><br>'
        if d['has_dx']:
            status_html += '<span class="status-low">△医療DX(補強済)</span>'
        
        if not d['has_renkei'] and not d['has_dx']:
            status_html = '<span class="status-ok">✅適合(修正不要)</span>'

        index_html += f"""
      <tr>
        <td style="white-space: nowrap;">{d['name']}</td>
        <td style="white-space: nowrap;"><a href="{d['file']}" target="_blank">📄 ページ確認</a></td>
        <td class="kasan-list">{d['kasan_list']}</td>
        <td style="white-space: nowrap;">{status_html}</td>
      </tr>"""

    index_html += """
    </tbody>
  </table>
</body>
</html>"""

    index_path = os.path.join(output_dir, "index.html")
    with open(index_path, mode='w', encoding='utf-8') as f:
        f.write(index_html)

    print("========================================")
    print(f"🎉 ダッシュボード(index.html)のアップデートが完了しました！")