# cPanel Deployment Guide for Anipreneur Flask App

## Prerequisites
- cPanel hosting with Python support
- Passenger enabled on your hosting plan
- SSH access (recommended)

## Step 1: Prepare Your Files

1. **Update passenger_wsgi.py**
   - Replace `YOUR_CPANEL_USERNAME` with your actual cPanel username
   - Update the Python path to match your server's Python version

2. **Update .htaccess**
   - Replace `YOUR_CPANEL_USERNAME` with your actual cPanel username
   - Adjust the virtualenv path if needed

## Step 2: Upload Files to cPanel

### Option A: Using File Manager
1. Log into cPanel
2. Open File Manager
3. Navigate to `public_html`
4. Upload all project files:
   - `app.py`
   - `passenger_wsgi.py`
   - `requirements.txt`
   - `.htaccess`
   - `templates/` folder
   - `static/` folder

### Option B: Using FTP/SFTP
```bash
# Upload files to your domain's root directory
scp -r ./* your_username@your_domain.com:public_html/
```

## Step 3: Set Up Python Environment

### Via cPanel Python Selector
1. In cPanel, find "Setup Python App"
2. Create a new Python app:
   - **Python version**: 3.9 or higher
   - **Application root**: `/home/YOUR_CPANEL_USERNAME/public_html`
   - **Application URL**: `yourdomain.com`
   - **Application startup file**: `passenger_wsgi.py`

### Via SSH (Alternative)
```bash
# Connect to your server
ssh your_username@your_domain.com

# Navigate to your app directory
cd public_html

# Create virtual environment
python3.9 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Step 4: Configure Passenger

### Update passenger_wsgi.py
Make sure the Python path matches your virtual environment:
```python
INTERP = os.path.expanduser("/home/YOUR_CPANEL_USERNAME/virtualenv/anipreneur/3.9/bin/python")
```

### Update .htaccess
Ensure the paths are correct:
```apache
PassengerPython /home/YOUR_CPANEL_USERNAME/virtualenv/anipreneur/3.9/bin/python
PassengerAppRoot /home/YOUR_CPANEL_USERNAME/public_html
```

## Step 5: Set Permissions

Via SSH or File Manager:
```bash
# Set proper permissions
chmod 755 public_html
chmod 644 public_html/*.py
chmod 644 public_html/.htaccess
chmod -R 755 public_html/templates
chmod -R 755 public_html/static
```

## Step 6: Test Your Application

1. Visit your domain: `https://yourdomain.com`
2. Test all routes:
   - Home: `/`
   - Blog: `/blog`
   - Detail: `/detail`

## Troubleshooting

### Common Issues

1. **500 Internal Server Error**
   - Check error logs in cPanel → Error Logs
   - Verify Python path in `passenger_wsgi.py`
   - Ensure all dependencies are installed

2. **Module Not Found Errors**
   - Run `pip install -r requirements.txt` in your virtual environment
   - Check if virtual environment is activated

3. **Static Files Not Loading**
   - Verify `.htaccess` configuration
   - Check file permissions
   - Ensure static files are in the correct directory

4. **Passenger Not Starting**
   - Check Passenger configuration in cPanel
   - Verify `passenger_wsgi.py` syntax
   - Check Python version compatibility

### Debug Mode (Development Only)
Add to `passenger_wsgi.py`:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check Logs
- **cPanel Error Logs**: cPanel → Error Logs
- **Passenger Logs**: Usually in `/tmp/passenger.log`
- **Application Logs**: Add logging to your Flask app

## Security Considerations

1. **Environment Variables**
   - Set `FLASK_ENV=production`
   - Set `FLASK_DEBUG=0`
   - Use environment variables for sensitive data

2. **File Permissions**
   - Restrict access to sensitive files
   - Use proper file permissions (755 for directories, 644 for files)

3. **HTTPS**
   - Enable SSL certificate in cPanel
   - Force HTTPS redirects

## Performance Optimization

1. **Static File Caching**
   - Already configured in `.htaccess`
   - Consider using CDN for static assets

2. **Database Optimization** (if adding database later)
   - Use connection pooling
   - Implement caching strategies

3. **Code Optimization**
   - Enable gzip compression
   - Minify CSS/JS files

## Maintenance

1. **Regular Updates**
   - Keep Flask and dependencies updated
   - Monitor security advisories

2. **Backup Strategy**
   - Regular backups of application files
   - Database backups (if applicable)

3. **Monitoring**
   - Set up uptime monitoring
   - Monitor error logs regularly 