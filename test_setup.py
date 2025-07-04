#!/usr/bin/env python3
"""
Test script to verify Flask app setup
Run this in your cPanel terminal to check if everything is working
"""

import sys
import os

def test_python_version():
    print(f"🐍 Python version: {sys.version}")
    return True

def test_imports():
    print("📦 Testing imports...")
    try:
        import flask
        print(f"✅ Flask version: {flask.__version__}")
    except ImportError as e:
        print(f"❌ Flask import failed: {e}")
        return False
    
    try:
        from flask_sqlalchemy import SQLAlchemy
        print("✅ SQLAlchemy imported successfully")
    except ImportError as e:
        print(f"❌ SQLAlchemy import failed: {e}")
        return False
    
    try:
        from flask_login import LoginManager
        print("✅ Flask-Login imported successfully")
    except ImportError as e:
        print(f"❌ Flask-Login import failed: {e}")
        return False
    
    return True

def test_app_import():
    print("🚀 Testing Flask app import...")
    try:
        from app import app
        print("✅ Flask app imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Flask app import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_file_structure():
    print("📁 Testing file structure...")
    required_files = [
        'app.py',
        'passenger_wsgi.py',
        'requirements.txt',
        'models.py'
    ]
    
    required_dirs = [
        'templates',
        'static'
    ]
    
    all_good = True
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} exists")
        else:
            print(f"❌ {file} missing")
            all_good = False
    
    for dir in required_dirs:
        if os.path.exists(dir) and os.path.isdir(dir):
            print(f"✅ {dir}/ directory exists")
        else:
            print(f"❌ {dir}/ directory missing")
            all_good = False
    
    return all_good

def test_passenger_wsgi():
    print("🔧 Testing passenger_wsgi.py...")
    try:
        with open('passenger_wsgi.py', 'r') as f:
            content = f.read()
            if 'application = app' in content:
                print("✅ passenger_wsgi.py looks correct")
                return True
            else:
                print("❌ passenger_wsgi.py missing 'application = app'")
                return False
    except FileNotFoundError:
        print("❌ passenger_wsgi.py not found")
        return False

def main():
    print("🧪 Anipreneur Flask App Setup Test")
    print("=" * 40)
    
    tests = [
        ("Python Version", test_python_version),
        ("File Structure", test_file_structure),
        ("Dependencies", test_imports),
        ("Passenger WSGI", test_passenger_wsgi),
        ("Flask App", test_app_import)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🔍 {test_name}:")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with error: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 40)
    print("📊 Test Results:")
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your Flask app should work.")
        print("\n📋 Next steps:")
        print("1. Visit your domain: https://anipreneur.com")
        print("2. Check cPanel error logs if it doesn't work")
        print("3. Contact hosting provider if Python isn't supported")
    else:
        print("⚠️  Some tests failed. Check the issues above.")
        print("\n🔧 Common fixes:")
        print("1. Install missing packages: pip install -r requirements.txt")
        print("2. Check file permissions: chmod 644 *.py")
        print("3. Verify all files are uploaded correctly")

if __name__ == "__main__":
    main() 