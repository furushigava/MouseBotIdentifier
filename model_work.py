import numpy as np
import pickle
import argparse
from tensorflow.keras.models import load_model
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

# Функция для загрузки данных
def load_data_from_pickle(filename):
    with open(filename, 'rb') as file:
        return pickle.load(file)

# Анализ результатов
def analyse(data, y_true, model):
    y_pred_prob = model.predict(data)
    y_pred = (y_pred_prob > 0.5).astype(int)
    
    # Среднее значение предсказанных вероятностей
    average_probability = np.mean(y_pred_prob)
    print(f'Average predicted probability: {average_probability}')

    # Большинство голосов
    majority_vote = np.mean(y_pred) > 0.5
    print(f'Majority vote result: {"Bot" if majority_vote else "Human"}')

    # Максимальная вероятность
    max_probability = np.max(y_pred_prob)
    print(f'Maximum predicted probability: {max_probability}')

    # Взвешенное голосование (можно усложнить взвешивание)
    weighted_vote = np.mean(y_pred_prob) > 0.5
    print(f'Weighted vote result: {"Bot" if weighted_vote else "Human"}')

    # Можно выбрать один из этих методов или их комбинацию для принятия решения.
    final_decision = majority_vote  # например, используем большинство голосов

    print(f'Final decision: {"Bot" if final_decision else "Human"}')

    # Отчет о классификации на уровне подпоследовательностей
    if y_true is not None:
        print(classification_report(y_true, y_pred))
        print(f"Accuracy on the test set: {accuracy_score(y_true, y_pred)}")

    print(f"Count block's was analyzed: {len(data)}")

def work_with_data(file_to_analyse, model):
    new_data_for_check_human = load_data_from_pickle(file_to_analyse)
    analyse(new_data_for_check_human, None, model)

def education(file, model, bot=True):
    data = load_data_from_pickle(file)

    # Заморозка слоёв, кроме последних (опционально)
    for layer in model.layers[:-2]:
        layer.trainable = False
    
    # Преобразование данных в numpy массивы и выравнивание формы
    n_samples = len(data)
    n_timesteps = len(data[0])  # количество временных шагов
    n_features = 2  # количество признаков (x, y)

    all_data = np.array(data).reshape((n_samples, n_timesteps, n_features))
    if bot:
        train_labels = np.array([1] * n_samples)
    else:
        train_labels = np.array([0] * n_samples)

    # Разделение данных на обучающую и валидационную выборки
    X_train, X_val, y_train, y_val = train_test_split(all_data, train_labels, test_size=0.2, random_state=42)

    # Компиляция модели перед дообучением (если требуется)
    model.compile(optimizer=Adam(learning_rate=1e-5), loss='binary_crossentropy', metrics=['accuracy'])

    # Дообучение модели
    history = model.fit(X_train, y_train, epochs=10, batch_size=64, validation_data=(X_val, y_val))

    # Сохранение дообученной модели
    new_model_path = args.model_path
    model.save(new_model_path)

    print(f"Model saved to {new_model_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script for analyzing and training a model on mouse data.")
    parser.add_argument('--model_path', type=str, default='saved_model/baseLSTM_on_our_datas_updated', help='Path to the saved model')
    parser.add_argument('--data_files', type=str, nargs='+', default=['mouse_positions_bot_my.pkl', 'mouse_positions_bot_original.pkl', 'mouse_positions_human.pkl'], help='List of data files to analyze or train on')
    parser.add_argument('--education', action='store_true', help='Flag to indicate if the script should train (education) the model')
    parser.add_argument('--bot', action='store_true', help='Flag to indicate if the data is for bot (used for training)')

    args = parser.parse_args()

    model = load_model(args.model_path)

    if args.education:
        for file in args.data_files:
            education(file, model, bot=args.bot)
    else:
        for file in args.data_files:
            work_with_data(file, model)
