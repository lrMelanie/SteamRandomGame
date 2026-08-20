import os, sys, io, re, json, time, base64, random, shutil, threading, webbrowser
import urllib.parse, urllib.request


def ensure(pkg, pip=None):
    try:
        __import__(pkg); return True
    except ImportError:
        try:
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", pip or pkg])
            __import__(pkg); return True
        except Exception:
            return False


import tkinter as tk
from tkinter import ttk, messagebox, filedialog

HAS_PIL = ensure("PIL", "Pillow")
if HAS_PIL:
    from PIL import Image, ImageTk

HERE = os.path.dirname(os.path.abspath(__file__))


def data_dir():
    base = os.environ.get("APPDATA") or os.path.join(os.path.expanduser("~"), ".config")
    d = os.path.join(base, "SteamRandomGame")
    try:
        os.makedirs(d, exist_ok=True)
    except Exception:
        return HERE
    return d


DATA = data_dir()
CONFIG = os.path.join(DATA, "config.json")
GAMES = os.path.join(DATA, "cache_games.json")
METAF = os.path.join(DATA, "cache_metadata.json")

CDN = "https://cdn.cloudflare.steamstatic.com/steam/apps"
TOKEN_URL = "https://store.steampowered.com/pointssummary/ajaxgetasyncconfig"
UA = "Randomat-4000S"

STEAM_LANG = {"en": "english", "pl": "polish", "es": "spanish", "fr": "french",
              "pt": "portuguese", "br": "brazilian", "cs": "czech", "zh": "schinese"}
LANG_NAMES = {"en": "English", "pl": "Polski", "es": "Espanol", "fr": "Francais",
              "pt": "Portugues", "br": "Portugues (BR)", "cs": "Cestina", "zh": "\u7b80\u4f53\u4e2d\u6587"}
LANG_ORDER = ["en", "pl", "es", "fr", "pt", "br", "cs", "zh"]

THEMES = {
    "neon":     {"bg": "#0d0b1a", "bg2": "#1a1636", "fg": "#d8d8ff", "accent": "#00e5ff", "accent2": "#ff2bd6", "btn": "#241d4d"},
    "steam":    {"bg": "#1b2838", "bg2": "#243747", "fg": "#c7d5e0", "accent": "#66c0f4", "accent2": "#1a9fff", "btn": "#2a3f52"},
    "arcade":   {"bg": "#0e1210", "bg2": "#182420", "fg": "#d7ffe6", "accent": "#39ff14", "accent2": "#ff9d00", "btn": "#1c2e22"},
    "dark":     {"bg": "#2b2b2b", "bg2": "#3a3a3a", "fg": "#e6e6e6", "accent": "#9aa0a6", "accent2": "#c8ccd0", "btn": "#454545"},
    "contrast": {"bg": "#000000", "bg2": "#161616", "fg": "#ffffff", "accent": "#ffffff", "accent2": "#ffff00", "btn": "#222222"},
}
THEME_LABELS = {"neon": "Neon", "steam": "Steam blue", "arcade": "Arcade",
                "dark": "Dark gray", "contrast": "High contrast"}

TR = {
    "en": {
        "title": "Randomat-4000S", "subtitle": "STEAM FAMILY RANDOMIZER",
        "lang": "Language:", "token": "Token:", "save": "Save", "refresh": "Refresh",
        "howto": "How to get token", "genre": "Genre:", "any": "(any)",
        "unplayed": "unplayed", "installed": "installed only", "count": "Count:",
        "account": "Account:", "all": "(all)", "roll": "\U0001F3B2 ROLL",
        "again": "Again", "getgenres": "Get genres", "blocklist": "Blocklist",
        "overlay": "Overlay", "theme": "Theme:", "settings": "Settings",
        "status": "Games: {n}  |  genres: {m}",
        "no_token": "Enter token.", "saved": "Saved. Now Refresh.",
        "bad_token": "Bad token.", "not_family": "No Steam Family found.",
        "no_steamid": "Can't read SteamID from token.",
        "fetching": "Downloading...", "got_games": "{n} games.",
        "refresh_first": "Refresh first.", "all_genres": "All genres ready.",
        "ask_genres": "Fetch genres for {n} games? It's slow.",
        "prog_genres": "Genres {i}/{n}", "genres_done": "Genres done.",
        "no_match": "No game matches the filters.", "no_cover": "no cover",
        "genres_hint": "get genres", "never": "never played", "played": "played {d}",
        "play": "Play", "library": "Library", "store": "Store",
        "block": "Block", "unblock": "Remove", "blocklist_empty": "Blocklist is empty.",
        "no_steam": "Steam folder not found. Set it in Settings.",
        "steam_label": "Steam folder (empty = auto-detect):",
        "grid_label": "Custom art folder:", "browse": "Browse",
        "names_label": "Account names (id=name):", "close": "Close",
        "error": "Error", "spin": "rolling...",
        "howto_text": ("Be logged in to Steam in your browser first.\n\n"
                       "1. Open this page:\n"
                       "store.steampowered.com/pointssummary/ajaxgetasyncconfig\n\n"
                       "2. Copy the value after \"webapi_token\" (starts with eyJ).\n\n"
                       "3. Paste it in Token, click Save, then Refresh.\n\n"
                       "The token lasts about a day. Paste a new one when it stops."),
        "open_page": "Open page",
    },
    "pl": {
        "title": "Randomat-4000S", "subtitle": "LOSOWARKA RODZINY STEAM",
        "lang": "Jezyk:", "token": "Token:", "save": "Zapisz", "refresh": "Odswiez",
        "howto": "Jak zdobyc token", "genre": "Gatunek:", "any": "(dowolny)",
        "unplayed": "nieograne", "installed": "tylko zainstalowane", "count": "Ile:",
        "account": "Konto:", "all": "(wszystkie)", "roll": "\U0001F3B2 LOSUJ",
        "again": "Jeszcze raz", "getgenres": "Pobierz gatunki", "blocklist": "Czarna lista",
        "overlay": "Nakladka", "theme": "Motyw:", "settings": "Ustawienia",
        "status": "Gry: {n}  |  gatunki: {m}",
        "no_token": "Wprowadz token.", "saved": "Zapisano. Kliknij Odswiez.",
        "bad_token": "Zly token.", "not_family": "Brak Rodziny Steam.",
        "no_steamid": "Nie moge odczytac SteamID z tokenu.",
        "fetching": "Pobieram...", "got_games": "{n} gier.",
        "refresh_first": "Najpierw Odswiez.", "all_genres": "Gatunki gotowe.",
        "ask_genres": "Pobrac gatunki dla {n} gier? To wolne.",
        "prog_genres": "Gatunki {i}/{n}", "genres_done": "Gatunki gotowe.",
        "no_match": "Nic nie pasuje do filtrow.", "no_cover": "brak okladki",
        "genres_hint": "pobierz gatunki", "never": "nieograna", "played": "grana {d}",
        "play": "Graj", "library": "Biblioteka", "store": "Sklep",
        "block": "Zablokuj", "unblock": "Usun", "blocklist_empty": "Czarna lista jest pusta.",
        "no_steam": "Nie znaleziono folderu Steam. Ustaw go w Ustawieniach.",
        "steam_label": "Folder Steam (puste = wykryj auto):",
        "grid_label": "Folder wlasnych okladek:", "browse": "Wybierz",
        "names_label": "Nazwy kont (id=nazwa):", "close": "Zamknij",
        "error": "Blad", "spin": "losuje...",
        "howto_text": ("Najpierw zaloguj sie na Steam w przegladarce.\n\n"
                       "1. Otworz strone:\n"
                       "store.steampowered.com/pointssummary/ajaxgetasyncconfig\n\n"
                       "2. Skopiuj wartosc po \"webapi_token\" (zaczyna sie od eyJ).\n\n"
                       "3. Wklej w Token, kliknij Zapisz, potem Odswiez.\n\n"
                       "Token dziala okolo doby. Gdy przestanie, wklej nowy."),
        "open_page": "Otworz strone",
    },
    "es": {
        "title": "Randomat-4000S", "subtitle": "SORTEADOR DE FAMILIA STEAM",
        "lang": "Idioma:", "token": "Token:", "save": "Guardar", "refresh": "Actualizar",
        "howto": "Como conseguir el token", "genre": "Genero:", "any": "(cualquiera)",
        "unplayed": "sin jugar", "installed": "solo instalados", "count": "Cuantos:",
        "account": "Cuenta:", "all": "(todas)", "roll": "\U0001F3B2 SORTEAR",
        "again": "Otra vez", "getgenres": "Obtener generos", "blocklist": "Lista negra",
        "overlay": "Superposicion", "theme": "Tema:", "settings": "Ajustes",
        "status": "Juegos: {n}  |  generos: {m}",
        "no_token": "Introduce el token.", "saved": "Guardado. Pulsa Actualizar.",
        "bad_token": "Token invalido.", "not_family": "Sin Familia de Steam.",
        "no_steamid": "No leo el SteamID del token.",
        "fetching": "Descargando...", "got_games": "{n} juegos.",
        "refresh_first": "Actualiza primero.", "all_genres": "Generos listos.",
        "ask_genres": "Obtener generos de {n} juegos? Es lento.",
        "prog_genres": "Generos {i}/{n}", "genres_done": "Generos listos.",
        "no_match": "Nada coincide con los filtros.", "no_cover": "sin caratula",
        "genres_hint": "obtener generos", "never": "sin jugar", "played": "jugado {d}",
        "play": "Jugar", "library": "Biblioteca", "store": "Tienda",
        "block": "Bloquear", "unblock": "Quitar", "blocklist_empty": "La lista negra esta vacia.",
        "no_steam": "No se encontro la carpeta de Steam. Indicala en Ajustes.",
        "steam_label": "Carpeta de Steam (vacio = auto):",
        "grid_label": "Carpeta de caratulas propias:", "browse": "Elegir",
        "names_label": "Nombres de cuenta (id=nombre):", "close": "Cerrar",
        "error": "Error", "spin": "sorteando...",
        "howto_text": ("Inicia sesion en Steam en el navegador primero.\n\n"
                       "1. Abre esta pagina:\n"
                       "store.steampowered.com/pointssummary/ajaxgetasyncconfig\n\n"
                       "2. Copia el valor tras \"webapi_token\" (empieza por eyJ).\n\n"
                       "3. Pegalo en Token, pulsa Guardar y luego Actualizar.\n\n"
                       "El token dura un dia aprox. Pega uno nuevo cuando falle."),
        "open_page": "Abrir pagina",
    },
    "fr": {
        "title": "Randomat-4000S", "subtitle": "TIRAGE FAMILLE STEAM",
        "lang": "Langue:", "token": "Token:", "save": "Enregistrer", "refresh": "Actualiser",
        "howto": "Obtenir le token", "genre": "Genre:", "any": "(tous)",
        "unplayed": "non joues", "installed": "installes seulement", "count": "Combien:",
        "account": "Compte:", "all": "(tous)", "roll": "\U0001F3B2 TIRER",
        "again": "Encore", "getgenres": "Recuperer genres", "blocklist": "Liste noire",
        "overlay": "Superposition", "theme": "Theme:", "settings": "Parametres",
        "status": "Jeux: {n}  |  genres: {m}",
        "no_token": "Entrez le token.", "saved": "Enregistre. Cliquez Actualiser.",
        "bad_token": "Token invalide.", "not_family": "Pas de Famille Steam.",
        "no_steamid": "SteamID illisible dans le token.",
        "fetching": "Telechargement...", "got_games": "{n} jeux.",
        "refresh_first": "Actualisez d'abord.", "all_genres": "Genres prets.",
        "ask_genres": "Recuperer les genres de {n} jeux? C'est lent.",
        "prog_genres": "Genres {i}/{n}", "genres_done": "Genres prets.",
        "no_match": "Rien ne correspond aux filtres.", "no_cover": "pas de jaquette",
        "genres_hint": "recuperer genres", "never": "jamais joue", "played": "joue {d}",
        "play": "Jouer", "library": "Bibliotheque", "store": "Magasin",
        "block": "Bloquer", "unblock": "Retirer", "blocklist_empty": "La liste noire est vide.",
        "no_steam": "Dossier Steam introuvable. Indiquez-le dans Parametres.",
        "steam_label": "Dossier Steam (vide = auto):",
        "grid_label": "Dossier de jaquettes perso:", "browse": "Choisir",
        "names_label": "Noms de compte (id=nom):", "close": "Fermer",
        "error": "Erreur", "spin": "tirage...",
        "howto_text": ("Connectez-vous d'abord a Steam dans le navigateur.\n\n"
                       "1. Ouvrez cette page:\n"
                       "store.steampowered.com/pointssummary/ajaxgetasyncconfig\n\n"
                       "2. Copiez la valeur apres \"webapi_token\" (commence par eyJ).\n\n"
                       "3. Collez dans Token, cliquez Enregistrer puis Actualiser.\n\n"
                       "Le token dure environ un jour. Collez-en un nouveau au besoin."),
        "open_page": "Ouvrir la page",
    },
    "pt": {
        "title": "Randomat-4000S", "subtitle": "SORTEIO DA FAMILIA STEAM",
        "lang": "Idioma:", "token": "Token:", "save": "Guardar", "refresh": "Atualizar",
        "howto": "Como obter o token", "genre": "Genero:", "any": "(qualquer)",
        "unplayed": "so por jogar", "installed": "so instalados", "count": "Quantos:",
        "account": "Conta:", "all": "(todas)", "roll": "\U0001F3B2 SORTEAR",
        "again": "Outra vez", "getgenres": "Obter generos", "blocklist": "Lista negra",
        "overlay": "Sobreposicao", "theme": "Tema:", "settings": "Definicoes",
        "status": "Jogos: {n}  |  generos: {m}",
        "no_token": "Introduza o token.", "saved": "Guardado. Agora Atualizar.",
        "bad_token": "Token invalido.", "not_family": "Nenhuma Familia Steam encontrada.",
        "no_steamid": "Nao consigo ler o SteamID do token.",
        "fetching": "A descarregar...", "got_games": "{n} jogos.",
        "refresh_first": "Atualize primeiro.", "all_genres": "Generos prontos.",
        "ask_genres": "Obter generos de {n} jogos? E lento.",
        "prog_genres": "Generos {i}/{n}", "genres_done": "Generos prontos.",
        "no_match": "Nenhum jogo corresponde aos filtros.", "no_cover": "sem capa",
        "genres_hint": "obter generos", "never": "nunca jogado", "played": "jogado {d}",
        "play": "Jogar", "library": "Biblioteca", "store": "Loja",
        "block": "Bloquear", "unblock": "Remover", "blocklist_empty": "A lista negra esta vazia.",
        "no_steam": "Pasta do Steam nao encontrada. Defina-a nas Definicoes.",
        "steam_label": "Pasta do Steam (vazio = auto):",
        "grid_label": "Pasta de capas personalizadas:", "browse": "Procurar",
        "names_label": "Nomes de conta (id=nome):", "close": "Fechar",
        "error": "Erro", "spin": "a sortear...",
        "howto_text": ("Inicie sessao no Steam no navegador primeiro.\n\n"
                       "1. Abra esta pagina:\n"
                       "store.steampowered.com/pointssummary/ajaxgetasyncconfig\n\n"
                       "2. Copie o valor apos \"webapi_token\" (comeca por eyJ).\n\n"
                       "3. Cole no Token, clique Guardar e depois Atualizar.\n\n"
                       "O token dura cerca de um dia. Cole um novo quando parar."),
        "open_page": "Abrir pagina",
    },
    "br": {
        "title": "Randomat-4000S", "subtitle": "SORTEIO DA FAMILIA STEAM",
        "lang": "Idioma:", "token": "Token:", "save": "Salvar", "refresh": "Atualizar",
        "howto": "Como obter o token", "genre": "Genero:", "any": "(qualquer)",
        "unplayed": "so nao jogados", "installed": "so instalados", "count": "Quantos:",
        "account": "Conta:", "all": "(todas)", "roll": "\U0001F3B2 SORTEAR",
        "again": "De novo", "getgenres": "Obter generos", "blocklist": "Lista negra",
        "overlay": "Sobreposicao", "theme": "Tema:", "settings": "Configuracoes",
        "status": "Jogos: {n}  |  generos: {m}",
        "no_token": "Digite o token.", "saved": "Salvo. Agora clique Atualizar.",
        "bad_token": "Token invalido.", "not_family": "Nenhuma Familia Steam encontrada.",
        "no_steamid": "Nao consigo ler o SteamID do token.",
        "fetching": "Baixando...", "got_games": "{n} jogos.",
        "refresh_first": "Atualize primeiro.", "all_genres": "Generos prontos.",
        "ask_genres": "Obter generos de {n} jogos? E lento.",
        "prog_genres": "Generos {i}/{n}", "genres_done": "Generos prontos.",
        "no_match": "Nenhum jogo corresponde aos filtros.", "no_cover": "sem capa",
        "genres_hint": "obter generos", "never": "nunca jogado", "played": "jogado {d}",
        "play": "Jogar", "library": "Biblioteca", "store": "Loja",
        "block": "Bloquear", "unblock": "Remover", "blocklist_empty": "A lista negra esta vazia.",
        "no_steam": "Pasta do Steam nao encontrada. Defina nas Configuracoes.",
        "steam_label": "Pasta do Steam (vazio = auto):",
        "grid_label": "Pasta de capas personalizadas:", "browse": "Procurar",
        "names_label": "Nomes de conta (id=nome):", "close": "Fechar",
        "error": "Erro", "spin": "sorteando...",
        "howto_text": ("Faca login no Steam no navegador primeiro.\n\n"
                       "1. Abra esta pagina:\n"
                       "store.steampowered.com/pointssummary/ajaxgetasyncconfig\n\n"
                       "2. Copie o valor apos \"webapi_token\" (comeca com eyJ).\n\n"
                       "3. Cole no Token, clique Salvar e depois Atualizar.\n\n"
                       "O token dura cerca de um dia. Cole um novo quando parar."),
        "open_page": "Abrir pagina",
    },
    "cs": {
        "title": "Randomat-4000S", "subtitle": "NAHODNY VYBER ZE STEAM RODINY",
        "lang": "Jazyk:", "token": "Token:", "save": "Ulozit", "refresh": "Obnovit",
        "howto": "Jak ziskat token", "genre": "Zanr:", "any": "(jakykoli)",
        "unplayed": "jen nehrane", "installed": "jen nainstalovane", "count": "Pocet:",
        "account": "Ucet:", "all": "(vsechny)", "roll": "\U0001F3B2 LOSOVAT",
        "again": "Znovu", "getgenres": "Nacist zanry", "blocklist": "Cerna listina",
        "overlay": "Prekryti", "theme": "Motiv:", "settings": "Nastaveni",
        "status": "Hry: {n}  |  zanry: {m}",
        "no_token": "Zadejte token.", "saved": "Ulozeno. Nyni Obnovit.",
        "bad_token": "Neplatny token.", "not_family": "Steam Rodina nenalezena.",
        "no_steamid": "Nelze nacist SteamID z tokenu.",
        "fetching": "Stahuji...", "got_games": "{n} her.",
        "refresh_first": "Nejprve Obnovit.", "all_genres": "Zanry jsou hotove.",
        "ask_genres": "Nacist zanry pro {n} her? Je to pomale.",
        "prog_genres": "Zanry {i}/{n}", "genres_done": "Zanry hotove.",
        "no_match": "Zadna hra neodpovida filtrum.", "no_cover": "bez obrazku",
        "genres_hint": "nacist zanry", "never": "nehrano", "played": "hrano {d}",
        "play": "Hrat", "library": "Knihovna", "store": "Obchod",
        "block": "Zablokovat", "unblock": "Odebrat", "blocklist_empty": "Cerna listina je prazdna.",
        "no_steam": "Slozka Steam nenalezena. Nastavte ji v Nastaveni.",
        "steam_label": "Slozka Steam (prazdne = auto):",
        "grid_label": "Slozka vlastnich obrazku:", "browse": "Prochazet",
        "names_label": "Nazvy uctu (id=nazev):", "close": "Zavrit",
        "error": "Chyba", "spin": "losuji...",
        "howto_text": ("Nejprve se prihlaste do Steamu v prohlizeci.\n\n"
                       "1. Otevrete tuto stranku:\n"
                       "store.steampowered.com/pointssummary/ajaxgetasyncconfig\n\n"
                       "2. Zkopirujte hodnotu za \"webapi_token\" (zacina eyJ).\n\n"
                       "3. Vlozte do pole Token, kliknete Ulozit a pak Obnovit.\n\n"
                       "Token plati asi jeden den. Kdyz prestane, vlozte novy."),
        "open_page": "Otevrit stranku",
    },
    "zh": {
        "title": "Randomat-4000S", "subtitle": "STEAM \u5bb6\u5ead\u5e93\u968f\u673a\u9009\u62e9\u5668",
        "lang": "\u8bed\u8a00:", "token": "\u4ee4\u724c:", "save": "\u4fdd\u5b58", "refresh": "\u5237\u65b0",
        "howto": "\u5982\u4f55\u83b7\u53d6\u4ee4\u724c", "genre": "\u7c7b\u578b:", "any": "(\u4efb\u610f)",
        "unplayed": "\u4ec5\u672a\u73a9\u8fc7", "installed": "\u4ec5\u5df2\u5b89\u88c5", "count": "\u6570\u91cf:",
        "account": "\u8d26\u6237:", "all": "(\u5168\u90e8)", "roll": "\U0001F3B2 \u62bd\u9009",
        "again": "\u518d\u62bd\u4e00\u6b21", "getgenres": "\u83b7\u53d6\u7c7b\u578b", "blocklist": "\u9ed1\u540d\u5355",
        "overlay": "\u60ac\u6d6e\u7a97", "theme": "\u4e3b\u9898:", "settings": "\u8bbe\u7f6e",
        "status": "\u6e38\u620f: {n}  |  \u7c7b\u578b: {m}",
        "no_token": "\u8bf7\u8f93\u5165\u4ee4\u724c\u3002", "saved": "\u5df2\u4fdd\u5b58\u3002\u73b0\u5728\u70b9\u51fb\u5237\u65b0\u3002",
        "bad_token": "\u65e0\u6548\u7684\u4ee4\u724c\u3002", "not_family": "\u672a\u627e\u5230 Steam \u5bb6\u5ead\u3002",
        "no_steamid": "\u65e0\u6cd5\u4ece\u4ee4\u724c\u8bfb\u53d6 SteamID\u3002",
        "fetching": "\u4e0b\u8f7d\u4e2d...", "got_games": "{n} \u4e2a\u6e38\u620f\u3002",
        "refresh_first": "\u8bf7\u5148\u5237\u65b0\u3002", "all_genres": "\u6240\u6709\u7c7b\u578b\u5df2\u5c31\u7eea\u3002",
        "ask_genres": "\u4e3a {n} \u4e2a\u6e38\u620f\u83b7\u53d6\u7c7b\u578b\uff1f\u901f\u5ea6\u8f83\u6162\u3002",
        "prog_genres": "\u7c7b\u578b {i}/{n}", "genres_done": "\u7c7b\u578b\u83b7\u53d6\u5b8c\u6210\u3002",
        "no_match": "\u6ca1\u6709\u7b26\u5408\u7b5b\u9009\u6761\u4ef6\u7684\u6e38\u620f\u3002", "no_cover": "\u65e0\u5c01\u9762",
        "genres_hint": "\u83b7\u53d6\u7c7b\u578b", "never": "\u4ece\u672a\u73a9\u8fc7", "played": "\u6e38\u73a9\u4e8e {d}",
        "play": "\u5f00\u59cb\u6e38\u620f", "library": "\u5e93", "store": "\u5546\u5e97",
        "block": "\u5c4f\u853d", "unblock": "\u79fb\u9664", "blocklist_empty": "\u9ed1\u540d\u5355\u4e3a\u7a7a\u3002",
        "no_steam": "\u672a\u627e\u5230 Steam \u6587\u4ef6\u5939\u3002\u8bf7\u5728\u8bbe\u7f6e\u4e2d\u6307\u5b9a\u3002",
        "steam_label": "Steam \u6587\u4ef6\u5939\uff08\u7559\u7a7a = \u81ea\u52a8\u68c0\u6d4b\uff09:",
        "grid_label": "\u81ea\u5b9a\u4e49\u5c01\u9762\u6587\u4ef6\u5939:", "browse": "\u6d4f\u89c8",
        "names_label": "\u8d26\u6237\u540d\u79f0\uff08id=\u540d\u79f0\uff09:", "close": "\u5173\u95ed",
        "error": "\u9519\u8bef", "spin": "\u62bd\u9009\u4e2d...",
        "howto_text": ("\u8bf7\u5148\u5728\u6d4f\u89c8\u5668\u4e2d\u767b\u5f55 Steam\u3002\n\n"
                       "1. \u6253\u5f00\u6b64\u9875\u9762\uff1a\n"
                       "store.steampowered.com/pointssummary/ajaxgetasyncconfig\n\n"
                       "2. \u590d\u5236 \"webapi_token\" \u540e\u9762\u7684\u503c\uff08\u4ee5 eyJ \u5f00\u5934\uff09\u3002\n\n"
                       "3. \u7c98\u8d34\u5230\u4ee4\u724c\u6846\uff0c\u70b9\u51fb\u4fdd\u5b58\uff0c\u7136\u540e\u5237\u65b0\u3002\n\n"
                       "\u4ee4\u724c\u7ea6\u4e00\u5929\u540e\u8fc7\u671f\u3002\u5931\u6548\u65f6\u6309\u76f8\u540c\u65b9\u6cd5\u7c98\u8d34\u65b0\u4ee4\u724c\u3002"),
        "open_page": "\u6253\u5f00\u9875\u9762",
    },
}


def get(url, timeout=25):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def getj(url, timeout=25):
    return json.loads(get(url, timeout).decode("utf-8", "replace"))


def steamid(token):
    try:
        p = token.split(".")[1]
        p += "=" * (-len(p) % 4)
        return str(json.loads(base64.urlsafe_b64decode(p)).get("sub", "")) or None
    except Exception:
        return None


def loadjson(path, default):
    if os.path.exists(path):
        try:
            return json.load(open(path, encoding="utf-8"))
        except Exception:
            pass
    return default


def savejson(path, data):
    try:
        json.dump(data, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    except Exception:
        pass


def migrate():
    pairs = [(os.path.join(HERE, "config.json"), CONFIG),
             (os.path.join(HERE, "cache_games.json"), GAMES),
             (os.path.join(HERE, "cache_metadata.json"), METAF)]
    for src, dst in pairs:
        if src != dst and os.path.exists(src) and not os.path.exists(dst):
            try:
                shutil.copy2(src, dst)
            except Exception:
                pass


def steam_dir(override=""):
    if override and os.path.isdir(override):
        return override
    try:
        import winreg
        spots = [(winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam", "SteamPath"),
                 (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Valve\Steam", "InstallPath"),
                 (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Valve\Steam", "InstallPath")]
        for hive, key, name in spots:
            try:
                k = winreg.OpenKey(hive, key)
                v, _ = winreg.QueryValueEx(k, name)
                if v and os.path.isdir(v):
                    return v
            except OSError:
                pass
    except Exception:
        pass
    for c in (r"C:\Program Files (x86)\Steam", r"C:\Program Files\Steam"):
        if os.path.isdir(c):
            return c
    return ""


def installed_ids(override=""):
    steam = steam_dir(override)
    if not steam:
        return None
    dirs = [os.path.join(steam, "steamapps")]
    try:
        txt = open(os.path.join(steam, "steamapps", "libraryfolders.vdf"),
                   encoding="utf-8", errors="ignore").read()
        for m in re.finditer(r'"path"\s*"([^"]+)"', txt):
            sa = os.path.join(m.group(1).replace("\\\\", "\\"), "steamapps")
            if os.path.isdir(sa):
                dirs.append(sa)
    except OSError:
        pass
    ids = set()
    for sa in dict.fromkeys(dirs):
        try:
            for f in os.listdir(sa):
                if f.startswith("appmanifest_") and f.endswith(".acf"):
                    try:
                        ids.add(int(f[12:-4]))
                    except ValueError:
                        pass
        except OSError:
            pass
    return ids


class Steam:
    API = "https://api.steampowered.com/IFamilyGroupsService"

    def __init__(self, token):
        self.token = token.strip()
        self.sid = steamid(self.token)

    def url(self, method, **p):
        p["access_token"] = self.token
        return f"{self.API}/{method}/v1/?" + urllib.parse.urlencode(p)

    def family_id(self):
        if not self.sid:
            raise RuntimeError("no_steamid")
        d = getj(self.url("GetFamilyGroupForUser", steamid=self.sid)).get("response", {})
        gid = d.get("family_groupid")
        if not gid or str(gid) == "0":
            raise RuntimeError("not_family")
        return str(gid)

    def library(self, gid):
        d = getj(self.url("GetSharedLibraryApps", family_groupid=gid, include_own=1,
                          include_free=0, include_non_games=0, max_apps=10000))
        out = []
        for a in d.get("response", {}).get("apps", []):
            if not a.get("appid") or not a.get("name"):
                continue
            if a.get("exclude_reason", 0) not in (0, None):
                continue
            out.append({"appid": int(a["appid"]), "name": a["name"],
                        "owners": [str(s) for s in a.get("owner_steamids", [])],
                        "last_played": a.get("rt_last_played", 0) or 0})
        return out


def fetch_meta(appid, lang):
    url = f"https://store.steampowered.com/api/appdetails?appids={appid}&l={lang}"
    try:
        node = getj(url).get(str(appid), {})
        if not node.get("success"):
            return {"genres": [], "desc": ""}
        d = node.get("data", {})
        return {"genres": [g.get("description", "") for g in d.get("genres", [])],
                "desc": d.get("short_description", "")}
    except Exception:
        return {"genres": [], "desc": ""}


class Loader:
    def __init__(self, folder=""):
        self.folder = folder
        self.cache = {}

    def local(self, appid):
        if self.folder and os.path.isdir(self.folder):
            for name in (f"{appid}.jpg", f"{appid}.png"):
                p = os.path.join(self.folder, name)
                if os.path.isfile(p):
                    return p
        return None

    def load(self, appid):
        if not HAS_PIL:
            return None
        if appid in self.cache:
            return self.cache[appid]
        img = None
        p = self.local(appid)
        if p:
            try:
                img = Image.open(p).convert("RGBA")
            except Exception:
                img = None
        if img is None:
            for url in (f"{CDN}/{appid}/header.jpg", f"{CDN}/{appid}/capsule_616x353.jpg"):
                try:
                    img = Image.open(io.BytesIO(get(url))).convert("RGBA"); break
                except Exception:
                    img = None
        self.cache[appid] = img
        return img


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        migrate()
        self.cfg = loadjson(CONFIG, {})
        self.lang = self.cfg.get("lang", "en")
        if self.lang not in TR:
            self.lang = "en"
        self.pal = THEMES.get(self.cfg.get("theme", "neon"), THEMES["neon"])
        self.meta = loadjson(METAF, {})
        self.loader = Loader(self.cfg.get("grid_folder", ""))
        self.games = loadjson(GAMES, {"apps": []}).get("apps", [])
        self.history = []
        self.photos = []
        self.inst = None
        self.ov = None
        self.geometry("1010x720")
        self.minsize(880, 580)
        self.style()
        self.build()
        self.after_build()

    def t(self, key, **kw):
        s = TR.get(self.lang, TR["en"]).get(key) or TR["en"].get(key, key)
        return s.format(**kw) if kw else s

    def style(self):
        p = self.pal
        self.configure(bg=p["bg"])
        self.option_add("*TCombobox*Listbox.background", p["bg2"])
        self.option_add("*TCombobox*Listbox.foreground", p["fg"])
        self.option_add("*TCombobox*Listbox.selectBackground", p["accent"])
        self.option_add("*TCombobox*Listbox.selectForeground", p["bg"])
        s = ttk.Style(self)
        try:
            s.theme_use("clam")
        except Exception:
            pass
        s.configure("TFrame", background=p["bg"])
        s.configure("Card.TFrame", background=p["bg2"])
        s.configure("Side.TFrame", background=p["bg2"])
        s.configure("TLabel", background=p["bg"], foreground=p["fg"])
        s.configure("Card.TLabel", background=p["bg2"], foreground=p["fg"])
        s.configure("Side.TLabel", background=p["bg2"], foreground=p["fg"])
        s.configure("Big.TLabel", background=p["bg"], foreground=p["accent"],
                    font=("Segoe UI Black", 22, "bold"))
        s.configure("Sub.TLabel", background=p["bg"], foreground=p["accent2"],
                    font=("Segoe UI", 9, "bold"))
        s.configure("Title.TLabel", background=p["bg2"], foreground=p["accent"],
                    font=("Segoe UI", 16, "bold"))
        s.configure("Head.TLabel", background=p["bg2"], foreground=p["accent"],
                    font=("Segoe UI", 12, "bold"))
        s.configure("Spin.TLabel", background=p["bg"], foreground=p["accent"],
                    font=("Segoe UI", 20, "bold"))
        s.configure("TCheckbutton", background=p["bg"], foreground=p["fg"])
        s.map("TCheckbutton", background=[("active", p["bg"])])
        s.configure("TButton", background=p["btn"], foreground=p["fg"],
                    borderwidth=0, focusthickness=0, padding=6)
        s.map("TButton", background=[("active", p["accent"])], foreground=[("active", p["bg"])])
        s.configure("Accent.TButton", background=p["accent"], foreground=p["bg"],
                    font=("Segoe UI", 10, "bold"))
        s.map("Accent.TButton", background=[("active", p["accent2"])])
        s.configure("Go.TButton", background=p["accent2"], foreground="#ffffff",
                    font=("Segoe UI", 14, "bold"), padding=8)
        s.map("Go.TButton", background=[("active", p["accent"])])
        for st in ("TEntry", "TCombobox", "TSpinbox"):
            s.configure(st, fieldbackground=p["bg2"], foreground=p["fg"], background=p["btn"],
                        arrowcolor=p["fg"], bordercolor=p["btn"], lightcolor=p["btn"],
                        darkcolor=p["btn"], insertcolor=p["fg"],
                        selectbackground=p["accent"], selectforeground=p["bg"])
            s.map(st, fieldbackground=[("readonly", p["bg2"]), ("disabled", p["bg2"]),
                                       ("focus", p["bg2"]), ("active", p["bg2"])],
                  foreground=[("readonly", p["fg"])],
                  background=[("readonly", p["btn"]), ("active", p["btn"])])
        s.configure("TProgressbar", background=p["accent"], troughcolor=p["bg2"], borderwidth=0)

    def txtbox(self, parent, **kw):
        p = self.pal
        return tk.Text(parent, bg=p["bg2"], fg=p["fg"], insertbackground=p["fg"],
                       relief="flat", highlightthickness=1, highlightbackground=p["btn"], **kw)

    def build(self):
        p = self.pal
        self.title(self.t("title"))
        body = ttk.Frame(self)
        body.pack(fill="both", expand=True)
        main = ttk.Frame(body)
        main.pack(side="left", fill="both", expand=True)

        header = ttk.Frame(main, padding=(12, 10, 12, 0))
        header.pack(fill="x")
        titles = ttk.Frame(header)
        titles.pack(side="left")
        ttk.Label(titles, text="RANDOMAT-4000S", style="Big.TLabel").pack(anchor="w")
        ttk.Label(titles, text=self.t("subtitle"), style="Sub.TLabel").pack(anchor="w")
        ttk.Button(header, text="\u2699", width=3, style="Accent.TButton",
                   command=self.open_settings).pack(side="right")
        tk.Frame(main, bg=p["accent"], height=2).pack(fill="x", padx=12, pady=(6, 0))

        top = ttk.Frame(main, padding=(12, 8, 12, 2))
        top.pack(fill="x")
        ttk.Label(top, text=self.t("token")).pack(side="left")
        self.token_var = tk.StringVar(value=self.cfg.get("token", ""))
        ttk.Entry(top, textvariable=self.token_var, show="•", width=26).pack(side="left", padx=4)
        ttk.Button(top, text=self.t("save"), command=self.save_token).pack(side="left", padx=2)
        ttk.Button(top, text=self.t("refresh"), command=self.refresh).pack(side="left", padx=2)
        ttk.Button(top, text=self.t("howto"), command=self.toggle_side).pack(side="left", padx=2)

        f = ttk.Frame(main, padding=(12, 0, 12, 4))
        f.pack(fill="x")
        ttk.Label(f, text=self.t("genre")).pack(side="left")
        self.genre_var = tk.StringVar(value=self.t("any"))
        self.genre_box = ttk.Combobox(f, textvariable=self.genre_var, width=18, state="readonly")
        self.genre_box.pack(side="left", padx=4)
        self.genre_box.bind("<<ComboboxSelected>>", self.save_filters)
        self.unplayed = tk.BooleanVar(value=False)
        ttk.Checkbutton(f, text=self.t("unplayed"), variable=self.unplayed,
                        command=self.save_filters).pack(side="left", padx=6)
        self.installed = tk.BooleanVar(value=False)
        ttk.Checkbutton(f, text=self.t("installed"), variable=self.installed,
                        command=self.save_filters).pack(side="left", padx=6)
        ttk.Label(f, text=self.t("count")).pack(side="left")
        self.count = tk.IntVar(value=1)
        ttk.Spinbox(f, from_=1, to=12, width=4, textvariable=self.count,
                    command=self.save_filters).pack(side="left", padx=4)
        ttk.Label(f, text=self.t("account")).pack(side="left", padx=(8, 0))
        self.owner_var = tk.StringVar(value=self.t("all"))
        self.owner_box = ttk.Combobox(f, textvariable=self.owner_var, width=16, state="readonly")
        self.owner_box.pack(side="left", padx=4)
        self.owner_box.bind("<<ComboboxSelected>>", self.save_filters)

        g = ttk.Frame(main, padding=(12, 2))
        g.pack(fill="x")
        ttk.Button(g, text=self.t("roll"), style="Go.TButton", command=self.roll).pack(side="left")
        ttk.Button(g, text=self.t("again"), command=self.roll).pack(side="left", padx=6)
        ttk.Button(g, text=self.t("overlay"), style="Accent.TButton", command=self.open_overlay).pack(side="right")
        ttk.Button(g, text=self.t("blocklist"), command=self.open_blocklist).pack(side="right", padx=6)
        ttk.Button(g, text=self.t("getgenres"), command=self.get_genres).pack(side="right")

        mid = ttk.Frame(main, padding=12)
        mid.pack(fill="both", expand=True)
        self.canvas = tk.Canvas(mid, bg=p["bg"], highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)
        sb = ttk.Scrollbar(mid, orient="vertical", command=self.canvas.yview)
        sb.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=sb.set)
        self.results = ttk.Frame(self.canvas)
        self.win = self.canvas.create_window((0, 0), window=self.results, anchor="nw")
        self.results.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(self.win, width=e.width))
        self.canvas.bind_all("<MouseWheel>", lambda e: self.canvas.yview_scroll(-1 if e.delta > 0 else 1, "units"))

        b = ttk.Frame(main, padding=(12, 2))
        b.pack(fill="x")
        self.status_var = tk.StringVar(value="")
        ttk.Label(b, textvariable=self.status_var).pack(side="left")
        self.progress = ttk.Progressbar(b, mode="determinate", length=200)
        self.progress.pack(side="right")

        self.side = ttk.Frame(body, style="Side.TFrame", padding=14, width=330)
        ttk.Label(self.side, text=self.t("howto"), style="Head.TLabel").pack(anchor="w")
        txt = self.txtbox(self.side, wrap="word", width=38, height=20, font=("Segoe UI", 10))
        txt.pack(fill="both", expand=True, pady=8)
        txt.insert("1.0", self.t("howto_text"))
        txt.configure(state="disabled")
        ttk.Button(self.side, text=self.t("open_page"),
                   command=lambda: webbrowser.open(TOKEN_URL)).pack(fill="x")
        ttk.Button(self.side, text=self.t("close"), command=self.toggle_side).pack(fill="x", pady=(6, 0))
        self.side_open = False

    def after_build(self):
        self.fill_filters()
        self.restore_filters()
        self.status()

    def rebuild(self):
        for w in self.winfo_children():
            w.destroy()
        self.ov = None
        self.style()
        self.build()
        self.after_build()

    def toggle_side(self):
        if self.side_open:
            self.side.pack_forget()
        else:
            self.side.pack(side="right", fill="y")
        self.side_open = not self.side_open

    def set_lang(self, code):
        if code not in TR or code == self.lang:
            return
        self.lang = code
        self.cfg["lang"] = code
        savejson(CONFIG, self.cfg)
        self.after(10, self.rebuild)

    def change_theme(self, key):
        if key not in THEMES:
            return
        self.cfg["theme"] = key
        savejson(CONFIG, self.cfg)
        self.pal = THEMES[key]
        self.after(10, self.rebuild)

    def owner_name(self, sid):
        return self.cfg.get("owner_names", {}).get(str(sid), f"...{str(sid)[-4:]}")

    def fill_filters(self):
        genres = [self.t("any")] + sorted({g for m in self.meta.values() for g in m.get("genres", []) if g})
        self.genre_box["values"] = genres
        if self.genre_var.get() not in genres:
            self.genre_var.set(self.t("any"))
        owners = {self.t("all")} | {self.owner_name(o) for a in self.games for o in a.get("owners", [])}
        self.owner_box["values"] = sorted(owners)
        if self.owner_var.get() not in owners:
            self.owner_var.set(self.t("all"))

    def save_filters(self, *_):
        self.cfg["filters"] = {"genre": self.genre_var.get(), "owner": self.owner_var.get(),
                               "unplayed": bool(self.unplayed.get()),
                               "installed": bool(self.installed.get()),
                               "count": int(self.count.get() or 1)}
        savejson(CONFIG, self.cfg)

    def restore_filters(self):
        fl = self.cfg.get("filters", {})
        if fl.get("genre") in self.genre_box["values"]:
            self.genre_var.set(fl["genre"])
        if fl.get("owner") in self.owner_box["values"]:
            self.owner_var.set(fl["owner"])
        self.unplayed.set(bool(fl.get("unplayed", False)))
        self.installed.set(bool(fl.get("installed", False)))
        try:
            self.count.set(int(fl.get("count", 1)))
        except Exception:
            pass

    def status(self):
        s = self.t("status", n=len(self.games), m=len(self.meta))
        api = self.api()
        if api and api.sid:
            s += f"   -   ...{api.sid[-5:]}"
        self.status_var.set(s)

    def api(self):
        tok = self.token_var.get().strip()
        return Steam(tok) if tok else None

    def save_token(self):
        tok = self.token_var.get().strip()
        if not tok:
            return messagebox.showwarning(self.t("title"), self.t("no_token"))
        if '"webapi_token"' in tok:
            try:
                tok = json.loads(tok).get("webapi_token", tok)
            except Exception:
                pass
        tok = tok.strip().strip('"')
        self.token_var.set(tok)
        self.cfg["token"] = tok
        self.cfg.pop("family_groupid", None)
        savejson(CONFIG, self.cfg)
        if steamid(tok):
            messagebox.showinfo(self.t("title"), self.t("saved"))
        else:
            messagebox.showwarning(self.t("title"), self.t("bad_token"))
        self.status()

    def refresh(self):
        if not self.api():
            return messagebox.showwarning(self.t("error"), self.t("no_token"))
        self.bg(self._refresh, self.t("fetching"))

    def _refresh(self):
        api = self.api()
        gid = self.cfg.get("family_groupid")
        if not gid:
            gid = api.family_id()
            self.cfg["family_groupid"] = gid
            savejson(CONFIG, self.cfg)
        apps = api.library(gid)
        self.games = apps
        savejson(GAMES, {"updated": int(time.time()), "apps": apps})
        self.after(0, lambda: (self.fill_filters(), self.status(),
                               messagebox.showinfo(self.t("title"), self.t("got_games", n=len(apps)))))

    def get_genres(self):
        if not self.games:
            return messagebox.showwarning(self.t("error"), self.t("refresh_first"))
        todo = [a for a in self.games if str(a["appid"]) not in self.meta]
        if not todo:
            return messagebox.showinfo(self.t("title"), self.t("all_genres"))
        if not messagebox.askyesno(self.t("getgenres"), self.t("ask_genres", n=len(todo))):
            return
        self.bg(lambda: self._genres(todo), None, total=len(todo))

    def _genres(self, todo):
        n = len(todo)
        lang = STEAM_LANG.get(self.lang, "english")
        for i, a in enumerate(todo, 1):
            self.meta[str(a["appid"])] = fetch_meta(a["appid"], lang)
            if i % 20 == 0:
                savejson(METAF, self.meta)
            self.after(0, lambda i=i: self.prog(i, n, self.t("prog_genres", i=i, n=n)))
            time.sleep(1.5)
        savejson(METAF, self.meta)
        self.after(0, lambda: (self.fill_filters(), self.status(),
                               messagebox.showinfo(self.t("title"), self.t("genres_done"))))

    def pool(self):
        blocked = set(self.cfg.get("blocklist", []))
        p = [a for a in self.games if a["appid"] not in blocked]
        if self.unplayed.get():
            p = [a for a in p if not a.get("last_played")]
        if self.installed.get() and self.inst is not None:
            p = [a for a in p if a["appid"] in self.inst]
        if self.owner_var.get() != self.t("all"):
            p = [a for a in p if any(self.owner_name(o) == self.owner_var.get() for o in a.get("owners", []))]
        if self.genre_var.get() != self.t("any"):
            p = [a for a in p if self.genre_var.get() in self.meta.get(str(a["appid"]), {}).get("genres", [])]
        return p

    def prepare_pool(self):
        self.inst = None
        if self.installed.get():
            self.inst = installed_ids(self.cfg.get("steam_path", ""))
            if self.inst is None:
                messagebox.showwarning(self.t("error"), self.t("no_steam"))
        return self.pool()

    def pick_from(self, p, k):
        k = max(1, min(k, len(p)))
        fresh = [a for a in p if a["appid"] not in self.history]
        picks = random.sample(fresh if len(fresh) >= k else p, k)
        for a in picks:
            self.history.append(a["appid"])
        self.history = self.history[-40:]
        return picks

    def spin(self, label, pick, done):
        flash = [a["name"] for a in self.games] or [pick["name"]]
        delays = [25 + int(150 * (i / 23.0) ** 2.2) for i in range(24)]

        def step(i):
            if i < len(delays):
                label.config(text=random.choice(flash))
                self.after(delays[i], step, i + 1)
            else:
                label.config(text=pick["name"])
                self.after(160, done)
        step(0)

    def roll(self):
        if not self.games:
            return messagebox.showwarning(self.t("error"), self.t("refresh_first"))
        p = self.prepare_pool()
        if not p:
            return messagebox.showinfo(self.t("title"), self.t("no_match"))
        picks = self.pick_from(p, int(self.count.get() or 1))
        for w in self.results.winfo_children():
            w.destroy()
        self.photos.clear()
        big = ttk.Label(self.results, style="Spin.TLabel", text=self.t("spin"),
                        anchor="center", wraplength=760)
        big.pack(fill="x", pady=30)

        def done():
            big.destroy()
            for a in picks:
                self.card(a)
            self.canvas.yview_moveto(0)
        self.spin(big, picks[0], done)

    def card(self, a):
        appid = a["appid"]
        m = self.meta.get(str(appid), {})
        c = ttk.Frame(self.results, style="Card.TFrame", padding=12)
        c.pack(fill="x", pady=6, padx=2)
        img = self.loader.load(appid)
        if img is not None and HAS_PIL:
            ratio = 320 / img.width
            photo = ImageTk.PhotoImage(img.resize((320, int(img.height * ratio))))
            self.photos.append(photo)
            ttk.Label(c, image=photo, style="Card.TLabel").grid(row=0, column=0, rowspan=4, sticky="nw", padx=(0, 12))
        else:
            ttk.Label(c, text=self.t("no_cover"), style="Card.TLabel").grid(row=0, column=0, rowspan=4, sticky="nw", padx=(0, 12))
        ttk.Label(c, text=a["name"], style="Title.TLabel", wraplength=520, justify="left").grid(row=0, column=1, sticky="w")
        genres = ", ".join(m.get("genres", [])) or self.t("genres_hint")
        ttk.Label(c, text=genres, style="Card.TLabel", wraplength=520, justify="left").grid(row=1, column=1, sticky="w", pady=(2, 0))
        owners = ", ".join(self.owner_name(o) for o in a.get("owners", [])) or "-"
        played = self.t("never") if not a.get("last_played") else self.t("played", d=time.strftime("%Y-%m-%d", time.localtime(a["last_played"])))
        ttk.Label(c, text=f"{owners}  -  {played}", style="Card.TLabel", wraplength=520, justify="left").grid(row=2, column=1, sticky="w", pady=(2, 0))
        if m.get("desc"):
            ttk.Label(c, text=m["desc"], style="Card.TLabel", wraplength=520, justify="left").grid(row=3, column=1, sticky="w", pady=(4, 0))
        bt = ttk.Frame(c, style="Card.TFrame")
        bt.grid(row=4, column=1, sticky="w", pady=(8, 0))
        ttk.Button(bt, text=self.t("play"), style="Accent.TButton",
                   command=lambda i=appid: webbrowser.open(f"steam://run/{i}")).pack(side="left")
        ttk.Button(bt, text=self.t("library"),
                   command=lambda i=appid: webbrowser.open(f"steam://nav/games/details/{i}")).pack(side="left", padx=6)
        ttk.Button(bt, text=self.t("store"),
                   command=lambda i=appid: webbrowser.open(f"https://store.steampowered.com/app/{i}")).pack(side="left")
        ttk.Button(bt, text=self.t("block"),
                   command=lambda i=appid, fr=c: self.block(i, fr)).pack(side="left", padx=6)

    def block(self, appid, frame):
        bl = self.cfg.setdefault("blocklist", [])
        if appid not in bl:
            bl.append(appid)
            savejson(CONFIG, self.cfg)
        frame.destroy()

    def unblock(self, appid):
        self.cfg["blocklist"] = [x for x in self.cfg.get("blocklist", []) if x != appid]
        savejson(CONFIG, self.cfg)

    def open_blocklist(self):
        w = tk.Toplevel(self)
        w.title(self.t("blocklist"))
        w.configure(bg=self.pal["bg"])
        w.geometry("420x460")
        holder = ttk.Frame(w, padding=8)
        holder.pack(fill="both", expand=True)

        def redraw():
            for x in holder.winfo_children():
                x.destroy()
            bl = self.cfg.get("blocklist", [])
            if not bl:
                ttk.Label(holder, text=self.t("blocklist_empty")).pack(anchor="w")
                return
            names = {a["appid"]: a["name"] for a in self.games}
            for appid in list(bl):
                row = ttk.Frame(holder)
                row.pack(fill="x", pady=2)
                ttk.Label(row, text=names.get(appid, str(appid)), width=36).pack(side="left")
                ttk.Button(row, text=self.t("unblock"),
                           command=lambda i=appid: (self.unblock(i), redraw())).pack(side="right")
        redraw()
        ttk.Button(w, text=self.t("close"), command=w.destroy).pack(pady=6)

    def open_settings(self):
        w = tk.Toplevel(self)
        w.title(self.t("settings"))
        w.configure(bg=self.pal["bg"])
        w.geometry("560x430")

        ttk.Label(w, text=self.t("theme")).pack(anchor="w", padx=10, pady=(10, 2))
        tv = tk.StringVar(value=THEME_LABELS.get(self.cfg.get("theme", "neon")))
        cbt = ttk.Combobox(w, textvariable=tv, state="readonly", values=list(THEME_LABELS.values()))
        cbt.pack(fill="x", padx=10)

        def on_theme(_=None):
            key = next((k for k, v in THEME_LABELS.items() if v == tv.get()), "neon")
            w.destroy()
            self.change_theme(key)
        cbt.bind("<<ComboboxSelected>>", on_theme)

        ttk.Label(w, text=self.t("lang")).pack(anchor="w", padx=10, pady=(10, 2))
        lv = tk.StringVar(value=LANG_NAMES[self.lang])
        cbl = ttk.Combobox(w, textvariable=lv, state="readonly",
                           values=[LANG_NAMES[c] for c in LANG_ORDER])
        cbl.pack(fill="x", padx=10)

        def on_lang(_=None):
            code = next((c for c, n in LANG_NAMES.items() if n == lv.get()), "en")
            w.destroy()
            self.set_lang(code)
        cbl.bind("<<ComboboxSelected>>", on_lang)

        ttk.Label(w, text=self.t("steam_label")).pack(anchor="w", padx=10, pady=(10, 2))
        srow = ttk.Frame(w)
        srow.pack(fill="x", padx=10)
        sv = tk.StringVar(value=self.cfg.get("steam_path", ""))
        ttk.Entry(srow, textvariable=sv).pack(side="left", fill="x", expand=True)
        ttk.Button(srow, text=self.t("browse"), command=lambda: sv.set(filedialog.askdirectory() or sv.get())).pack(side="left", padx=6)

        ttk.Label(w, text=self.t("grid_label")).pack(anchor="w", padx=10, pady=(10, 2))
        grow = ttk.Frame(w)
        grow.pack(fill="x", padx=10)
        gv = tk.StringVar(value=self.cfg.get("grid_folder", ""))
        ttk.Entry(grow, textvariable=gv).pack(side="left", fill="x", expand=True)
        ttk.Button(grow, text=self.t("browse"), command=lambda: gv.set(filedialog.askdirectory() or gv.get())).pack(side="left", padx=6)

        ttk.Label(w, text=self.t("names_label")).pack(anchor="w", padx=10, pady=(10, 2))
        txt = self.txtbox(w, height=4)
        txt.pack(fill="both", expand=True, padx=10)
        txt.insert("1.0", "\n".join(f"{k}={v}" for k, v in self.cfg.get("owner_names", {}).items()))

        def save():
            self.cfg["steam_path"] = sv.get().strip()
            self.cfg["grid_folder"] = gv.get().strip()
            self.loader.folder = self.cfg["grid_folder"]
            names = {}
            for line in txt.get("1.0", "end").splitlines():
                if "=" in line:
                    k, v = line.split("=", 1)
                    if k.strip():
                        names[k.strip()] = v.strip()
            self.cfg["owner_names"] = names
            savejson(CONFIG, self.cfg)
            self.fill_filters()
            w.destroy()
        ttk.Button(w, text=self.t("save"), style="Accent.TButton", command=save).pack(pady=8)

    def open_overlay(self):
        if self.ov is not None and self.ov.winfo_exists():
            self.ov.deiconify()
            self.ov.lift()
            return
        p = self.pal
        pos = self.cfg.get("overlay_pos", "+120+120")
        self._ov_pos = pos
        ov = tk.Toplevel(self)
        self.ov = ov
        ov.overrideredirect(True)
        ov.attributes("-topmost", True)
        try:
            ov.attributes("-alpha", 0.96)
        except Exception:
            pass
        ov.configure(bg=p["accent"])
        ov.geometry("380x230" + pos)
        inner = tk.Frame(ov, bg=p["bg"])
        inner.pack(fill="both", expand=True, padx=2, pady=2)

        bar = tk.Frame(inner, bg=p["bg2"], height=28)
        bar.pack(fill="x")
        tk.Label(bar, text="RANDOMAT", bg=p["bg2"], fg=p["accent"],
                 font=("Segoe UI", 9, "bold")).pack(side="left", padx=8)
        tk.Button(bar, text="\u2715", bg=p["bg2"], fg=p["fg"], relief="flat",
                  command=self.close_overlay).pack(side="right")

        def start(e):
            ov._x, ov._y = e.x, e.y

        def move(e):
            x, y = e.x_root - ov._x, e.y_root - ov._y
            ov.geometry(f"+{x}+{y}")
            self._ov_pos = f"+{x}+{y}"
        bar.bind("<Button-1>", start)
        bar.bind("<B1-Motion>", move)

        res = tk.Label(inner, text=self.t("overlay"), bg=p["bg"], fg=p["accent"],
                       font=("Segoe UI", 15, "bold"), wraplength=340, justify="center")
        res.pack(fill="both", expand=True, padx=10)
        tk.Button(inner, text=self.t("roll"), bg=p["accent2"], fg="#ffffff", relief="flat",
                  font=("Segoe UI", 13, "bold"),
                  command=lambda: self.overlay_roll(res)).pack(fill="x", padx=10, pady=(0, 10))

    def close_overlay(self):
        if self.ov is not None:
            self.cfg["overlay_pos"] = getattr(self, "_ov_pos", "+120+120")
            savejson(CONFIG, self.cfg)
            self.ov.destroy()
            self.ov = None

    def overlay_roll(self, label):
        if not self.games:
            label.config(text=self.t("refresh_first"))
            return
        p = self.prepare_pool()
        if not p:
            label.config(text=self.t("no_match"))
            return
        pick = self.pick_from(p, 1)[0]

        def done():
            label.config(text=pick["name"])
            webbrowser.open(f"steam://nav/games/details/{pick['appid']}")
        self.spin(label, pick, done)

    def prog(self, cur, total, text):
        self.progress["maximum"] = total
        self.progress["value"] = cur
        self.status_var.set(text)

    def bg(self, worker, text, total=0):
        if text:
            self.status_var.set(text)
        if total:
            self.progress["maximum"] = total
            self.progress["value"] = 0

        def run():
            try:
                worker()
            except RuntimeError as e:
                self.after(0, lambda: messagebox.showerror(self.t("error"), self.t(str(e))))
            except Exception as e:
                self.after(0, lambda: messagebox.showerror(self.t("error"), str(e)))
            finally:
                self.after(0, lambda: self.progress.configure(value=0))
                self.after(0, self.status)
        threading.Thread(target=run, daemon=True).start()


if __name__ == "__main__":
    App().mainloop()
