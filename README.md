### Building and running application

start your application by running:
`docker-compose up --build`

* application will be available at http://localhost:8080

#### Note
* Docker compose will also run postgres DB on port 5432
* Application will startup with total 5 inital users and other necessary tables. No need to run any scripts for it.
* Data is only added in User table, all other tables would be empty.

### Testing Application

* Please import the postman collection present at `test_resources\Splitwise REST.postman_collection.json`
* It contains the request for all the endpoints of application, with necessary details.

### Choice of Database

* I have choosed the SQL DB for the application (PostgresDB)
* As this application has very defined schema in which we want to store the data. The chances of modifications is less.
* We require JOINS in fulfilling some requirements, which will be costly in No SQL DB, or it will require a data duplication.

### Database Schema

* Database schema is defined in `src\models\schema_models.py`.

### Additional Note
* In the api for adding the expense, I have assumed that if we want to devide expense based on percentage, than that calculaiton will be done on client side.
* At the api side, we will get the input in form of money only.
* API parameters are not validated as of now. Due to that, in case of invalid access request for resource will result in Internal Server error.

