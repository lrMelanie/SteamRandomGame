@echo off
chcp 65001 >nul
title Randomat-4000S
cd /d "%~dp0"

where python >nul 2>nul
if errorlevel 1 (
  echo Python not found. Install from https://www.python.org/downloads/
  echo During install, tick "Add Python to PATH".
  pause
  exit /b
)

echo Install Pillow (image library) if needed...
python -m pip install --user --quiet Pillow

echo Start Randomat-4000S...
python randomat.py
if errorlevel 1 pause
