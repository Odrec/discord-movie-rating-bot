import discord
from discord.ext import commands
import re
from typing import List, Dict, Optional

# Bot configuration
intents = discord.Intents.default()
intents.message_content = True  # This requires privileged intent to be enabled
intents.reactions = True
intents.guilds = True
intents.guild_messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

class RatingBot:
    def __init__(self, bot):
        self.bot = bot
        self.numeric_emojis = {
            '0️⃣': 0, '1️⃣': 1, '2️⃣': 2, '3️⃣': 3, '4️⃣': 4,
            '5️⃣': 5, '6️⃣': 6, '7️⃣': 7, '8️⃣': 8, '9️⃣': 9, '🔟': 10
        }
    
    async def extract_numeric_reactions(self, message: discord.Message) -> List[int]:
        """Extract numeric values from reactions (0-10)"""
        ratings = []
        
        for reaction in message.reactions:
            # Check for numeric emoji reactions
            if str(reaction.emoji) in self.numeric_emojis:
                rating = self.numeric_emojis[str(reaction.emoji)]
                # Add the rating for each user who reacted (excluding the bot)
                async for user in reaction.users():
                    if not user.bot:
                        ratings.append(rating)
            
            # Check for custom numeric reactions (like :1:, :2:, etc.)
            elif hasattr(reaction.emoji, 'name'):
                match = re.match(r'^(\d+)$', reaction.emoji.name)
                if match:
                    rating = int(match.group(1))
                    if 0 <= rating <= 10:
                        async for user in reaction.users():
                            if not user.bot:
                                ratings.append(rating)
        
        return ratings
    
    def calculate_average(self, ratings: List[int]) -> Optional[float]:
        """Calculate average rating"""
        if not ratings:
            return None
        return sum(ratings) / len(ratings)

class MoviePlaylist:
    def __init__(self, rating_bot):
        self.rating_bot = rating_bot
        self.movies = {}  # Store movie data: {movie_title: {'ratings': [], 'average': float, 'count': int}}
    
    async def analyze_movie_ratings(self, channel, limit: int = 100) -> Dict[str, Dict]:
        """Analyze ratings for all movies in a channel"""
        movie_data = {}
        
        async for message in channel.history(limit=limit):
            if message.content and not message.author.bot:  # Exclude bot messages
                # Extract movie title from message content
                movie_title = self.extract_movie_title(message.content)
                if movie_title:
                    ratings = await self.rating_bot.extract_numeric_reactions(message)
                    # Include ALL movies, even those with no reactions at all
                    movie_data[movie_title] = {
                        'ratings': ratings,
                        'average': self.rating_bot.calculate_average(ratings) if ratings else None,
                        'count': len(ratings),
                        'message': message
                    }
        
        return movie_data
    
    def extract_movie_title(self, message_content: str) -> Optional[str]:
        """Extract movie title from message content"""
        title = message_content.strip()
        
        # Basic validation
        if not title:
            return None
        
        # Skip bot commands
        if title.startswith('!'):
            return None
        
        # Skip obvious bot responses (but be careful not to exclude movie titles)
        # Only skip if it contains multiple bot indicators or starts with them
        bot_response_patterns = [
            'Total Movies:', 'No Ratings:', '< 3 Ratings:', 'Excluded (', 'Included (',
            'Analysis of', 'Movie Playlist Created', 'Detailed Movie Statistics',
            'Top Rated Movies', 'Excluded Movies', 'Playlist Statistics'
        ]
        
        if any(pattern in title for pattern in bot_response_patterns):
            return None
        
        # Skip very long messages (likely descriptions, not titles)
        if len(title) > 150:
            return None
                
        return title
    
    def calculate_playlist_frequency(self, movie_data: Dict[str, Dict], default_frequency: int = 3) -> Dict[str, int]:
        """Calculate how many times each movie should appear in playlist"""
        playlist_frequencies = {}
        rated_movies = []
        
        for title, data in movie_data.items():
            count = data['count']
            average = data['average']
            
            if count < 3:
                # Less than 3 ratings: appears default_frequency times regardless of rating
                playlist_frequencies[title] = default_frequency
            else:
                # 3 or more ratings: consider average
                if average < 5.0:
                    # Below 5: remove from playlist
                    playlist_frequencies[title] = 0
                else:
                    # 5 or above: frequency based on rating
                    rated_movies.append((title, average))
        
        # Calculate proportional frequencies for rated movies
        if rated_movies:
            # Normalize ratings to determine relative frequencies
            total_rating_weight = sum(rating for _, rating in rated_movies)
            base_frequency = default_frequency  # Use configurable minimum frequency for rated movies
            
            for title, rating in rated_movies:
                # Proportional frequency: base + extra based on rating
                proportion = rating / total_rating_weight if total_rating_weight > 0 else 0
                extra_frequency = int(proportion * len(rated_movies) * 2)  # Scale factor
                playlist_frequencies[title] = max(base_frequency, base_frequency + extra_frequency)
        
        return playlist_frequencies
    
    def create_smart_playlist(self, frequencies: Dict[str, int]) -> List[str]:
        """Create a smart shuffled playlist with optimal distribution"""
        if not frequencies:
            return []
        
        # Remove movies with 0 frequency
        active_movies = {title: freq for title, freq in frequencies.items() if freq > 0}
        if not active_movies:
            return []
        
        # Create the playlist
        playlist = []
        for title, frequency in active_movies.items():
            playlist.extend([title] * frequency)
        
        # Smart shuffle: distribute repeated movies evenly
        return self.smart_shuffle(playlist)
    
    def smart_shuffle(self, playlist: List[str]) -> List[str]:
        """Shuffle playlist ensuring no consecutive duplicates and optimal distribution"""
        if len(playlist) <= 1:
            return playlist
        
        # Count occurrences of each movie
        movie_counts = {}
        for movie in playlist:
            movie_counts[movie] = movie_counts.get(movie, 0) + 1
        
        # Check if it's possible to avoid all consecutive duplicates
        max_count = max(movie_counts.values())
        if max_count > (len(playlist) + 1) // 2:
            # If one movie appears more than half the time, perfect distribution is impossible
            # Fall back to best effort
            return self.best_effort_shuffle(playlist)
        
        # Use backtracking to find a valid arrangement
        result = self.backtrack_shuffle(playlist, movie_counts)
        if result:
            return result
        
        # If backtracking fails, use best effort
        return self.best_effort_shuffle(playlist)
    
    def backtrack_shuffle(self, playlist: List[str], movie_counts: Dict[str, int]) -> Optional[List[str]]:
        """Use backtracking to find a valid arrangement with no consecutive duplicates"""
        remaining = dict(movie_counts)
        result = []
        
        def backtrack():
            if len(result) == len(playlist):
                return True
            
            # Get available movies (not same as last placed)
            last_movie = result[-1] if result else None
            available_movies = [movie for movie, count in remaining.items()
                             if count > 0 and movie != last_movie]
            
            if not available_movies:
                # No valid movies available, try to place any remaining movie
                available_movies = [movie for movie, count in remaining.items() if count > 0]
                if not available_movies:
                    return False
            
            # Sort by remaining count (descending) to prioritize movies that need placement
            available_movies.sort(key=lambda x: remaining[x], reverse=True)
            
            for movie in available_movies:
                # Place this movie
                result.append(movie)
                remaining[movie] -= 1
                
                # Recursively try to complete the arrangement
                if backtrack():
                    return True
                
                # Backtrack
                result.pop()
                remaining[movie] += 1
            
            return False
        
        if backtrack():
            return result
        return None
    
    def best_effort_shuffle(self, playlist: List[str]) -> List[str]:
        """Best effort shuffle when perfect distribution isn't possible"""
        result = []
        remaining = list(playlist)
        
        while remaining:
            last_movie = result[-1] if result else None
            
            # Try to find a different movie than the last one
            valid_movies = [movie for movie in remaining if movie != last_movie]
            
            if valid_movies:
                # Choose the movie with the highest remaining count
                next_movie = max(valid_movies, key=lambda x: remaining.count(x))
            else:
                # No choice but to repeat (shouldn't happen often)
                next_movie = remaining[0]
            
            result.append(next_movie)
            remaining.remove(next_movie)
        
        return result
    

rating_bot = RatingBot(bot)
movie_playlist = MoviePlaylist(rating_bot)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print(f'Bot is ready to analyze ratings in channels.')

@bot.command(name='analyze_ratings')
async def analyze_channel_ratings(ctx, channel_id: int = None, limit: int = 100):
    """
    Analyze ratings in a channel
    Usage: !analyze_ratings [channel_id] [limit]
    If no channel_id is provided, uses the current channel
    """
    try:
        # Use current channel if no channel_id provided
        if channel_id is None:
            channel = ctx.channel
        else:
            channel = bot.get_channel(channel_id)
            if not channel:
                await ctx.send(f"❌ Channel with ID {channel_id} not found.")
                return
        
        await ctx.send(f"🔍 Analyzing ratings in {channel.mention}...")
        
        # Collect messages and their ratings
        message_ratings = []
        total_ratings = []
        
        async for message in channel.history(limit=limit):
            if message.reactions:
                ratings = await rating_bot.extract_numeric_reactions(message)
                if ratings:
                    avg_rating = rating_bot.calculate_average(ratings)
                    message_ratings.append({
                        'message': message,
                        'ratings': ratings,
                        'average': avg_rating,
                        'count': len(ratings)
                    })
                    total_ratings.extend(ratings)
        
        if not message_ratings:
            await ctx.send("❌ No messages with numeric ratings (0-10) found in this channel.")
            return
        
        # Calculate overall statistics
        overall_average = rating_bot.calculate_average(total_ratings)
        total_messages_with_ratings = len(message_ratings)
        total_individual_ratings = len(total_ratings)
        
        # Create summary embed
        embed = discord.Embed(
            title="📊 Channel Rating Analysis",
            description=f"Analysis of {channel.mention}",
            color=0x00ff00
        )
        
        embed.add_field(
            name="📈 Overall Statistics",
            value=f"**Average Rating:** {overall_average:.2f}/10\n"
                  f"**Messages with Ratings:** {total_messages_with_ratings}\n"
                  f"**Total Individual Ratings:** {total_individual_ratings}",
            inline=False
        )
        
        # Add top rated messages
        if message_ratings:
            sorted_messages = sorted(message_ratings, key=lambda x: x['average'], reverse=True)
            top_messages = sorted_messages[:5]
            
            top_messages_text = ""
            for i, msg_data in enumerate(top_messages, 1):
                message_preview = msg_data['message'].content[:50] + "..." if len(msg_data['message'].content) > 50 else msg_data['message'].content
                if not message_preview.strip():
                    message_preview = "[Media/Embed content]"
                
                top_messages_text += f"**{i}.** {msg_data['average']:.2f}/10 ({msg_data['count']} ratings)\n"
                top_messages_text += f"└ {message_preview}\n\n"
            
            embed.add_field(
                name="🏆 Top Rated Messages",
                value=top_messages_text[:1024],  # Discord field limit
                inline=False
            )
        
        await ctx.send(embed=embed)
        
    except Exception as e:
        await ctx.send(f"❌ An error occurred: {str(e)}")

@bot.command(name='rate_message')
async def rate_specific_message(ctx, message_id: int):
    """
    Analyze ratings for a specific message
    Usage: !rate_message <message_id>
    """
    try:
        message = await ctx.channel.fetch_message(message_id)
        ratings = await rating_bot.extract_numeric_reactions(message)
        
        if not ratings:
            await ctx.send("❌ No numeric ratings (0-10) found on this message.")
            return
        
        average = rating_bot.calculate_average(ratings)
        
        embed = discord.Embed(
            title="📊 Message Rating Analysis",
            color=0x00ff00
        )
        
        message_preview = message.content[:100] + "..." if len(message.content) > 100 else message.content
        if not message_preview.strip():
            message_preview = "[Media/Embed content]"
        
        embed.add_field(
            name="📝 Message",
            value=message_preview,
            inline=False
        )
        
        embed.add_field(
            name="📈 Rating Statistics",
            value=f"**Average Rating:** {average:.2f}/10\n"
                  f"**Total Ratings:** {len(ratings)}\n"
                  f"**Individual Ratings:** {', '.join(map(str, sorted(ratings)))}",
            inline=False
        )
        
        embed.add_field(
            name="🔗 Message Link",
            value=f"[Jump to Message]({message.jump_url})",
            inline=False
        )
        
        await ctx.send(embed=embed)
        
    except discord.NotFound:
        await ctx.send("❌ Message not found.")
    except Exception as e:
        await ctx.send(f"❌ An error occurred: {str(e)}")

@bot.command(name='create_playlist')
async def create_movie_playlist(ctx, channel_id: int = None, limit: int = 100, default_frequency: int = 3):
    """
    Create a movie playlist based on ratings
    Usage: !create_playlist [channel_id] [limit] [default_frequency]
    default_frequency: How many times unrated/low-rated movies appear (default: 3)
    """
    try:
        # Validate default_frequency
        if default_frequency < 1 or default_frequency > 10:
            await ctx.send("❌ Default frequency must be between 1 and 10.")
            return
        
        # Use current channel if no channel_id provided
        if channel_id is None:
            channel = ctx.channel
        else:
            channel = bot.get_channel(channel_id)
            if not channel:
                await ctx.send(f"❌ Channel with ID {channel_id} not found.")
                return
        
        await ctx.send(f"🎬 Creating movie playlist from {channel.mention}...")
        
        # Analyze movie ratings
        movie_data = await movie_playlist.analyze_movie_ratings(channel, limit)
        
        if not movie_data:
            await ctx.send("❌ No movies found in this channel.")
            return
        
        # Calculate playlist frequencies
        frequencies = movie_playlist.calculate_playlist_frequency(movie_data, default_frequency)
        
        # Create smart playlist
        playlist = movie_playlist.create_smart_playlist(frequencies)
        
        if not playlist:
            await ctx.send("❌ No movies qualify for the playlist (all rated below 5.0).")
            return
        
        # Create summary embed
        embed = discord.Embed(
            title="🎬 Movie Playlist Created",
            description=f"Smart shuffled playlist from {channel.mention}",
            color=0x9932cc
        )
        
        # Add statistics
        total_movies = len(movie_data)
        playlist_movies = len([f for f in frequencies.values() if f > 0])
        total_playlist_length = len(playlist)
        
        embed.add_field(
            name="📊 Playlist Statistics",
            value=f"**Total Movies Found:** {total_movies}\n"
                  f"**Movies in Playlist:** {playlist_movies}\n"
                  f"**Playlist Length:** {total_playlist_length}\n"
                  f"**Default Frequency:** {default_frequency}x",
            inline=False
        )
        
        # Show movie frequencies
        freq_text = ""
        for title, freq in sorted(frequencies.items(), key=lambda x: x[1], reverse=True):
            if freq > 0:
                movie_info = movie_data[title]
                if movie_info['count'] >= 3:
                    avg_str = f" (avg: {movie_info['average']:.1f})"
                else:
                    avg_str = f" ({movie_info['count']} ratings)"
                
                freq_text += f"**{freq}x** {title[:40]}{'...' if len(title) > 40 else ''}{avg_str}\n"
        
        if freq_text:
            embed.add_field(
                name="🎭 Movie Frequencies",
                value=freq_text[:1024],  # Discord field limit
                inline=False
            )
        
        await ctx.send(embed=embed)
        
        # Send playlist as a file if it's long
        if len(playlist) > 20:
            playlist_text = "\n".join(f"{i+1}. {movie}" for i, movie in enumerate(playlist))
            
            # Create a text file with the playlist
            import io
            playlist_bytes = io.BytesIO(playlist_text.encode('utf-8'))
            file = discord.File(playlist_bytes, filename="movie_playlist.txt")
            
            await ctx.send("📋 Complete playlist:", file=file)
        else:
            # Show short playlist directly
            playlist_text = "\n".join(f"{i+1}. {movie}" for i, movie in enumerate(playlist))
            embed2 = discord.Embed(
                title="📋 Complete Playlist",
                description=f"```\n{playlist_text}\n```",
                color=0x9932cc
            )
            await ctx.send(embed=embed2)
        
    except Exception as e:
        await ctx.send(f"❌ An error occurred: {str(e)}")

@bot.command(name='movie_stats')
async def movie_statistics(ctx, channel_id: int = None, limit: int = 100):
    """
    Show detailed movie statistics
    Usage: !movie_stats [channel_id] [limit]
    """
    try:
        # Use current channel if no channel_id provided
        if channel_id is None:
            channel = ctx.channel
        else:
            channel = bot.get_channel(channel_id)
            if not channel:
                await ctx.send(f"❌ Channel with ID {channel_id} not found.")
                return
        
        await ctx.send(f"📊 Analyzing movie statistics in {channel.mention}...")
        
        # Analyze movie ratings
        movie_data = await movie_playlist.analyze_movie_ratings(channel, limit)
        
        if not movie_data:
            await ctx.send("❌ No movies found in this channel.")
            return
        
        # Categorize movies
        no_ratings = []
        insufficient_ratings = []
        excluded_movies = []
        included_movies = []
        
        for title, data in movie_data.items():
            if data['count'] == 0:
                no_ratings.append(title)
            elif data['count'] < 3:
                insufficient_ratings.append((title, data['count']))
            elif data['average'] < 5.0:
                excluded_movies.append((title, data['average'], data['count']))
            else:
                included_movies.append((title, data['average'], data['count']))
        
        # Create detailed embed
        embed = discord.Embed(
            title="📊 Detailed Movie Statistics",
            description=f"Analysis of {channel.mention}",
            color=0x00bfff
        )
        
        # Summary
        embed.add_field(
            name="📈 Summary",
            value=f"**Total Movies:** {len(movie_data)}\n"
                  f"**No Ratings:** {len(no_ratings)}\n"
                  f"**< 3 Ratings:** {len(insufficient_ratings)}\n"
                  f"**Excluded (< 5.0):** {len(excluded_movies)}\n"
                  f"**Included (≥ 5.0):** {len(included_movies)}",
            inline=False
        )
        
        # Top rated movies
        if included_movies:
            top_movies = sorted(included_movies, key=lambda x: x[1], reverse=True)[:5]
            top_text = ""
            for title, avg, count in top_movies:
                top_text += f"**{avg:.1f}/10** {title[:30]}{'...' if len(title) > 30 else ''} ({count} ratings)\n"
            
            embed.add_field(
                name="🏆 Top Rated Movies (≥ 5.0)",
                value=top_text,
                inline=False
            )
        
        # Excluded movies
        if excluded_movies:
            excluded_text = ""
            for title, avg, count in excluded_movies[:5]:
                excluded_text += f"**{avg:.1f}/10** {title[:30]}{'...' if len(title) > 30 else ''} ({count} ratings)\n"
            
            embed.add_field(
                name="❌ Excluded Movies (< 5.0)",
                value=excluded_text,
                inline=False
            )
        
        await ctx.send(embed=embed)
        
    except Exception as e:
        await ctx.send(f"❌ An error occurred: {str(e)}")

@bot.command(name='help_ratings')
async def help_ratings(ctx):
    """Show help for rating commands"""
    embed = discord.Embed(
        title="🤖 Discord Movie Rating Bot Help",
        description="This bot analyzes numeric reactions (0-10) on messages and creates movie playlists",
        color=0x0099ff
    )
    
    embed.add_field(
        name="📊 Rating Commands",
        value="**!analyze_ratings [channel_id] [limit]**\n"
              "└ Analyze ratings in a channel\n\n"
              "**!rate_message <message_id>**\n"
              "└ Analyze ratings for a specific message\n\n"
              "**!help_ratings**\n"
              "└ Show this help message",
        inline=False
    )
    
    embed.add_field(
        name="🎬 Movie Playlist Commands",
        value="**!create_playlist [channel_id] [limit] [default_frequency]**\n"
              "└ Create smart shuffled movie playlist\n"
              "└ default_frequency: How many times unrated movies appear (default: 3)\n\n"
              "**!movie_stats [channel_id] [limit]**\n"
              "└ Show detailed movie statistics",
        inline=False
    )
    
    embed.add_field(
        name="🔢 Supported Rating Reactions",
        value="**Emoji Numbers:** 0️⃣ 1️⃣ 2️⃣ 3️⃣ 4️⃣ 5️⃣ 6️⃣ 7️⃣ 8️⃣ 9️⃣ 🔟\n"
              "**Custom Emojis:** Any custom emoji named with numbers 0-10",
        inline=False
    )
    
    embed.add_field(
        name="🎭 Playlist Rules",
        value="• **No ratings or < 3 ratings:** Movie appears default_frequency times\n"
              "• **≥ 3 ratings, avg < 5.0:** Movie excluded\n"
              "• **≥ 3 ratings, avg ≥ 5.0:** Frequency based on rating\n"
              "• **Smart shuffling:** No consecutive duplicates, optimal distribution\n"
              "• **Customizable:** Set default_frequency (1-10, default: 3)",
        inline=False
    )
    
    await ctx.send(embed=embed)

# Error handling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ Command not found. Use `!help_ratings` for available commands.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ Missing required argument: {error.param}")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("❌ Invalid argument provided.")
    else:
        await ctx.send(f"❌ An error occurred: {str(error)}")

if __name__ == "__main__":
    # Load environment variables
    import os
    from dotenv import load_dotenv
    
    # Load .env file
    load_dotenv()
    
    token = os.getenv('DISCORD_BOT_TOKEN')
    if not token:
        print("❌ Please set the DISCORD_BOT_TOKEN environment variable")
        print("You can get a token from https://discord.com/developers/applications")
        print("Make sure to create a .env file with your token or set the environment variable")
    else:
        print("🤖 Starting Discord Rating Bot...")
        bot.run(token)