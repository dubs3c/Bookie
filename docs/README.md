
## Run your own Bookie installation

Right now, Bookie uses telegram to send data to Bookie. Therefore you need your own Telegram bot which you can read more about here [https://core.telegram.org/bots#3-how-do-i-create-a-bot](https://core.telegram.org/bots#3-how-do-i-create-a-bot).

Once you have acquired your bot for bookie, you need to set a webhook to your Bookie intsallation. Your installation needs to be accessible from the Internet.

```
http POST https://api.telegram.org/bot<API_KEY>/setWebhook url=<YOUR_HOST>/api/telegram/API_KEY/
```

Bookie is designed to use docker for running in production while the vagrant and default setup is for local development.

### Default setup

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
6. `python manage.py runserver --settings=bookie.env.dev` *(Run bookie in development mode)*

### Vagrant setup

1. vagrant up && vagrant ssh
2. Set your telegram api key
```
export TELEGRAM_API_KEY=<api_key>
```
3. cd /vagrant_data
4. Run Boookie
```
python3.7 manage.py runserver --settings=bookie.env.dev 0.0.0.0:8000
```
5. Visit http://127.0.0.1:8000 on your host machine     

### Docker setup (Production)

1. Create `/root/bookie.env` with the following contents:
```
TELEGRAM_API_KEY=
DJANGO_SECRET_KEY=
ALLOWED_DOMAINS=yourdomain.com,www.yourdomain.com
SENTRY_KEY=
```
2. `sudo docker-compose -f prod.yml up -d`

This will start a docker container listening on the host at `127.0.0.1:8000`. You will need to configure nginx or apache as a reverse proxy to serve static content, below you will find an nginx configuration example.

```
upstream bookie.local {
    server 127.0.0.1:8000;
}


server {                                                                                                                
    listen   443 ssl;                                                                                                   
    server_name yourdomain.com;                                                                                       
    root /var/www/yourdomain.com;                                                                                     
    access_log /var/log/nginx/yourdomain.com.access.log main;                                                         
    error_log /var/log/nginx/yourdomain.com.error.log error;                                                          
                                                                                                                        
    location / {                                                                                                        
        proxy_set_header X-Forwarded-Proto https;                                                                       
        proxy_pass http://bookie.local;                                                                                 
        proxy_set_header Host $host;                                                                                    
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;                                                    
        proxy_buffering off;                                                                                            
        add_header Front-End-Https   on;                                                                                
        add_header Strict-Transport-Security max-age=63072000;                                                          
        add_header X-Xss-Protection "1; mode=block" always;                                                             
        add_header X-Content-Type-Options "nosniff" always;                                                             
        add_header X-Frame-Options "SAMEORIGIN" always;                                                                 
        add_header Referrer-Policy "no-referrer-when-downgrade" always;                                                 
    }                                                                                                                   
                                                                                                                        
    location /static {                                                                                                  
        alias /var/www/yourdomain.com/media;                                                                          
    }                                                                                                                   
                                                                                                                                                                                        
    ssl on;                                                                                                             
                                                                                                                        
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;                                                 
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;                                               
    ssl_dhparam /etc/letsencrypt/live/yourdomain.com/dhparam.pem;                                                            
                                                                                                                        
    # enables all versions of TLS, but not SSLv2 or 3 which are weak and now deprecated.                                 
    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;                                                                                
                                                                                                                        
    ssl_ciphers 'AES128+EECDH:AES128+EDH:!aNULL';                                                                       
    ssl_session_cache shared:SSL:10m;                                                                                   
    #ssl_stapling on;                                                                                                   
    #ssl_stapling_verify on;                                                                                            
    resolver 8.8.4.4 8.8.8.8 valid=300s;                                                                                
    resolver_timeout 10s;                                                                                               
                                                                                                                        
    ssl_prefer_server_ciphers on;                                                                                       
}                                                                                                                       

```