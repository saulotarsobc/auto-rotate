param(
    [string]$NewVersion
)

$versionFile = "version.txt"

if (-not $NewVersion) {
    if (-not (Test-Path $versionFile)) {
        
        $NewVersion = "1.0.0"
    }
    else {
        $currentVersion = Get-Content $versionFile | Select-Object -First 1
        $currentVersion = $currentVersion.Trim()
        
        if ($currentVersion -match "^\d+\.\d+\.\d+") {
            $currentVersion = $matches[0]
        }
        $parts = $currentVersion -split "\."
        if ($parts.Count -ne 3) {
            Write-Error "Formato de versão inválido no arquivo version.txt"
            exit 1
        }
        
        $major = [int]$parts[0]
        $minor = [int]$parts[1]
        $patch = [int]$parts[2] + 1
        $NewVersion = "$major.$minor.$patch"
    }
}

Write-Host "Preparando release da versão: $NewVersion"

Set-Content -Path $versionFile -Value $NewVersion

git add .

$commitMsg = "Release version $NewVersion"
$commitResult = git commit -m $commitMsg 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Nenhum commit realizado ou ocorreu um erro: $commitResult" -ForegroundColor Yellow
    exit 1
}
else {
    Write-Host "Commit realizado: $commitMsg" -ForegroundColor Blue
}

$tagName = "v$NewVersion"

$existingTags = git tag
if ($existingTags -notmatch $tagName) {
    git tag $tagName
    Write-Host "Tag criada: $tagName" -ForegroundColor Blue
}
else {
    Write-Host "Tag $tagName já existe, ela não será recriada." -ForegroundColor Yellow
}

git push origin
git push origin $tagName

Write-Host "Release enviada! O workflow de release será acionado automaticamente." -ForegroundColor Green