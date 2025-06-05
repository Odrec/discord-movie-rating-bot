#!/usr/bin/env python3
"""
Discord Rating Bot Setup Script
"""

import os
import sys
import subprocess

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install requirements")
        return False

def setup_env_file():
    """Setup environment file"""
    if not os.path.exists('.env'):
        print("📝 Creating .env file...")
        with open('.env', 'w') as f:
            f.write("# Discord Bot Token\n")
            f.write("# Get this from https://discord.com/developers/applications\n")
            f.write("DISCORD_BOT_TOKEN=\n")
        print("✅ .env file created! Please add your bot token.")
    else:
        print("ℹ️  .env file already exists")

def main():
    print("🤖 Discord Rating Bot Setup")
    print("=" * 30)
    
    # Install requirements
    if not install_requirements():
        return
    
    # Setup environment file
    setup_env_file()
    
    print("\n🎉 Setup complete!")
    print("\nNext steps:")
    print("1. Get a bot token from https://discord.com/developers/applications")
    print("2. Add your token to the .env file")
    print("3. Run the bot with: python bot.py")
    print("\nFor help with bot setup, see README.md")

if __name__ == "__main__":
    main()