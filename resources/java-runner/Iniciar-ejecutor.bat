@echo off
chcp 65001 >nul
title Ejecutor de Java - GhecoSoft-Code
cd /d "%~dp0"
where java >nul 2>nul
if errorlevel 1 (
    echo.
    echo  No encontre Java en esta compu.
    echo  Instala el JDK 21 desde https://adoptium.net  ^(Temurin 21 LTS, el instalador .msi^)
    echo  y deja marcada la opcion "Add to PATH". Despues volve a abrir este archivo.
    echo.
    pause
    exit /b 1
)
echo.
echo  Ejecutor de Java de GhecoSoft-Code
echo  Deja esta ventana abierta mientras uses la plataforma. Para cerrarlo, cerra la ventana.
echo.
java JavaRunner.java
echo.
pause
