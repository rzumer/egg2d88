@ECHO off

if "%1"=="" (
    ECHO An input file is required.
    EXIT -1
)

del /F /Q img\*
quickbms.exe -F "*.exe" -o project_egg.bms %~1 img

set /A idx=0

:loop
    if not errorlevel 1 (
        python egg2d88.py img/EGGFDIMG%idx% %~n1-%idx%.d88
        set /A idx=idx+1
        goto loop
    )

echo Done.
