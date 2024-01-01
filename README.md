<span style="width:100%;display:flex;justify-content:center;">![title](static/public/images/company_logo.jpg)</span>

## Compatibility: Python 3.10 and above is a currently supported version of Python

#### Setup Steps :

- ##### <span style="color:red">Step 1</span> :
  Clone Repository using below command
  Using Https
  ```GIT
  git clone https://github.com/sharad-infobeans/smart-recuitement-assessment.git
  ```
  Using SSH
  ```GIT
  git clone git@github.com:sharad-infobeans/smart-recuitement-assessment.git
  ```
- ##### Step 2 :
- Install conda before proceeding to further step
- for installation in ubuntu refer this doc https://docs.anaconda.com/free/anaconda/install/linux/
- 
  Now After successfull installation Create the conda enviroment for the project
  ```shell
  conda create -n ENV_NAME flask
  ```
  ````shell
  conda activate ENV_NAME
    ```
  To check existing Environment list.
  ````

```shell
 conda env list
```

- ##### Step 3 :

  Now execute command one by one to install models and remaining dependencies

  ```shell
  sudo pip install git+https://github.com/openai/whisper.git
  ```

  ```shell
  sudo apt update && sudo apt install ffmpeg
  ```

  ```shell
  conda install mysqlclient
  ```

  ```shell
  sudo pip install mysql-connector-python
  ```

  ```shell
  sudo pip install kaleido
  ```

  ```shell
  sudo apt-get install wkhtmltopdf

  ```

- ##### Step 4 :
  Now install all required dependencies using below command
  ```shell
  pip install -r requirements.txt
  ```
- ##### Step 5 :

  Now Update credentials in the demo-config.ini file [https://github.com/sharad-infobeans/smart-recuitement-assessment/blob/master/demo-config.ini] 

```
[AppConfig]
DIRECTORY_PATH = /var/www/html/Ib-Investors-report/data/
SECRET_KEY = mysecret
OPENAI_API_KEY = REPLACE_ME_YOUR_OPENAI_SECRET_KEY
```
```
[Google]
GOOGLE_CLIENT_ID = xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
GOOGLE_CLIENT_SECRET = xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
GOOGLE_ENV_LOCAL = True
GOOGLE_SCOPE = profile email
GOOGLE_CLIENT_ID_JWT = xxxxxxxxxxxxxxxxxxxxxxxxxxx
```
```
[Mail]
MAIL_SERVER = smtp.gmail.com
MAIL_PORT = 587
MAIL_USERNAME = xxxxxxxxxxxxxxxxxxx
MAIL_PASSWORD = xxxxxxxxxxxxxxxxxxx
MAIL_USE_TLS = True
MAIL_USE_SSL = False
```
```
[Database]
USERNAME = xxxxxxx
PASSWORD = xxxxxxxx
HOST = localhost
DATABASE = xxxxx
```
```
[REACT]
REACT_APP = http://localhost:3000 (https://betascreening.creatingwow.in/)
REACT_APP_BACKEND_LOGOUT_URL = http://localhost:5000/auth/logout  or (https://betascreeningapi.creatingwow.in/auth/logout)
```

- ##### Step 6 :
  Now set the flask app file to FLASK_APP path
  ```shell
  export FLASK_APP=app.py
  ```
  run to enable debug mode
  ```shell
  export FLASK_DEBUG=1
  ```
- #### Step 7:

  Run the Database migration command

  ```shell
  flask db init
  ```

  ```shell
  flask db migrate
  ```

  ```shell
  flask db upgrade
  ```

  ```shell
  flask migrate-data
  ```

- ##### Step 8 :

  Now run the flask application using below command
Final step:  python app.py

  ```shell
  flask run
  ```



- ##### Note\*: Restart the server after installation of all modules
