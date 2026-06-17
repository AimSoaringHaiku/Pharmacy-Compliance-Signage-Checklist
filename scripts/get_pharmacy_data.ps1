[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
$ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

Write-Host "ステップ1：URL取得中..."
$listUrl = "https://www.merhalsa.jp/yakkyoku/shop/"
$html = (Invoke-WebRequest -Uri $listUrl -UseBasicParsing -UserAgent $ua).Content

$urlList = @()
$matches = [regex]::Matches($html, 'href="([^"]+)"')
foreach ($m in $matches) {
    $u = $m.Groups[1].Value
    if ($u -match "[a-zA-Z0-9_-]+/(index\.php)?$" -and $u -notmatch "\.css$|\.js$|\.png$|\.jpg$|#") {
        if ($u -match "^/") { $u = "https://www.merhalsa.jp" + $u }
        elseif ($u -notmatch "^http") { $u = "https://www.merhalsa.jp/yakkyoku/shop/" + $u }
        if ($u -match "/shop/[a-zA-Z0-9_-]+/" -and $urlList -notcontains $u) { $urlList += $u }
    }
}

if ($urlList.Count -eq 0) {
    Write-Host "エラー: URL取得0件。ブラウザ偽装でも弾かれたか、HTML構造が変わりました。"
    return
}
Write-Host ("取得成功: " + $urlList.Count + " 件")

$results = @()
$counter = 1
foreach ($target in $urlList) {
    Write-Host ("[" + $counter + "/" + $urlList.Count + "] 抽出中: " + $target)
    try {
        $text = ((Invoke-WebRequest -Uri $target -UseBasicParsing -UserAgent $ua).Content -replace '<br\s*/?>', "`n") -replace '<[^>]+>', ""
        $kasan = "記載なし"; $web = "記載なし"
        if ($text -match '(?s)施設基準の届出(?<c>.*?)居宅療養管理指導について') { $kasan = $matches['c'].Trim() -replace "`n|`r", " " }
        if ($text -match '(?s)WEBサービス(?<c>.*?)アクセス & MAP') { $web = $matches['c'].Trim() -replace "`n|`r", " " }
        $results += [PSCustomObject]@{ URL=$target; 加算=$kasan; Web=$web }
    } catch {
        Write-Host "取得エラー"
        $results += [PSCustomObject]@{ URL=$target; 加算="エラー"; Web="エラー" }
    }
    $counter++
    Start-Sleep -Seconds 2
}

$results | Export-Csv -Path (Join-Path ([Environment]::GetFolderPath("Desktop")) "店舗加算状況リスト.csv") -Encoding UTF8 -NoTypeInformation
Write-Host "完了！デスクトップにCSVを保存しました。"