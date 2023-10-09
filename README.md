# SQLAlchemy Promise

Created on 2023-10-07 5:27am

## Description

This is a simple project to demonstrate how to use SQLAlchemy with promises
in order to asynchronously query the database.

Where a lot of the time seems to be taken up:

1. Actual insertion
2. Serializing SQL results into Python objects

Conclusion: threads help with a naive improvement of 37.8377419%.

## Installation

pip install and docker compose build a PostgreSQL database.

```bash
pip install -r requirements.txt
docker compose up --build
```

In a separate terminal, run:

```bash
psql -h localhost -p 5432 -U postgres -d postgres
```

The password is `postgres`

Then, in the psql terminal, run:

```sql
CREATE DATABASE test;
```

Then quit with `quit` or `\q`.

Finally, in the main terminal, run:

```bash
python main.py
```

### Results

```
0.0008928775787353516
0.00019025802612304688
0.00019097328186035156
Async query class: 10.702302932739258
8.075119733810425
3.282888889312744
3.3937840461730957
Default query class: 14.75181269645691
```

The top three times are the asynchronous query times, ensuring
that we're deploying SQLAlchemy into a thread. The second
three times without labels are the default query times.

Async query class allows for the queries to be run in a thread.

## License

This project is licensed under the terms of the MIT license.
The license can be found in the root directory of this project in the file [LICENSE](LICENSE).
