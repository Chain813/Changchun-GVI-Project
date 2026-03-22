@echo off
chcp 65001 >nul
echo ========================================
echo   长春伪满皇宫周边街区多模态微更新决策平台
echo   Multi-modal Micro-renewal Decision Support System
echo ========================================
echo.
echo 正在启动 Streamlit 应用...
echo.
python -m streamlit run app.py --server.headless=false --server.port=8501
pause
