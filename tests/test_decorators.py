"""
Тестовый-модуль tests_decorators.py содержит кейсы для тестирования функций модуля generators.py.
"""

from typing import Any

from src.decorators import log_file
from src.decorators import my_function


def test_log_my_function(capsys: Any) -> Any:
    my_function(1, 2)
    captured = capsys.readouterr()

    if not captured.out and not captured.err:

        #  Данные не выводятся в stdout, они выводятся в file, смотрим в него.
        with open("mylog.txt", "r", encoding="utf-8") as file:
            log_content = file.read()

        generator_logs = (line_log.strip() for line_log in log_content.split("\n") if line_log.strip())

        for log_report in generator_logs:
            components_log_report = log_report.split()
            function_operation_status = components_log_report[3]

            assert function_operation_status == "ok", f"В {log_file} есть данные об ошибках."

    else:

        components_log_terminal = captured.out.split()

        name_func = components_log_terminal[2]
        function_operation_status = components_log_terminal[3]

        assert name_func == my_function.__name__, "Декоратор в логах формирует не правильно имя_функции"
        assert captured.err == "", "Декоратор работает не корректно"

        if captured.err == "":
            assert function_operation_status == "ok", "Декоратор не правильно формирует логи"
