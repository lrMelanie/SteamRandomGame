# 🎲 Randomat-4000S

Elige un juego al azar de toda tu biblioteca de **Familia de Steam** (más tus propios juegos).

Idiomas: **English (por defecto), Polski, Español, Français, Português,
Português (BR), Čeština, 简体中文** - elígelo en **⚙ Ajustes**. También fija el
idioma de géneros/descripciones desde Steam.
🌐 [English](README.md) · [Polski](README_pl.md) · [Español](README_es.md) · [Français](README_fr.md) · [Português](README_pt.md) · [Português BR](README_br.md) · [Čeština](README_cs.md) · [简体中文](README_zh.md)

## Ejecutar (Windows)

1. Instala Python 3.9+ desde https://www.python.org/downloads/ (marca **"Add Python to PATH"**).
2. Haz doble clic en **`Run.bat`**. La primera vez instala Pillow y abre la app.

## Token (necesario para juegos de Familia)

Inicia sesión en Steam en tu navegador y luego:

1. Abre `store.steampowered.com/pointssummary/ajaxgetasyncconfig`
2. Copia el valor tras `"webapi_token"` (empieza por `eyJ`).
3. Pégalo en **Token**, pulsa **Guardar** y luego **Actualizar**.

El token dura un día aprox.; pega uno nuevo cuando falle. Se guarda localmente
en `config.json`. El botón **Cómo conseguir el token** muestra estos pasos en la app.

## Géneros

Pulsa **Obtener géneros** para activar el filtro por género. Steam limita el
ritmo, así que una biblioteca grande tarda; corre en segundo plano y puede reanudarse.

## Carátulas propias (opcional)

En **Ajustes**, indica `...\Steam\userdata\<id>\config\grid` para usar tus carátulas.

## Temas, superposición y atajos

En **⚙ Ajustes** cambias el tema (Neon, Steam blue, Arcade, Dark gray, High
contrast) y abres la **Superposición** - una ventanita siempre visible que
colocas sobre Steam; sortear ahí abre el juego elegido en tu biblioteca Steam.
La barra espaciadora sortea. Los juegos ajenos a Steam añadidos a tu biblioteca
también entran en el sorteo.

## Logros

Activa **Mostrar logros** en **⚙ Ajustes** para ver desbloqueados/total del juego
sorteado, y marca **cazador de logros** (junto a solo-instalados) para obtener
además un logro aleatorio por conseguir. Usa tu token; si no funciona, pega una
**clave de Steam API** en Ajustes. Las estadísticas de logros deben ser públicas.

## Dónde se guardan los ajustes

Tu token, tema, filtros y cachés viven en `%APPDATA%\SteamRandomGame`
(`config.json`, `cache_games.json`, `cache_metadata.json`) - no junto a la app,
así que la carpeta pública nunca contiene tu token. Se pueden borrar; se recrean
al descargar.
