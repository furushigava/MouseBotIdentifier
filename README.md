# MouseBotIdentifier

Этот проект включает в себя модель машинного обучения, которая определяет, является ли движение мыши человеком или ботом. Проект включает в себя как создание и тренировку модели, так и веб-версию для тестирования и сбора данных.

## Структура проекта

- `saved_model/` - директория для сохранения моделей и чекпоинтов.
- `web/` - директория для веб-приложения (данные, статические файлы, шаблоны и приложение Flask).
- `add_angles.py` - скрипт для добавления углов в данные перемещений мыши.
- `const.py` - конфигурационный файл с путями к данным и модели.
- `create_model.py` - скрипт для создания и тренировки модели.
- `model_work.py` - скрипт для работы с моделью (предсказания и оценка).
- `mouse_position_saver.py` - скрипт для сохранения данных перемещений мыши.
- `random_move.py` - скрипт для генерации случайных перемещений мыши.
- `resource_override_mouse_checker_client.js` - скрипт для сохранения данных перемещений мыши из браузера.
- `transform_desktop_pkl_to_normal.py` - скрипт для нормализации данных из `mouse_position_saver`.
- `transform_pkl_from_js_to_normal.py` - скрипт для нормализации данных из браузера.

## Установка и запуск

```bash
git clone https://github.com/furushigava/Mouse_Movement_Detection_Model
```

## Работа с моделью

### Веб-версия

Веб-версия доступна по ссылке: https://furushigava.github.io/MouseBotIdentifier/
PS: Чем ближе значение к 0 — тем больше вероятность того, что движется человек. 1 — бот.

Чтобы запустить локально:
```bash
python web/app.py
```
Тестирование модели будет здесь: http://127.0.0.1:5000/check_model

### Терминальная версия

```bash
python model_work.py --model_path saved_model/CNN_LSTM --data_files path_to_your_pkl_file
```

## Скрипты

### 1. `mouse_position_saver.py`

Этот скрипт используется для сбора данных о перемещениях мыши. Он записывает координаты мыши в .pkl файл.

### 2. `transform_desktop_pkl_to_normal.py`

Этот скрипт преобразует данные о перемещениях мыши, полученных с помощью mouse_position_saver, сохранённые в .pkl файле, в диапазон [0;1]. Это необходимо для нормализации данных перед обучением модели.

### 3. `resource_override_mouse_checker_client.js`

Этот скрипт обеспечивает обработку данных из браузера. Установите расширение Resource Override и используйте resource_override_mouse_checker_client.js для сбора данных с помощью этого расширения Запустите app.py для приема данных на сервере.

### 4. `transform_pkl_from_js_to_normal.py`

Этот скрипт преобразует данные о перемещениях мыши, полученных с помощью resource_override_mouse_checker_client.js + app.py, сохранённые в .pkl файле, в диапазон [0;1]. Это необходимо для нормализации данных перед обучением модели.

### 5. `add_angles.py`

Все данные, что полученные с помощью mouse_position_saver, что полученные через resource_override_mouse_checker_client.js+app.py и нормализованные через соответствующие скрипты-трансорматоры, необходимо прогнать ещё через add_angles.py, чтобы добавить третью переменную — угол

### 6. `random_move.py`

Делает рандомные передвижения по экрану.

### 7. `create_model.py`

Дописать. По модель обучалась на следующих данных. Входные данные имеют формат: [Count_batches,40,3], то есть 1 батч = 40 перемещений, перемещение = 2 координаты и угол между векторами (первый вектор: нынешняя точка и предыдущая, второй ветор: нынешняя и следующая), на выходе массив [Count_batches,1], то есть на выходе Count_batches чисел принадлежащих промежутку от 0 до 1, где 0 — человек, 1 — бот.
