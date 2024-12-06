<#
.SYNOPSIS
    Creates GitHub releases and tags for the Vector SDK project.

.DESCRIPTION
    This script automates the release process for Vector SDK by:
    1. Creating git tags
    2. Pushing changes to GitHub
    3. Creating GitHub releases (either pre-release or full release)

    The script reads the current version from pyproject.toml and creates appropriate
    releases based on whether it's a release candidate (rc) or full release.

.PARAMETER version_type
    Specifies the type of release to create:
    - 'rc' for release candidates
    - 'release' for full releases

.EXAMPLE
    # First bump the version using bump_version.py
    python bump_version.py rc        # Bumps to next RC version (e.g., 0.1.1rc1)
    .\release.ps1 rc                # Creates a pre-release

    # For full releases
    python bump_version.py release   # Converts RC to release version (e.g., 0.1.1)
    .\release.ps1 release           # Creates a full release

.NOTES
    Prerequisites:
    - GitHub CLI (gh) must be installed and authenticated
    - Git must be configured
    - Must be run from the root directory of the project
    - Version must be already bumped using bump_version.py

    Files Modified:
    - Creates git tags
    - Creates GitHub releases
    - Pushes changes to remote repository

    Version Format:
    - Follows semantic versioning (X.Y.Z or X.Y.ZrcN)
    - RC versions are marked as pre-releases
    - Full versions are marked as latest releases

.LINK
    GitHub Repository: https://github.com/AI-Northstar-Tech/vector-sdk
#>

param(
    [Parameter(Mandatory=$true)]
    [string]$version_type
)

# Get current branch name
$current_branch = git rev-parse --abbrev-ref HEAD

# Get the new version from pyproject.toml
$version = (Select-String -Path "pyproject.toml" -Pattern 'version = "(.*?)"').Matches.Groups[1].Value

# Check if this is a pre-release (contains 'rc')
$isPrerelease = $version -match "rc"

# Create a git tag
git add .
git commit -m "Bump version to $version"
git tag -a "v$version" -m "Release version $version"
git push origin $current_branch --tags

# Create a GitHub release with prerelease flag if it's an RC
if ($isPrerelease) {
    gh release create "v$version" --prerelease --title "Pre-release v$version" --notes "Release candidate version $version"
} else {
    gh release create "v$version" --title "Release v$version" --notes "Release version $version"
}