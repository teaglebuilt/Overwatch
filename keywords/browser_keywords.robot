*** Settings ***
Documentation  Common keywords for test execution

Library  SeleniumProxy
Library  UIRepository
Library  Collections
Library  String


*** Keywords ***
Configure Proxy Settings
    ${options}=  Create Dictionary
    ${false}=  Convert To Boolean  False
    Set To Dictionary  ${options}  ssl_verify  ${false}
    [Return]  ${options}

Open Custom Browser
    [Documentation]  Starts selected browser with respect to environment
    ...              settings.
    [Arguments]  ${url}  ${alias}=${NONE}
    Run Keyword if  '${BROWSER}' == 'chrome'  Run Chrome  ${url}  ${alias}
    ...    ELSE IF  '${BROWSER}' == 'firefox'  Run Firefox  ${url}  ${alias}
    ...    ELSE IF  '${BROWSER}' == 'ie'  Run Internet Explorer  ${url}  ${alias}
    ...    ELSE IF  '${BROWSER}' == 'edge'  Run Edge  ${url}  ${alias}

Run Chrome
    [documentation]  Startup keyword for Chrome browser
    ...              Here can be custom setup of browser
    [arguments]  ${url}  ${alias}
    Set Selenium Timeout  15 sec
    ${options}=  Configure Proxy Settings
    Open Proxy Browser  https://cardatonce.eftsource.com  Chrome  proxy_options=${options}
    Wait Until Page Loads