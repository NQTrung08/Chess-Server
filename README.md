# Chess-Server

```CMD
$ python3 -m venv venv
$ . venv/bin/activate
```
Install dependencies

```CMD
$ pip install -r requirements.txt
$ (venv) pip install torch torchvision nltk
$ (venv) pip install underthesea (nếu file requirements.txt không cài được)
```

Install nltk package


```CMD
$ (venv) python
>>> import nltk
>>> nltk.download('punkt')
```

Modify `intents.json` with different intents and responses for your Chatbot
Run

```CMD
$ (venv) python app/train.py
```

This will dump  `data.pth` file. And then run the following command to test it in the console.

```CMD
$ (venv) python run.py
```
