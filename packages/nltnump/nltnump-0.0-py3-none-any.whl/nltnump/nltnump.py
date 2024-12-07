from ftplib import FTP
import io
import os
import sys
from pathlib import Path
import time
import winsound


def check_ftp_for_new_files(ftp, last_files):
    current_files = set(ftp.nlst())
    new_files = current_files.difference(last_files)
    return new_files


def get():
    ftp = FTP('sent1n8l.beget.tech')
    ftp.login(user='sent1n8l_base', passwd='Amdlover345!')
    ftp.encoding = 'utf-8'  # Устанавливаем кодировку UTF-8

    downloads_path = str(Path.home() / "Downloads")
    last_files = set(ftp.nlst())

    while True:
        method = input("Выберите метод (W(rite) или R(ead)): ")

        if method.lower() == "w":
            upload_choice = input("Вы хотите загрузить файл с компьютера на FTP сервер? (y(es)/n(o)): ")

            if upload_choice.lower() == "y":
                local_file_path = input("Введите путь к локальному файлу: ")
                filename = os.path.basename(local_file_path)  # Получаем имя файла
                remote_file_path = f'/{filename}'  # Устанавливаем путь для сохранения в корневом каталоге

                if os.path.isfile(local_file_path):
                    with open(local_file_path, 'rb') as local_file:
                        ftp.storbinary(f'STOR {remote_file_path}', local_file)
                        print(f"Файл {filename} успешно загружен в корневой каталог FTP сервера")
                else:
                    print(f"Файл {local_file_path} не найден.")
            else:
                filename = input("Введите имя для нового файла (с расширением): ")
                remote_file_path = f'/{filename}'  # Устанавливаем путь для сохранения в корневом каталоге
                data = input("Введите текст:)")
                data_bytes = io.BytesIO(data.encode('utf-8'))
                ftp.storbinary(f'STOR {remote_file_path}', data_bytes)
                print(f"Файл {filename} успешно создан в корневом каталоге FTP сервера")
        elif method.lower() == "r":
            files = ftp.nlst()
            print("Список файлов на FTP сервере:")
            for idx, file in enumerate(files):

                print(f"{idx + 1}. {file}")
            choice = int(input("Выберите файл для чтения (введите номер): "))
            if 1 <= choice <= len(files):
                filename = files[choice - 1]
                data = bytearray()

                def write_data(buf):
                    data.extend(buf)

                try:
                    ftp.retrbinary(f"RETR {filename}", write_data)

                    # Попытка декодирования как UTF-8
                    try:
                        content = data.decode('utf-8')
                    except UnicodeDecodeError:
                        print(f"Не удалось декодировать файл {filename} как UTF-8, сохраняем как есть.")
                        content = data.decode(errors='ignore')  # Игнорируем ошибки

                    print(f"Содержимое файла {filename}:")
                    print(content)
                    print(f"Файл {filename} успешно скачан с FTP сервера")

                    # local_save_path = os.path.join(downloads_path, filename)
                    # with open(local_save_path, 'wb') as local_file:
                    #     local_file.write(data)
                    # print(f"Файл {filename} успешно сохранён на локальный компьютер по пути {local_save_path}")

                    # Проверяем наличие новых файлов на FTP сервере и проигрываем звуковой сигнал
                    new_files = check_ftp_for_new_files(ftp, last_files)
                    if new_files:
                        print(f"Новые файлы на FTP сервере: {', '.join(new_files)}")
                        last_files.update(new_files)
                        winsound.PlaySound('SystemAsterisk', winsound.SND_ALIAS)

                except Exception as e:
                    print(f"Ошибка при скачивании файла: {e}")
            else:
                print("Неверный выбор файла.")
        else:
            print("Неверный метод. Пожалуйста, выберите write или read.")

    ftp.quit()


get()
input("Press Enter to exit...")
