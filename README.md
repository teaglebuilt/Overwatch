# Production Monitoring System

This demo is an example of a production monitoring system that runs automated tests in production with a data pipeline to elasticsearch / kibana.

<div align="center">
    <a href="https://developers.google.com/web/tools/lighthouse/">
      <img src="https://raw.githubusercontent.com/teaglebuilt/Overwatch/master/assets/pipeline.png" alt="System Diagram" />
    </a>
</div>

# Purpose

I believe RobotFramework is an incredible tool in because of its extensibility and capabilities for python developers.

I created a library [robotframework-seleniumproxy](https://github.com/teaglebuilt/robotframework-seleniumproxy) that extends [robotframework-seleniumlibrary](https://github.com/robotframework/SeleniumLibrary). The difference is that it uses a threaded proxy server / client to capture the request / responses generated from the webdriver.

# How is this relevant?

In finding a solution for automating production tests. We typically go with the approach for a basic solution like sanity tests. Others may feel comftorable automating user behaviour without writing to production databases. This can still be a tricky process.

I have found the best solution is to adleast test the services integrated with the application. To record the actual request / responses generated by the actions webdriver would be ideal.

This would allow for us to create keywords in our test cases that will pass or fail from the result of a service that was called by the action of the test suite at run time.

None the less, even better would be to log this data and send it to our ELK stack for long term visualition and to analyze our product as it continues to exist as we merge changes.

# Tools

1. Python / RobotFramework
2. Extending Seleniums Webdriver / Extending SeleniumLibrary
3. Python Logging Libraries
4. RabbitMQ
5. Logstash
6. ElasticSearch
7. Kibana
