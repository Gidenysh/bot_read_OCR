#!/usr/bin/env python3
# run.py - Точка входа для запуска бота

import sys
from pathlib import Path

# Добавляем корень проекта в путь импортов
sys.path.insert(0, str(Path(__file__).resolve().parent))

# Теперь импортируем и запускаем бота
from bot.main import main
import asyncio

if __name__ == "__main__":
    asyncio.run(main())