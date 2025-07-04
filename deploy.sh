#!/bin/bash

echo "🚀 Anipreneur Flask App Deployment Script"
echo "=========================================="

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo "❌ Error: app.py not found. Please run this script from your Flask app directory."
    exit 1
fi

echo "✅ Found Flask app in current directory"

# Create necessary directories if they don't exist
echo "📁 Creating necessary directories..."

# Create public_html if it doesn't exist
if [ ! -d "../public_html" ]; then
    mkdir -p ../public_html
    echo "✅ Created public_html directory"
fi

# Copy files to public_html
echo "📋 Copying files to public_html..."

# Copy the Flask app to public_html
cp -r . ../public_html/
echo "✅ Copied Flask app to public_html"

# Set proper permissions
echo "🔐 Setting proper permissions..."
chmod 755 ../public_html/
chmod 644 ../public_html/*.py
chmod 644 ../public_html/*.txt
chmod 644 ../public_html/.htaccess

echo "✅ Permissions set"

# Create a simple index.html for testing
cat > ../public_html/index.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>Anipreneur - Loading...</title>
    <meta http-equiv="refresh" content="0;url=/">
</head>
<body>
    <h1>Anipreneur Flask App</h1>
    <p>If you're seeing this, the Flask app is loading...</p>
    <p>If the page doesn't redirect automatically, <a href="/">click here</a>.</p>
</body>
</html>
EOF

echo "✅ Created index.html"

echo ""
echo "🎉 Deployment setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Upload all files to your cPanel public_html directory"
echo "2. Make sure Python is enabled in your cPanel"
echo "3. Install requirements: pip install -r requirements.txt"
echo "4. Check your domain: https://yourdomain.com"
echo ""
echo "🔧 If you have issues:"
echo "- Check cPanel error logs"
echo "- Verify Python version compatibility"
echo "- Ensure all dependencies are installed"
echo ""
echo "📞 For support, check the error logs in cPanel" 