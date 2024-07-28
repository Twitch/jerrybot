# JerryBot Beta (RobertBot?)

## Table of Contents

- [Prerequisites](#prerequisites)
- [Environment Variables](#environment-variables)
- [Configuring the Bot in Discord](#configuring-the-bot-in-discord)
- [Obtaining Server/Guild and Channel IDs](#obtaining-serverguild-and-channel-ids)
- [Running the Script Manually](#running-the-script-manually)
- [Gettin' Dockery with it](#dockerize-it-guv)
- [Scheduling Options](#do-it-again)


## Prerequisites

Before you begin, ensure you have the following installed on your system:

- Python 3.7+ 
- Python's discord library
- Python's schedule library
   ```sh
   pip install discord.py schedule
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
2. Click "Copy ID". This is your `SERVER_ID`.

## Running the Script Manually

To run the script manually, follow these steps:

### Environment Variables

The script requires the following environment variables to be set:

    - `JERRYBOT_TOKEN`: Your bot token.
    - `GUILD_ID`: The ID of the (server) where the bot will operate.
    - `CHANNEL_NAME`: The name of the channel that the bot will tidy.

1. Clone the repository:

    ```sh
    git clone https://github.com/Twitch/jerrybot
    cd jerrybot
    ```
2. You can set these environment variables in your shell session using the `export` command:

    ```sh
    export JERRYBOT_TOKEN="your-bot-token"
    export SERVER_ID=your-server-id
    export CHANNEL_NAME="your-channel-name"
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
    -e SERVER_ID=your-server-id \
    -e CHANNEL_NAME="name-of-your-channel" \
    jerry-bot
    ```

4. To run your personal JerryBot again next time:
    ```sh
    docker start jerry-bot
    ```

## Do It Again
This branch relies on Python's `schedule` libary to execute the tidy at the time specified in the `SCHEDULE_TIME` variable at the top of jerrybot.py, and Docker's restart functionality to fire the script back up once it's run once.

It isn't the most elegant solution, but it's our solution (for now) and it works. For now. 

1. If you're mucked about with other branches of this, go do your tidying:
    ```sh
    docker stop jerry-bot
    docker rm jerry-bot
    ```
2. Set your scheduled run time with the `SCHEDULE_TIME` variable in `jerrybot.py`, which uses a 24hr format

3. Build your sweet new image:
    ```sh
    docker build -t jerry-bot .
    ```

4. Kick it off and make sure Docker restarts our JerryBot after it's done erasing all of your mistakes:
    ```sh
    docker run -d \
    --restart unless-stopped \
    --name jerry-bot \
    -e JERRYBOT_TOKEN="your-bot-token" \
    -e SERVER_ID=your-server-id \
    -e CHANNEL_NAME="name-of-your-channel" \
    jerry-bot
    ```