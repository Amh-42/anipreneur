# 🚀 Anipreneur Flask App - cPanel Deployment Troubleshooting

## ❌ Common Issues & Solutions

### 1. "Index file is not available" Error
**Problem**: cPanel can't find your Flask app
**Solution**: 
- Make sure all files are in `/public_html/` directory
- Ensure `passenger_wsgi.py` is in the root of public_html
- Check that `.htaccess` file exists and is readable

### 2. "cannot determine application type" Error
**Problem**: Passenger can't detect your Python app
**Solution**:
- Verify `passenger_wsgi.py` exists and is named correctly
- Check that Python is enabled in your cPanel
- Ensure the file has proper permissions (644)

### 3. Import Errors
**Problem**: Flask app can't import modules
**Solution**:
- Install requirements: `pip install -r requirements.txt`
- Check Python version compatibility
- Verify all files are uploaded correctly

## 📋 Step-by-Step Fix

### Step 1: Upload Files Correctly
```
public_html/
├── app.py
├── passenger_wsgi.py
├── requirements.txt
├── .htaccess
├── templates/
├── static/
└── models.py
```

### Step 2: Set Permissions
```bash
chmod 644 *.py
chmod 644 *.txt
chmod 644 .htaccess
chmod 755 templates/
chmod 755 static/
```

### Step 3: Install Dependencies
In cPanel Terminal or SSH:
```bash
cd public_html
pip install -r requirements.txt
```

### Step 4: Test the Setup
1. Visit your domain: `https://yourdomain.com`
2. Check for any error messages
3. Look at cPanel error logs

## 🔧 Advanced Troubleshooting

### Check Python Version
```bash
python3 --version
```

### Test Flask App Locally
```bash
python3 app.py
```

### Check Passenger Logs
Look in cPanel → Error Logs for specific error messages.

### Common Error Messages

| Error | Solution |
|-------|----------|
| "ModuleNotFoundError" | Install missing packages |
| "Permission denied" | Fix file permissions |
| "Application startup failed" | Check passenger_wsgi.py syntax |
| "No module named 'flask'" | Install Flask: `pip install flask` |

## 📞 Getting Help

1. **Check cPanel Error Logs** - Most specific error info
2. **Test locally first** - Ensure app works on your computer
3. **Verify file structure** - All files must be in public_html
4. **Check Python support** - Contact hosting provider if Python isn't available

## ✅ Success Checklist

- [ ] All files uploaded to public_html
- [ ] passenger_wsgi.py exists and is readable
- [ ] .htaccess file is present
- [ ] requirements.txt dependencies installed
- [ ] Python enabled in cPanel
- [ ] No syntax errors in Python files
- [ ] Domain resolves to your site

## 🚨 Emergency Fix

If nothing works, try this minimal setup:

1. Create a simple `passenger_wsgi.py`:
```python
def application(environ, start_response):
    status = '200 OK'
    output = b'Hello World!'
    response_headers = [('Content-type', 'text/plain'),
                       ('Content-Length', str(len(output)))]
    start_response(status, response_headers)
    return [output]
```

2. Test if this works, then gradually add your Flask app back.

---

**Need more help?** Check your hosting provider's documentation for Python/Flask deployment. 