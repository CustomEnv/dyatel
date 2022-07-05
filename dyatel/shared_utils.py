import io
import logging
from subprocess import Popen, PIPE, run

from PIL import Image


def set_logging_settings(level=logging.INFO):
    logging.getLogger('WDM').setLevel(logging.ERROR)
    logging.getLogger("urllib3").setLevel(logging.ERROR)
    logging.basicConfig(level=level, format='[%(asctime)s][%(levelname)s][%(filename)s:%(lineno)s] %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    return logging


def resize_image(screenshot_binary, scale=3, img_format='JPEG'):
    img = Image.open(io.BytesIO(screenshot_binary))
    img = img.resize((img.width // scale, img.height // scale), Image.ANTIALIAS)

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
    return f'{data[:length]} >>> {len(data[length:])} characters' if len(data) > length else data
