*** Settings ***
Library    SeleniumProxy



*** Keywords ***
Wait Until Page Loads
    Wait Until Keyword Succeeds  ${PAGE_LOAD_TIMEOUT}  1 sec  _page is loaded

_page is loaded
    [documentation]  Checks if page is fully loaded. If not, it will fail.
    ${state}=  Execute Javascript  return document.readyState
    Run Keyword If  '${state}' != 'complete'  Fail  Page is not loaded

Robust Click Element
    [arguments]  ${locator}
    Wait Until Keyword Succeeds  4 sec  1 sec  Click Element  ${locator}