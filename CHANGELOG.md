# Changelog

## [1.0.0] - 2026-05-17

### Added
- Initial release
- Real-time synced Spotify lyrics display in Conky
- LRCLIB API integration with artist-name matching
- Multi-monitor support (left + right display)
- Karaoke-style current line highlighting with ❯ indicator
- Progress bar showing playback position
- Plain lyrics fallback with even time distribution
- Local lyrics caching to minimize API calls
- Sarasa Mono J font for CJK character support
- Auto-start via bspwmrc / conky-startup.sh

### CI/CD
- GitHub Actions CI: Python syntax + shell syntax + Conky config checks
- GitHub Actions Release: auto-builds tar.gz, zip, PKGBUILD on version tags
- Auto-generated SHA256 checksums for all release artifacts

### Dependencies
- Python 3.8+
- playerctl
- conky (with XFT support)
