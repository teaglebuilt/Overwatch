*** Settings ***
Documentation  Common keywords for capturing http activity

Library  SeleniumProxy
Library  UIRepository
Library  Collections
Library  String


*** Keywords ***
Capture Response
    [Arguments]  ${url}
    ${res}=  Wait For Request  ${url}  
    ${response}=  Get From Dictionary  ${res}  response
    [Return]  ${response}