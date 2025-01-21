# ha-autopi

Run the app

```sh
poetry run uvicorn main:app --reload
```

# TO-DO

- Add actual example model from https://docs.autopi.io/getting_started/api/send-device-data-to-own-server/
- add UUID primary key to each event: one model for table, one for post without unique id
- rework so that instead a post request saves to a database and also calls mqtt server. Alternatively drop the database altogether (but how to do retries and stuff then?)

sqlite should be fine