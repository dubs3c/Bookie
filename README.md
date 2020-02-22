# Bookie!

[![Build Status](https://travis-ci.com/mjdubell/Bookie.svg?branch=master)](https://travis-ci.com/mjdubell/Bookie)

**Bookie** is a simple Django app that stores links to information you intend to consume later. For example, if you found yourself bookmarking information from social media and websites, but your bookmarks are stored all over the place *and* you also forget to check what you have saved, then Bookie is for you!

*Right now, you can only save links through Telegram.*

![bookie](docs/screenshots/bookie1.png)
![bookie](docs/screenshots/bookie2.png)
![bookie](docs/screenshots/bookie3.png)

## Motivation

I save a lot of links, tweets and articles that I intend to read later, but I always forget to actually check my what I have saved. On twitter I use the *like* or *bookmark* functionality to save interesting tweets for later. Sometimes I save them to my *Saved messages* on Telegram or use the Google Inbox bookmark functionality. Needless to say, I need a single source which stores all my links and notifies me after some period of time to remind me what I recently saved. And so Bookie was born.


## Vision

My vision for Bookie includes:
- Mobile app
- Browser extension to save links directly from the browser
- More integrated services
- To be the number one source for all your saved links

## Local Development

If you want to add features to Bookie, you have a few options to run it locally:
1. Docker
2. Docker in Vagrant
3. Vagrant
4. Native

I personally use option 2 because I am using Windows and I have Virtualbox installed which doesn't play nice with docker :/

When running locally, the telegram integration wont work out of the box, you will need to register your own bot and use something like https://ngrok.com/. But this isn't necessary unless you are specifically developing features using telegram. Therefore Bookie will just set the telegram token to `123` unless otherwise specified.

Use the guideline below to start developing locally with vagrant and docker. If you don't want to use vagrant, simply skip the vagrant part and run `docker-compose`.
```
$ vagrant up
$ vagrant ssh
vagrant@ubuntu-xenial:~$ cd /vagrant_data
vagrant@ubuntu-xenial:/vagrant_data$ sudo docker-compose -f dev.yml up -d  
```

Now your local Bookie instance should be available on `http://localhost:8000` on your host machine.

### Running tests locally

Tests should be run using Django, like below:

```
python manage.py test --settings=bookie.env.test
```

## Contributing
Any feedback or ideas are welcome! Want to improve something? Create a pull request!

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Configure pre commit checks: `pre-commit install`
4. Commit your changes: `git commit -am 'Add some feature'`
5. Push to the branch: `git push origin my-new-feature`
6. Submit a pull request :D
