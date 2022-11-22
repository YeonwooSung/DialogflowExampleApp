# Dialogflow Example App

## Set up

```bash
# activate venv
source venv/bin/activate

# install python libraries
pip install -r requirements.txt

# export global variable
export GOOGLE_APPLICATION_CREDENTIALS="PATH_TO_CREDENTIAL_JSON_FILE"
```

## Update requirements

Whenever new packages have been installed, run the follow code to update the "requirements.txt".

```bash
pip3 freeze > requirements.txt
```
