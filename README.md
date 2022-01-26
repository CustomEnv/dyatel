## UI_Automation

This project created to show [my](https://github.com/VladimirPodolyan) skills in UI automation process with:
- Python
- [Selenium](https://pypi.org/project/selenium/) in web application
- [Appium](https://pypi.org/project/Appium-Python-Client/) in Native app of iOS and Android
- Custom wrapper of selenium/appium named `selenium_master`

Frameworks for testing is [Tox](https://pypi.org/project/tox/) (should be manually installed) 
& [Pytest](https://pypi.org/project/pytest/). For reports used [Allure](https://pypi.org/project/allure-pytest/).


### Android automation with UiAutomator2:

Automated native app is a free project from [TestingBot](https://testingbot.com/appium/sample.apk).
Settings: 
- Appium parameters is `ip=0.0.0.0` `port=1000`
- Environment (Emulator/PATH/Java etc.) must be pre-builded before test run. 

This is how application looks like:

![anroid](https://user-images.githubusercontent.com/36446855/151223751-cf3bd790-b71e-40b0-8874-f3523497b9d0.png)

### iOS automation with XCUITest:

Automated native app is my custom project for iOS 15.2. 
Settings:
- Appium parameters is `ip=0.0.0.0` `port=2000`
- Environment (Simulator/PATH/Xcode etc.) must be pre-built before test run.

This is how application looks like:

![iPhone](https://user-images.githubusercontent.com/36446855/151223800-b6fad673-3b8c-44e3-8c3f-6c9824e15bd9.jpg)

### Chrome Web automation:

Web application is an edited free html pages from [W3C Sidebar](https://www.w3schools.com/w3css/w3css_sidebar.asp) 
and [W3C Tabs](https://www.w3schools.com/w3css/w3css_tabulators.asp).


### Example of report:

![Report](https://user-images.githubusercontent.com/36446855/151223843-14fbd2c0-1da5-47e0-8be0-19855393a98a.jpg)
