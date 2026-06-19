#!/bin/bash
set -e

echo "🔍 更新されたMarpファイルを自動検知中..."

# 1. ［自動検知］Gitのステージングや直前のコミットから、変更された.mdファイルを抽出
# (slides/ フォルダ内の .md ファイルだけを対象にします)
CHANGED_FILES=$(git status --porcelain | grep 'slides/.*\.md$' | awk '{print $2}' || true)

# もし未ステージングの変更がない場合、直前のコミット（HEAD）の変更点も探す
if [ -z "$CHANGED_FILES" ]; then
  CHANGED_FILES=$(git diff --name-only HEAD~1 HEAD | grep 'slides/.*\.md$' || true)
fi

# 変更されたファイルがない場合は安全に終了
if [ -z "$CHANGED_FILES" ]; then
  echo "✅ 更新されたMarpファイル（.md）は見つかりませんでした。処理を終了します。"
  exit 0
fi

# 2. ［ループ処理］更新されたファイルの数だけHTMLに変換
for FILE in $CHANGED_FILES; do
  if [ -f "$FILE" ]; then
    # ファイル名から拡張子を除いた名前でHTMLを書き出す (例: presentation2.html)
    BASENAME=$(basename "$FILE" .md)
    OUTPUT_HTML="docs/${BASENAME}.html"
    
    echo "🏗️  更新検知: ${FILE} ➔ ${OUTPUT_HTML} へ組み立て中..."
    marp "$FILE" -o "$OUTPUT_HTML"
  fi
done

# 3. ［自動化］すべての変更をステージング
echo "📦 成果物をステージング中..."
git add .

# 4. ［自動化］自動コミット
COMMIT_MSG="Auto-deploy updated slides: $(date '+%Y-%m-%d %H:%M:%S')"
echo "💾 コミット中: ${COMMIT_MSG}"
git commit -m "${COMMIT_MSG}" || echo "⚠️ 変更内容がなかったためコミットをスキップします"

# 5. ［自動化］出荷（プッシュ）
echo "🚀 GitHubへ送信中..."
git push origin main

echo "✨ すべての更新ファイルの出荷が安全に完了しました！"
