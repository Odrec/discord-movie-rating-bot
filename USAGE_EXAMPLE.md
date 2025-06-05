# Discord Movie Rating Bot - Usage Example 🎬

This guide shows you how to use the Discord Movie Rating Bot to create smart playlists for your movie streaming sessions.

## Setup Your Movie Channel 📺

1. **Create a dedicated channel** for movie ratings (e.g., #movie-ratings)
2. **Post movie titles** as individual messages:
   ```
   The Matrix
   Inception
   Avatar
   Pulp Fiction
   The Godfather
   ```

## Rate Movies 🌟

Users react to movie messages with number emojis (0️⃣-🔟):

```
The Matrix
Reactions: 8️⃣ 9️⃣ 🔟 8️⃣ 7️⃣

Inception  
Reactions: 9️⃣ 🔟 9️⃣ 8️⃣

Avatar
Reactions: 4️⃣ 3️⃣ 5️⃣ 4️⃣

Pulp Fiction
Reactions: 🔟 9️⃣ 🔟

The Godfather
Reactions: 7️⃣ (only 1 rating)
```

## Generate Playlist 🎭

Use the bot command to create your playlist:

```
!create_playlist
```

## Example Output 📊

```
🎬 Movie Playlist Created
Smart shuffled playlist from #movie-ratings

📊 Playlist Statistics
Total Movies Found: 5
Movies in Playlist: 4  
Playlist Length: 13

🎭 Movie Frequencies
5x Inception (avg: 9.0)
4x The Matrix (avg: 8.4)  
3x Pulp Fiction (2 ratings)
3x The Godfather (1 ratings)

❌ Avatar excluded (avg: 4.0)

📋 Complete Playlist
1. Inception
2. The Matrix
3. Inception
4. Pulp Fiction
5. The Godfather
6. The Matrix
7. Inception
8. Pulp Fiction
9. The Matrix
10. Inception
11. The Godfather
12. The Matrix
13. Inception
```

## Playlist Rules Explained 📋

### Frequency Rules:
- **No ratings or < 3 ratings**: Movie appears **3 times**
- **≥ 3 ratings, avg < 5.0**: Movie **excluded**
- **≥ 3 ratings, avg ≥ 5.0**: Frequency **proportional to rating**

### In This Example:
- **Inception** (avg: 9.0, 4 ratings) → 5 times (highest rated)
- **The Matrix** (avg: 8.4, 5 ratings) → 4 times (high rated)
- **Pulp Fiction** (2 ratings) → 3 times (insufficient ratings)
- **The Godfather** (1 rating) → 3 times (insufficient ratings)
- **Avatar** (avg: 4.0, 4 ratings) → 0 times (below 5.0 threshold)

## Smart Shuffling 🔀

The bot uses advanced shuffling algorithms to:
- **Prevent consecutive duplicates**: No movie ever appears twice in a row
- **Distribute repeated movies evenly** throughout the playlist
- **Maximize variety** while maintaining proportional representation
- **Use backtracking algorithm** for optimal placement

Notice how in the example playlist:
- ✅ No consecutive duplicates (Inception never follows Inception)
- ✅ Even distribution with good spacing between repeats
- ✅ High-rated movies appear more frequently but spread out
- ✅ Perfect variety for continuous streaming

## Additional Commands 🛠️

### Get Detailed Statistics:
```
!movie_stats
```

Shows categorized breakdown of all movies:
- Movies with no ratings
- Movies with insufficient ratings (< 3)
- Excluded movies (avg < 5.0)
- Included movies (avg ≥ 5.0)

### Analyze Specific Channel:
```
!create_playlist 123456789012345678
!movie_stats 123456789012345678
```

### Limit Message Scan:
```
!create_playlist 123456789012345678 50
```
Only analyzes the last 50 messages.

## Best Practices 💡

1. **Use clear movie titles** as message content
2. **Encourage multiple ratings** (need ≥3 for filtering)
3. **Rate honestly** (movies below 5.0 get excluded)
4. **Update playlists regularly** as new ratings come in
5. **Use dedicated channels** for better organization

## Streaming Integration 🎥

The generated playlist is perfect for:
- **Movie night planning**
- **Streaming queue management** 
- **Fair rotation** based on group preferences
- **Automatic exclusion** of poorly rated content

Export the playlist and use it with your streaming setup for optimal movie night experiences! 🍿