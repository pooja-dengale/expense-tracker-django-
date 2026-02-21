# Complete Render Production Deployment Guide

## 🚀 Quick Start (5 Steps)

### 1. Generate SECRET_KEY
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
**Save this output** - you'll need it in Step 4.

### 2. Create PostgreSQL Database on Render
- Go to https://dashboard.render.com/
- Click **"New +"** → **"PostgreSQL"**
- Name: `expense-tracker-db`
- Region: Choose closest to you
- Click **"Create Database"**
- **Copy the "Internal Database URL"** (starts with `postgresql://`)

### 3. Create Web Service on Render
- Click **"New +"** → **"Web Service"**
- Connect your GitHub repository
- Configure:
  - **Name:** `expense-tracker` (or your choice)
  - **Region:** Same as database (important!)
  - **Branch:** `main`
  - **Build Command:** `./build.sh`
  - **Start Command:** `gunicorn expense_tracker.wsgi:application`

### 4. Set Environment Variables
Click **"Advanced"** → **"Add Environment Variable"**

Add these 4 variables:

| Key | Value |
|-----|-------|
| `SECRET_KEY` | Paste from Step 1 |
| `DEBUG` | `False` |
| `DATABASE_URL` | Paste from Step 2 |
| `ALLOWED_HOSTS` | `<your-app-name>.onrender.com` |

Replace `<your-app-name>` with your actual Render app name.

### 5. Deploy!
- Click **"Create Web Service"**
- Wait 5-10 minutes for build
- Your app will be live at: `https://<your-app-name>.onrender.com`

---

## 📋 Post-Deployment Setup

### Create Admin Account
1. Go to your web service in Render Dashboard
2. Click **"Shell"** tab
3. Run:
```bash
python manage.py createsuperuser
```
4. Enter username, email, and password

### Test Your Application
Visit these URLs:
- Homepage: `https://<your-app-name>.onrender.com`
- Register: `https://<your-app-name>.onrender.com/accounts/register/`
- Login: `https://<your-app-name>.onrender.com/accounts/login/`
- Admin: `https://<your-app-name>.onrender.com/admin/`

---

## 🔧 Troubleshooting 500 Errors

### Check Logs First
```
Render Dashboard → Your Service → Logs
```

### Common Causes & Fixes

#### 1. Missing Environment Variables
**Error in logs:** `KeyError: 'SECRET_KEY'` or similar

**Fix:**
- Verify all 4 environment variables are set
- Check for typos in variable names
- Ensure no extra spaces in values

#### 2. Wrong DATABASE_URL
**Error in logs:** `could not connect to server`

**Fix:**
- Use **Internal Database URL** (not External)
- Copy from: Database → "Internal Database URL"
- Format: `postgresql://user:password@host:5432/database`

#### 3. ALLOWED_HOSTS Mismatch
**Error in logs:** `Invalid HTTP_HOST header`

**Fix:**
- Set ALLOWED_HOSTS to your exact Render domain
- Example: `myapp.onrender.com` (no https://)
- No trailing slash

#### 4. Static Files Missing
**Symptoms:** Page loads but no styling

**Fix:**
- Check build logs for "Collecting static files"
- Verify build.sh ran successfully
- Manually trigger redeploy

#### 5. Database Not Migrated
**Error in logs:** `no such table` or `relation does not exist`

**Fix:**
- Check build logs for "Running database migrations"
- Manually run in Shell:
```bash
python manage.py migrate
```

---

## 🔍 Debugging Steps

### Step 1: Check Environment Variables
```
Render Dashboard → Your Service → Environment
```
Verify all 4 variables are set correctly.

### Step 2: Check Build Logs
```
Render Dashboard → Your Service → Logs → Filter: "Build"
```
Look for errors during:
- Installing dependencies
- Collecting static files
- Running migrations

### Step 3: Check Runtime Logs
```
Render Dashboard → Your Service → Logs → Filter: "Deploy"
```
Look for Python errors or Django exceptions.

### Step 4: Test Database Connection
In Shell tab:
```bash
python manage.py dbshell
```
Should connect without errors.

### Step 5: Check Django Configuration
In Shell tab:
```bash
python manage.py check --deploy
```
Should show no critical errors.

---

## 📊 What Gets Deployed

### Files Used by Render:
- `build.sh` - Build commands
- `Procfile` - Start command
- `requirements.txt` - Python packages
- `runtime.txt` - Python version
- `expense_tracker/settings.py` - Django configuration

### Build Process:
1. Install Python 3.11.9
2. Install dependencies from requirements.txt
3. Collect static files
4. Run database migrations
5. Start gunicorn server

---

## 🎯 Environment Variables Explained

### SECRET_KEY
- **Purpose:** Django security (encryption, sessions, CSRF)
- **Format:** Random 50+ character string
- **Generate:** `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
- **Example:** `django-insecure-abc123xyz...`

### DEBUG
- **Purpose:** Controls error display
- **Value:** `False` (always in production)
- **Impact:** Shows generic error pages instead of detailed tracebacks

### DATABASE_URL
- **Purpose:** PostgreSQL connection string
- **Format:** `postgresql://user:password@host:5432/database`
- **Source:** Render PostgreSQL "Internal Database URL"
- **Important:** Use Internal, not External URL

### ALLOWED_HOSTS
- **Purpose:** Security - prevents host header attacks
- **Format:** Comma-separated domains
- **Example:** `myapp.onrender.com` or `myapp.onrender.com,www.myapp.com`
- **Important:** Must match your actual domain exactly

---

## 🔒 Security Checklist

✅ SECRET_KEY is random and unique (50+ characters)
✅ DEBUG=False in production
✅ ALLOWED_HOSTS set to your domain only
✅ DATABASE_URL uses internal connection
✅ HTTPS enabled (automatic on Render)
✅ Security headers configured (HSTS, SSL redirect)
✅ CSRF protection enabled
✅ Session cookies secure
✅ Password validation enabled

---

## 💡 Tips & Best Practices

### Free Tier Behavior
- App spins down after 15 minutes of inactivity
- First request after spin-down takes 30-60 seconds
- This is normal for free tier

### Updating Your App
1. Make changes locally
2. Test locally: `python manage.py runserver`
3. Commit: `git add . && git commit -m "Update"`
4. Push: `git push origin main`
5. Render auto-deploys from GitHub

### Manual Redeploy
```
Render Dashboard → Your Service → Manual Deploy → Deploy latest commit
```

### Viewing Logs in Real-Time
```
Render Dashboard → Your Service → Logs → Enable "Live tail"
```

### Database Backups
Free tier: No automatic backups
Upgrade to paid plan for automatic daily backups

---

## 📞 Getting Help

### Check These First:
1. **Logs** - Render Dashboard → Logs
2. **PRODUCTION_CHECKLIST.md** - Detailed checklist
3. **TROUBLESHOOTING.md** - Common issues
4. **Render Docs** - https://render.com/docs

### Still Stuck?
- Check environment variables are correct
- Verify database and web service in same region
- Test locally with DEBUG=True
- Review build logs for specific errors

---

## ✅ Success Indicators

Your deployment is successful when:
- ✅ Build completes without errors
- ✅ Service shows "Live" status
- ✅ Homepage loads at your Render URL
- ✅ Can register new account
- ✅ Can login successfully
- ✅ Dashboard displays without 500 error
- ✅ Can add expenses/income
- ✅ Admin panel accessible

---

## 🎉 You're Done!

Your expense tracker is now live on Render!

**Next Steps:**
1. Create your admin account
2. Test all features
3. Share your app URL
4. Monitor logs for any issues
5. Consider upgrading for better performance

**Your App:** `https://<your-app-name>.onrender.com`

---

**Need more help?** Check PRODUCTION_CHECKLIST.md for detailed troubleshooting.
