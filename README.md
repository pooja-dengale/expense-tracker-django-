# Expense Tracker - Django Application

A complete Django web application for tracking personal expenses with user authentication, categories, and expense management.

## Features

✅ **User Authentication**
- User registration with email validation
- Secure login/logout
- Session management

✅ **Expense Management**
- Add, edit, and delete expenses
- Organize expenses by categories
- View expense history with date filtering

✅ **Dashboard**
- Total expense summary
- Monthly expense tracking
- Recent expense list
- Category statistics

✅ **Security**
- All views protected with login_required decorator
- Users can only see their own data
- CSRF protection
- Password validation

✅ **Responsive UI**
- Bootstrap 5 integration
- Mobile-friendly design
- Intuitive navigation

## Project Structure

```
expense_tracker/
├── manage.py                          # Django management script
├── requirements.txt                   # Project dependencies
├── expense_tracker/                   # Main project settings
│   ├── settings.py                   # Django configuration
│   ├── urls.py                       # Main URL routing
│   └── wsgi.py                       # WSGI application
├── accounts/                         # User authentication app
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── admin.py
├── expenses/                         # Expense management app
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── admin.py
└── templates/                        # HTML templates
    ├── base.html
    ├── accounts/
    │   ├── register.html
    │   └── login.html
    └── expenses/
        ├── dashboard.html
        ├── expense_list.html
        ├── add_expense.html
        ├── edit_expense.html
        └── add_category.html
```

## Installation & Setup

### 1. Create Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Apply Migrations

```bash
python manage.py migrate
```

### 4. Create Superuser (Admin Account)

```bash
python manage.py createsuperuser
```
Follow the prompts to create an admin account.

### 5. Run Development Server

```bash
python manage.py runserver
```

The application will be available at: http://127.0.0.1:8000/

## Usage

### Registration & Login
1. Visit http://127.0.0.1:8000/accounts/register/
2. Create a new account with username, email, and password
3. Login with your credentials at http://127.0.0.1:8000/accounts/login/

### Using the Application
1. **Dashboard** - View expense summary when you login
2. **Add Expense** - Click "Add Expense" button to create new entries
3. **View All Expenses** - See complete expense list with filtering options
4. **Edit Expense** - Click "Edit" to modify existing expenses
5. **Delete Expense** - Click "Delete" to remove expenses
6. **Add Category** - Create custom categories for organizing expenses

### Admin Interface
- Admin URL: http://127.0.0.1:8000/admin/
- Use superuser credentials created during setup
- Manage users, expenses, and categories from admin panel

## Models

### User (Django Built-in)
- username, email, password, first_name, last_name

### Category
- `name` - Category name (e.g., "Food", "Transport")
- `user` - Foreign key to User
- `created_at` - Creation timestamp

### Expense
- `title` - Expense description
- `amount` - Numeric amount
- `category` - Foreign key to Category
- `date` - Date when expense occurred
- `user` - Foreign key to User
- `created_at` - Creation timestamp
- `updated_at` - Last modification timestamp

## Security Features

1. **Authentication** - All views protected with `@login_required` decorator
2. **Authorization** - Users can only access/modify their own data
3. **CSRF Protection** - All forms include CSRF tokens
4. **Password Security** - Django's password validation and hashing
5. **Email Validation** - Unique email requirement on registration

## URL Routing

### Accounts App
- `/accounts/register/` - User registration
- `/accounts/login/` - User login
- `/accounts/logout/` - User logout

### Expenses App
- `/` - Dashboard (home page)
- `/expenses/list/` - Expense list
- `/expenses/add/` - Add new expense
- `/expenses/edit/<id>/` - Edit expense
- `/expenses/delete/<id>/` - Delete expense
- `/expenses/category/add/` - Add new category

### Admin
- `/admin/` - Django admin interface

## Customization

### Change Secret Key (Required for Production)
Edit `expense_tracker/settings.py`:
```python
SECRET_KEY = 'your-secret-key-here'
```

### Update Database
Default is SQLite. To use PostgreSQL, MySQL, etc., modify `DATABASES` in settings.py

### Add Custom Fields
Edit models in `expenses/models.py` and `accounts/models.py`, then:
```bash
python manage.py makemigrations
python manage.py migrate
```

## Troubleshooting

### Port Already in Use
```bash
python manage.py runserver 8001
```

### Database Errors
```bash
python manage.py migrate --run-syncdb
```

### Template Not Found
Ensure `TEMPLATES['DIRS']` in settings.py includes `BASE_DIR / 'templates'`

## Future Enhancements

- Expense CSV export
- Budget alerts
- Monthly reports with charts
- Recurring expenses
- Multi-currency support
- Mobile app
- Email notifications
- Data backup system

## License

This project is open source and available under the MIT License.

## Support

For issues or questions, refer to the Django documentation at https://docs.djangoproject.com/
