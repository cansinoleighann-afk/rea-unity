param(
    [string]$ArchivePath,
    [string]$Destination = (Join-Path $PSScriptRoot '../.cache/assetripper/2.0.0/win-x64')
)

$ErrorActionPreference = 'Stop'
$expectedHash = '9A7EF0E7C5C3EA5B90B4E6D855E2D98D5F7EC8C3F9E26FCCBC194C6A7B01BAF7'
$url = 'https://github.com/AssetRipper/AssetRipper/releases/download/2.0.0/AssetRipper_win_x64.zip'
$destinationPath = [IO.Path]::GetFullPath($Destination)
if (Test-Path -LiteralPath $destinationPath) {
    throw "Destination already exists; refusing to overwrite: $destinationPath"
}

$temporaryArchive = $null
try {
    if (-not $ArchivePath) {
        $temporaryArchive = Join-Path ([IO.Path]::GetTempPath()) ("rea-assetripper-" + [guid]::NewGuid().ToString('N') + '.zip')
        Invoke-WebRequest -Uri $url -OutFile $temporaryArchive
        $ArchivePath = $temporaryArchive
    }
    $actualHash = (Get-FileHash -LiteralPath $ArchivePath -Algorithm SHA256).Hash
    if ($actualHash -ne $expectedHash) {
        throw "Archive SHA-256 mismatch: $actualHash"
    }
    # The checked digest identifies the upstream archive; no unverified ZIP is extracted.
    Expand-Archive -LiteralPath $ArchivePath -DestinationPath $destinationPath
    $executable = Join-Path $destinationPath 'AssetRipper.GUI.Free.exe'
    if (-not (Test-Path -LiteralPath $executable -PathType Leaf)) {
        throw "Expected executable missing: $executable"
    }
    Write-Output "AssetRipper 2.0.0 installed: $executable"
    Write-Output 'The tool was not started. Close the tool before exporting over any existing session.'
} finally {
    if ($temporaryArchive -and (Test-Path -LiteralPath $temporaryArchive)) {
        Remove-Item -LiteralPath $temporaryArchive
    }
}
