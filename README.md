## Technologies used
* [Django](https://www.djangoproject.com/)

## Installation
* If you wish to run your own build, first ensure you have python globally installed in your computer. If not, you can get python [here](https://www.python.org").
* After doing this, confirm that you have installed virtualenv globally as well. If not, run this:
    ```bash
        $ pip install virtualenv
    ```
* Then, Git clone this repo to your PC
    ```bash
        $ git clone https://github.com/EijiYoshimura/lem.git
    ```

* #### Dependencies
    1. Cd into your the cloned repo as such:
        ```bash
            $ cd lem/lem
        ```
    2. Create and fire up your virtual environment:
        ```bash
            $ virtualenv  venv -p python3
            $ source venv/bin/activate
        ```
    3. Install the dependencies needed to run the app:
        ```bash
            $ pip install -r requirements.txt
        ```
    4. Make those migrations work
        ```bash
            $ python manage.py makemigrations
            $ python manage.py migrate
        ```

* #### Run It
    Fire up the server using this one simple command:
    ```bash
        $ python manage.py runserver
    ```
    You can now access the file api service on your browser by using
    ```
        http://localhost:8000/app/employee 
        or
        http://localhost:8000/app/department
    ```
    
    ```/app/employee/
    API RESTFUL for employee management

    GET - return a list of employees that match parameters
        /app/employee/                  - list all employees
        /app/employee/?id=00            - list employee for specified id
        /app/employee/?email=xxx@xx.c   - list employee with informed email
        /app/employee/?name=xxxx        - list all employees that matches the string sequence (SQL LIKE). It is insensitive case
        /app/employee/?department_id=00 - list all employees for department

    POST - create a new employee registry. it will be set as active by default
        request.body should be in JSON format:
        {
            "name": "", 
            "email": "",
            "department_id": ""
        }

        - name          - REQUIRED - String(200)
        - email         - REQUIRED - String(200) - UNIQUE
        - department_id - OPTIONAL - integer - foreign key to Department
    
    PUT - allows to edit name, email, department and if it is active. Inform only the field to be edited
        request.body should be in JSON format:
        {
            "id": "",
            "name": "", 
            "email": "",
            "department_id": "",
            "active": ""
        }

        - id            - REQUIRED - employee.id
        - name          - OPTIONAL
        - email         - OPTIONAL
        - department_id - OPTIONAL
        - active        - OPTIONAL

    ```
