# Chatbot

Basic chatbot behaviour.

## Requirements

You need a valid OpenAI API key for this to work. Set it up in your profile (bash or zshrc for instance).
```bash
export OPENAI_API_KEY="<The key gos here>"
```

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the required packages.

```bash
pip install -r requirements.txt
```

## Usage

### Setup
```python
chmod +x app.py
```

```python
./app.py
```

The chatbot with ChatGPT.

Read chatlogs
```sql
SELECT * FROM chatlog WHERE user = 'username' ORDER BY timestamp DESC LIMIT 5;
```

### Control
Use any IRC client to connect.



### Documentation
To access Swagger (OpenAPI) docs fire up your favorite browser and point it to 
http://127.0.0.1:5050/openapi/swagger



## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.



## License

[MIT](https://choosealicense.com/licenses/mit/)
