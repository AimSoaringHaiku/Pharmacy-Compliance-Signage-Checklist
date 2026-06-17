import csv
import os
import re

# 1. 読み込むCSV
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

# 目次（ダッシュボード）用のデータを貯める箱
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
                    
                    if has_renkei:
                        final_html += HTML_RENKEI
                    if has_dx:
                        final_html += HTML_DX
                        
                    with open(file_path, mode='w', encoding='utf-8') as out_f:
                        out_f.write(final_html)
                    
                    # ダッシュボード用に情報を記録
                    dashboard_data.append({
                        "name": tenant_name,
                        "file": file_name,
                        "has_renkei": has_renkei,
                        "has_dx": has_dx
                    })
                    count += 1

    # ====== ここから時短テク：目次（ダッシュボード）index.html の自動生成 ======
    index_html = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<title>薬局コンプライアンス監査・更新ダッシュボード</title>
<style>
  body { font-family: sans-serif; font-size: 11px; margin: 10px; } /* 余白少なめ・小さめ */
  h1 { font-size: 16px; margin: 0 0 10px 0; }
  table { width: 100%; border-collapse: collapse; }
  th, td { border: 1px solid #999; padding: 4px; text-align: left; }
  th { background-color: #eee; white-space: nowrap; }
  .risk-high { background-color: #ffebee; color: #c62828; font-weight: bold; } /* 薄い赤色 */
  .risk-low { background-color: #fff9c4; color: #2e7d32; } /* 薄い黄色 */
  a { color: #0066cc; text-decoration: none; }
  a:hover { text-decoration: underline; }
  @media print {
    body { font-size: 10px; }
    a { color: #000; text-decoration: none; }
  }
</style>
</head>
<body>
  <h1>薬局Webサイト コンプライアンス監査・更新一覧（最新ルール適用版）</h1>
  <p>※以下は最新の施設基準に適合するよう自動生成された修正後ページへのリンクです。印刷時はそのままA4に収まります。</p>
  <table>
    <thead>
      <tr>
        <th>店舗URL(ID)</th>
        <th>更新後ページ</th>
        <th>連携強化加算<br>(災害体制)</th>
        <th>医療DX加算<br>(情報活用)</th>
        <th>修正前リスク・今回の対応内容</th>
      </tr>
    </thead>
    <tbody>
"""
    for d in dashboard_data:
        renkei_str = "あり" if d['has_renkei'] else "なし"
        dx_str = "あり" if d['has_dx'] else "なし"
        
        if d['has_renkei']:
            risk_class = "risk-high"
            status_text = "⚠️重大不備(返還ﾘｽｸ) → 災害対応テキストを追加済"
        elif d['has_dx']:
            risk_class = "risk-low"
            status_text = "△文言不足(指導ﾘｽｸ) → 医療DXの具体文言を補強済"
        else:
            risk_class = ""
            status_text = "適合（修正不要）"

        index_html += f"""
      <tr class="{risk_class}">
        <td>{d['name']}</td>
        <td><a href="{d['file']}" target="_blank">📄 完成版を確認</a></td>
        <td>{renkei_str}</td>
        <td>{dx_str}</td>
        <td>{status_text}</td>
      </tr>"""

    index_html += """
    </tbody>
  </table>
</body>
</html>"""

    # index.htmlを保存
    index_path = os.path.join(output_dir, "index.html")
    with open(index_path, mode='w', encoding='utf-8') as f:
        f.write(index_html)

    print("========================================")
    print(f"🎉 全 {count} 店舗のHTML保存 ＋ ダッシュボード(index.html)の作成が完了しました！")