@echo off
python -c "from bot.constant import TEST_MODE; import sys; sys.exit(1 if TEST_MODE else 0)"
if %errorlevel% neq 0 (
    echo При коммите флаг TEST_MODE должен быть False
    exit /b 1
)
exit /b 0
