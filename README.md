# Bookie!

**Bookie** is a simple Django app that stores links to information you intend to consume later. For example, if you found yourself bookmarking information from social media and websites, but your bookmarks are stored all over the place *and* you also forget to check what you have saved, then Bookie is for you!

*Right now, you can only save links through Telegram.*

## Motivation

I save a lot of links, tweets and articles that I intend to read later, but I always forget to actually check my what I have saved. On twitter I use the *like* or *bookmark* functionality to save interesting tweets for later. Sometimes I save them to my *Saved messages* on Telegram or use the Google Inbox bookmark functionality. Needless to say, I need a single source which stores all my links and notifies me after some period of time to remind me what I recently saved. And so Bookie was born.


## Vision

My vision for Bookie includes:
- Mobile app
- Browser extension to save links directly from the browser
- More integrated services
- To be the number one source for all your saved links

## Run your own Bookie installation

Right now, Bookie uses telegram to send data to Bookie. Therefore you need your own Telegram bot which you can read more about here [https://core.telegram.org/bots#3-how-do-i-create-a-bot](https://core.telegram.org/bots#3-how-do-i-create-a-bot).

1. Clone the repo
2. `pip install pipenv --user`
3. `pipenv shell`
4. `pipenv install`
5. Set your telegram api key
```
# Windows
set TELEGRAM_API_KEY=<api_key>

# Unix
export TELEGRAM_API_KEY=<api_key>
```
6. `python manage.py runserver --settings=bookie.env.dev` *(Run bookie in development mode)*¨

You also need to configure your bot to set a webhook to Bookie:

```
http POST https://api.telegram.org/bot<API_KEY>/setWebhook url=<YOUR_HOST>/api/telegram/API_KEY/
```

## Contributing
Any feedback or ideas are welcome! Want to improve something? Create a pull request!

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D
