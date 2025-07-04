# 🔧 cPanel IP Access Troubleshooting Guide

## Quick Fix Steps

### 1. **Temporary Bypass (For Testing)**
Set this environment variable to temporarily disable IP restrictions:
```bash
export ADMIN_DEBUG_MODE=True
```

### 2. **Find Your Real IP**
Run the debug script to see what IP cPanel is actually detecting:
```bash
python debug_ip.py
```
Then visit `yourdomain.com/debug-ip` to see the recommended IP.

### 3. **Update Your IP Whitelist**
Use the IP from the debug tool:
```bash
export ADMIN_ALLOWED_IPS='127.0.0.1,::1,YOUR_REAL_IP_HERE'
```

## Common cPanel Issues

### **Problem 1: Proxy Headers**
cPanel often uses proxy servers that change the client IP. The updated code now checks multiple headers:
- `X-Forwarded-For`
- `X-Real-IP` 
- `X-Client-IP`
- `CF-Connecting-IP` (Cloudflare)

### **Problem 2: Environment Variables Not Set**
Make sure your environment variables are properly set in cPanel:
1. Go to cPanel → Software → Setup Python App
2. Add environment variables:
   - `ADMIN_ALLOWED_IPS=127.0.0.1,::1,YOUR_IP`
   - `ADMIN_DEBUG_MODE=False`

### **Problem 3: Application Not Restarted**
After changing environment variables, restart your Python app in cPanel.

## Step-by-Step Solution

### **Step 1: Enable Debug Mode**
```bash
export ADMIN_DEBUG_MODE=True
```
This will temporarily bypass IP restrictions so you can access admin.

### **Step 2: Find Your Real IP**
1. Upload `debug_ip.py` to your cPanel
2. Run it: `python debug_ip.py`
3. Visit `yourdomain.com/debug-ip`
4. Copy the "Recommended IP"

### **Step 3: Update Whitelist**
```bash
export ADMIN_ALLOWED_IPS='127.0.0.1,::1,YOUR_REAL_IP'
```

### **Step 4: Disable Debug Mode**
```bash
export ADMIN_DEBUG_MODE=False
```

### **Step 5: Test Access**
Try accessing `/admin/login` again.

## Alternative Solutions

### **Option 1: Use .htaccess (Apache)**
If you're using Apache, you can also restrict access via `.htaccess`:

```apache
# .htaccess file
<Files "admin/*">
    Order Deny,Allow
    Deny from all
    Allow from 127.0.0.1
    Allow from YOUR_IP_HERE
</Files>
```

### **Option 2: Disable IP Check Temporarily**
Comment out the `@admin_ip_required` decorators in `app.py` temporarily:

```python
# @admin_ip_required  # Comment this out temporarily
def admin_login():
    # ... rest of function
```

### **Option 3: Use Session-Based Security**
Instead of IP restrictions, you could implement:
- Two-factor authentication
- Session timeouts
- Login attempt limits

## Debugging Commands

### **Check Current Environment**
```bash
echo $ADMIN_ALLOWED_IPS
echo $ADMIN_DEBUG_MODE
```

### **Test IP Detection**
```bash
curl -H "X-Forwarded-For: YOUR_IP" yourdomain.com/debug-ip
```

### **View Application Logs**
Check your cPanel error logs for IP-related messages.

## cPanel-Specific Settings

### **Python App Configuration**
1. cPanel → Software → Setup Python App
2. Add environment variables:
   ```
   ADMIN_ALLOWED_IPS=127.0.0.1,::1,YOUR_IP
   ADMIN_DEBUG_MODE=False
   ```

### **Passenger Configuration**
If using Passenger, add to `passenger_wsgi.py`:
```python
import os
os.environ['ADMIN_ALLOWED_IPS'] = '127.0.0.1,::1,YOUR_IP'
os.environ['ADMIN_DEBUG_MODE'] = 'False'
```

## Emergency Access

If you're completely locked out:

1. **SSH Access**: Connect via SSH and edit files directly
2. **File Manager**: Use cPanel File Manager to edit `app.py`
3. **Temporary Disable**: Comment out all `@admin_ip_required` decorators
4. **Database Access**: Use phpMyAdmin to modify settings directly

## Testing Your Setup

### **Test 1: Debug Mode**
```bash
export ADMIN_DEBUG_MODE=True
# Try accessing /admin/login
```

### **Test 2: IP Detection**
```bash
python debug_ip.py
# Visit /debug-ip and note the IP
```

### **Test 3: Whitelist**
```bash
export ADMIN_DEBUG_MODE=False
export ADMIN_ALLOWED_IPS='127.0.0.1,::1,YOUR_IP'
# Try accessing /admin/login
```

## Common IP Addresses

- **Localhost**: `127.0.0.1` or `::1`
- **cPanel Server**: Usually starts with `192.168.` or `10.`
- **Your Network**: Check with `whatismyip.com`

## Still Having Issues?

1. **Check cPanel logs** for error messages
2. **Verify environment variables** are set correctly
3. **Test with debug mode** first
4. **Contact your hosting provider** for proxy configuration
5. **Consider alternative security** methods (2FA, session limits)

## Security Notes

- ⚠️ **Debug mode should only be used temporarily**
- 🔒 **Always re-enable security after testing**
- 📝 **Keep a backup of your original configuration**
- 🔍 **Monitor logs for unauthorized access attempts**

---

**Need Help?** If you're still having issues, please share:
1. The output from `/debug-ip`
2. Your cPanel environment variables
3. Any error messages from logs 