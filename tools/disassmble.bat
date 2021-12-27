for %%i in (../doc/update sample/*.mjo) do python -m mjotool -G update -d ./update/%%i
for %%i in (../doc/update sample/*.mjil) do move ../doc/update sample/%%i ../texts/original mjil
pause
