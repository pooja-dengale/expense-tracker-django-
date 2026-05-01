# Troubleshooting Guide

## Common Issues and Solutions

### 500 Server Error After Login/Registration

**Cause:** Missing context variables in dashboard template

**Solution:** ✅ Fixed! The DashboardView now provides all required variables:
- `recent_expenses` - Last 5 expenses
- `recent_incomes` - Last 5 incomes  
- `categories_count` - Total categories
- `chart_data` - Data for category pie chart
- `monthly_data` - Data for monthly trend chart

### Testing Locally

1. **Run migrations:**
```bash
python manage.py migrate
```

2. **Create test user:**
```bash
python test_views.py
```

3. **Start development server:**
```bash
python manage.py runserver
```

4. **Login with test credentials:**
- Username: `testuser`
- Password: `testpass123`

### Database Issues

**SQLite locked error:**
```bash
# Close all connections and restart server
python manage.py migrate --run-syncdb
```

**Missing migrations:**
```bash
python manage.py makemigrations
python manage.py migrate
```

### Static Files Not Loading

**Development:**
```bash
# Django serves static files automatically in DEBUG=True
```

**Production:**
```bash
python manage.py collectstatic --no-input
```

### Template Not Found Errors

**Check template structure:**
```
templates/
├── base.html
├── accounts/
│   ├── login.html
│   └── register.html
└── expenses/
    ├── dashboard.html
    ├── expense_list.html
    └── ... (other templates)
```

**Verify settings.py:**
```python
TEMPLATES = [
    {
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
    }
]
```

### Import Errors

**Missing dependencies:**
```bash
pip install -r requirements.txt
```

**Virtual environment not activated:**
```bash
# Windows
.\venv\Scripts\Activate.ps1

# Mac/Linux
source venv/bin/activate
```

### Render Deployment Issues

**Build fails:**
- Check `build.sh` has correct commands
- Verify all dependencies in `requirements.txt`
- Check Python version matches `runtime.txt`

**Database connection fails:**
- Use Internal Database URL (not External)
- Verify DATABASE_URL environment variable
- Check database and web service in same region

**Static files 404:**
- Verify `collectstatic` ran in build logs
- Check WhiteNoise middleware is enabled
- Ensure STATIC_ROOT is set correctly

**500 errors in production:**
```bash
# Check Render logs
# Verify environment variables:
# - SECRET_KEY (50+ random characters)
# - DEBUG=False
# - DATABASE_URL (from Render PostgreSQL)
# - ALLOWED_HOSTS (your-app.onrender.com)
```

### Chart.js Not Loading

**Check CDN:**
```html
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.js"></script>
```

**Verify data format:**
```javascript
// chart_data should be valid JSON
const chartData = JSON.parse('{{ chart_data|escapejs }}');
```

### CSRF Token Errors

**Form missing token:**
```html
<form method="post">
    {% csrf_token %}
    <!-- form fields -->
</form>
```

**AJAX requests:**
```javascript
// Include CSRF token in headers
headers: {
    'X-CSRFToken': getCookie('csrftoken')
}
```

### Permission Denied Errors

**User can't access other user's data:**
✅ This is correct! All views filter by `user=request.user`

**Admin can't access admin panel:**
```bash
# Create superuser
python manage.py createsuperuser
```

### Performance Issues

**Slow queries:**
- Views use `select_related('category')` for optimization
- Database indexes on frequently queried fields
- Consider adding caching for dashboard

**Large database:**
- Add pagination (already implemented: 10 items/page)
- Archive old transactions
- Consider PostgreSQL for production

## Getting Help

1. **Check logs:**
   - Development: Terminal output
   - Render: Dashboard → Logs tab

2. **Verify configuration:**
   ```bash
   python manage.py check
   python manage.py check --deploy
   ```

3. **Test specific component:**
   ```bash
   python test_views.py
   ```

4. **Django shell debugging:**
   ```bash
   python manage.py shell
   >>> from expenses.models import Expense
   >>> Expense.objects.all()
   ```

## Quick Fixes

**Reset everything:**
```bash
# Delete database
rm db.sqlite3

# Recreate
python manage.py migrate
python manage.py createsuperuser
```

**Clear browser cache:**
- Hard refresh: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)
- Clear cookies and cache

**Restart server:**
- Stop: Ctrl+C
- Start: `python manage.py runserver`

## Environment Variables Checklist

Development (.env or local):
- ✅ DEBUG=True
- ✅ SECRET_KEY=any-value-for-dev

Production (Render):
- ✅ DEBUG=False
- ✅ SECRET_KEY=<50-char-random-string>
- ✅ DATABASE_URL=<render-postgresql-url>
- ✅ ALLOWED_HOSTS=<your-app>.onrender.com
- ✅ PYTHON_VERSION=3.11.9

## Still Having Issues?

1. Check Django documentation: https://docs.djangoproject.com/
2. Check Render documentation: https://render.com/docs
3. Review error logs carefully
4. Test locally first before deploying
5. Verify all environment variables are set correctly
