# cPanel Deployment Checklist

## Before Upload
- [ ] Update `passenger_wsgi.py` with your cPanel username
- [ ] Update `.htaccess` with your cPanel username
- [ ] Change `SECRET_KEY` in `app.py` or set environment variable
- [ ] Test locally: `python app.py`

## File Upload
- [ ] Upload `app.py` to `public_html/`
- [ ] Upload `passenger_wsgi.py` to `public_html/`
- [ ] Upload `requirements.txt` to `public_html/`
- [ ] Upload `.htaccess` to `public_html/`
- [ ] Upload `templates/` folder to `public_html/`
- [ ] Upload `static/` folder to `public_html/`

## cPanel Configuration
- [ ] Go to "Setup Python App" in cPanel
- [ ] Create new Python app
- [ ] Set Python version to 3.9+
- [ ] Set application root to `/home/YOUR_USERNAME/public_html`
- [ ] Set startup file to `passenger_wsgi.py`
- [ ] Set application URL to your domain

## Environment Setup
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Set file permissions:
  - [ ] `chmod 755 public_html`
  - [ ] `chmod 644 public_html/*.py`
  - [ ] `chmod 644 public_html/.htaccess`
  - [ ] `chmod -R 755 public_html/templates`
  - [ ] `chmod -R 755 public_html/static`

## Testing
- [ ] Visit your domain
- [ ] Test home page: `/`
- [ ] Test blog page: `/blog`
- [ ] Test detail page: `/detail`
- [ ] Test 404 page: `/nonexistent`
- [ ] Check static files load correctly

## Troubleshooting
- [ ] Check cPanel error logs
- [ ] Verify Python path in `passenger_wsgi.py`
- [ ] Confirm all dependencies installed
- [ ] Check file permissions
- [ ] Verify `.htaccess` syntax

## Security
- [ ] Set `FLASK_ENV=production`
- [ ] Set `FLASK_DEBUG=0`
- [ ] Change default `SECRET_KEY`
- [ ] Enable SSL certificate
- [ ] Set up HTTPS redirects

## Performance
- [ ] Enable gzip compression
- [ ] Set up static file caching
- [ ] Consider CDN for static assets
- [ ] Monitor application performance 