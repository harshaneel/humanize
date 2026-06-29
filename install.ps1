# PowerShell script to install humanize and ai-check skills for any agent that reads from a skills directory on Windows.
#
# Usage:
#   .\install.ps1                  # Claude Code     (~/.claude/skills)
#   .\install.ps1 codex            # Codex CLI       (~/.codex/skills)
#   .\install.ps1 chatgpt          # ChatGPT agents  (~/.agents/skills)
#   .\install.ps1 all              # all three of the above
#   .\install.ps1 -Copy            # copy files instead of symlinking
#   .\install.ps1 all -Copy        # combinable with any target

$Target = "claude"
$Mode = "symlink"

foreach ($arg in $args) {
    switch -Regex ($arg) {
        "(?i)^claude$"  { $Target = "claude" }
        "(?i)^codex$"   { $Target = "codex" }
        "(?i)^chatgpt$" { $Target = "chatgpt" }
        "(?i)^all$"     { $Target = "all" }
        "(?i)^-copy$"   { $Mode = "copy" }
        "(?i)^-h|--help$" {
            Write-Host "Usage:"
            Write-Host "  .\install.ps1                  # Install for Claude Code"
            Write-Host "  .\install.ps1 codex            # Install for Codex CLI"
            Write-Host "  .\install.ps1 chatgpt          # Install for ChatGPT agents"
            Write-Host "  .\install.ps1 all              # Install for all three"
            Write-Host "  .\install.ps1 -Copy            # Copy files instead of symlinking"
            exit 0
        }
        Default {
            Write-Error "Unknown argument: $arg`nRun with -h or --help for usage."
            exit 1
        }
    }
}

$RepoDir = $PSScriptRoot
if (-not $RepoDir) {
    $RepoDir = Get-Location
}

$Skills = @("humanize", "ai-check")
$Dests = @()

$HomeDir = [System.Environment]::GetFolderPath("UserProfile")

switch ($Target) {
    "claude"  { $Dests += Join-Path $HomeDir ".claude\skills" }
    "codex"   { $Dests += Join-Path $HomeDir ".codex\skills" }
    "chatgpt" { $Dests += Join-Path $HomeDir ".agents\skills" }
    "all"     {
        $Dests += Join-Path $HomeDir ".claude\skills"
        $Dests += Join-Path $HomeDir ".codex\skills"
        $Dests += Join-Path $HomeDir ".agents\skills"
    }
}

function Install-Into($dest) {
    if (-not (Test-Path $dest)) {
        New-Item -ItemType Directory -Force -Path $dest | Out-Null
    }
    
    Write-Host "`nInstalling skills to $dest (mode: $Mode)"
    
    foreach ($skill in $Skills) {
        $src = Join-Path $RepoDir $skill
        $dst = Join-Path $dest $skill
        
        if (-not (Test-Path $src)) {
            Write-Host "  SKIP $skill (missing source directory $src)"
            continue
        }
        
        if (Test-Path $dst) {
            Write-Host "  removing existing $dst"
            Remove-Item -Recurse -Force $dst
        }
        
        if ($Mode -eq "symlink") {
            # Directory junctions do not require admin privileges on Windows
            New-Item -ItemType Junction -Path $dst -Value $src | Out-Null
            Write-Host "  linked $skill (Junction)"
        } else {
            Copy-Item -Recurse -Force -Path $src -Destination $dst
            Write-Host "  copied $skill"
        }
    }
}

foreach ($dest in $Dests) {
    Install-Into $dest
}

Write-Host "`nDone. Restart your agent (or run /reload-skills in Claude Code) to pick up the new skills."
Write-Host "Try it: ask your agent to 'humanize this paragraph' or 'run ai-check on this text'."
