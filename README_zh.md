# 🎲 Randomat-4000S

从你的整个 **Steam 家庭库**（以及你自己的游戏）中随机抽选一款游戏。

语言：**English（默认）、Polski、Español、Français、Português、Português (BR)、
Čeština、简体中文** - 在 **⚙ 设置** 中选择。它同时决定从 Steam 获取的类型/描述的语言。
🌐 [English](README.md) · [Polski](README_pl.md) · [Español](README_es.md) · [Français](README_fr.md) · [Português](README_pt.md) · [Português BR](README_br.md) · [Čeština](README_cs.md) · [简体中文](README_zh.md)

## 运行（Windows）

1. 从 https://www.python.org/downloads/ 安装 Python 3.9+（勾选 **"Add Python to PATH"**）。
2. 双击 **`Run.bat`**。首次运行会安装 Pillow 并打开程序。

## 令牌（Steam 家庭游戏所需）

先在浏览器中登录 Steam，然后：

1. 打开 `store.steampowered.com/pointssummary/ajaxgetasyncconfig`
2. 复制 `"webapi_token"` 后面的值（以 `eyJ` 开头）。
3. 粘贴到 **令牌** 框，点击 **保存**，然后 **刷新**。

令牌大约一天后过期 - 失效时粘贴一个新的。它保存在本地。程序中的
**如何获取令牌** 按钮会显示这些步骤。

## 类型

点击 **获取类型** 以启用类型筛选。Steam 会限制请求速度，因此大型库需要一些时间；
它在后台运行，之后可以继续。

## 自定义封面（可选）

在 **设置** 中指定 `...\Steam\userdata\<id>\config\grid` 即可使用你自己的封面。

## 主题与悬浮窗

打开 **⚙ 设置** 切换主题（Neon、Steam blue、Arcade、Dark gray、High contrast）。
**悬浮窗** 按钮会打开一个始终置顶的小窗口，可放在 Steam 上方；在那里抽选会在你的
Steam 库中打开选中的游戏。

## 设置保存位置

你的令牌、主题、筛选和缓存保存在 `%APPDATA%\SteamRandomGame`（`config.json`、
`cache_games.json`、`cache_metadata.json`）- 不在程序旁边，所以公开文件夹绝不会
包含你的令牌。可以删除；下次下载时会重建。
