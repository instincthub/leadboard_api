# leadboard_api


This project uses celery and redis 

to work on it, I created the celery as a systemd which enables me start as a service on the background 

The start celery on the server currently or check status we use

Check status 
`sudo systemctl status leadboard_api_celery`

Start celery

`sudo systemctl start leadboard_api_celery`

Stop celery

`sudo systemctl stop leadboard_api_celery`

