#!/usr/bin/env python3
"""
IP Debugging Script for cPanel Environments

This script helps identify the real client IP address when running on cPanel.
"""

from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/debug-ip')
def debug_ip():
    """Debug endpoint to show all IP-related information"""
    
    # Get various IP sources
    remote_addr = request.remote_addr
    x_forwarded_for = request.headers.get('X-Forwarded-For', 'Not set')
    x_real_ip = request.headers.get('X-Real-IP', 'Not set')
    x_client_ip = request.headers.get('X-Client-IP', 'Not set')
    cf_connecting_ip = request.headers.get('CF-Connecting-IP', 'Not set')
    
    # Get all headers for debugging
    all_headers = dict(request.headers)
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>IP Debug Information</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .section {{ margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }}
            .ip {{ font-family: monospace; background: #f5f5f5; padding: 5px; margin: 5px 0; }}
            .header {{ background: #e9ecef; padding: 10px; margin: 5px 0; border-radius: 3px; }}
            .warning {{ color: #856404; background: #fff3cd; padding: 10px; border-radius: 5px; }}
        </style>
    </head>
    <body>
        <h1>🔍 IP Debug Information</h1>
        
        <div class="section">
            <h2>IP Address Sources</h2>
            <p><strong>request.remote_addr:</strong> <span class="ip">{remote_addr}</span></p>
            <p><strong>X-Forwarded-For:</strong> <span class="ip">{x_forwarded_for}</span></p>
            <p><strong>X-Real-IP:</strong> <span class="ip">{x_real_ip}</span></p>
            <p><strong>X-Client-IP:</strong> <span class="ip">{x_client_ip}</span></p>
            <p><strong>CF-Connecting-IP:</strong> <span class="ip">{cf_connecting_ip}</span></p>
        </div>
        
        <div class="section">
            <h2>Recommended IP to Use</h2>
    """
    
    # Determine the best IP to use
    best_ip = remote_addr
    if x_forwarded_for != 'Not set':
        best_ip = x_forwarded_for.split(',')[0].strip()
    elif x_real_ip != 'Not set':
        best_ip = x_real_ip
    elif x_client_ip != 'Not set':
        best_ip = x_client_ip
    elif cf_connecting_ip != 'Not set':
        best_ip = cf_connecting_ip
    
    html += f"""
            <p><strong>Recommended IP for whitelist:</strong> <span class="ip">{best_ip}</span></p>
            <p class="warning">⚠️ Use this IP address in your ADMIN_ALLOWED_IPS environment variable</p>
        </div>
        
        <div class="section">
            <h2>All Request Headers</h2>
    """
    
    for header, value in all_headers.items():
        html += f'<div class="header"><strong>{header}:</strong> {value}</div>'
    
    html += """
        </div>
        
        <div class="section">
            <h2>Next Steps</h2>
            <ol>
                <li>Copy the "Recommended IP" above</li>
                <li>Add it to your ADMIN_ALLOWED_IPS environment variable</li>
                <li>Restart your Flask application</li>
                <li>Test admin access again</li>
            </ol>
        </div>
    </body>
    </html>
    """
    
    return html

@app.route('/')
def home():
    return """
    <h1>IP Debug Tool</h1>
    <p>Visit <a href="/debug-ip">/debug-ip</a> to see your IP information.</p>
    """

if __name__ == '__main__':
    print("🔍 IP Debug Server Starting...")
    print("Visit http://localhost:5000/debug-ip to see your IP information")
    app.run(debug=True, host='0.0.0.0', port=5000) 