import serial
import logging
import time
from typing import Optional
from serial.tools import list_ports

logger = logging.getLogger(__name__)

class SerialCommunicator:
    def __init__(self, port: str, baudrate: int = 9600, timeout: int = 3000):
        """
        Инициализирует последовательный порт.

        :param port: Порт, к которому подключено устройство (например, 'COM3' или '/dev/ttyUSB0')
        :param baudrate: Скорость передачи данных
        :param timeout: Таймаут чтения в секундах
        """
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser: Optional[serial.Serial] = None

        self._open_serial_port()

    def _open_serial_port(self):
        """Открывает последовательный порт с обработкой исключений."""
        try:
            self.ser = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=self.timeout,
                write_timeout=self.timeout  # Таймаут для записи
            )
            logging.info(f"Открыт последовательный порт {self.port} со скоростью {self.baudrate} бод")
            time.sleep(2.0) # Задержка после открытия порта
            logging.info(f"{self.port} готов к работе")
        except serial.SerialException as e:
            logging.error(f"Не удалось открыть порт {self.port}: {e}")
            self.ser = None

    def send_command(
            self,
            command: str,
            expected_response: Optional[str] = None,
            retries: int = 3,
            delay: float = 0.5
        ) -> bool:
        """
        Отправляет команду на устройство и проверяет ожидаемый ответ с повторными попытками.

        :param command: Команда для отправки
        :param expected_response: Ожидаемый ответ от устройства
        :param retries: Количество попыток отправки команды
        :param delay: Задержка между попытками в секундах
        :return: True, если команда успешно отправлена и получен ожидаемый ответ, иначе False
        """
        if not self.ser or not self.ser.is_open:
            logging.error("Последовательный порт не открыт")
            return False

        for attempt in range(1, retries + 1):
            try:
                # Очистка буферов перед отправкой команды
                self.ser.reset_input_buffer()
                self.ser.reset_output_buffer()

                # Отправка команды
                full_command = command.strip() + '\n'
                self.ser.write(full_command.encode('utf-8'))
                logging.debug(f"Отправлено (попытка {attempt}): {command}")

                # Ожидание ответа с использованием read_response
                response = self.read_response()

                if response is None:
                    logging.warning("Не получен ответ от устройства")
                elif expected_response is None:
                    logging.info("Команда отправлена без ожидания ответа")
                    return True
                elif expected_response.lower() in response.lower():
                    logging.info(f"Ожидаемый ответ получен: {response}")
                    return True
                else:
                    logging.warning(f"Неожиданный ответ от устройства: {response}")
            except Exception as e:
                logging.error(f"Необработанная ошибка: {e}")  # Дополнительная безопасность

            if attempt < retries:
                logging.debug(f"Повторная попытка через {delay} секунд...")
                time.sleep(delay)
            else:
                logging.error(f"Не удалось получить ожидаемый ответ после {retries} попыток")

        return False

    def read_response(self, timeout: Optional[float] = None) -> Optional[str]:
        """
        Читает ответ от устройства без отправки команды.

        :param  timeout: Временной лимит ожидания ответа. Если None, используется таймаут, установленный при инициализации
        :return: Полученный ответ или None в случае ошибки
        """
        if not self.ser or not self.ser.is_open:
            logging.error("Серийный порт не открыт")
            return None

        original_timeout = self.ser.timeout
        if timeout is not None:
            self.ser.timeout = timeout

        try:
            response = self.ser.readline().decode('utf-8').strip()
            if response:
                logging.debug(f"Получен ответ: {response}")
                return response
            else:
                logging.warning("Ответ не получен (таймаут)")
                return None
        except serial.SerialException as e:
            logging.error(f"Ошибка при чтении ответа: {e}")
            return None
        except UnicodeDecodeError as e:
            logging.error(f"Ошибка декодирования ответа: {e}")
            return None
        finally:
            # Восстановление оригинального таймаута
            if timeout is not None:
                self.ser.timeout = original_timeout

    def close(self):
        """Закрывает последовательный порт."""
        if self.ser and self.ser.is_open:
            self.ser.close()
            logging.info(f"Последовательный порт {self.port} закрыт")

    def __enter__(self):
        """Метод для использования класса в блоке with."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Гарантирует закрытие порта при выходе из блока with."""
        self.close()
    
    def __del__(self):
        self.close()
        """Гарантирует закрытие порта при удалении объекта."""
    
    @staticmethod
    def find_controller_port(
            command: str = "i",
            expected_response: str = "i",
            baudrate: int = 115200,
            timeout: float = 1.0,   # seconds
            retries: int = 5,
            delay: float = 1.0,
            delay_between_ports: float = 1
        ) -> Optional[str]:
        """
        Перебирает все доступные COM-порты, отправляет команду и ищет ответ от контроллера.

        :param command: Команда для отправки на каждый порт
        :param expected_response: Ожидаемый ответ от контроллера
        :param baudrate: Скорость передачи данных для портов
        :param timeout: Таймаут для чтения ответа
        :param retries: Количество попыток отправки команды на каждый порт
        :param delay: Задержка между попытками внутри порта
        :param delay_between_ports: Задержка между перебором разных портов
        :return: Строка с именем порта, если контроллер найден, иначе None
        """
        ports = list_ports.comports()
        logging.info("Доступные COM-порты: %s", [port.device for port in ports])

        for port_info in ports:
            port = port_info.device
            logging.info("Проверка порта: %s", port)

            if SerialCommunicator.check_port(port, command, expected_response, baudrate, timeout, retries, delay):
                logging.info("Контроллер найден на порту: %s", port)
                return port
            else:
                logging.debug("Контроллер не найден на порту: %s", port)

            time.sleep(delay_between_ports)

        logging.critical("Контроллер не найден на доступных COM-портах")
        return None

    @staticmethod
    def check_port(port: str, command: str, expected_response: str, baudrate: int, timeout: float, retries: int, delay: float) -> bool:
        """Проверяет указанный порт на наличие контроллера, отправляя команду и ожидая ответ."""
        try:
            with SerialCommunicator(port, baudrate=baudrate, timeout=timeout) as device:
                return device.send_command(command=command, expected_response=expected_response, retries=retries, delay=delay)
        except SerialException as e:
            logging.error("Не удалось открыть порт %s: %s", port, e)
        except Exception as e:
            logging.error("Произошла ошибка при проверке порта %s: %s", port, e)

        return False
