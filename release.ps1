param(
    [string]$NewVersion
)

# Se a versão não for fornecida via parâmetro, usa a do arquivo version.txt
$versionFile = "version.txt"
if (-not $NewVersion) {
    if (-not (Test-Path $versionFile)) {
        Write-Error "Arquivo version.txt não encontrado!"
        exit 1
    }
    $NewVersion = Get-Content $versionFile | Select-Object -First 1
    $NewVersion = $NewVersion.Trim()
}

Write-Host "Preparando release da versão: $NewVersion"

# Atualiza o arquivo version.txt com a nova versão (caso o arquivo precise ser alterado)
Set-Content -Path $versionFile -Value $NewVersion

# Adiciona todos os arquivos modificados
git add .

# Cria o commit com a mensagem de release
$commitMsg = "Release version $NewVersion"
$commitResult = git commit -m $commitMsg 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Nenhum commit realizado ou ocorreu um erro: $commitResult"
}
else {
    Write-Host "Commit realizado: $commitMsg"
}

# Cria a tag no formato v<versão>
$tagName = "v$NewVersion"
git tag $tagName
Write-Host "Tag criada: $tagName"

# Faz push dos commits e da tag para o repositório remoto
git push origin
git push origin $tagName

Write-Host "Release enviada! O workflow de release será acionado automaticamente."