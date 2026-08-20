# 🎲 Randomat-4000S

Escolha um jogo aleatório de toda a sua biblioteca da **Família Steam** (mais os seus próprios jogos).

Idiomas: **English (padrão), Polski, Español, Français, Português,
Português (BR), Čeština, 简体中文** - escolha um em **⚙ Configurações**. Também define
o idioma dos gêneros/descrições do Steam.
🌐 [English](README.md) · [Polski](README_pl.md) · [Español](README_es.md) · [Français](README_fr.md) · [Português](README_pt.md) · [Português BR](README_br.md) · [Čeština](README_cs.md) · [简体中文](README_zh.md)

## Executar (Windows)

1. Instale o Python 3.9+ em https://www.python.org/downloads/ (marque **"Add Python to PATH"**).
2. Dê dois cliques em **`Run.bat`**. Na primeira vez instala o Pillow e abre o app.

## Token (necessário para jogos da Família Steam)

Esteja logado no Steam no navegador e então:

1. Abra `store.steampowered.com/pointssummary/ajaxgetasyncconfig`
2. Copie o valor após `"webapi_token"` (começa com `eyJ`).
3. Cole em **Token**, clique **Salvar** e depois **Atualizar**.

O token dura cerca de um dia - cole um novo quando parar. Fica salvo localmente.
O botão **Como obter o token** mostra esses passos no app.

## Gêneros

Clique **Obter gêneros** para ativar o filtro por gênero. O Steam limita a taxa,
então uma biblioteca grande demora; roda em segundo plano e pode continuar depois.

## Capas personalizadas (opcional)

Nas **Configurações**, aponte para `...\Steam\userdata\<id>\config\grid` para usar suas capas.

## Temas e sobreposição

Abra **⚙ Configurações** para trocar o tema (Neon, Steam blue, Arcade, Dark gray,
High contrast). O botão **Sobreposição** abre uma janelinha sempre no topo que você
coloca sobre o Steam; sortear ali abre o jogo escolhido na sua biblioteca Steam.

## Onde as configurações ficam salvas

Seu token, tema, filtros e caches ficam em `%APPDATA%\SteamRandomGame`
(`config.json`, `cache_games.json`, `cache_metadata.json`) - não junto ao app, então
a pasta pública nunca contém seu token. Pode apagar; são recriados no próximo download.
