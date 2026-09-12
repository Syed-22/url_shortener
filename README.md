# URL Shortener

You paste in a long link, and get back a short one. Built with Flask and SQLite.

The first version made the short code straight from the row number, so links looked like `/1`, `/2`, `/3`. That is a real problem: anyone could guess every link ever made just by trying numbers one by one. Fixed by using a random 6-character code instead. Before saving a new code, it is checked against the database, so two links never end up with the same code.

`/stats/<code>` shows how many times a link has been opened.

## Running it

```
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000`. The database file (`urls.db`) is made on its own the first time you run it.
