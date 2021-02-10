1. Create a Slack bot and add it to #general channel
2. On the local machine run ./ngrok http 8000
3. On Event Subscriptions page activate Enable Events and add a URL with the ngrok domain, e.g. 
`http://60f142130650.ngrok.io/event/hook/`
4. Subscribe to bot events -> add `message.channels`
5. Oauth & Permissions -> add the next scopes
`files:read`, `im:read`, `im:history`, `channels:history`
6. Do git clone
7. Edit `docker-compose.yml` VERIFICATION_TOKEN, BOT_USER_ACCESS_TOKEN, AWS_ACCESS_KEY_ID , AWS_SECRET_ACCESS_KEY variables.
8. in the project directory run `docker-compose run -d`
9. Go to http://localhost:8000/admin/ credentials alex/alex, add a few patterns and send a message/file to #general
10. Check if it was caught on http://localhost:8000/admin/web/entry/
11. (Optionally) See `docker logs --follow app-django`
`docker logs --follow app-dlp`


