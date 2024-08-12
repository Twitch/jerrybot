# JerryBot Beta (RobertBot?)

## Table of Contents

- [Prerequisites](#prerequisites)
- [Environment Variables](#environment-variables)
- [Configuring the Bot in Discord](#configuring-the-bot-in-discord)
- [Obtaining Server/Guild and Channel IDs](#obtaining-serverguild-and-channel-ids)
- [Running the Script Manually](#running-the-script-manually)
- [Gettin' Dockery with it](#dockerize-it-guv)
- [Scheduling Options](#do-it-again-man)


## Prerequisites

Before you begin, ensure you have the following installed on your system:

- Python 3.7+ 
- Python's discord library
   ```sh
   pip install discord.py
   ```

## New Channel Name Functionality

The JerryBot now includes a channel name rotation feature that enhances its functionality. This feature allows the bot to dynamically change the name of the channel it manages based on a list of names specified in a file.

### How It Works:

1. **Name Rotation**: The bot reads from a file named `new-names`, which contains new channel name drop-ins. Each name should be on a separate line. The bot retrieves the top name from this list and removes it after use, ensuring that names are not reused until the list is replenished.

2. **Default Name**: If the `new-names` file is empty or not found, the bot will fall back to a default name specified by the `JERRYBOT_DEFAULT_NAME` environment variable. This ensures that the bot always has a valid channel name to use.

3. **Channel Name Format**: The bot constructs the new channel name by prefixing it with "venting-" and suffixing it with "-stay-professional". 

4. **State Management**: The current channel name is tracked in a file named `curr-name`, which allows the bot to remember the last used name for future operations. Used channel names are logged in a file named `used-names` for reference.

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
2. Click "Copy ID". This is your `SERVER_ID`.

## Running the Script Manually

To run the script manually, follow these steps:

### Environment Variables

The script requires the following environment variables:

- `JERRYBOT_TOKEN`: Your Discord bot token.
- `JERRYBOT_SERVER_ID`: The ID of the server where the bot will operate.
- `JERRYBOT_DEFAULT_NAME`: Default channel name to use if no new names are available.

JerryBot will look for, and use, the following optional settings, as well:

- `JERRYBOT_NAMES_PATH`: Path to the directory containing name files (default is current working directory).
- `JERRYBOT_DEBUG`: Set to 'true' for verbose logging (default is 'False').

1. Clone the repository:

    ```sh
    git clone https://github.com/Twitch/jerrybot
    cd jerrybot
    ```
2. You can set these environment variables in your shell session using the `export` command:

    ```
    export JERRYBOT_TOKEN="your-bot-token"
    export JERRYBOT_SERVER_ID=your-server-id
    export JERRYBOT_NAMES_PATH="/path/to/names/directory" # Optional
    export JERRYBOT_DEBUG=true  # Optional
    export JERRYBOT_DEFAULT_NAME="default-channel-name"
    ```
3. Run the script:

    ```sh
    python jerrybot.py
    ```

## Dockerize It Guv

If you want to run this in a tidy tidying container, because that's hot

1. Clone this repo:
    ```sh
    git clone https://github.com/Twitch/jerrybot
    cd jerrybot
    ```

2. Build that beautiful ~bean footage~ Jerry image:
    ```sh
    docker build -t jerry-bot .
    ```

3. Run that new container for its first time, friend!
    (There are absolutely fancier and more secure ways to store and pass in your tokens. Look them up. Use an LLM. It's the future and all.)
    ```sh
    docker run -d --name jerry-bot \
    -e JERRYBOT_TOKEN="your-bot-token" \
    -e JERRYBOT_SERVER_ID=your-server-id \
    -e JERRYBOT_DEFAULT_NAME="default-channel-name" \
    -e JERRYBOT_NAMES_PATH="/path/in/container" \ # Optional
    -e JERRYBOT_DEBUG=true \ # Optional
    -v /path/on/host:/path/in/container \ # Optional
    jerry-bot
    ```

4. To run your personal JerryBot again next time:
    ```sh
    docker start jerry-bot
    ```

## Do It Again Man
You can schedule JerryBot to run again in a myriad of ways. Figger' it out.

- The jerrybot.py script (available on its own in the [standalone branch](https://github.com/Twitch/jerrybot/tree/standalone)) can be scheduled via cron
- Do some cool Compose stuff 
- Let the container run forever and let python do the scheduling magic
- Do some quick adjustments to run the standalone python in an AWS Lambda and be all cloud forward, mate