import io
import logging
from subprocess import Popen, PIPE, run

from PIL import Image


def rescale_image(screenshot_binary: bytes, scale=3, img_format='JPEG') -> bytes:
    img = Image.open(io.BytesIO(screenshot_binary))
    img = img.resize((img.width // scale, img.height // scale), Image.Resampling.LANCZOS)

    return save_image(img, img_format)


def resize_image(image1: str, image2: str, img_format='JPEG') -> bytes:
    img1 = Image.open(image1)
    img2 = Image.open(image2)

    width, height = img2.size
    img1.resize((width, height), Image.Resampling.LANCZOS)

    return save_image(img1, img_format)


def save_image(img: Image, img_format='JPEG'):
    result_img_binary = io.BytesIO()
    img.convert('RGB').save(result_img_binary, format=img_format, optimize=True)
    return result_img_binary.getvalue()


def shell_running_command(cmd, **kwargs):
    return Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE, close_fds=True, **kwargs)


def shell_command(cmd,  **kwargs):
    process = run(cmd, shell=True, **kwargs)

    if process.stdout:
        process.output = process.stdout.decode('utf8').replace('\n', '')
    if process.stderr:
        process.errors = process.stderr.decode('utf8').replace('\n', '')
    if isinstance(process.returncode, int):
        process.is_success = process.returncode == 0

    return process


def cut_log_data(data: str, length=50) -> str:
    """
    Cut given data for reducing log length

    :param data: original data ~ 'very long string for typing. string endless continues'
    :param length: length to cut given data ~ 20
    :return: edited data ~ 'Type text: "very long string for >>> 36 characters"'
    """
    data = str(data)
    return f'{data[:length]} >>> {len(data[length:])} characters' if len(data) > length else data


def disable_logging(loggers: list) -> None:
    """
    Disable logging for given loggers

    :param loggers: list of loggers to be disabled
    :return: None
    """
    for logger in loggers:
        logging.getLogger(logger).disabled = True


def set_log_level(loggers: list, level: int) -> None:
    """
    Set log level for given loggers

    :param loggers: list of loggers to be disabled
    :param level: level to be set
    :return: None
    """
    for logger in loggers:
        logging.getLogger(logger).setLevel(level)
