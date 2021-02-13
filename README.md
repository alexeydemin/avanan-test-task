1. Create a Slack bot and add it to #general channel
2. On the local machine run `./ngrok http 8000`
3. On Event Subscriptions page activate Enable Events and add a URL with the ngrok domain, e.g. 
`http://60f142130650.ngrok.io/event/hook/`
4. Subscribe to bot events -> add `message.channels`
5. Oauth & Permissions -> add the next scopes
`files:read`, `im:read`, `im:history`, `channels:history`
6. Do git clone
7. Do `cp .env.example .env` and edit VERIFICATION_TOKEN, BOT_USER_ACCESS_TOKEN, AWS_ACCESS_KEY_ID , AWS_SECRET_ACCESS_KEY values.
8. in the project directory run `docker-compose --env-file .env up -d`
9. Run migrations `docker-compose exec app-django python manage.py migrate`
10. `docker-compose exec app-django python manage.py createsuperuser` Create admin user
11. Go to http://localhost:8000/admin/ credentials alex/alex, add a few patterns and send a message/file to #general
12. Check if it was caught on http://localhost:8000/admin/web/entry/
13. (Optionally) See `docker logs --follow app-django`
`docker logs --follow app-dlp`


