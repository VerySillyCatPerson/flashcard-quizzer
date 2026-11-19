param([switch]$SkipInteractive)

# All learning state and exports stay in a fresh temporary directory.
$quizRoot = Split-Path -Parent $PSScriptRoot
$quizPython = Join-Path $quizRoot '.venv\Scripts\python.exe'
$quizEntry = Join-Path $quizRoot 'main.py'
$quizTemp = Join-Path ([IO.Path]::GetTempPath()) ('flashcard-manual-' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $quizTemp | Out-Null
$quizDeck = Join-Path $quizTemp 'deck.json'
$quizHistory = Join-Path $quizTemp 'history.json'
$quizExport = Join-Path $quizTemp 'results.json'
'[{"front":"A","back":"Alpha"},{"front":"B","back":"Beta"},{"front":"C","back":"Gamma"}]' | Set-Content -LiteralPath $quizDeck -Encoding UTF8

& $quizPython $quizEntry --help # Expected: usage; exit 0.
' alpha ', 'wrong', 'GAMMA' | & $quizPython $quizEntry -f $quizDeck --history $quizHistory --export $quizExport
Write-Host "Sequential exit: $LASTEXITCODE (expected 0; 2/3, 66.67%, missed #2 B)"
Get-Content -Raw -LiteralPath $quizExport | ConvertFrom-Json | Select-Object answered_count, correct_count, accuracy_percent
'beta', 'alpha', 'gamma' | & $quizPython $quizEntry -f $quizDeck -m adaptive --history $quizHistory
Write-Host "Adaptive exit: $LASTEXITCODE (expected 0; order B,A,C; 100%)"
'wrong', 'wrong', 'wrong' | & $quizPython $quizEntry -f $quizDeck -m random --seed 7 --history $quizHistory
Write-Host "Random exit: $LASTEXITCODE (expected 0; each card once; same seed reproduces order)"
'alpha' | & $quizPython $quizEntry -f $quizDeck --history $quizHistory --export (Join-Path $quizTemp 'partial.json')
Write-Host "EOF exit: $LASTEXITCODE (expected 1; partial 1/3, 100%, no missed cards)"
& $quizPython $quizEntry -f $quizDeck --history $quizHistory --export $quizDeck
Write-Host "Conflict exit: $LASTEXITCODE (expected 2; no quiz or file changes)"
$quizBadHistory = Join-Path $quizTemp 'corrupt.json'
'{bad history' | Set-Content -LiteralPath $quizBadHistory -Encoding UTF8
'alpha', 'beta', 'gamma' | & $quizPython $quizEntry -f $quizDeck -m adaptive --history $quizBadHistory --export (Join-Path $quizTemp 'degraded.json')
Write-Host "Corrupt-history exit: $LASTEXITCODE (expected 1; warning, 100%, corrupt file preserved, export written)"
'alpha', 'beta', 'gamma' | & $quizPython $quizEntry -f $quizDeck --history $quizHistory --export $quizTemp --overwrite
Write-Host "Export-failure exit: $LASTEXITCODE (expected 1; summary/history retained)"
$quizOverwriteHistory = Join-Path $quizTemp 'overwrite-history.json'
$quizOriginalExportHash = (Get-FileHash -LiteralPath $quizExport).Hash
'alpha', 'beta', 'gamma' | & $quizPython $quizEntry -f $quizDeck --history $quizOverwriteHistory --export $quizExport
Write-Host "Export-refusal exit: $LASTEXITCODE (expected 1; existing export preserved; history updated)"
$quizRefusedExportHash = (Get-FileHash -LiteralPath $quizExport).Hash
Write-Host "Refusal preserved bytes: $($quizOriginalExportHash -eq $quizRefusedExportHash) (expected True)"
'alpha', 'beta', 'gamma' | & $quizPython $quizEntry -f $quizDeck --history $quizOverwriteHistory --export $quizExport --overwrite
Write-Host "Authorized-overwrite exit: $LASTEXITCODE (expected 0; replacement has 3 correct; history updated normally)"
Write-Host "Temporary artifacts retained for inspection: $quizTemp"

if (-not $SkipInteractive) {
    Write-Host 'Enter alpha, then press Ctrl+C at the next prompt. Expected: partial summary and application status 130.'
    & $quizPython $quizEntry -f $quizDeck --history $quizHistory --export (Join-Path $quizTemp 'interrupted.json')
    Write-Host "Ctrl+C exit: $LASTEXITCODE (expected 130). If the host stopped this script, inspect `$LASTEXITCODE at the prompt."
}
