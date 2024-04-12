@echo off
cd c:\!pyfixonic

rem Перечислять сети через запятую без пробелов!
set PYFIX_TARGET_NETWORKS=XXX

set PYFIX_TESTING=0
set PYFIX_IGNORE_FIXING_FLAG=0
set PYFIX_ONLY_CHECK_FIXING_FLAG=1
pyfix\venv\Scripts\python.exe pyfix\pyfix_auto.py

timeout /t -1
timeout /t -1
timeout /t -1