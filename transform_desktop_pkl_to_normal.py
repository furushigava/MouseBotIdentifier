import pickle
import numpy as np
import os
import argparse
# Функция загрузки, нормализации и сохранения данных
def normalize_and_save_data(folder_path):
    # Получаем список всех файлов в указанной папке
    for filename in os.listdir(folder_path):
        if filename.endswith('.pkl'):
            file_path = os.path.join(folder_path, filename)
            
            with open(file_path, 'rb') as file:
                data = pickle.load(file)
                # Преобразование данных в float64 для избежания ошибок с типами данных
                data = np.array(data, dtype=np.float64)
                # Нормализация данных
                data[..., 0] /= 1920  # Нормализуем координаты X
                data[..., 1] /= 1080  # Нормализуем координаты Y
                
                # Определение нового имени файла
                base, ext = os.path.splitext(filename)
                new_filename = f"{base}_normal{ext}"
                new_file_path = os.path.join(folder_path, new_filename)
                
                # Сохранение нормализованных данных в новый файл
                with open(new_file_path, 'wb') as new_file:
                    pickle.dump(data, new_file)
                print(f"Сохранены нормализованные данные в файл: {new_file_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Normalize .pkl files in a folder.")
    parser.add_argument("folder_path", type=str, help="Path to the folder containing .pkl files.")
    args = parser.parse_args()

    normalize_and_save_data(args.folder_path)


