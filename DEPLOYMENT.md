# Discord Movie Rating Bot - Deployment Guide 🚀

This guide will help you deploy your Discord Movie Rating Bot to Railway for 24/7 operation.

## 🎯 Recommended: Railway Deployment

Railway is the easiest option for Discord bots with a generous free tier.

### Step 1: Prepare Your Code

✅ **Already Done!** Your project includes:
- `Procfile` - Tells Railway how to run your bot
- `runtime.txt` - Specifies Python version
- `requirements.txt` - Lists dependencies
- `.gitignore` - Excludes sensitive files

### Step 2: Create Railway Account

1. Go to [railway.app](https://railway.app)
2. Click "Login" → "Login with GitHub"
3. Authorize Railway to access your GitHub

### Step 3: Upload Your Code to GitHub

**Option A: Create New Repository**
1. Go to [github.com](https://github.com)
2. Click "New repository"
3. Name it `discord-movie-bot`
4. Make it **Private** (recommended)
5. Don't initialize with README

**Option B: Use GitHub Desktop or Git Commands**
```bash
# In your project folder
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/discord-movie-bot.git
git push -u origin main
```

### Step 4: Deploy to Railway

1. **Go to Railway Dashboard**
   - Visit [railway.app/dashboard](https://railway.app/dashboard)

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your `discord-movie-bot` repository

3. **Configure Environment Variables**
   - In Railway dashboard, go to your project
   - Click "Variables" tab
   - Add: `DISCORD_BOT_TOKEN` = `your_actual_bot_token`
   - **Important**: Don't include quotes around the token

4. **Deploy**
   - Railway will automatically detect it's a Python app
   - It will install dependencies and start your bot
   - Check "Deployments" tab for progress

### Step 5: Verify Deployment

1. **Check Logs**
   - In Railway dashboard → "Deployments" → Click latest deployment
   - Look for: "ratings-bot#9490 has connected to Discord!"

2. **Test Your Bot**
   - Go to your Discord server
   - Try: `!help_ratings`
   - Your bot should respond!

## 🎉 Success!

Your bot is now running 24/7 on Railway's servers!

## 📊 Railway Free Tier Limits

- **$5 credit per month** (usually enough for Discord bots)
- **500 hours of runtime** (more than enough for 24/7)
- **1GB RAM, 1 vCPU**
- **Automatic sleep after 30 days of inactivity**

## 🔧 Alternative Options

### Option 2: Render
1. Go to [render.com](https://render.com)
2. Connect GitHub repository
3. Choose "Web Service"
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `python bot.py`
6. Add environment variable: `DISCORD_BOT_TOKEN`

### Option 3: PythonAnywhere
1. Go to [pythonanywhere.com](https://pythonanywhere.com)
2. Create free account
3. Upload files via "Files" tab
4. Create "Always On Task" (paid feature)
5. Or use "Tasks" for scheduled runs

## 🛠️ Troubleshooting

### Bot Not Starting
- Check Railway logs for errors
- Verify `DISCORD_BOT_TOKEN` is set correctly
- Ensure bot has proper Discord permissions

### Bot Goes Offline
- Railway free tier may sleep after inactivity
- Check your monthly usage in Railway dashboard
- Consider upgrading if you exceed free limits

### Environment Variables
- Never commit `.env` file to GitHub
- Always set `DISCORD_BOT_TOKEN` in Railway dashboard
- Use the exact token from Discord Developer Portal

## 🔄 Updating Your Bot

1. **Make changes locally**
2. **Test changes**: `python bot.py`
3. **Commit to GitHub**:
   ```bash
   git add .
   git commit -m "Update bot features"
   git push
   ```
4. **Railway auto-deploys** from GitHub

## 🎬 Your Bot Features (Deployed)

Once deployed, your bot will run 24/7 with:
- ✅ Smart movie playlist generation
- ✅ No consecutive duplicates
- ✅ Customizable frequency (1-10x)
- ✅ Rating-based filtering
- ✅ Automatic exclusion of poor movies

## 📞 Support

If you encounter issues:
1. Check Railway deployment logs
2. Verify Discord bot permissions
3. Test locally first: `python bot.py`
4. Check Discord Developer Portal for bot status

---

**Happy streaming with your 24/7 movie rating bot! 🍿🎬**