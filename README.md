# Discord Movie Rating Bot 🎬🤖

A Discord bot that analyzes numeric reactions (0-10) on movie messages and creates smart shuffled playlists for streaming.

## Features ✨

- **Movie Rating Analysis**: Analyze numeric reactions on movie messages
- **Smart Playlist Generation**: Create optimally shuffled playlists based on ratings
- **No Consecutive Duplicates**: Advanced algorithm ensures no movie appears twice in a row
- **Intelligent Frequency Control**: Movies appear based on rating quality and quantity
- **Rating-Based Filtering**: Automatically exclude poorly rated movies (< 5.0 average)
- **Optimized Distribution**: Smart shuffling spreads repeated movies evenly apart
- **Multiple Rating Formats**: Supports both emoji numbers (0️⃣-🔟) and custom numeric emojis
- **Detailed Statistics**: Comprehensive movie statistics and playlist insights

## Quick Start 🚀

### 1. Clone and Setup

```bash
git clone https://github.com/Odrec/discord-movie-rating-bot.git
cd discord-ratings-bot
python setup.py
```

### 2. Create a Discord Bot

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Go to the "Bot" section
4. Click "Add Bot"
5. Copy the bot token

### 3. Enable Privileged Intents

1. In Discord Developer Portal, go to your application
2. Click on the "Bot" section in the left sidebar
3. Scroll down to "Privileged Gateway Intents"
4. Enable "Message Content Intent" (required for reading message content)
5. Save changes

### 4. Configure the Bot

1. Open the `.env` file
2. Add your bot token:
   ```
   DISCORD_BOT_TOKEN=your_actual_bot_token_here
   ```

### 5. Invite Bot to Server

1. In Discord Developer Portal, go to "OAuth2" > "URL Generator"
2. Select scopes: `bot`
3. Select permissions:
   - `Read Messages/View Channels`
   - `Send Messages`
   - `Read Message History`
   - `Add Reactions`
   - `Use External Emojis`
4. Copy the generated URL and open it to invite the bot

### 6. Run the Bot

```bash
python bot.py
```

## Commands 📝

### Movie Playlist Commands 🎬

### `!create_playlist [channel_id] [limit] [default_frequency]`
Create a smart shuffled movie playlist based on ratings

**Examples:**
```
!create_playlist                    # Create playlist from current channel (default: 3x)
!create_playlist 123456789012345678 # Create playlist from specific channel
!create_playlist 123456789012345678 50  # Analyze 50 messages
!create_playlist 123456789012345678 100 5  # Use 5x default frequency
```

### `!movie_stats [channel_id] [limit]`
Show detailed movie statistics and categorization

**Example:**
```
!movie_stats                        # Show stats for current channel
```

### Rating Analysis Commands 📊

### `!analyze_ratings [channel_id] [limit]`
Analyze ratings in a channel (default: current channel, 100 messages)

### `!rate_message <message_id>`
Analyze ratings for a specific message

### `!help_ratings`
Show help information and available commands

## Supported Rating Reactions 🔢

The bot recognizes these reaction types as numeric ratings:

### Emoji Numbers
- 0️⃣ 1️⃣ 2️⃣ 3️⃣ 4️⃣ 5️⃣ 6️⃣ 7️⃣ 8️⃣ 9️⃣ 🔟

### Custom Emojis
- Any custom emoji with names like `:0:`, `:1:`, `:2:`, etc. (0-10)

## How Movie Playlists Work 🔧

### Rating Rules:
1. **No ratings or < 3 ratings**: Movie appears **default_frequency times** (customizable, default: 3)
2. **≥ 3 ratings with average < 5.0**: Movie is **excluded** from playlist
3. **≥ 3 ratings with average 5.0-5.9**: Movie appears **default_frequency times**
4. **≥ 3 ratings with average 6.0-7.9**: Movie appears **default_frequency + 1 times**
5. **≥ 3 ratings with average 8.0-10.0**: Movie appears **default_frequency + 2 times**

### Smart Round-Based Shuffling:
- **All movies play before any repeats**: Every movie appears once before any movie appears twice
- **Round-based system**: Movies are organized into rounds where each round contains every movie once
- **No consecutive duplicates**: Advanced algorithm prevents the same movie playing back-to-back
- **Maximum variety**: Ensures optimal viewing experience with perfect distribution

## Example Usage 💡

### 1. Setup Movie Channel
```
User posts: "The Matrix"
User posts: "Inception"
User posts: "Avatar"
```

### 2. Rate Movies
```
The Matrix: 8️⃣ 9️⃣ 🔟 8️⃣ 7️⃣ (avg: 8.4, 5 ratings → default + 2)
Inception: 9️⃣ 🔟 9️⃣ (avg: 9.3, 3 ratings → default + 2)
Good Movie: 7️⃣ 6️⃣ 7️⃣ 6️⃣ (avg: 6.5, 4 ratings → default + 1)
Average Movie: 5️⃣ 5️⃣ 6️⃣ (avg: 5.3, 3 ratings → default)
Avatar: 4️⃣ 3️⃣ 5️⃣ 4️⃣ (avg: 4.0, 4 ratings → excluded!)
```

### 3. Generate Playlist
```
!create_playlist          # Default: 3x frequency
!create_playlist 0 100 5  # Custom: 5x frequency for unrated movies
```

### 4. Result
```
🎬 Movie Playlist Created
Playlist Length: 12 (with 3x default) or 18 (with 5x default)
Default Frequency: 3x (or 5x if customized)

- The Matrix appears 5x/7x times (8.0-10.0 tier: default + 2)
- Inception appears 5x/7x times (8.0-10.0 tier: default + 2)
- Good Movie appears 4x/6x times (6.0-7.9 tier: default + 1)
- Average Movie appears 3x/5x times (5.0-5.9 tier: default)
- Avatar excluded (below 5.0 average)
Smart shuffled with no consecutive duplicates
```

## Installation (Manual) 🛠️

If you prefer manual installation:

```bash
# Install dependencies
pip install discord.py python-dotenv

# Create environment file
cp .env.example .env

# Edit .env with your bot token
nano .env

# Run the bot
python bot.py
```

## Troubleshooting 🔧

### Common Issues

**Bot doesn't respond to commands:**
- Check if bot has proper permissions in the channel
- Verify the bot token is correct
- Ensure the bot is online

**No ratings found:**
- Make sure messages have numeric emoji reactions (0️⃣-🔟)
- Check that reactions are from real users (not bots)
- Verify the channel has messages with reactions

**Permission errors:**
- Bot needs `Read Message History` permission
- Bot needs `Send Messages` permission
- Bot needs `View Channel` permission

### Getting Message IDs

To get a message ID for `!rate_message`:
1. Enable Developer Mode in Discord (User Settings > Advanced > Developer Mode)
2. Right-click on a message
3. Select "Copy ID"

## Development 👨‍💻

### Project Structure
```
discord-ratings-bot/
├── bot.py              # Main bot code
├── requirements.txt    # Python dependencies
├── setup.py           # Setup script
├── .env.example       # Environment template
├── .env               # Your environment variables (created)
└── README.md          # This file
```

### Key Components

- **RatingBot Class**: Core functionality for rating analysis
- **Command Handlers**: Discord command implementations
- **Error Handling**: Comprehensive error management
- **Embed Formatting**: Rich message formatting

## Contributing 🤝

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License 📄

This project is open source. Feel free to use and modify as needed.

## Support 💬

If you encounter issues:
1. Check the troubleshooting section
2. Verify your bot setup
3. Check Discord permissions
4. Review the console output for errors

---

**Happy rating! 🌟**