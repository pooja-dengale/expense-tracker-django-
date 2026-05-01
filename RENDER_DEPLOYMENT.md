# Render Deployment Guide

## Prerequisites
- GitHub account with your code pushed
- Render account (free tier available)

## Step 1: Create PostgreSQL Database on Render

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New +" → "PostgreSQL"
3. Configure:
   - Name: `expense-tracker-db`
   - Database: `expense_tracker`
   - User: (auto-generated)
   - Region: Choose closest to you
   - Plan: Free
4. Click "Create Database"
5. Copy the "Internal Database URL" (starts with `postgresql://`)

## Step 2: Create Web Service on Render

1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Configure:
   - Name: `expense-tracker`
   - Region: Same as database
   - Branch: `main` (or your default branch)
   - Runtime: `Python 3`
   - Build Command: `./build.sh`
   - Start Command: `gunicorn expense_tracker.wsgi:application`
   - Plan: Free

## Step 3: Set Environment Variables

In your web service settings, add these environment variables:

```
SECRET_KEY=<generate-random-50-char-string>
DEBUG=False
DATABASE_URL=<paste-internal-database-url-from-step-1>
ALLOWED_HOSTS=<your-app-name>.onrender.com
PYTHON_VERSION=3.11.9
```

### Generate SECRET_KEY:
Run locally:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## Step 4: Deploy

1. Click "Create Web Service"
2. Render will automatically:
   - Install dependencies
   - Run migrations
   - Collect static files
   - Start the application

## Step 5: Create Superuser (Admin Account)

After deployment succeeds:

1. Go to your web service → "Shell" tab
2. Run:
```bash
python manage.py createsuperuser
```
3. Follow prompts to create admin account

## Step 6: Access Your Application

- App URL: `https://<your-app-name>.onrender.com`
- Admin: `https://<your-app-name>.onrender.com/admin`

## Important Notes

### Free Tier Limitations
- App spins down after 15 minutes of inactivity
- First request after spin-down takes 30-60 seconds
- Database limited to 90 days (then deleted)

### Troubleshooting

**Build fails:**
- Check build logs in Render dashboard
- Verify `build.sh` has execute permissions
- Ensure all dependencies in `requirements.txt`

**Database connection errors:**
- Verify DATABASE_URL is correct
- Check database is in same region
- Use "Internal Database URL" not "External"

**Static files not loading:**
- Verify `collectstatic` ran in build logs
- Check STATIC_ROOT and STATICFILES_STORAGE settings

**500 errors:**
- Check logs in Render dashboard
- Verify SECRET_KEY is set
- Ensure DEBUG=False in production

### Updating Your App

Push changes to GitHub:
```bash
git add .
git commit -m "Update application"
git push origin main
```

Render will automatically redeploy.

### Manual Redeploy

In Render dashboard:
1. Go to your web service
2. Click "Manual Deploy" → "Deploy latest commit"

## Environment Variables Reference

| Variable | Required | Example | Description |
|----------|----------|---------|-------------|
| SECRET_KEY | Yes | `django-insecure-abc123...` | Django secret key (50+ chars) |
| DEBUG | Yes | `False` | Must be False in production |
| DATABASE_URL | Yes | `postgresql://user:pass@host/db` | PostgreSQL connection string |
| ALLOWED_HOSTS | Yes | `myapp.onrender.com` | Your Render domain |
| PYTHON_VERSION | No | `3.11.9` | Python version (matches runtime.txt) |

## Security Checklist

- ✅ SECRET_KEY is random and secret
- ✅ DEBUG=False in production
- ✅ ALLOWED_HOSTS set to your domain
- ✅ DATABASE_URL uses internal URL
- ✅ SSL/HTTPS enabled (automatic on Render)
- ✅ Security headers configured
- ✅ Static files served via WhiteNoise

## Monitoring

- View logs: Render Dashboard → Your Service → Logs
- Check metrics: Dashboard → Metrics tab
- Set up alerts: Dashboard → Settings → Notifications

## Backup Database

```bash
# From Render Shell
pg_dump $DATABASE_URL > backup.sql
```

Or use Render's automatic backups (paid plans).

## Cost Optimization

Free tier is sufficient for personal use. For production:
- Upgrade to paid plan ($7/month) for:
  - No spin-down
  - More resources
  - Better performance
  - Database backups

## Support

- Render Docs: https://render.com/docs
- Django Docs: https://docs.djangoproject.com/
- Check logs first for debugging
