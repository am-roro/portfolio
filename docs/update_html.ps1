$dir = "c:\Users\amokr\Documents\portfolio"
$files = Get-ChildItem -Path $dir -Filter "*.html"

foreach ($file in $files) {
    # Read the file content
    $content = Get-Content -Path $file.FullName -Raw -Encoding UTF8

    # Apply regex replacements
    $content = [regex]::Replace($content, '(?i)Rosa\s+Amokrane', 'ROSA')
    $content = [regex]::Replace($content, '(?i)ROSA_AMOKRANE', 'ROSA')
    $content = [regex]::Replace($content, '(?i)rosa-amokrane', 'rosa')
    $content = [regex]::Replace($content, '(?i)\s*amokrane', '')
    
    # Remove img tags
    $content = [regex]::Replace($content, '(?i)<img[^>]*>', '')

    # Save the modified content back
    [System.IO.File]::WriteAllText($file.FullName, $content, [System.Text.Encoding]::UTF8)
}
Write-Output "PowerShell Script: Replacements complete."
