# insuranceAPI
This is an insurance recommendation API. A user can register, login, logout, and post questionaire data, for which you will get a set of insurance reccomendation as response.

## API usage

The app ist currenty hosted and accessible at ```http://insurance-agent.store```. It is hosted on a Heroku dyno, so it might take some time for startup at the first request.  
**Important**: The connection is not SSL/TLS encrypted, so do not send personal information. The endpoint is just for demonstration purposes.

### Register
POST request to ```http://insurance-agent.store/register``` with JSON-payload:
```
{
	"username": <username>,
	"email": <email>,
	"password": <password>
}
```
### Get a recommendation
Post request to ```http://insurance-agent.store/recommendation``` with JSON-payload:
```
{
  "first_name": <firstname>,
  "address": <address>,
  "occupation": <{Employed, Student, Self-employed}>,
  "email_address": <email>,
  "children": <Boolean>,
  "num_children": >int> (optional)
}
```
### Login/Logout
The app also supports login (post username and passwort) at ```http://insurance-agent.store/login``` and logout at  ```http://insurance-agent.store/logout```. Registering will automatically log you in.

## Run the app locally

1. Clone repository  
```git clone https://github.com/d-e-h-i-o/insuranceAPI.git```  
```cd insuranceAPI/```
2. Create virtual environment (Python 3 is required)  
```python -m venv venv```
3. Activate virtual environment 
```source venv/bin/activate``` (on macOS)
4. Install requirements  
```pip install -r requirements.txt```
5. Set environements variables 
toto  
6. Set up database  
toto  
7. Run app  
todo  

## Run test suite
1. Set up database  
todo 
2. Run tests  
```python -m pytest tests/ --capture=tee-sys```
