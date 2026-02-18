# climb-comp-hub

A website for climbers and gym owners to better manage and keep track of their competitions.

## Setup:

Start a virtual environment, and then: (if on windows, do python -m before the command, i.e. python -m pip install flask)

```
cd backend
pip install -r requirements.txt
```

if databases are not created, do the following:

```
cd backend
python -m table_scripts.create_tables
```

create a .env file and do: `SQLALCHEMY_DATABASE_URI='postgresql://postgres:{password}@localhost:5432/climbing_comp'`, where password is the password stored in 1password.

also do `JWT_SECRET_KEY=my-dev-secret-key-change-in-prod`: will change this later, but just for testing purposes I will leave this as it is.

testing backend:

```
cd backend
python main.py
```

testing frontend:

```
cd backend
npm run dev
```

navigate to `http:localhost:5173`.
