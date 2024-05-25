@echo off
echo [ %date% %time% ]: START
echo [ %date% %time% ]: Creating virtual env
py -m venv .venv
echo [ %date% %time% ]: activate venv
call .venv\Scripts\activate
echo [ %date% %time% ]: installing the requirements
pip install -r requirements.txt
echo [ %date% %time% ]: creating folders and files
python template.py
echo [ %date% %time% ]: END
