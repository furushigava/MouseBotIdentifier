import numpy as np
import tensorflow
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, MaxPooling1D, LSTM, Dropout, Dense, GRU, Attention, Concatenate, Input
from tensorflow.keras.optimizers import Adam
from keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.models import Model
import pickle
from tensorflow.keras.layers import Dropout
import os
from keras.regularizers import l2
from tensorflow.keras.callbacks import ModelCheckpoint, ProgbarLogger
from const import *
#data_directory = 'C:\\Users\\USER\\Desktop\\mouse_checker\\web\\data\\game\\'
data_directory = DATA_DIRECTORY_FOR_MODEL_TRAIN
checkpoint_dir = CHECKPOINT_DIR
save_path = PATH_TO_SAVE_MODEL

#МБ СДЕЛАТЬ ЖЕСТЧЕ ПРОВЕРКУ НА ЗАСТОЙ МЫШИ, так как там тупо повторы по 30 мб
#ПОСМОТРЕТЬ МОДЕЛЬ КОТОРАЯ ЗА НОЧЬ ДОУЧИТСЯ, ПЕРЕИМЕНОВАТЬ ЕЁ В _40
#без углов максимум обучения на 3х файлах с хрома — ~60%, добавляем углы и она около 90.
#ограничить повторы 1, чтобы угл имел смысл

print(tensorflow.config.get_visible_devices())

def load_data_from_pickle(filenames):
    data = []
    for filename in filenames:
        with open(filename, 'rb') as file:
            loaded_data = pickle.load(file)
            data.extend(loaded_data)
    return np.array(data)  # Ensure it returns a numpy array

def get_files_from_directory(directory):
    human_files = []
    bot_files = []
    for filename in os.listdir(directory):
        if filename.endswith('.pkl'):
            filepath = os.path.join(directory, filename)
            if 'bot' in filename.lower():
                bot_files.append(filepath)
            else:
                human_files.append(filepath)
    return human_files, bot_files

# Получение списков файлов
human_files, bot_files = get_files_from_directory(data_directory)

# Загрузка данных
data_human = load_data_from_pickle(human_files)
data_bot = load_data_from_pickle(bot_files)
print(f'Shape of human data: {data_human.shape}')
print(f'Shape of bot data: {data_bot.shape}')

# Проверка и подготовка данных
n_samples_human = len(data_human)
n_samples_bot = len(data_bot)
n_timesteps = len(data_human[0])  # количество временных шагов
n_features = len(data_human[0][0])  # количество признаков (x, y)

# Преобразование данных в numpy массивы и выравнивание формы
data_human = np.array(data_human).reshape((n_samples_human, n_timesteps, n_features))
data_bot = np.array(data_bot).reshape((n_samples_bot, n_timesteps, n_features))

# Объединение данных человека и бота
all_data = np.concatenate((data_human, data_bot), axis=0)

# Метки классов: 0 для человека, 1 для бота
train_labels = np.array([0] * n_samples_human + [1] * n_samples_bot)

class_weights = {0: 1., 1: n_samples_human / n_samples_bot}

# Создание модели
#CNN + LSTM
model = Sequential()
model.add(Conv1D(filters=64, kernel_size=3, activation='relu', input_shape=(40, 3)))
model.add(MaxPooling1D(pool_size=2))
model.add(Conv1D(filters=128, kernel_size=3, activation='relu'))
model.add(MaxPooling1D(pool_size=2))
model.add(Dropout(0.5))
model.add(LSTM(64))
model.add(Dropout(0.5))
model.add(Dense(1, activation='sigmoid'))

# Компиляция модели
model.compile(loss='binary_crossentropy', optimizer=Adam(learning_rate=0.0001), metrics=['accuracy'])

model.summary()

# Путь для сохранения модели и чекпоинтов

if not os.path.exists(checkpoint_dir):
    os.makedirs(checkpoint_dir)

checkpoint_filepath = os.path.join(checkpoint_dir, 'model_epoch_{epoch:02d}_acc_{val_accuracy:.2f}.h5')
# Callback для сохранения чекпоинтов
checkpoint = ModelCheckpoint(
    filepath=checkpoint_filepath,
    save_weights_only=False,
    monitor='val_accuracy',
    mode='max',
    save_best_only=True
)

# Callback для отображения прогресса
progbar_logger = ProgbarLogger(count_mode='samples')

# Обучение модели с использованием callback-ов
verbose, epochs, batch_size = 1, 10000, 256
history = model.fit(
    all_data, train_labels,
    epochs=epochs,
    batch_size=batch_size,
    verbose=verbose,
    validation_split=0.2,  # если есть валидационные данные
    callbacks=[checkpoint, progbar_logger],
    class_weight=class_weights
)

# Оценка модели
_, accuracy = model.evaluate(all_data, train_labels, batch_size=batch_size, verbose=0)
print(f'Accuracy: {accuracy}')

# Сохранение окончательной модели
model.save(save_path)

#epochs, batch_size, batch len

#epochs, batch_size, batch len
#model = Sequential()
#model.add(LSTM(200, input_shape=(n_timesteps, n_features)))
#model.add(Dense(1, activation='sigmoid'))
#model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
#model.summary()