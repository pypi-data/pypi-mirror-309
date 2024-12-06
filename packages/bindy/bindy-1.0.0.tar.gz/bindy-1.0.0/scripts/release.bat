cd ..
setlocal enableextensions

if exist build-venv rd /s/q build-venv
if exist dist rd /s/q dist
if exist src rd /s/q src
if exist tests rd /s/q tests
if exist LICENSE del LICENSE

md src
xcopy /i /s /e /h /y .\bindy .\src\bindy
md tests
copy ..\..\LICENSE LICENSE

python -m venv build-venv
build-venv\Scripts\python -m pip install --upgrade pip
build-venv\Scripts\python -m pip install build
build-venv\Scripts\python -m build

build-venv\Scripts\python -m pip install twine
build-venv\Scripts\python -m twine upload dist\* 
