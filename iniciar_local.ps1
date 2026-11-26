$ErrorActionPreference = 'Stop'
$myrCredentialFile = Join-Path $PSScriptRoot '.secrets\myr-app.credential.xml'
$myrPython = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $myrCredentialFile)) { throw 'Falta la credencial local de MyR.' }
if (-not (Test-Path -LiteralPath $myrPython)) { throw 'Falta el entorno virtual del proyecto.' }
$myrCredential = Import-Clixml -LiteralPath $myrCredentialFile
try {
    $env:PGPASSWORD = $myrCredential.GetNetworkCredential().Password
    Set-Location -LiteralPath $PSScriptRoot
    & $myrPython -m streamlit run app.py --server.address 127.0.0.1
} finally {
    Remove-Item Env:PGPASSWORD -ErrorAction SilentlyContinue
}

