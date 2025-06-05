#!/usr/bin/env python3
"""
Test script to verify consecutive duplicate fix
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from bot import MoviePlaylist, RatingBot

class MockBot:
    pass

def test_consecutive_duplicates():
    """Test with the exact scenario that caused consecutive duplicates"""
    
    # Create instances
    mock_bot = MockBot()
    rating_bot = RatingBot(mock_bot)
    movie_playlist = MoviePlaylist(rating_bot)
    
    # Movies from your test case
    movies = [
        "Vertigo", "May", "Aliens", "Predator", "Ringu", 
        "Jeepers Creepers", "Us", "Halloween", "Friday the 13th", 
        "The Shining", "+1", "Them"
    ]
    
    # Create a test scenario with multiple frequencies
    test_frequencies = {}
    for i, movie in enumerate(movies):
        # Vary frequencies to create the scenario where duplicates might occur
        if i < 4:
            test_frequencies[movie] = 3  # Some movies appear 3 times
        elif i < 8:
            test_frequencies[movie] = 2  # Some appear 2 times
        else:
            test_frequencies[movie] = 1  # Some appear once
    
    print("🎬 Testing Consecutive Duplicate Fix")
    print("=" * 50)
    print(f"Movies: {movies}")
    print(f"Frequencies: {test_frequencies}")
    
    # Run multiple tests to catch any randomness issues
    for test_num in range(5):
        print(f"\n🔄 Test Run #{test_num + 1}:")
        
        playlist = movie_playlist.create_smart_playlist(test_frequencies)
        
        print(f"Generated playlist (length: {len(playlist)}):")
        for i, movie in enumerate(playlist, 1):
            print(f"{i:2d}. {movie}")
        
        # Check for consecutive duplicates
        consecutive_found = []
        for i in range(len(playlist) - 1):
            if playlist[i] == playlist[i + 1]:
                consecutive_found.append((i + 1, i + 2, playlist[i]))
        
        if consecutive_found:
            print(f"❌ CONSECUTIVE DUPLICATES FOUND:")
            for pos1, pos2, movie in consecutive_found:
                print(f"   Positions {pos1}-{pos2}: {movie}")
        else:
            print("✅ No consecutive duplicates found!")
        
        print("-" * 30)

if __name__ == "__main__":
    test_consecutive_duplicates()