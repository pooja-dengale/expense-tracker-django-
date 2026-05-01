# Production Deployment Checklist for Render

## Pre-Deployment Checklist

### 1. Environment Variables (CRITICAL)
Set these in Render Dashboard → Your Service → Environment:

```bash
# Required Variables
SECRET_KEY=<generate-50-char-random-string>
DEBUG=False
DATABASE_URL=<internal-postgresql-url-from-render>
ALLOWED_HOSTS=<your-app-name>.onrender.com

# Optional
PYTHON_VERSION=3.11.9
```

### 2. Generate SECRET_KEY
Run locally:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
Copy the output and paste it as SECRET_KEY in Render.

### 3. Database Setup
1. Create PostgreSQL database on Render first
2. Copy the **Internal Database URL** (not External)
3. Paste it as DATABASE_URL environment variable
4. Ensure database and web service are in the same region

### 4. Verify Files

✅ Check these files exist:
- `build.sh` - Build script
- `Procfile` - Start command
- `requirements.txt` - Dependencies
- `runtime.txt` - Python version
- `templates/500.html` - Error page
- `templates/404.html` - Not found page

✅ Verify requirements.txt contains:
```
Django==4.2.7
python-dateutil==2.8.2
whitenoise==6.6.0
gunicorn==21.2.0
dj-database-url==2.1.0
psycopg2-binary==2.9.9
```

## Deployment Steps

### Step 1: Create PostgreSQL Database
1. Go to Render Dashboard
2. Click "New +" → "PostgreSQL"
3. Configure:
   - Name: `expense-tracker-db`
   - Database: `expense_tracker`
   - Region: Choose closest to you
   - Plan: Free
4. Click "Create Database"
5. **Copy Internal Database URL** (starts with `postgresql://`)

### Step 2: Create Web Service
1. Click "New +" → "Web Service"
2. Connect GitHub repository
3. Configure:
   - Name: `expense-tracker` (or your choice)
   - Region: **Same as database**
   - Branch: `main`
   - Runtime: `Python 3`
   - Build Command: `./build.sh`
   - Start Command: `gunicorn expense_tracker.wsgi:application`
   - Plan: Free

### Step 3: Set Environment Variables
In web service settings, add:

| Variable | Value | Example |
|----------|-------|---------|
| SECRET_KEY | Random 50+ chars | `django-insecure-abc123...` |
| DEBUG | False | `False` |
| DATABASE_URL | From Step 1 | `postgresql://user:pass@host/db` |
| ALLOWED_HOSTS | Your domain | `myapp.onrender.com` |

### Step 4: Deploy
1. Click "Create Web Service"
2. Wait for build to complete (5-10 minutes)
3. Check logs for errors

### Step 5: Create Superuser
After successful deployment:
1. Go to web service → "Shell" tab
2. Run:
```bash
python manage.py createsuperuser
```
3. Follow prompts

### Step 6: Test Application
1. Visit: `https://<your-app-name>.onrender.com`
2. Test registration
3. Test login
4. Test dashboard
5. Test adding expense
6. Access admin: `https://<your-app-name>.onrender.com/admin`

## Common Issues & Solutions

### Issue 1: 500 Error After Login
**Symptoms:** Login works but redirects to 500 error

**Causes:**
- Missing environment variables
- DATABASE_URL not set
- SECRET_KEY not set
- ALLOWED_HOSTS incorrect

**Solution:**
1. Check Render logs: Dashboard → Logs
2. Verify all environment variables are set
3. Ensure DATABASE_URL uses Internal URL
4. Check ALLOWED_HOSTS matches your domain

### Issue 2: Static Files Not Loading
**Symptoms:** Page loads but no CSS/styling

**Causes:**
- collectstatic didn't run
- WhiteNoise not configured

**Solution:**
1. Check build logs for "Collecting static files"
2. Verify WhiteNoise in MIDDLEWARE (settings.py)
3. Manually run: `python manage.py collectstatic --no-input`

### Issue 3: Database Connection Error
**Symptoms:** "could not connect to server"

**Causes:**
- Wrong DATABASE_URL
- Database and web service in different regions
- Using External URL instead of Internal

**Solution:**
1. Use **Internal Database URL** from Render
2. Ensure same region for database and web service
3. Check database is running (Render Dashboard)

### Issue 4: Build Fails
**Symptoms:** Build fails during deployment

**Causes:**
- Missing dependencies
- Python version mismatch
- Syntax errors

**Solution:**
1. Check build logs for specific error
2. Verify requirements.txt is complete
3. Test locally: `pip install -r requirements.txt`
4. Check runtime.txt matches your Python version

### Issue 5: CSRF Verification Failed
**Symptoms:** "CSRF verification failed" on forms

**Causes:**
- ALLOWED_HOSTS not set correctly
- CSRF_COOKIE_SECURE issues

**Solution:**
1. Add your domain to ALLOWED_HOSTS
2. Ensure DEBUG=False in production
3. Check SECURE_PROXY_SSL_HEADER is set

## Monitoring & Maintenance

### Check Logs
```
Render Dashboard → Your Service → Logs
```

### View Metrics
```
Render Dashboard → Your Service → Metrics
```

### Manual Redeploy
```
Render Dashboard → Your Service → Manual Deploy → Deploy latest commit
```

### Database Backup
Free tier: No automatic backups
Paid tier: Automatic daily backups

Manual backup from Shell:
```bash
pg_dump $DATABASE_URL > backup.sql
```

## Performance Tips

### Free Tier Limitations
- App spins down after 15 minutes inactivity
- First request takes 30-60 seconds (cold start)
- 750 hours/month free compute

### Upgrade Benefits ($7/month)
- No spin-down
- Better performance
- More resources
- Database backups

## Security Checklist

✅ SECRET_KEY is random and secret (50+ characters)
✅ DEBUG=False in production
✅ ALLOWED_HOSTS set to your domain only
✅ DATABASE_URL uses internal connection
✅ SSL/HTTPS enabled (automatic on Render)
✅ Security headers configured (HSTS, etc.)
✅ CSRF protection enabled
✅ Session cookies secure

## Troubleshooting Commands

### Check Django Configuration
```bash
python manage.py check --deploy
```

### Test Database Connection
```bash
python manage.py dbshell
```

### View Migrations
```bash
python manage.py showmigrations
```

### Create Test Data
```bash
python manage.py shell
>>> from django.contrib.auth.models import User
>>> User.objects.create_user('testuser', 'test@example.com', 'testpass123')
```

## Support Resources

- Render Docs: https://render.com/docs
- Django Docs: https://docs.djangoproject.com/
- Project Issues: Check GitHub repository

## Post-Deployment

After successful deployment:

1. ✅ Test all features
2. ✅ Create superuser account
3. ✅ Add test data
4. ✅ Monitor logs for errors
5. ✅ Set up monitoring/alerts (optional)
6. ✅ Document your deployment
7. ✅ Share app URL with users

## Quick Reference

**Your App URL:** `https://<your-app-name>.onrender.com`
**Admin Panel:** `https://<your-app-name>.onrender.com/admin`
**Logs:** Render Dashboard → Logs
**Shell:** Render Dashboard → Shell
**Redeploy:** Push to GitHub (auto-deploys)

---

Need help? Check TROUBLESHOOTING.md or Render documentation.
