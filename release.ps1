param(
    [string]$NewVersion
)

$versionFile = "version.txt"

# Se não for passado a nova versão manualmente, incrementa o patch da versão atual
if (-not $NewVersion) {
    if (-not (Test-Path $versionFile)) {
        # Se o arquivo não existir, inicializa com 1.0.0
        $NewVersion = "1.0.0"
    }
    else {
        $currentVersion = Get-Content $versionFile | Select-Object -First 1
        $currentVersion = $currentVersion.Trim()
        # Remove qualquer comentário se existir
        if ($currentVersion -match "^\d+\.\d+\.\d+") {
            $currentVersion = $matches[0]
        }
        $parts = $currentVersion -split "\."
        if ($parts.Count -ne 3) {
            Write-Error "Formato de versão inválido no arquivo version.txt"
            exit 1
        }
        # Incrementa o patch
        $major = [int]$parts[0]
        $minor = [int]$parts[1]
        $patch = [int]$parts[2] + 1
        $NewVersion = "$major.$minor.$patch"
    }
}

Write-Host "Preparando release da versão: $NewVersion"

# Atualiza o arquivo version.txt com a nova versão
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
# Se a tag já existir, a função abaixo ignora a criação
$existingTags = git tag
if ($existingTags -notmatch $tagName) {
    git tag $tagName
    Write-Host "Tag criada: $tagName"
}
else {
    Write-Host "Tag $tagName já existe, ela não será recriada."
}

# Faz push dos commits e da tag para o repositório remoto
git push origin
git push origin $tagName

Write-Host "Release enviada! O workflow de release será acionado automaticamente."