Edit the DB settings in `app.py` to point to a local DB (I specifically used postgreqsql for this):

```
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost:5432/classified_ads'
```


Use a python virtual environment (or not) to install the dependencies. I used `pipenv`:

`pipenv install`

Run the env:

`pipenv shell`

Source the .env variables included

`source .env`

Run the project using:

`flask run`
