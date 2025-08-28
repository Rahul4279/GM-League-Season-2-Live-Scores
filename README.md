# GMU Live Sports Score Website

A real-time sports score tracking website built with Flask, SocketIO, and modern web technologies. This application allows administrators to update live scores for multiple sports events, which are instantly broadcast to all connected viewers.

## 🏆 Features

### For Viewers
- **Real-time Score Updates**: Live score updates without page refresh
- **Beautiful UI**: Modern, responsive design with smooth animations
- **Multiple Sports**: Support for Football, Kabaddi, Basketball, and Badminton
- **Live Indicators**: Visual indicators showing live match status
- **Mobile Responsive**: Works perfectly on all devices

### For Administrators
- **Secure Admin Dashboard**: Protected login system
- **Easy Score Management**: Simple forms to update scores for each sport
- **Real-time Broadcasting**: Updates are instantly sent to all viewers
- **Current Score Overview**: See all current scores at a glance
- **Form Validation**: Built-in validation and error handling

## 🚀 Technologies Used

- **Backend**: Flask (Python web framework)
- **Database**: SQLite with SQLAlchemy ORM
- **Real-time Communication**: Flask-SocketIO
- **Authentication**: Flask-Login
- **Frontend**: HTML5, CSS3, JavaScript
- **UI Framework**: Bootstrap 5
- **Icons**: Font Awesome
- **WebSocket**: Eventlet

## 📋 Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## 🛠️ Installation

1. **Clone or download the project files**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Access the website**:
   - Open your browser and go to `http://localhost:5000`
   - Admin login: `http://localhost:5000/login`

## 🔐 Default Admin Credentials

- **Username**: `admin`
- **Password**: `password`

## 📱 How to Use

### For Viewers
1. Open the website in your browser
2. View live scores for all sports
3. Scores update automatically in real-time
4. No login required for viewing

### For Administrators
1. Click "Admin Login" or go to `/login`
2. Enter admin credentials
3. Access the admin dashboard
4. Update scores using the forms:
   - **Football**: Enter team names and scores
   - **Kabaddi**: Enter team names and scores
   - **Basketball**: Enter team names and scores
   - **Badminton**: Enter player names and scores
5. Click "Update" to broadcast changes
6. All viewers will see updates instantly

## 🏗️ Project Structure

```
gmu-score/
├── app.py              # Main Flask application
├── config.py           # Configuration settings
├── models.py           # Database models
├── requirements.txt    # Python dependencies
├── README.md          # Project documentation
├── templates/         # HTML templates
│   ├── base.html      # Base template with navigation
│   ├── index.html     # Home page with live scores
│   ├── admin.html     # Admin dashboard
│   └── login.html     # Login page
└── instance/          # Database files (auto-generated)
```

## 🔧 Configuration

The application uses a simple configuration system in `config.py`:

- **SECRET_KEY**: Used for session management
- **SQLALCHEMY_DATABASE_URI**: Database connection string
- **SQLALCHEMY_TRACK_MODIFICATIONS**: SQLAlchemy configuration

## 🎯 Key Features Explained

### Real-time Updates
- Uses WebSocket connections via SocketIO
- Updates are pushed to all connected clients instantly
- No polling required - true real-time experience

### Database Design
- **User Model**: Stores admin credentials
- **Score Model**: Stores current scores for each sport
- Automatic database creation on first run

### Security Features
- Login required for admin access
- Session management with Flask-Login
- Form validation and sanitization

### UI/UX Features
- Responsive design that works on all devices
- Smooth animations and transitions
- Intuitive navigation
- Clear visual hierarchy
- Loading states and feedback

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production Deployment
For production deployment, consider:
1. Using a production WSGI server (Gunicorn, uWSGI)
2. Setting up a reverse proxy (Nginx)
3. Using a production database (PostgreSQL, MySQL)
4. Implementing proper password hashing
5. Setting up HTTPS
6. Using environment variables for sensitive data

## 🔄 Adding New Sports

To add a new sport:

1. **Update the games list** in `app.py`:
   ```python
   games = ['Football', 'Kabaddi', 'Basketball', 'Badminton', 'NewSport']
   ```

2. **Add the sport to templates**:
   - Update `index.html` with new score card
   - Update `admin.html` with new form

3. **Add dummy data** in the initialization section

## 🐛 Troubleshooting

### Common Issues

1. **Port already in use**:
   - Change the port in `app.py`: `socketio.run(app, debug=True, port=5001)`

2. **Database errors**:
   - Delete the `instance/` folder and restart the application

3. **SocketIO connection issues**:
   - Check if all dependencies are installed correctly
   - Ensure no firewall is blocking WebSocket connections

### Debug Mode
The application runs in debug mode by default. For production, set `debug=False` in `socketio.run()`.

## 📞 Support

If you encounter any issues or have questions:
1. Check the console for error messages
2. Verify all dependencies are installed
3. Ensure the database file has proper permissions

## 🎉 Future Enhancements

Potential improvements for the future:
- User registration system
- Match scheduling
- Historical score tracking
- Multiple admin users
- Email notifications
- Mobile app integration
- Advanced statistics
- Match commentary
- Team/player profiles

---

**Built with ❤️ using Flask and modern web technologies** 