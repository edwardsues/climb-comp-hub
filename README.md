# climb-comp-hub

A website for climbers and gym owners to better manage and keep track of their competitions.

## Local Development:

Start a virtual environment, and then: (if on windows, do python -m before the command, i.e. python -m pip install flask)

```
cd backend
pip install -r requirements.txt
```

if databases are not created, do the following and seed with dummy values:

```
cd backend
python -m table_scripts.create_tables
python -m table_scripts.seed
```

testing backend:

```
cd backend
python main.py
```

testing frontend:

```
cd frontend
npm run dev
```

navigate to `http:localhost:5173`.
