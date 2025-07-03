from flask import Flask, render_template
import os

app = Flask(__name__)

# Production configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-this')
app.config['FLASK_ENV'] = os.environ.get('FLASK_ENV', 'production')
app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/detail')
def detail():
    return render_template('detail-page.html')

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    # For development only
    app.run(debug=app.config['DEBUG'], host='0.0.0.0', port=5000) 