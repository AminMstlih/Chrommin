@echo off
echo Updating Chrommin...
git pull origin main
call venv\Scripts\activate.bat
pip install -r requirements.txt --upgrade
echo Update complete!
pause