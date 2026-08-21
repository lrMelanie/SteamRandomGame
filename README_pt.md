# 🎲 Randomat-4000S

Escolhe um jogo aleatório de toda a tua biblioteca da **Família Steam** (mais os teus próprios jogos).

Idiomas: **English (predefinido), Polski, Español, Français, Português,
Português (BR), Čeština, 简体中文** - escolhe um em **⚙ Definições**. Também define
o idioma dos géneros/descrições do Steam.
🌐 [English](README.md) · [Polski](README_pl.md) · [Español](README_es.md) · [Français](README_fr.md) · [Português](README_pt.md) · [Português BR](README_br.md) · [Čeština](README_cs.md) · [简体中文](README_zh.md)

## Executar (Windows)

1. Instala o Python 3.9+ em https://www.python.org/downloads/ (marca **"Add Python to PATH"**).
2. Faz duplo clique em **`Run.bat`**. Na primeira vez instala o Pillow e abre a app.

## Token (necessário para jogos da Família Steam)

Tem sessão iniciada no Steam no navegador e depois:

1. Abre `store.steampowered.com/pointssummary/ajaxgetasyncconfig`
2. Copia o valor após `"webapi_token"` (começa por `eyJ`).
3. Cola-o em **Token**, clica **Guardar** e depois **Atualizar**.

O token dura cerca de um dia - cola um novo quando parar. É guardado localmente.
O botão **Como obter o token** mostra estes passos na app.

## Géneros

Clica **Obter géneros** para ativar o filtro por género. O Steam limita o ritmo,
por isso uma biblioteca grande demora; corre em segundo plano e pode continuar depois.

## Capas personalizadas (opcional)

Nas **Definições**, indica `...\Steam\userdata\<id>\config\grid` para usar as tuas capas.

## Temas, sobreposição e atalhos

Nas **⚙ Definições** mudas o tema (Neon, Steam blue, Arcade, Dark gray, High
contrast) e abres a **Sobreposição** - uma janelinha sempre visível para pores
sobre o Steam; sortear aí abre o jogo escolhido na tua biblioteca Steam. A barra
de espaço sorteia. Os jogos fora do Steam adicionados à tua biblioteca também entram.

## Conquistas

Ativa **Mostrar conquistas** nas **⚙ Definições** para ver desbloqueadas/total do
jogo sorteado, e marca **caçador de conquistas** (ao lado de só-instalados) para
receberes também uma conquista aleatória por obter. Usa o teu token; se não
funcionar, cola uma **chave da API Steam** nas Definições. As estatísticas devem ser públicas.

## Onde são guardadas as definições

O teu token, tema, filtros e caches ficam em `%APPDATA%\SteamRandomGame`
(`config.json`, `cache_games.json`, `cache_metadata.json`) - não junto à app, por
isso a pasta pública nunca contém o teu token. Podes apagar; são recriados no próximo download.
