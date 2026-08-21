# 🎲 Randomat-4000S

Tire un jeu au hasard dans toute votre bibliothèque **Famille Steam** (plus vos propres jeux).

Langues : **English (par défaut), Polski, Español, Français, Português,
Português (BR), Čeština, 简体中文** - choisissez dans **⚙ Paramètres**. Cela règle
aussi la langue des genres/descriptions depuis Steam.
🌐 [English](README.md) · [Polski](README_pl.md) · [Español](README_es.md) · [Français](README_fr.md) · [Português](README_pt.md) · [Português BR](README_br.md) · [Čeština](README_cs.md) · [简体中文](README_zh.md)

## Lancer (Windows)

1. Installez Python 3.9+ depuis https://www.python.org/downloads/ (cochez **« Add Python to PATH »**).
2. Double-cliquez sur **`Run.bat`**. Au premier lancement, il installe Pillow et ouvre l'app.

## Token (nécessaire pour les jeux Famille)

Connectez-vous à Steam dans votre navigateur, puis :

1. Ouvrez `store.steampowered.com/pointssummary/ajaxgetasyncconfig`
2. Copiez la valeur après `"webapi_token"` (commence par `eyJ`).
3. Collez-la dans **Token**, cliquez **Enregistrer** puis **Actualiser**.

Le token dure environ un jour - collez-en un nouveau au besoin. Il est stocké
localement dans `config.json`. Le bouton **Obtenir le token** montre ces étapes dans l'app.

## Genres

Cliquez **Récupérer genres** pour activer le filtre par genre. Steam limite le
rythme, donc une grande bibliothèque prend du temps ; ça tourne en arrière-plan et peut reprendre.

## Jaquettes personnalisées (optionnel)

Dans **Paramètres**, indiquez `...\Steam\userdata\<id>\config\grid` pour utiliser vos jaquettes.

## Thèmes, superposition et raccourcis

Dans **⚙ Paramètres** vous changez de thème (Neon, Steam blue, Arcade, Dark
gray, High contrast) et ouvrez la **Superposition** - une petite fenêtre
toujours au premier plan à poser sur Steam ; y tirer ouvre le jeu choisi dans
votre bibliothèque Steam. La barre d'espace tire. Les jeux hors Steam ajoutés à
votre bibliothèque sont aussi inclus.

## Succès

Activez **Afficher les succès** dans **⚙ Paramètres** pour voir débloqués/total
du jeu tiré, et cochez **chasseur de succès** (à côté d'installés seulement) pour
obtenir aussi un succès verrouillé à débloquer. Cela utilise votre token ; sinon,
collez une **clé API Steam** dans Paramètres. Les stats de succès doivent être publiques.

## Où sont stockés les réglages

Votre token, thème, filtres et caches sont dans `%APPDATA%\SteamRandomGame`
(`config.json`, `cache_games.json`, `cache_metadata.json`) - pas à côté de
l'app, donc le dossier public ne contient jamais votre token. Supprimables ;
recréés au téléchargement.
