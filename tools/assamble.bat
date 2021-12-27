for %%i in (./distribution/*.mjil) do python -m mjotool -G update -a ./dis/%%i
for %%i in (./dis/*.mjo) do move .\dis\%%i .\assamble\
pause