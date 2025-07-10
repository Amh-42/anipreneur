#!/usr/bin/env python3
"""
Open Graph Meta Tag Debugger
Helps test and debug social media meta tags for your blog posts.
"""

import requests
import json
import sys
from urllib.parse import urlparse

def test_facebook_sharing(url):
    """Test how your URL appears when shared on Facebook"""
    print(f"\n🔍 Testing Facebook Sharing for: {url}")
    print("=" * 50)
    
    try:
        # Use Facebook's sharing debugger API
        debug_url = f"https://graph.facebook.com/v18.0/?id={url}&scrape=true"
        response = requests.get(debug_url)
        data = response.json()
        
        if 'error' in data:
            print(f"❌ Error: {data['error']['message']}")
            return False
        
        print("✅ Facebook Debug Results:")
        print(f"   Title: {data.get('title', 'Not found')}")
        print(f"   Description: {data.get('description', 'Not found')}")
        print(f"   Image: {data.get('image', 'Not found')}")
        print(f"   Type: {data.get('type', 'Not found')}")
        print(f"   URL: {data.get('url', 'Not found')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing Facebook: {e}")
        return False

def test_twitter_sharing(url):
    """Test how your URL appears when shared on Twitter"""
    print(f"\n🐦 Testing Twitter Sharing for: {url}")
    print("=" * 50)
    
    try:
        # Twitter doesn't have a public API for this, but we can check the meta tags
        response = requests.get(url)
        html = response.text
        
        # Extract Twitter Card meta tags
        twitter_tags = {}
        lines = html.split('\n')
        
        for line in lines:
            if 'twitter:' in line and 'content=' in line:
                # Extract tag name and content
                if 'name="twitter:' in line:
                    start = line.find('name="twitter:') + 13
                    end = line.find('"', start)
                    tag_name = line[start:end]
                    
                    start = line.find('content="') + 9
                    end = line.find('"', start)
                    content = line[start:end]
                    
                    twitter_tags[tag_name] = content
        
        if twitter_tags:
            print("✅ Twitter Card Meta Tags Found:")
            for tag, content in twitter_tags.items():
                print(f"   {tag}: {content}")
        else:
            print("❌ No Twitter Card meta tags found")
            
        return len(twitter_tags) > 0
        
    except Exception as e:
        print(f"❌ Error testing Twitter: {e}")
        return False

def test_linkedin_sharing(url):
    """Test how your URL appears when shared on LinkedIn"""
    print(f"\n💼 Testing LinkedIn Sharing for: {url}")
    print("=" * 50)
    
    try:
        # LinkedIn uses similar meta tags to Facebook
        response = requests.get(url)
        html = response.text
        
        # Extract Open Graph meta tags
        og_tags = {}
        lines = html.split('\n')
        
        for line in lines:
            if 'property="og:' in line and 'content=' in line:
                # Extract tag name and content
                start = line.find('property="og:') + 13
                end = line.find('"', start)
                tag_name = line[start:end]
                
                start = line.find('content="') + 9
                end = line.find('"', start)
                content = line[start:end]
                
                og_tags[tag_name] = content
        
        if og_tags:
            print("✅ Open Graph Meta Tags Found:")
            for tag, content in og_tags.items():
                print(f"   {tag}: {content}")
        else:
            print("❌ No Open Graph meta tags found")
            
        return len(og_tags) > 0
        
    except Exception as e:
        print(f"❌ Error testing LinkedIn: {e}")
        return False

def validate_image_url(image_url):
    """Validate that the Open Graph image URL is accessible"""
    print(f"\n🖼️  Validating Image URL: {image_url}")
    print("=" * 50)
    
    try:
        response = requests.head(image_url, timeout=10)
        
        if response.status_code == 200:
            content_type = response.headers.get('content-type', '')
            content_length = response.headers.get('content-length', '0')
            
            print("✅ Image is accessible")
            print(f"   Content-Type: {content_type}")
            print(f"   File Size: {int(content_length):,} bytes")
            
            # Check if it's an image
            if 'image/' in content_type:
                print("✅ Valid image format")
            else:
                print("⚠️  Warning: URL doesn't seem to be an image")
                
            return True
        else:
            print(f"❌ Image not accessible (Status: {response.status_code})")
            return False
            
    except Exception as e:
        print(f"❌ Error validating image: {e}")
        return False

def generate_test_urls(base_url):
    """Generate test URLs for different pages"""
    urls = {
        'Homepage': base_url,
        'Blog': f"{base_url}/blog",
        'Courses': f"{base_url}/courses",
        'Social Links': f"{base_url}/links"
    }
    return urls

def main():
    print("🚀 Anipreneur Open Graph Meta Tag Debugger")
    print("=" * 60)
    
    if len(sys.argv) < 2:
        print("Usage: python og_debug.py <your-domain>")
        print("Example: python og_debug.py https://anipreneur.com")
        sys.exit(1)
    
    base_url = sys.argv[1].rstrip('/')
    
    # Test different pages
    test_urls = generate_test_urls(base_url)
    
    for page_name, url in test_urls.items():
        print(f"\n{'='*60}")
        print(f"📄 Testing {page_name}")
        print(f"{'='*60}")
        
        # Test each platform
        facebook_ok = test_facebook_sharing(url)
        twitter_ok = test_twitter_sharing(url)
        linkedin_ok = test_linkedin_sharing(url)
        
        # Summary
        print(f"\n📊 {page_name} Summary:")
        print(f"   Facebook: {'✅' if facebook_ok else '❌'}")
        print(f"   Twitter: {'✅' if twitter_ok else '❌'}")
        print(f"   LinkedIn: {'✅' if linkedin_ok else '❌'}")
    
    # Test image validation
    print(f"\n{'='*60}")
    print("🖼️  Testing Default Open Graph Image")
    print(f"{'='*60}")
    validate_image_url(f"{base_url}/static/images/anipreneur-default-og.jpg")
    
    print(f"\n{'='*60}")
    print("🎯 Manual Testing Tools")
    print(f"{'='*60}")
    print("You can also test your URLs manually using these tools:")
    print(f"   Facebook: https://developers.facebook.com/tools/debug/")
    print(f"   Twitter: https://cards-dev.twitter.com/validator")
    print(f"   LinkedIn: https://www.linkedin.com/post-inspector/")
    print(f"   Pinterest: https://developers.pinterest.com/tools/url-debugger/")

if __name__ == "__main__":
    main() 