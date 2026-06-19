#!/bin/bash
set -e

echo "📦 新しい原稿（.md）をそのままGitHubへ出荷します..."

INDEX_FILE="docs/menu.md"
echo "# 🗂 AIナレッジ倉庫（サブ目次）" > "$INDEX_FILE"
echo "ファイルを追加してデプロイするだけで、以下に自動でカテゴリ分けされたリンクが生成されます。" >> "$INDEX_FILE"
echo "" >> "$INDEX_FILE"

# 一時的な作業フォルダを作成
TMP_DIR=$(mktemp -d)

# docs内の .md ファイルをループ処理
for FILE in docs/*.md; do
  BF=$(basename "$FILE")
  
  # システム系のファイル（READMEや既存の01~03）は一覧から除外
  if [ "$BF" = "menu.md" ] || [ "$BF" = "README.md" ] || [[ "$BF" =~ ^0[1-3]_.* ]]; then
    continue
  fi
  
  # アンダースコアをスペースにして見やすい名前に
  DISPLAY_NAME=$(echo "$BF" | sed 's/\.md//g' | sed 's/_/ /g')
  
  # 🔍 【ここでブロック分けを自動判定】ファイル名に含まれる文字でカテゴリを決定
  case "$BF" in
    *Risk_Verification*|*Collaboration_Addition*)
      CATEGORY="監査・リスク検証ルール"
      ;;
    *Web_Column*|*Request_Letter*)
      CATEGORY="Web更新・現場への依頼書"
      ;;
    *for_human*|*presentation*)
      CATEGORY="人間用プレゼン・一覧資料"
      ;;
    *)
      CATEGORY="その他のドキュメント"
      ;;
  esac

  # 判定したカテゴリ名の一時ファイルにリンクを書き込む
  echo "- [$DISPLAY_NAME]($BF)" >> "$TMP_DIR/$CATEGORY.txt"
done

# カテゴリごとに menu.md に見出しを作って結合する
for CAT_FILE in "$TMP_DIR"/*.txt; do
  if [ -f "$CAT_FILE" ]; then
    CAT_NAME=$(basename "$CAT_FILE" .txt)
    echo "## 📌 $CAT_NAME" >> "$INDEX_FILE"
    cat "$CAT_FILE" >> "$INDEX_FILE"
    echo "" >> "$INDEX_FILE"
  fi
done

# お掃除
rm -rf "$TMP_DIR"

# 出荷処理
git add .
COMMIT_MSG="Deploy markdown notes with Auto-Categories: $(date '+%Y-%m-%d %H:%M:%S')"
git commit -m "${COMMIT_MSG}" || echo "⚠️ 変更なし"
git push origin main

echo "✨ 自動ブロック分け目次（menu.md）の生成と出荷が完了しました！"
