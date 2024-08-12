import argparse
import pickle

def load_data(filename):
    with open(filename, 'rb') as file:
        return pickle.load(file)

def transform_data(data):
    transformed = []
    
    for group in data:
        transformed_group = [[point['x'], point['y']] for point in group]
        transformed.append(transformed_group)
    
    return transformed

def main(input_file, output_file):
    # Загрузка данных
    data = load_data(input_file)
    
    # Преобразование данных
    transformed_data = transform_data(data)
    
    # Сохранение преобразованных данных в новый файл
    with open(output_file, 'wb') as file:
        pickle.dump(transformed_data, file)
    
    print(f"Data transformed and saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Преобразование данных из файла и сохранение их в новый файл.")
    parser.add_argument('input_file', type=str, help='Имя входного файла для обработки (pickle формат)')
    parser.add_argument('output_file', type=str, help='Имя выходного файла для сохранения преобразованных данных')

    args = parser.parse_args()

    main(args.input_file, args.output_file)
