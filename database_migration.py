#!/usr/bin/env python3
"""
Database Migration Script
Adds new SEO columns to existing database tables.
"""

import os
import sys
from sqlalchemy import create_engine, text

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import Post, Page, Category

def add_seo_columns():
    """Add SEO columns to existing database tables"""
    
    with app.app_context():
        print("🔧 Starting database migration...")
        
        # Get database engine
        engine = db.engine
        
        try:
            # Add columns to Post table
            print("📝 Adding SEO columns to Post table...")
            
            # Check if columns already exist
            inspector = db.inspect(engine)
            existing_columns = [col['name'] for col in inspector.get_columns('post')]
            
            columns_to_add = [
                ('meta_description', 'VARCHAR(160)'),
                ('meta_keywords', 'VARCHAR(255)'),
                ('primary_keyword', 'VARCHAR(100)'),
                ('secondary_keywords', 'TEXT'),
                ('schema_markup', 'TEXT'),
                ('canonical_url', 'VARCHAR(255)'),
                ('focus_keyword', 'VARCHAR(100)')
            ]
            
            for column_name, column_type in columns_to_add:
                if column_name not in existing_columns:
                    print(f"  ✓ Adding {column_name} column...")
                    with engine.connect() as conn:
                        conn.execute(text(f"ALTER TABLE post ADD COLUMN {column_name} {column_type}"))
                        conn.commit()
                else:
                    print(f"  ⚠️  Column {column_name} already exists")
            
            # Add columns to Page table
            print("\n📄 Adding SEO columns to Page table...")
            existing_page_columns = [col['name'] for col in inspector.get_columns('page')]
            
            page_columns_to_add = [
                ('meta_description', 'VARCHAR(160)'),
                ('meta_keywords', 'VARCHAR(255)'),
                ('primary_keyword', 'VARCHAR(100)'),
                ('schema_markup', 'TEXT')
            ]
            
            for column_name, column_type in page_columns_to_add:
                if column_name not in existing_page_columns:
                    print(f"  ✓ Adding {column_name} column...")
                    with engine.connect() as conn:
                        conn.execute(text(f"ALTER TABLE page ADD COLUMN {column_name} {column_type}"))
                        conn.commit()
                else:
                    print(f"  ⚠️  Column {column_name} already exists")
            
            # Add columns to Category table
            print("\n🏷️  Adding SEO columns to Category table...")
            existing_category_columns = [col['name'] for col in inspector.get_columns('category')]
            
            category_columns_to_add = [
                ('meta_description', 'VARCHAR(160)'),
                ('meta_keywords', 'VARCHAR(255)')
            ]
            
            for column_name, column_type in category_columns_to_add:
                if column_name not in existing_category_columns:
                    print(f"  ✓ Adding {column_name} column...")
                    with engine.connect() as conn:
                        conn.execute(text(f"ALTER TABLE category ADD COLUMN {column_name} {column_type}"))
                        conn.commit()
                else:
                    print(f"  ⚠️  Column {column_name} already exists")
            
            print("\n✅ Database migration completed successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error during migration: {e}")
            return False

def verify_migration():
    """Verify that all columns were added successfully"""
    
    with app.app_context():
        print("\n🔍 Verifying migration...")
        
        engine = db.engine
        inspector = db.inspect(engine)
        
        # Check Post table
        post_columns = [col['name'] for col in inspector.get_columns('post')]
        required_post_columns = [
            'id', 'title', 'slug', 'content', 'excerpt', 'featured_image', 
            'status', 'author_id', 'created_at', 'updated_at',
            'meta_description', 'meta_keywords', 'primary_keyword', 
            'secondary_keywords', 'schema_markup', 'canonical_url', 'focus_keyword'
        ]
        
        missing_post_columns = [col for col in required_post_columns if col not in post_columns]
        
        if missing_post_columns:
            print(f"❌ Missing columns in Post table: {missing_post_columns}")
            return False
        else:
            print("✅ Post table has all required columns")
        
        # Check Page table
        page_columns = [col['name'] for col in inspector.get_columns('page')]
        required_page_columns = [
            'id', 'title', 'slug', 'content', 'status', 'created_at', 'updated_at',
            'meta_description', 'meta_keywords', 'primary_keyword', 'schema_markup'
        ]
        
        missing_page_columns = [col for col in required_page_columns if col not in page_columns]
        
        if missing_page_columns:
            print(f"❌ Missing columns in Page table: {missing_page_columns}")
            return False
        else:
            print("✅ Page table has all required columns")
        
        # Check Category table
        category_columns = [col['name'] for col in inspector.get_columns('category')]
        required_category_columns = [
            'id', 'name', 'slug', 'description', 'created_at',
            'meta_description', 'meta_keywords'
        ]
        
        missing_category_columns = [col for col in required_category_columns if col not in category_columns]
        
        if missing_category_columns:
            print(f"❌ Missing columns in Category table: {missing_category_columns}")
            return False
        else:
            print("✅ Category table has all required columns")
        
        return True

def show_database_info():
    """Show current database structure"""
    
    with app.app_context():
        print("\n📊 Current Database Structure:")
        print("=" * 50)
        
        engine = db.engine
        inspector = db.inspect(engine)
        
        # Show Post table structure
        print("\n📝 Post Table:")
        post_columns = inspector.get_columns('post')
        for col in post_columns:
            print(f"  - {col['name']}: {col['type']}")
        
        # Show Page table structure
        print("\n📄 Page Table:")
        page_columns = inspector.get_columns('page')
        for col in page_columns:
            print(f"  - {col['name']}: {col['type']}")
        
        # Show Category table structure
        print("\n🏷️  Category Table:")
        category_columns = inspector.get_columns('category')
        for col in category_columns:
            print(f"  - {col['name']}: {col['type']}")

def main():
    print("🚀 Anipreneur Database Migration Tool")
    print("=" * 50)
    
    # Check if database exists
    if not os.path.exists('instance/anipreneur.db'):
        print("❌ Database not found. Please run the app first to create the database.")
        sys.exit(1)
    
    # Show current structure
    show_database_info()
    
    # Run migration
    if add_seo_columns():
        # Verify migration
        if verify_migration():
            print("\n🎉 Migration completed successfully!")
            print("You can now run the SEO migration script to populate the new fields.")
        else:
            print("\n⚠️  Migration completed but verification failed.")
            sys.exit(1)
    else:
        print("\n❌ Migration failed!")
        sys.exit(1)

if __name__ == "__main__":
    main() 