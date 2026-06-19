#!/bin/bash
set -e

echo "🔍 更新されたMarpファイルを自動検知中..."

# 1. ［自動検知］変更された.mdファイルを抽出
CHANGED_FILES=$(git status --porcelain | grep 'slides/.*\.md$' | awk '{print $2}' || true)
if [ -z "$CHANGED_FILES" ]; then
  CHANGED_FILES=$(git diff --name-only HEAD~1 HEAD | grep 'slides/.*\.md$' || true)
fi

# 2. ［ループ処理］更新されたファイルの数だけHTMLに変換（共通設定ファイルを指定）
for FILE in $CHANGED_FILES; do
  if [ -f "$FILE" ]; then
    BASENAME=$(basename "$FILE" .md)
    OUTPUT_HTML="docs/${BASENAME}.html"
    
    echo "🏗️  更新検知: ${FILE} ➔ ${OUTPUT_HTML} へ組み立て中..."
    marp --config marp.config.yml "$FILE" -o "$OUTPUT_HTML"
  fi
done

# 🌟［自動化］サブ目次ページ（menu.html）を自動作成
echo "🗂️  サブ目次ページ（menu.html）を自動作成中..."
INDEX_FILE="docs/menu.html"

cat << 'html' > "$INDEX_FILE"
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AIナレッジスライド倉庫</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #f5f5f5; color: #333; max-width: 800px; margin: 40px auto; padding: 0 20px; }
        h1 { border-bottom: 2px solid #ccc; padding-bottom: 10px; }
        ul { list-style: none; padding: 0; }
        li { background: white; margin: 10px 0; padding: 15px; border-radius: 6px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
        a { color: #0066cc; text-decoration: none; font-weight: bold; font-size: 1.1rem; width: 100%; display: block; }
        a:hover { color: #004499; text-decoration: underline; }
    </style>
</head>
<body>
    <h1>🗂️ AIナレッジスライド倉庫（サブ目次）</h1>
    <ul>
html

for HTML_FILE in docs/*.html; do
  BF=$(basename "$HTML_FILE")
  if [ "$BF" != "index.html" ] && [ "$BF" != "menu.html" ]; then
    DISPLAY_NAME=$(echo "$BF" | sed 's/\.html//g' | sed 's/_/ /g')
    echo "        <li><a href=\"${BF}\">📄 ${DISPLAY_NAME}</a></li>" >> "$INDEX_FILE"
  fi
done

cat << 'html' >> "$INDEX_FILE"
    </ul>
</body>
</html>
html

# 3. ［出荷］すべての変更をステージング
echo "📦 成果物をステージング中..."
git add .

# 4. ［出荷］自動コミット
COMMIT_MSG="Upgrade: Separate data and design with marp.config.yml: $(date '+%Y-%m-%d %H:%M:%S')"
echo "💾 コミット中: ${COMMIT_MSG}"
git commit -m "${COMMIT_MSG}" || echo "⚠️ 変更なし"

# 5. ［出荷］プッシュ
echo "🚀 GitHubへ送信中..."
git push origin main

echo "✨ deploy.shのアップデートが完了しました！"
