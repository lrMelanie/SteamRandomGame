# 🎲 Randomat-4000S

Pick a random game from your whole **Steam Family** library (plus your own games).

Languages: **English (default), Polski, Español, Français, Português,
Português (BR), Čeština, 简体中文** — pick one in **⚙ Settings**. It also sets the
language of genres/descriptions from Steam.
🌐 [English](README.md) · [Polski](README_pl.md) · [Español](README_es.md) · [Français](README_fr.md) · [Português](README_pt.md) · [Português BR](README_br.md) · [Čeština](README_cs.md) · [简体中文](README_zh.md)

## Run (Windows)

1. Install Python 3.9+ from https://www.python.org/downloads/ (tick **"Add Python to PATH"**).
2. Double-click **`Run.bat`**. First run installs Pillow and opens the app.

## Token (needed for Steam Family)

Be logged in to Steam in your browser, then:

1. Open `store.steampowered.com/pointssummary/ajaxgetasyncconfig`
2. Copy the value after `"webapi_token"` (starts with `eyJ`).
3. Paste it in **Token**, click **Save**, then **Refresh**.

The token lasts about a day — paste a new one when it stops. It's stored locally
in `config.json`. The **How to get token** button shows these steps in the app.

## Genres

Click **Get genres** to enable the genre filter. Steam rate-limits this, so a big
library takes a while; it runs in the background and can resume later.

## Custom cover art (optional)

In **Settings**, point to `...\Steam\userdata\<id>\config\grid` to use your own covers.

## Themes & overlay

Open **⚙ Settings** to switch theme (Neon, Steam blue, Arcade, Dark gray, High
contrast). The **Overlay** button opens a small always-on-top window you can
float over Steam; rolling there opens the picked game in your Steam library.

## Where settings are stored

Your token, theme, filters and caches live in `%APPDATA%\SteamRandomGame`
(`config.json`, `cache_games.json`, `cache_metadata.json`) — not next to the
app, so the public folder never holds your token. Safe to delete; rebuilt on
the next download.
