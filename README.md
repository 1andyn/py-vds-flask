# py-vds-flask
Python Flask based backend for vue-days-since

###### What this is:
This is a sample flask webservice used for my [*vue-days-since*](https://github.com/1andyn/vue-days-since) single page web app.
The webapp uses *Auth0* for authentication and identify users since the app stores event data on a MongoDB on Atlas by user.
To ensure only authenticated users can access the database, this backend webservice checks for authorization.

###### Setup:
 * Setting up Single Page Web App on Auth0
    * Modify SPA to use authentication token when making API requests
 * Setting up API on Auth0
    * Configuring permissions on API
 * Installing Auth0 Authorization extension
    * Configuring Auth0 Authorization extension
        * Adding Roles
        * Adding Permissions
        * Other misc. authorization config
 * Setting up rules (Auth0 Dashboard)
    * Used for authentication pipeline (i.e what to put in the access token)
 * Host SPA (Single Page Application)
 * Host backend service (this)
 
 An indepth guide on Auth0 can be found [here](https://auth0.com/docs/architecture-scenarios/spa-api).

###### authfile sample (used to store sensitive info):
```
c_pa = "connect_password_mongo"
c_sr = "connection_user_mongo"
c_co = "mongo_endpoint"
a_dm = "authorization_domain"
a_ap = "api_end_here"
```
 
###### Requirements:
```
flask
python-dotenv
python-jose[cryptography]
flask-cors
six
pipmongo
dnspython
ssl
```

I had to manually use pip to install in contrast to Auth0's doc:
```
pip install python-jose[cryptography]
```
Using other jwt imports resulted in inability to parse token
