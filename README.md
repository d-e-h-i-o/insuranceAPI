# insuranceAPI  
![image](assets/contract_picture.jpg)  

This is an insurance recommendation API. A user can register, login, logout, and post questionnaire data for which he will get a set of insurance recomendation as response.
## API usage

The app ist currenty hosted and accessible at ```http://insurance-agent.store```. It is hosted on a Heroku dyno, so it might take some time for startup at the first request.
  
**Important**: The connection is not SSL/TLS encrypted, so do not send any personal information or passwords you use at other services. The endpoint is just for demonstration purposes.
Also please understand that the API results are not an official consultation and just used for information purposes.

### Register
POST to ```http://insurance-agent.store/register``` with JSON-payload:
```
{
	"username": <username>,
	"email": <email>,
	"password": <password>
}
```
### Get a recommendation
POST to ```http://insurance-agent.store/recommendation``` with JSON-payload:
```
{
  "first_name": <firstname>,
  "address": <address>,
  "occupation": <occupation>, (in {Employed, Student, Self-employed})
  "email_address": <email>,
  "children": <Boolean>,
  "num_children": <int> (optional)
}
```
### Login/Logout
The app also supports login (```{"username": <username>, "password": <password>}```) at ```http://insurance-agent.store/login``` and logout at  ```http://insurance-agent.store/logout```. Registering will automatically log you in.

## Run the app locally

1. Clone repository  
```git clone https://github.com/d-e-h-i-o/insuranceAPI.git```  
```cd insuranceAPI/```
2. Create virtual environment  
```python3 -m venv venv```
3. Activate virtual environment   
```source venv/bin/activate``` 
4. Install requirements  
```pip install -r requirements.txt```
5. Set environment variables  
```export DATABASE_URL="postgresql:///insuranceapi_dev"```  
```export APP_SETTINGS="config.DevelopmentConfig"```  
```export FLASK_APP="api_app:create_app()"```  
```export SECRET_KEY=<something_really_secret>```  
6. Set up database   
```createdb insuranceapi_dev```  
7. Run app  
```flask run```  

## Run test suite
1. Set up database   
```createdb insuranceapi_test``` 
2. Run tests  
```python -m pytest tests/ --capture=tee-sys```  

# Todo
* Integrate JWT
* Integrate Flask-Admin
* Use mypy and type hints
* Use docker
