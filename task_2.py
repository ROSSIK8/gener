import datetime
import os
import time


def logger(path):
    def __logger(old_function):
        def new_function(*args, **kwargs):
            title = old_function.__name__
            time = str(datetime.datetime.now())[11:19]
            with open(path, 'a', encoding='utf-8') as file:
                file.write(f'Название функции: {title}\nВремя исполнения: '
                           f'{time}\nАргументы: {args}, {kwargs}\n'
                           f'Возвращаемое значение: {old_function(*args, **kwargs)}\n\n')
            return old_function(*args, **kwargs)

        return new_function

    return __logger


def test_2():
    paths = ('log_1.log', 'log_2.log', 'log_3.log')

    for path in paths:
        if os.path.exists(path):
            os.remove(path)

        @logger(path)
        def hello_world():
            return 'Hello World'

        @logger(path)
        def summator(a, b=0):
            return a + b

        @logger(path)
        def div(a, b):
            return a / b

        assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
        result = summator(2, 2)
        assert isinstance(result, int), 'Должно вернуться целое число'
        assert result == 4, '2 + 2 = 4'
        result = div(6, 2)
        assert result == 3, '6 / 2 = 3'
        summator(4.3, b=2.2)
        time.sleep(1)

    for path in paths:

        assert os.path.exists(path), f'файл {path} должен существовать'

        with open(path, 'r', encoding='utf-8') as log_file:
            log_file_content = log_file.read()

        assert 'summator' in log_file_content, 'должно записаться имя функции'

        for item in (4.3, 2.2, 6.5):
            assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__ == '__main__':
    test_2()