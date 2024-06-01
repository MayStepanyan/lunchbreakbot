# lunchbreakbot

A telegram bot that that collects and aggregates multiple users orders within a group chat

# Usage

Place a telegram bot token and Redis Client credentials in .env file:

```dotenv
TOKEN="YOUR_BOT_TOKEN"
HOST="DB_HOST"
PORT="DB_PORT"
#OTHER POSSIBLE ARGUMENTS LIKE PASSWORD etc
```

and run

```bash
python -m app.main
```

For example, you can run the Redis locally like:

```bash
docker run -d --name redis-stack-server -p 6379:6379 redis/redis-stack-server:latest
```

# Available commands

After adding the bot to group chat, it will start listening to every message. The following
commands will be available

- `/start` - Start collecting every message as an order
- `/orders` - Print a summary of current orders
- `/cancel` - Remove current orders and stop collecting them
- `/done` - Print a summary of current orders and remove them from memory

# Roadmap

- [X] Move to Redis db
- [ ] Enable per user order removal
- [ ] Enable per user order summarization
- [ ] Enable reminders to start ordering
- [ ] Enable reminders to pay
- [ ] Host a bot for demo/usage

## Internal TODOs

- [ ] Add basic tests
- [ ] Dockerize the project
- [ ] Move static responses to constants


