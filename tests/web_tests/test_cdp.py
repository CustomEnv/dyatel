from time import sleep


def test_mock_response(driver_wrapper):
    sleep(1)
    print('start')
    driver_wrapper.cdp.enable_intercept('dyatel-playground/advanced.html')
    print('enabled')
    driver_wrapper.get('https://envinc.github.io/dyatel-playground/advanced.html')
    print('navigated')
    driver_wrapper.cdp.mock_response('dyatel-playground/advanced.html')
    print('paused')
    # driver_wrapper.cdp.request_paused('dyatel-playground/advanced.html')
    # driver_wrapper.cdp.get_request_data('dyatel-playground/advanced.html')

