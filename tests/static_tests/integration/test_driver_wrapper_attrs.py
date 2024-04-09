def test_driver_variables_android_tablet(mocked_android_tablet_driver):
    dw = mocked_android_tablet_driver

    assert dw.is_desktop is False
    assert dw.is_mobile is False
    assert dw.is_ios is False
    assert dw.is_android_mobile is False
    assert dw.is_ios_mobile is False
    assert dw.is_ios_tablet is False

    assert dw.is_tablet is True
    assert dw.is_appium is True
    assert dw.is_android is True
    assert dw.is_android_tablet is True


def test_driver_variables_ios_tablet(mocked_ios_tablet_driver):
    dw = mocked_ios_tablet_driver

    assert dw.is_desktop is False
    assert dw.is_mobile is False
    assert dw.is_android is False
    assert dw.is_ios_mobile is False
    assert dw.is_android_mobile is False
    assert dw.is_android_tablet is False

    assert dw.is_tablet is True
    assert dw.is_appium is True
    assert dw.is_ios is True
    assert dw.is_ios_tablet is True


def test_driver_variables_android_mobile(mocked_ios_driver):
    dw = mocked_ios_driver

    assert dw.is_desktop is False
    assert dw.is_android_mobile is False
    assert dw.is_ios_tablet is False
    assert dw.is_tablet is False
    assert dw.is_android_tablet is False
    assert dw.is_android is False

    assert dw.is_ios is True
    assert dw.is_ios_mobile is True
    assert dw.is_mobile is True
    assert dw.is_appium is True


def test_driver_variables_ios_mobile(mocked_android_driver):
    dw = mocked_android_driver

    assert dw.is_desktop is False
    assert dw.is_ios_mobile is False
    assert dw.is_android_tablet is False
    assert dw.is_tablet is False
    assert dw.is_ios_tablet is False
    assert dw.is_ios is False

    assert dw.is_android is True
    assert dw.is_android_mobile is True
    assert dw.is_mobile is True
    assert dw.is_appium is True
