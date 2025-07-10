#!/usr/bin/env python3
"""
Test script to verify featured image functionality
"""

import requests
from bs4 import BeautifulSoup
import re

def test_featured_image_meta_tags():
    """Test that featured images are properly used in meta tags"""
    
    # Test URLs (replace with your actual domain)
    base_url = "http://localhost:5000"  # Change this to your actual domain
    
    print("🔍 Testing Featured Image Meta Tags...")
    print("=" * 50)
    
    try:
        # Test blog listing page
        print("\n1. Testing Blog Listing Page...")
        response = requests.get(f"{base_url}/blog")
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Check for Open Graph image
            og_image = soup.find('meta', property='og:image')
            if og_image:
                print(f"✅ Blog listing has Open Graph image: {og_image.get('content')}")
            else:
                print("❌ Blog listing missing Open Graph image")
            
            # Check for Twitter Card image
            twitter_image = soup.find('meta', attrs={'name': 'twitter:image'})
            if twitter_image:
                print(f"✅ Blog listing has Twitter Card image: {twitter_image.get('content')}")
            else:
                print("❌ Blog listing missing Twitter Card image")
        
        # Test homepage
        print("\n2. Testing Homepage...")
        response = requests.get(base_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            og_image = soup.find('meta', property='og:image')
            if og_image:
                print(f"✅ Homepage has Open Graph image: {og_image.get('content')}")
            else:
                print("❌ Homepage missing Open Graph image")
        
        # Test individual post (if any exist)
        print("\n3. Testing Individual Post...")
        response = requests.get(f"{base_url}/blog")
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for first post link
            post_link = soup.find('a', href=re.compile(r'/blog/'))
            if post_link:
                post_url = post_link.get('href')
                if not post_url.startswith('http'):
                    post_url = base_url + post_url
                
                print(f"Testing post: {post_url}")
                response = requests.get(post_url)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Check for featured image in content
                    featured_img = soup.find('img', class_='featured-image')
                    if featured_img:
                        print(f"✅ Post has featured image: {featured_img.get('src')}")
                    else:
                        print("ℹ️ Post has no featured image in content")
                    
                    # Check for Open Graph image
                    og_image = soup.find('meta', property='og:image')
                    if og_image:
                        print(f"✅ Post has Open Graph image: {og_image.get('content')}")
                    else:
                        print("❌ Post missing Open Graph image")
                    
                    # Check for Twitter Card image
                    twitter_image = soup.find('meta', attrs={'name': 'twitter:image'})
                    if twitter_image:
                        print(f"✅ Post has Twitter Card image: {twitter_image.get('content')}")
                    else:
                        print("❌ Post missing Twitter Card image")
                else:
                    print(f"❌ Could not access post: {response.status_code}")
            else:
                print("ℹ️ No posts found to test")
        
        print("\n" + "=" * 50)
        print("✅ Featured Image Testing Complete!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the server. Make sure the Flask app is running.")
    except Exception as e:
        print(f"❌ Error during testing: {e}")

def test_social_media_preview():
    """Test social media preview tools"""
    
    print("\n🔗 Social Media Preview Testing")
    print("=" * 50)
    print("Test your URLs with these tools:")
    print("\n📘 Facebook:")
    print("https://developers.facebook.com/tools/debug/")
    print("\n🐦 Twitter:")
    print("https://cards-dev.twitter.com/validator")
    print("\n💼 LinkedIn:")
    print("https://www.linkedin.com/post-inspector/")
    print("\n📌 Pinterest:")
    print("https://developers.pinterest.com/tools/url-debugger/")
    
    print("\n📋 Steps to test:")
    print("1. Start your Flask app: python app.py")
    print("2. Create a post with a featured image")
    print("3. Copy the post URL")
    print("4. Paste it into the social media preview tools above")
    print("5. Verify the image appears correctly")

if __name__ == "__main__":
    test_featured_image_meta_tags()
    test_social_media_preview() 