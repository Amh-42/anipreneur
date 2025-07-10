from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import os
from models import db, User, Post, Page, Category
from datetime import datetime
import re
from functools import wraps

app = Flask(__name__)

# Production configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-this')
app.config['FLASK_ENV'] = os.environ.get('FLASK_ENV', 'production')
app.config['DEBUG'] = True



# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///anipreneur.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin_login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def slugify(text):
    """Convert text to URL-friendly slug"""
    # Strip HTML tags first
    text = re.sub(r'<[^>]+>', '', text)
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')

# Public routes
@app.route('/')
def index():
    posts = Post.query.filter_by(status='published').order_by(Post.created_at.desc()).limit(3).all()
    return render_template('index.html', posts=posts)

@app.route('/links')
def social_links():
    return render_template('social_links.html')

@app.route('/courses')
def courses():
    return render_template('courses.html')

@app.route('/coming-soon')
def coming_soon():
    return render_template('coming_soon.html')

@app.route('/blog')
def blog():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(status='published').order_by(Post.created_at.desc()).paginate(
        page=page, per_page=6, error_out=False)
    return render_template('blog.html', posts=posts)

@app.route('/blog/<slug>')
def post_detail(slug):
    post = Post.query.filter_by(slug=slug, status='published').first_or_404()
    return render_template('post_detail.html', post=post)

@app.route('/detail')
def detail():
    return render_template('detail-page.html')

# Admin routes
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            if not user.is_approved:
                flash('Your account is pending approval from the main admin.', 'error')
                return render_template('admin/login.html')
            
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('admin/login.html')

@app.route('/admin/register', methods=['GET', 'POST'])
def admin_register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validation
        if not username or not email or not password:
            flash('All fields are required.', 'error')
            return render_template('admin/register.html')
        
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('admin/register.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'error')
            return render_template('admin/register.html')
        
        # Check if user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists.', 'error')
            return render_template('admin/register.html')
        
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            flash('Email already exists.', 'error')
            return render_template('admin/register.html')
        
        # Create new user (not approved yet)
        new_user = User(
            username=username,
            email=email,
            is_admin=True,
            is_approved=False
        )
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please wait for approval from the main admin.', 'success')
        return redirect(url_for('admin_login'))
    
    return render_template('admin/register.html')

@app.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('admin_login'))

@app.route('/admin')
@login_required
def admin_dashboard():
    post_count = Post.query.count()
    page_count = Page.query.count()
    user_count = User.query.count()
    recent_posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html', 
                         post_count=post_count, 
                         page_count=page_count, 
                         user_count=user_count,
                         recent_posts=recent_posts)

# Admin management routes
@app.route('/admin/users')
@login_required
def admin_users():
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('admin_dashboard'))
    
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin/users.html', users=users)

@app.route('/admin/users/<int:user_id>/approve', methods=['POST'])
@login_required
def approve_user(user_id):
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('admin_users'))
    
    user = User.query.get_or_404(user_id)
    user.is_approved = True
    db.session.commit()
    
    flash(f'User {user.username} has been approved.', 'success')
    return redirect(url_for('admin_users'))

@app.route('/admin/users/<int:user_id>/reject', methods=['POST'])
@login_required
def reject_user(user_id):
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('admin_users'))
    
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    
    flash(f'User {user.username} has been rejected and deleted.', 'success')
    return redirect(url_for('admin_users'))

# Post management
@app.route('/admin/posts')
@login_required
def admin_posts():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('admin/posts.html', posts=posts)

@app.route('/admin/posts/new', methods=['GET', 'POST'])
@login_required
def admin_new_post():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        excerpt = request.form.get('excerpt')
        featured_image = request.form.get('featured_image')
        status = request.form.get('status', 'draft')
        
        post = Post(
            title=title,
            slug=slugify(title),
            content=content,
            excerpt=excerpt,
            featured_image=featured_image,
            status=status,
            author_id=current_user.id
        )
        
        db.session.add(post)
        db.session.commit()
        flash('Post created successfully!', 'success')
        return redirect(url_for('admin_posts'))
    
    return render_template('admin/post_form.html')

@app.route('/admin/posts/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def admin_edit_post(id):
    post = Post.query.get_or_404(id)
    
    if request.method == 'POST':
        post.title = request.form.get('title')
        post.slug = slugify(request.form.get('title'))
        post.content = request.form.get('content')
        post.excerpt = request.form.get('excerpt')
        post.featured_image = request.form.get('featured_image')
        post.status = request.form.get('status', 'draft')
        post.updated_at = datetime.utcnow()
        
        db.session.commit()
        flash('Post updated successfully!', 'success')
        return redirect(url_for('admin_posts'))
    
    return render_template('admin/post_form.html', post=post)

@app.route('/admin/posts/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def admin_delete_post(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted successfully!', 'success')
    return redirect(url_for('admin_posts'))

# Page management
@app.route('/admin/pages')
@login_required
def admin_pages():
    pages = Page.query.order_by(Page.created_at.desc()).all()
    return render_template('admin/pages.html', pages=pages)

@app.route('/admin/pages/new', methods=['GET', 'POST'])
@login_required
def admin_new_page():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        status = request.form.get('status', 'draft')
        
        page = Page(
            title=title,
            slug=slugify(title),
            content=content,
            status=status
        )
        
        db.session.add(page)
        db.session.commit()
        flash('Page created successfully!', 'success')
        return redirect(url_for('admin_pages'))
    
    return render_template('admin/page_form.html')

@app.route('/admin/pages/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def admin_edit_page(id):
    page = Page.query.get_or_404(id)
    
    if request.method == 'POST':
        page.title = request.form.get('title')
        page.slug = slugify(request.form.get('title'))
        page.content = request.form.get('content')
        page.status = request.form.get('status', 'draft')
        page.updated_at = datetime.utcnow()
        
        db.session.commit()
        flash('Page updated successfully!', 'success')
        return redirect(url_for('admin_pages'))
    
    return render_template('admin/page_form.html', page=page)

@app.route('/admin/pages/<int:id>/delete', methods=['POST'])
@login_required
def admin_delete_page(id):
    page = Page.query.get_or_404(id)
    db.session.delete(page)
    db.session.commit()
    flash('Page deleted successfully!', 'success')
    return redirect(url_for('admin_pages'))

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

@app.errorhandler(403)
def forbidden_error(error):
    return render_template('403.html'), 403

# Database initialization
def init_db():
    with app.app_context():
        db.create_all()
        
        # Create admin user if it doesn't exist
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@anipreneur.com',
                is_admin=True,
                is_approved=True  # Main admin is automatically approved
            )
            admin.set_password('admin123')  # Change this password!
            db.session.add(admin)
            db.session.commit()
            print("Admin user created: username=admin, password=admin123")

if __name__ == '__main__':
    init_db()
    app.run(debug=app.config['DEBUG'], host='0.0.0.0', port=5050) 