import pytest


def skip_platform(item: pytest.Item, platform: str):
    """
    Skip test on given platform in args

    Example::
      @pytest.mark.skip_platform('ios', reason='Fix needed')
      @pytest.mark.skip_platform(platform='desktop', reason='Fix needed')

    :param item: test function object ~ <function test_non_adult_sign_up_dialogue_and_links at 0x10ad658b0>
    :param platform: current platform name ~ selenium, playwright, appium
    :return: None
    """
    skip_platform_marker = item.get_closest_marker('skip_platform')
    skip_platform_kwargs = getattr(skip_platform_marker, 'kwargs', {})

    if platform in str(getattr(skip_platform_marker, 'args', [])):
        skip_message = f"Skip platform {platform}. Reason={skip_platform_kwargs.get('reason')}"
        item.add_marker(pytest.mark.skip(skip_message))
