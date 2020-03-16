*** Settings ***
Documentation  Common keywords for authentication needed across all test suites
...
...            NOTE! This resource file expects UI Repository to by loaded in
...            global variable ${UI}

Library   SeleniumProxy
Resource  keywords/browser_keywords.robot
Resource  keywords/http_keywords.robot
Resource  keywords/common_keywords.robot


*** Keywords ***
Login of ${username} with ${password} should be ${expected}
    [documentation]  Template for data driven tests
    Login User  ${username}  ${password}
    Run Keyword If  '${expected}' == 'success'  User Should Be Logged In
    Run Keyword If  '${expected}' == 'failure'  User Should Not Be Logged In

Submit Credentials
    Input Text  //input[@id='UserName']  dteagle@cpicardgroup.com
    Input Password  //input[@id='Password']  Cosimoto!101
    Submit Form

Login User
    [documentation]  Logs in with ${username} and ${password}
    [arguments]  ${username}  ${password}  ${login_page}=${HOST}  ${alias}=${NONE}
    Open Custom Browser  ${login_page}  alias=${alias}
    Wait Until Page Loads
    Wait Until Page Contains Element  ${UI['login']}  timeout=10
    Submit Credentials  ${username}  ${password}

Login User And Verify
    [documentation]  Logs user and checks if login was successfull
    [arguments]  ${username}  ${password}  ${alias}=${NONE}
    Login User  ${username}  ${password}  alias=${alias}
    Wait Until Page Loads
    Wait Until Page Contains Element  ${UI['homepage.menu_bar']}  timeout=10
    User Should Be Logged In

User Should Be Logged In
    [documentation]  Checks several elements on page to verify that user is
    ...              IS logged
    Wait Until Page Loads
    Wait Until Page Contains  Profile
    Wait Until Page Contains  Version
    
    Wait Until Page Contains Element  ${UI['homepage.logout']}  
    Wait Until Page Contains Element  ${UI['homepage.menu_bar']}  
    Page Should Not Contain Element  ${UI['login.username']}
    Page Should Not Contain Element  ${UI['login.password']}

User Should Not Be Logged In
    [documentation]  Checks several elements on page to verify that user is
    ...              IS NOT logged
    Wait Until Page Loads
    Wait Until Page Contains Element  ${UI['login.username']}  
    Wait Until Page Contains Element  ${UI['login.password']}  
    Page Should Not Contain Element  ${UI['homepage.logout']}
    Page Should Not Contain Element  ${UI['homepage.menu_bar']}


Login Page Should display Locked Account Message
    Wait Until Page Contains Element  ${UI['login.username']}  
    Wait Until Page Contains Element  ${UI['login.password']}  
    Page Should Contain  Your account has been temporarily locked

Login Page Should Display Error Message
    Wait Until Page Contains Element  ${UI['login.username']}  
    Wait Until Page Contains Element  ${UI['login.password']}  
    Wait Until Page Contains Element  ${UI['login.errors']}  

Logout User
    Wait Until Page Contains Element  ${UI['homepage.logout']}
    Robust Click Element  ${UI['homepage.logout']}

Login User And Expect Expired Password
    [documentation]  Logs user and checks if expired password page is displayed
    [arguments]  ${username}  ${password}  ${alias}=${NONE}
    Login User  ${username}  ${password}  alias=${alias}
    Wait Until Page Loads
    Wait Until Element Is Visible  ${UI['expired_pass']}

Set New Password
    [arguments]  ${password}  ${new_password}
    Input Password  ${UI['expired_pass.original']}  ${password}
    Input Password  ${UI['expired_pass.new1']}  ${new_password}
    Input Password  ${UI['expired_pass.new2']}  ${new_password}
    Robust Click Element  ${UI['expired_pass.submit']}

Simulate 3 Unsuccessful Login Attempts
    [arguments]  ${user_name}  ${wrong_pass}
    Login User  ${user_name}  ${wrong_pass}
    # Sleep  5 sec
    Wait Until Page Loads
    Wait Until Element Is Visible  ${UI['login.errors']}
    User Should Not Be Logged In
    Robust Click Element  ${UI['login.errors']}
    Wait Until Element Is Not Visible  ${UI['login.errors']}

    Submit Credentials  ${user_name}  ${wrong_pass}
    # Sleep  5 sec
    Wait Until Page Loads
    Wait Until Element Is Visible  ${UI['login.errors']}
    User Should Not Be Logged In
    Robust Click Element  ${UI['login.errors']}
    Wait Until Element Is Not Visible  ${UI['login.errors']}

    Submit Credentials  ${user_name}  ${wrong_pass}
    # Sleep  5 sec
    Wait Until Page Loads
    Wait Until Element Is Visible  ${UI['login.errors']}
    User Should Not Be Logged In
