# 🎲 Randomat-4000S

Losuje grę z całej biblioteki **Rodziny Steam** (plus Twoje własne gry).

Języki: **English (domyślny), Polski, Español, Français, Português,
Português (BR), Čeština, 简体中文** - wybierasz w **⚙ Ustawieniach**. Ustawia też
język gatunków/opisów pobieranych ze Steama.
🌐 [English](README.md) · [Polski](README_pl.md) · [Español](README_es.md) · [Français](README_fr.md) · [Português](README_pt.md) · [Português BR](README_br.md) · [Čeština](README_cs.md) · [简体中文](README_zh.md)

## Uruchomienie (Windows)

1. Zainstaluj Python 3.9+ z https://www.python.org/downloads/ (zaznacz **„Add Python to PATH"**).
2. Kliknij dwukrotnie **`Run.bat`**. Za pierwszym razem doinstaluje Pillow i otworzy program.

## Token (potrzebny do gier z Rodziny Steam)

Bądź zalogowana na Steam w przeglądarce, potem:

1. Otwórz `store.steampowered.com/pointssummary/ajaxgetasyncconfig`
2. Skopiuj wartość po `"webapi_token"` (zaczyna się od `eyJ`).
3. Wklej w pole **Token**, kliknij **Zapisz**, potem **Odśwież**.

Token działa około doby - gdy przestanie, wklej nowy. Zapisywany jest lokalnie
w `config.json`. Przycisk **Jak zdobyć token** pokazuje te kroki w programie.

## Gatunki

Kliknij **Pobierz gatunki**, żeby włączyć filtr gatunku. Steam ogranicza tempo,
więc duża biblioteka trochę potrwa; leci w tle i można wznowić później.

## Własne okładki (opcjonalnie)

W **Ustawieniach** wskaż `...\Steam\userdata\<id>\config\grid`, by użyć swoich okładek.

## Motywy, nakładka i skróty

W **⚙ Ustawieniach** zmienisz motyw (Neon, Steam blue, Arcade, Dark gray, High
contrast) i otworzysz **Nakładkę** - małe okienko zawsze na wierzchu, które
kładziesz na Steamie; losowanie tam otwiera wylosowaną grę w bibliotece Steam.
Spacja losuje. Gry spoza Steama dodane do biblioteki też biorą udział w losowaniu.

## Osiągnięcia

Włącz **Pokazuj osiągnięcia** w **⚙ Ustawieniach**, żeby przy wylosowanej grze
widzieć odblokowane/łącznie, a zaznacz **łowca osiągnięć** (obok „tylko
zainstalowane"), by dostać też losowe niezdobyte osiągnięcie do zrobienia. Używa
Twojego tokenu; jeśli nie działa, wklej **klucz Steam API** w Ustawieniach.
Statystyki osiągnięć gry muszą być publiczne.

## Gdzie zapisują się ustawienia

Token, motyw, filtry i cache trzymane są w `%APPDATA%\SteamRandomGame`
(`config.json`, `cache_games.json`, `cache_metadata.json`) - nie obok programu,
więc publiczny folder nigdy nie zawiera Twojego tokenu. Można skasować -
odtworzą się przy pobieraniu.
