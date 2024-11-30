# Throne and Liberty Dice Roller Discord Bot

This Discord bot is designed to facilitate fair item rolls within your **Throne and Liberty** guild using slash commands. Perfect for managing loot distribution in an organized and transparent way.

## Features

- **Ping Command**: Check the bot's latency using `/ping`.
- **Start Item Roll**: Use `/go_dice` to initiate a roll session for an item, specifying eligible roles.
- **Roll Command**: Players use `/dice` to roll for the active item, ensuring only eligible members participate.
- **End Roll Session**: Conclude the rolling session with `/end_dice` to announce the winner and reset for the next roll.
- **Role-Based Access**: Commands like `/go_dice` and `/end_dice` are restricted to specific roles like `STAFF` and `GM` for added security.

## Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/RautuA/Throne-and-Liberty-Dice-Roller-Discord-Bot
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Add your bot token to `apikeys.py`:
   ```python
   BOTTOKEN = "your-discord-bot-token"
   ```
4. Run the bot:
   ```bash
   python bot.py
   ```

## Permissions

Make sure the bot has the following permissions:
- **Read Messages**
- **Send Messages**
- **Manage Messages**
- **Use Slash Commands**
- **Manage Roles** (if applicable)

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
