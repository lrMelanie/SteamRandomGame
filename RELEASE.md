# 🎲 SRG v1.0.0 - Steam Random Game

Official first release of **SRG (Steam Random Game)** - a small desktop app that
picks a random game from your **whole Steam Family library** (plus your own and
non-Steam games), so you can stop scrolling and just play.

## Features

- Random pick from the **whole Steam Family** library + your own + non-Steam games
- Filters: genre, unplayed only, installed only, by family account
- **Achievement hunter** - also draws a random achievement to earn, plus optional unlocked/total counter
- Roll one or several games at once, with a synced cover + title animation
- **Blocklist** to keep games out of the draw, remembered filters, roll history
- **Steam overlay** - a small always-on-top window that opens the pick in your library
- 5 themes (Neon, Steam blue, Arcade, Dark gray, High contrast)
- 8 interface languages: EN, PL, ES, FR, PT, PT-BR, CS, ZH
- Uses your custom Steam grid art; window icon changes to the rolled game
- `Space` = roll

## Run (Windows)

1. Install Python 3.9+ (tick "Add Python to PATH").
2. Double-click `Run.bat` (first launch installs Pillow automatically).

To pull Steam Family games you paste a one-time access token - the in-app
**How to get token** button walks you through it. Your token and settings stay
local in `%APPDATA%\SteamRandomGame`.

See the README (available in 8 languages) for full details.
