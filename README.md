# lunchbreakbot

A telegram bot that that collects and aggregates multiple users orders within a group chat

# Usage

Place a token in .env file:

```dotenv
TOKEN="YOUR_BOT_TOKEN"
```

and run

```bash
python -m app.main
```

# Available commands

After adding the bot to group chat, it will start listening to every message. The following
commands will be available

- `/start` - Start collecting every message as an order
- `/orders` - Print a summary of current orders
- `/cancel` - Remove current orders and stop collecting them
- `/done` - Print a summary of current orders and remove them from memory

# Roadmap

- [ ] Move to Redis db
- [ ] Enable per user order removal
- [ ] Enable per user order summarization
- [ ] Enable reminders to start ordering
- [ ] Enable reminders to pay
- [ ] Host a bot for demo/usage

## Internal TODOs

- [ ] Add basic tests
- [ ] Dockerize the project
- [ ] Move static responses to constants


