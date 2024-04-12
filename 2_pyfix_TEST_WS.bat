@echo off
cd c:\!pyfixonic

rem Перечислять сети через запятую без пробелов!
set PYFIX_TARGET_NETWORKS=XXXXX

set PYFIX_TESTING=1
set PYFIX_IGNORE_FIXING_FLAG=1
set PYFIX_ONLY_CHECK_FIXING_FLAG=0
pyfix\venv\Scripts\python.exe pyfix\pyfix_auto.py

timeout /t -1
timeout /t -1
timeout /t -1