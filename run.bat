@echo off
start %~dp0.venv\Scripts\python acquire.py
start %~dp0.venv\Scripts\python webapp.py