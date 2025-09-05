import pandas as pd
import os
import glob


def show_files():
    csv_files = glob.glob("*.csv")

    if not csv_files:
        print("В текущей директории нет CSV файлов")
        return None

    print("\nДоступные файлы")
    for i, file_name in enumerate(csv_files, 1):
        file_size = os.path.getsize(file_name)
        file_size_mb = file_size / (1024 * 1024)
        print(f"{i}. {file_name} ({file_size_mb:.2f} МБ)")

    return csv_files


def select_file():
    csv_files = show_files()

    if not csv_files:
        return None

    try:
        choice = input("\nВыберите файл: ").strip()

        if not choice.isdigit():
            print("Пожалуйста, введите номер файла")
            return None

        choice_num = int(choice) - 1
        if 0 <= choice_num < len(csv_files):
            selected_file = csv_files[choice_num]
            return selected_file
        else:
            print(f"Некорректный номер")
            return None

    except ValueError:
        print("Введите корректный номер")
        return None


def validate_data(file_data):

    if file_data.empty:
        print("В файле нет данных")
        return None, None

    for col in file_data.columns:
        if col == 'region':
            continue

        for index, value in enumerate(file_data[col]):
            try:
                pd.to_numeric([value])
            except (ValueError, TypeError):
                print(f"Ошибка: Некорректные данные в колонке '{col}', строка {index + 2}: '{value}'")
                exit(1)


def load_file():
    file_name = select_file()
    if not file_name:
        return None, None

    file_size = os.path.getsize(file_name)
    if file_size > 20 * 1024 * 1024:
        print("Файл слишком большой (максимум 20 МБ)")
        return None, None

    try:
        file_data = pd.read_csv(file_name)

        validate_data(file_data)

        print(f"\nФайл '{file_name}' успешно загружен ")
        print(f"Строк: {len(file_data)}, Колонок: {len(file_data.columns)}")
        print("Колонки:", list(file_data.columns))

        return file_data, file_name

    except Exception as error:
        print(f"Ошибка при чтении файла: {error}")
        return None, None


def calculate_metrics(file_data):
    numeric_columns = []
    for col in file_data.columns:
        try:
            pd.to_numeric(file_data[col].dropna())
            numeric_columns.append(col)
        except:
            continue

    print("Доступные колонки:")
    for i, col in enumerate(numeric_columns, 1):
        print(f"{i}. {col}")

    try:
        choice = input("Выберите номер колонки: ").strip()

        if not choice.isdigit():
            print("Пожалуйста, введите номер колонки")
            return

        choice_num = int(choice) - 1
        if choice_num < 0 or choice_num >= len(numeric_columns):
            print("Некорректный номер колонки")
            return

        column_name = numeric_columns[choice_num]

        try:
            data = pd.to_numeric(file_data[column_name])

            if data.isna().any():
                print("Ошибка: Обнаружены некорректные значения")
                exit(1)

            print(f"\nМетрики для колонки '{column_name}':")
            print(f"Количество значений: {len(data)}")
            print(f"Минимум: {data.min():.2f}")
            print(f"Максимум: {data.max():.2f}")
            print(f"Среднее: {data.mean():.2f}")
            print(f"Медиана: {data.median():.2f}")

        except ValueError as error:
            print(f"Ошибка: '{error}'")
            exit(1)

    except ValueError:
        print("Введите корректный номер")
    except Exception as error:
        print(f"Ошибка: {error}")


def calculate_percentiles(file_data):
    numeric_columns = []
    for col in file_data.columns:
        try:
            pd.to_numeric(file_data[col].dropna())
            numeric_columns.append(col)
        except:
            continue

    if not numeric_columns:
        print("В файле нет числовых колонок")
        return

    print("Доступные числовые колонки:")
    for i, col in enumerate(numeric_columns, 1):
        print(f"{i}. {col}")

    try:
        choice = input("Выберите номер колонки: ").strip()

        if not choice.isdigit():
            print("Пожалуйста, введите номер колонки")
            return

        choice_num = int(choice) - 1
        if choice_num < 0 or choice_num >= len(numeric_columns):
            print(f"Неверный выбор. Выберите от 1 до {len(numeric_columns)}")
            return

        column_name = numeric_columns[choice_num]

        try:
            data = pd.to_numeric(file_data[column_name])

            if data.isna().any():
                print("Ошибка: Обнаружены некорректные значения")
                exit(1)

            print(f"\nПерцентили для колонки '{column_name}':")
            for p in range(0, 101, 5):
                percentile_value = data.quantile(p / 100)
                print(f"{p:2d}%: {percentile_value:.2f}")

        except ValueError as error:
            print(f"Ошибка: '{error}'")
            exit(1)

    except ValueError:
        print("Введите корректный номер")
    except Exception as error:
        print(f"Ошибка: {error}")


def command_interface():
    current_file = None
    current_file_name = None

    while True:
        print("\nВыберите действие")
        if current_file_name:
            print(f"Текущий файл: {current_file_name}")
        else:
            print("Файл не выбран")
        print("1. Выбрать файл")
        print("2. Рассчитать метрики")
        print("3. Рассчитать перцентили")
        print("4. Выход")

        choice = input("Выберите действие (1-4): ").strip()

        if choice == "1":
            file_data, file_name = load_file()
            if file_data is not None:
                current_file = file_data
                current_file_name = file_name

        elif choice == "2":
            if current_file is None:
                print("Файл не выбран")
            else:
                calculate_metrics(current_file)

        elif choice == "3":
            if current_file is None:
                print("Файл не выбран")
            else:
                calculate_percentiles(current_file)

        elif choice == "4":
            break

        else:
            print("Неизвестная команда")


if __name__ == "__main__":
    command_interface()