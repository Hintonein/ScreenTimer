@echo off
if "%1" == "h" goto begin
mshta vbscript:createobject("wscript.shell").run("""%~0"" h",0)(window.close)&&exit
:begin
cd src
set path=F:\\programer_files\\mini_conda
python F:\\server\\screentimer\\src\\main.py
Pause
