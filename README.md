Math Web service
----------------

Web service accepts a function short name and value or values as inputs and return the corresponding calculated value.

During Service running all called functions are monitored, for that created 'monitor.log' file.
Will be logged python math's module function name with its argument and run time in seconds and microseconds.

It is presumed that negative value will not be provided, as otherwise will be provided error message.


Example: 
--------
    INFO: factorial_s((124545,)): 13 seconds
    INFO: ackermann((3, 5)): 0 seconds
    INFO: ackermann((3, 4)): 0 seconds

Available function list is following:
-------------------------------------
    -The n:th Fibonacci number F(n) with the value of n provided by the user.
    -The Ackermann function A(m,n) with values of m and n provided by the user.
    -The factorial n! of a non-negative integer n provided by the user.


Example with curl:
-------------------
    - curl -X GET --data "fib(147)" 127.0.0.1:8888 # 2353412818241252672952597492098
    - curl -X GET --data "ack(3, 4)" 127.0.0.1:8888 # 125
    - curl -X GET --data "fac(6)" 127.0.0.1:8888 # 720

For deployment in the cloud environment:
----------------------------------------
    - Created "Dockerfile" file, which can be used to create a docker image and be deployed as a container an send requests to the RESTful web service

Docker deployment commands:
---------------------------
    Docker build:
        - docker build --pull --rm -f "math-web-service/Dockerfile" -t math-web-service:latest "math-web-service" 
    Docker run:
        - docker run --rm -it  -p 8888:8888/tcp math-web-service:latest



For interacting with docker container, commands are following:
--------------------------------------------------------------
    - docker exec <contianer_id> curl -X GET --data "fib(147)" 127.0.0.1:8888 # 2353412818241252672952597492098
    - docker exec <contianer_id> curl -X GET --data "ack(3, 4)" 127.0.0.1:8888 # 125
    - docker exec <contianer_id> curl -X GET --data "fac(6)" 127.0.0.1:8888 # 720

    To get information about <container_id> can be used 'docker ps' command


Dependencies
-------------
* Docker
* Python 3

Test
----
    - For testing math functions used doctest module 
    - They are simple mathematical functions and doctest in this case is fitting very well

CMD
---
    - python app.py