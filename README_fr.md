# 🎲 Randomat-4000S

Tire un jeu au hasard dans toute votre bibliothèque **Famille Steam** (plus vos propres jeux).

Langues : **English (par défaut), Polski, Español, Français, Português,
Português (BR), Čeština, 简体中文** — choisissez dans **⚙ Paramètres**. Cela règle
aussi la langue des genres/descriptions depuis Steam.
Autres README : [README.md](README.md) · [README_pl.md](README_pl.md) · [README_es.md](README_es.md)

## Lancer (Windows)

1. Installez Python 3.9+ depuis https://www.python.org/downloads/ (cochez **« Add Python to PATH »**).
2. Double-cliquez sur **`Run.bat`**. Au premier lancement, il installe Pillow et ouvre l'app.

## Token (nécessaire pour les jeux Famille)

Connectez-vous à Steam dans votre navigateur, puis :

1. Ouvrez `store.steampowered.com/pointssummary/ajaxgetasyncconfig`
2. Copiez la valeur après `"webapi_token"` (commence par `eyJ`).
3. Collez-la dans **Token**, cliquez **Enregistrer** puis **Actualiser**.

Le token dure environ un jour — collez-en un nouveau au besoin. Il est stocké
localement dans `config.json`. Le bouton **Obtenir le token** montre ces étapes dans l'app.

## Genres

Cliquez **Récupérer genres** pour activer le filtre par genre. Steam limite le
rythme, donc une grande bibliothèque prend du temps ; ça tourne en arrière-plan et peut reprendre.

## Jaquettes personnalisées (optionnel)

Dans **Paramètres**, indiquez `...\Steam\userdata\<id>\config\grid` pour utiliser vos jaquettes.

## Thèmes et superposition

Ouvrez **⚙ Paramètres** pour changer de thème (Neon, Steam blue, Arcade, Dark
gray, High contrast). Le bouton **Superposition** ouvre une petite fenêtre
toujours au premier plan que vous posez sur Steam ; y tirer ouvre le jeu choisi
dans votre bibliothèque Steam.

## Où sont stockés les réglages

Votre token, thème, filtres et caches sont dans `%APPDATA%\SteamRandomGame`
(`config.json`, `cache_games.json`, `cache_metadata.json`) — pas à côté de
l'app, donc le dossier public ne contient jamais votre token. Supprimables ;
recréés au téléchargement.
