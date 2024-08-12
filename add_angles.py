import numpy as np
import pickle
import os
import argparse
def calculate_angles(data):
    """
    Вычисляет углы между последовательными точками траекторий в данных и добавляет их к данным.

    Args:
        data (numpy.ndarray): Массив координат траекторий в формате (n_samples, n_timesteps, 2).

    Returns:
        numpy.ndarray: Массив данных с добавленными углами в виде третьей координаты.
    """
    n_samples, n_timesteps, _ = data.shape
    augmented_data = np.zeros((n_samples, n_timesteps, 3))
    i = 0
    while i < n_samples:
        j = 0
        while j < n_timesteps:
            if (j == 0 and i == 0) or (i == n_samples - 1 and j == n_timesteps - 1):
                angle = 0
            elif j == n_timesteps - 1:
                v1 = data[i][j] - data[i][j-1]
                v2 = data[i+1][0] - data[i][j]
                v1 = v1 / np.linalg.norm(v1)
                v2 = v2 / np.linalg.norm(v2)
                angle = np.arccos(np.clip(np.dot(v1, v2), -1.0, 1.0))           
            else:
                v1 = data[i][j] - data[i][j-1]
                v2 = data[i][j+1] - data[i][j]
                
                v1 = v1 / np.linalg.norm(v1)
                v2 = v2 / np.linalg.norm(v2)
                angle = np.arccos(np.clip(np.dot(v1, v2), -1.0, 1.0))   
            if np.isnan(angle):
                angle = 0
            
            augmented_data[i][j] = np.array([data[i, j, 0], data[i, j, 1], angle])   
            
            #print(augmented_data[i][j])
            #input()
            j += 1
        i += 1
    return augmented_data
def process_pkl_files(folder_path):
    """
    Обрабатывает все .pkl файлы в указанной папке, вычисляет углы и сохраняет результат в новые файлы в папке angles.

    Args:
        folder_path (str): Путь к папке с файлами .pkl.
    """
    # Папка для сохранения обработанных файлов
    angles_folder_path = os.path.join(folder_path, 'angles')
    os.makedirs(angles_folder_path, exist_ok=True)
    
    for filename in os.listdir(folder_path):
        if filename.endswith('.pkl'):
            file_path = os.path.join(folder_path, filename)
            
            # Загрузка данных из файла
            with open(file_path, 'rb') as file:
                data = pickle.load(file)
            
            # Проверка, что данные имеют нужную форму
            if isinstance(data, list):
                data = np.array(data)
                
            if isinstance(data, np.ndarray) and data.ndim == 3 and data.shape[2] == 2:
                # Вычисление углов
                angles = calculate_angles(data)
                
                # Сохранение обработанных данных в новый файл
                new_filename = f"{os.path.splitext(filename)[0]}_angles.pkl"
                new_file_path = os.path.join(angles_folder_path, new_filename)
                
                with open(new_file_path, 'wb') as file:
                    pickle.dump(angles, file)
                
                print(f"Файл сохранён: {new_file_path}")
            else:
                print(f"Неверный формат данных в файле: {file_path}")
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process .pkl files and calculate angles.")
    parser.add_argument("folder_path", type=str, help="Path to the folder containing .pkl files.")
    args = parser.parse_args()

    process_pkl_files(args.folder_path)
