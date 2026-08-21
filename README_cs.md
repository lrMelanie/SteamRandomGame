# 🎲 Randomat-4000S

Vylosuje náhodnou hru z celé tvé knihovny **Steam Rodiny** (plus tvé vlastní hry).

Jazyky: **English (výchozí), Polski, Español, Français, Português,
Português (BR), Čeština, 简体中文** - vyber v **⚙ Nastavení**. Nastaví také jazyk
žánrů/popisů ze Steamu.
🌐 [English](README.md) · [Polski](README_pl.md) · [Español](README_es.md) · [Français](README_fr.md) · [Português](README_pt.md) · [Português BR](README_br.md) · [Čeština](README_cs.md) · [简体中文](README_zh.md)

## Spuštění (Windows)

1. Nainstaluj Python 3.9+ z https://www.python.org/downloads/ (zaškrtni **"Add Python to PATH"**).
2. Dvakrát klikni na **`Run.bat`**. Při prvním spuštění doinstaluje Pillow a otevře aplikaci.

## Token (nutný pro hry ze Steam Rodiny)

Buď přihlášen(a) do Steamu v prohlížeči a pak:

1. Otevři `store.steampowered.com/pointssummary/ajaxgetasyncconfig`
2. Zkopíruj hodnotu za `"webapi_token"` (začíná `eyJ`).
3. Vlož ji do pole **Token**, klikni **Uložit** a pak **Obnovit**.

Token platí asi jeden den - když přestane fungovat, vlož nový. Ukládá se lokálně.
Tlačítko **Jak získat token** ukazuje tyto kroky v aplikaci.

## Žánry

Klikni **Načíst žánry** pro zapnutí filtru podle žánru. Steam omezuje rychlost,
takže velká knihovna chvíli trvá; běží na pozadí a lze pokračovat později.

## Vlastní obrázky her (volitelné)

V **Nastavení** zadej `...\Steam\userdata\<id>\config\grid`, aby se použily tvé obrázky.

## Motivy, překrytí a zkratky

V **⚙ Nastavení** změníš motiv (Neon, Steam blue, Arcade, Dark gray, High
contrast) a otevřeš **Překrytí** - malé okno vždy navrchu, které položíš přes
Steam; losování tam otevře vylosovanou hru ve tvé knihovně Steam. Mezerník
losuje. Hry mimo Steam přidané do knihovny se také losují.

## Achievementy

Zapni **Zobrazovat achievementy** v **⚙ Nastavení**, abys u vylosované hry viděl
odemčené/celkem, a zaškrtni **lovec achievementů** (vedle jen-nainstalované) pro
náhodný nezískaný achievement k získání. Používá tvůj token; pokud nefunguje,
vlož **Steam API klíč** v Nastavení. Statistiky achievementů musí být veřejné.

## Kde se ukládá nastavení

Tvůj token, motiv, filtry a mezipaměť jsou v `%APPDATA%\SteamRandomGame`
(`config.json`, `cache_games.json`, `cache_metadata.json`) - ne vedle aplikace,
takže veřejná složka nikdy neobsahuje tvůj token. Lze smazat; obnoví se při dalším stažení.
