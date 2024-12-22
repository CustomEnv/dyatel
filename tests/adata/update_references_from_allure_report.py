import base64
import json
import os
from io import BytesIO
from pathlib import Path

from PIL import Image


def get_project_path(suffix: str = ''):
    return str(Path(os.path.dirname(__file__)).parent.parent.joinpath(suffix))


def get_reference_screenshots_path():
    return os.path.dirname(__file__) + '/visual/reference/'


def collect_screenshot_names_and_files(directory):
    sources = {}

    for root, _, files in os.walk(f'{directory}/data/test-cases'):
        for filename in files:
            file_path = os.path.join(root, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)  # Parse allure tests case file
                attachments = data['testStage'].get('attachments', {})
                if attachments:
                    for attachment in attachments:
                        if attachment['type'] == 'application/vnd.allure.image.diff':
                            _screenshot_name = attachment['name'].replace('diff_for_', '') + '.png'
                            sources[_screenshot_name] = attachment['source']

    return sources


def replace_references(directory):
    reference_screenshots_dir_path = get_reference_screenshots_path()
    for screenshot_name, file_name in collect_screenshot_names_and_files(directory).items():
        with open(f'{directory}/data/attachments/{file_name}', 'r', encoding='utf-8') as file:
            data = json.load(file)
            image_bytes = base64.b64decode(data['actual'].replace('data:image/png;base64,', ''))
            image = Image.open(BytesIO(image_bytes))  # noqa
            image.save(reference_screenshots_dir_path + screenshot_name)
            print('Replaced: ', screenshot_name)


if __name__ == '__main__':
    replace_references(get_project_path('allure-report'))
