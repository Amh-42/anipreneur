#!/usr/bin/env python3
"""
SEO Fields Migration Script
Adds SEO-related fields to existing posts in the database.
"""

import os
import sys
from datetime import datetime
import re

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import Post, User
from seo_utils import SEOUtils

def migrate_seo_fields():
    """Migrate existing posts to include SEO fields"""
    
    with app.app_context():
        print("Starting SEO fields migration...")
        
        # Get all posts
        posts = Post.query.all()
        print(f"Found {len(posts)} posts to migrate")
        
        migrated_count = 0
        
        for post in posts:
            print(f"\nProcessing post: {post.title}")
            
            # Generate meta description if not exists
            if not post.meta_description:
                if post.excerpt:
                    post.meta_description = post.excerpt[:160]
                elif post.content:
                    post.meta_description = SEOUtils.generate_meta_description(post.content)
                print(f"  ✓ Generated meta description: {post.meta_description[:50]}...")
            
            # Extract focus keyword from title if not exists
            if not post.focus_keyword:
                keywords = SEOUtils.extract_keywords_from_title(post.title)
                if keywords:
                    post.focus_keyword = keywords[0]
                    print(f"  ✓ Extracted focus keyword: {post.focus_keyword}")
            
            # Generate schema markup if not exists
            if not post.schema_markup:
                schema_data = {
                    'title': post.title,
                    'meta_description': post.meta_description,
                    'featured_image': post.featured_image,
                    'author_name': post.author.username,
                    'created_at': post.created_at.isoformat(),
                    'updated_at': post.updated_at.isoformat(),
                    'canonical_url': f"https://anipreneur.com/blog/{post.slug}"
                }
                post.schema_markup = SEOUtils.generate_schema_markup(schema_data)
                print(f"  ✓ Generated schema markup")
            
            # Set default meta keywords if not exists
            if not post.meta_keywords:
                post.meta_keywords = "anime, business, entrepreneurship, strategy"
                print(f"  ✓ Set default meta keywords")
            
            # Update the post
            post.updated_at = datetime.utcnow()
            migrated_count += 1
        
        # Commit all changes
        try:
            db.session.commit()
            print(f"\n✅ Successfully migrated {migrated_count} posts!")
            print("All SEO fields have been added to existing posts.")
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error during migration: {e}")
            return False
        
        return True

def verify_migration():
    """Verify that migration was successful"""
    
    with app.app_context():
        print("\nVerifying migration...")
        
        posts = Post.query.all()
        issues = []
        
        for post in posts:
            if not post.meta_description:
                issues.append(f"Post '{post.title}' missing meta description")
            if not post.focus_keyword:
                issues.append(f"Post '{post.title}' missing focus keyword")
            if not post.schema_markup:
                issues.append(f"Post '{post.title}' missing schema markup")
        
        if issues:
            print("❌ Migration verification failed:")
            for issue in issues:
                print(f"  - {issue}")
            return False
        else:
            print("✅ Migration verification successful!")
            print(f"All {len(posts)} posts have required SEO fields.")
            return True

def show_seo_stats():
    """Show SEO statistics for all posts"""
    
    with app.app_context():
        posts = Post.query.all()
        
        print("\n📊 SEO Statistics:")
        print(f"Total posts: {len(posts)}")
        
        # Count posts with different SEO elements
        with_meta_desc = sum(1 for p in posts if p.meta_description)
        with_focus_keyword = sum(1 for p in posts if p.focus_keyword)
        with_schema = sum(1 for p in posts if p.schema_markup)
        with_canonical = sum(1 for p in posts if p.canonical_url)
        
        print(f"Posts with meta description: {with_meta_desc}/{len(posts)}")
        print(f"Posts with focus keyword: {with_focus_keyword}/{len(posts)}")
        print(f"Posts with schema markup: {with_schema}/{len(posts)}")
        print(f"Posts with canonical URL: {with_canonical}/{len(posts)}")
        
        # Show focus keywords
        print("\n🎯 Focus Keywords Used:")
        keywords = {}
        for post in posts:
            if post.focus_keyword:
                keywords[post.focus_keyword] = keywords.get(post.focus_keyword, 0) + 1
        
        for keyword, count in sorted(keywords.items(), key=lambda x: x[1], reverse=True):
            print(f"  {keyword}: {count} posts")

if __name__ == "__main__":
    print("🚀 Anipreneur SEO Migration Tool")
    print("=" * 40)
    
    # Check if database exists
    if not os.path.exists('instance/anipreneur.db'):
        print("❌ Database not found. Please run the app first to create the database.")
        sys.exit(1)
    
    # Run migration
    if migrate_seo_fields():
        # Verify migration
        if verify_migration():
            # Show statistics
            show_seo_stats()
            print("\n🎉 Migration completed successfully!")
        else:
            print("\n⚠️  Migration completed but verification failed.")
    else:
        print("\n❌ Migration failed!")
        sys.exit(1) 