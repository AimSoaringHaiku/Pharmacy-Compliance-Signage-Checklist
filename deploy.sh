#!/bin/bashset -e  # 👈 どこかでエラーが起きたらその場で安全に止まるおまじない
# 1. ［自動化］MarpのMarkdownを、公開用の縦スクロールHTMLに自動変換！
echo "🏗️ MarpスライドをHTMLに組み立て中..."
marp slides/presentation.md -o docs/index.html
# 2. ［自動化］すべての変更フォルダ（_docs, slides, docs）をステージング
echo "📦 すべてのファイルをステージング中..."
git add .
# 3. ［自動化］今日の日付と時間で自動コミット
COMMIT_MSG="Update slideshow: $(date '+%Y-%m-%d %H:%M:%S')"
echo "💾 コミット中: ${COMMIT_MSG}"
git commit -m "${COMMIT_MSG}"
# 4. ［自動化］GitHubへ安全に出荷（プッシュ）！
echo "🚀 GitHubへ送信中..."
git push origin main

echo "✨ スライド変換からGitHub世界公開まで、すべて安全に完了しました！"