## Set up:

1. ```terminal
    virtualenv venv
    venv/Scripts/activate
    pip install -r requirements.txt
    copy .env.example .env
    ```
2. Add actual DHL api key to the new `.env` file
3. Run `main.py`

## Tests:
You need to run this in the main directory cause there are 2 static json
files and else the pathing kind of gets all over the place
```
python -m pytest tests/
```

