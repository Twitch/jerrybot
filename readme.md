# v 0.0.0.0.1 JerryBot Alpha

## Table of Contents

- [Prerequisites](#prerequisites)
- [Environment Variables](#environment-variables)
- [Configuring the Bot in Discord](#configuring-the-bot-in-discord)
- [Obtaining Server/Guild and Channel IDs](#obtaining-serverguild-and-channel-ids)
- [Running the Script Manually](#running-the-script-manually)


## Prerequisites

Before you begin, ensure you have the following installed on your system:

- Python 3.7+ 
- Python's discord library
   ```sh
   pip install discord.py
   ```

## Environment Variables

The script requires the following environment variables to be set:

- `JERRYBOT_TOKEN`: Your bot token.
- `GUILD_ID`: The ID of the (server) where the bot will operate.
- `CHANNEL_NAME`: The name of the channel that the bot will tidy.

### Setting Environment Variables

You can set these environment variables in your shell session using the `export` command:

```sh
export JERRYBOT_TOKEN="your-bot-token"
export GUILD_ID="your-server-id"
export CHANNEL_NAME="your-channel-name"
```

## Configuring the Bot in Discord

To set up your bot in Discord, follow these steps:

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications).
2. Click on "New Application" and give your bot a name.
3. In the left sidebar, click on "Bot" and then "Add Bot" on the right.
4. Customize your bot's username and avatar as desired.
5. Under the "Token" section, click "Copy" to get your bot token. This is your `JERRYBOT_TOKEN`.
6. In the left sidebar, click on "OAuth2" > "URL Generator".
7. In the "Scopes" section, select "bot".
8. In the "Bot Permissions" section, select the permissions your bot needs. (Manage Channels, View Channels, and Send Messages if you want the bot to send a note after it has performed the cleanup)
9. Copy the generated URL at the bottom of the page.
10. Open this URL in a new browser tab and select the server where you want to add the bot.

## Obtaining Server/Guild and Channel IDs

To get the server (guild) ID and channel ID:

1. Open Discord and go to User Settings > Advanced.
2. Enable "Developer Mode".

### Getting the Server/Guild ID:

1. Right-click on the server name in the server list.
2. Click "Copy ID". This is your `GUILD_ID`.

## Running the Script Manually

To run the script manually, follow these steps:

1. Clone the repository:

    ```sh
    git clone https://github.com/Twitch/jerrybot
    cd jerrybot
    ```

2. Ensure the environment variables are set.

3. Run the script:

    ```sh
    python jerrybot.py
    ```


