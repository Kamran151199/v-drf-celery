# Demo application of Pearson correlation computation.

## Used:
    * Django Rest Framework
    * Celery
    * Postgresql
    * Flower
    * JWT auth
    * Swagger
    * Docker 

## Need production ready ??? (There are features to be implemented)
    * Request nginx implementation
    * Request helm charts
    * Request HA mode of all service

## How to run ?
    * Fill up .env file using keys from env-example file.
    * docker-compose up

## Want to have a glance to Docs ?
    * For Documentation go to /redoc/
    * For Swagger go to /swagger/   (please make sure that after
        you get your token, you insert it to Authenticate input 
        field as shown: "Bearer {access_token}")

## Tests
    Only user-service tests have been implemented. For additional coverage, please contact (raise issue)

## Demo usage
    0. Go to /swagger/
    1. Register - POST /users/
    2. Sign In - POST /token/   (copy the access_token)
    3. Set headers - Press Authorize button in the UI and put the access_token with the preceading 'Bearer ' keyword  
    4. Provide data for computation - POST /pearson-correlation/compute/    (make sure you provide a valid user_id - you can put your's)
    5. Filter/List/Search the computed correlations - GET /pearson-correlation/

### !!! IMPORTANT !!!
    If you do not have a client side ready yet, please make sure you disable email verification (.env  EMAIL_VERIFICATION_REQUIRED)

### For any additional info contact me <a>valijonov_kamron@mail.ru</a>