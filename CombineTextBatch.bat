@echo off
setlocal enabledelayedexpansion

echo Combined Python Files > combined_py_files.txt
echo. >> combined_py_files.txt

for /r %%a in (*.py) do (
  echo -------------------------------------------------- >> combined_py_files.txt
  echo [FILE] "%%~nxa" [PATH] "%%~dpnxa" >> combined_py_files.txt
  echo -------------------------------------------------- >> combined_py_files.txt
  type "%%~dpnxa" >> combined_py_files.txt
  echo. >> combined_py_files.txt
  echo. >> combined_py_files.txt
)

echo All .py files have been combined into combined_py_files.txt
pause