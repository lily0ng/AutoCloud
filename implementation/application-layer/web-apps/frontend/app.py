#!/usr/bin/env python3
"""
SaaS Web Application - Frontend Service
Application Layer Implementation
"""

from flask import Flask, render_template_string, request, jsonify, session
import requests
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'

# Backend API endpoints
API_GATEWAY = "http://api-gateway:8000"
SERVICE_A_URL = "http://service-a:8080"
SERVICE_B_URL = "http://service-b:8081"

@app.route('/')
def index():
    """Main dashboard"""
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>AutoCloud SaaS Platform</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
            .container { max-width: 1200px; margin: 0 auto; }
            .header { background: #2c3e50; color: white; padding: 20px; border-radius: 5px; }
            .card { background: white; padding: 20px; margin: 10px 0; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            .status { display: inline-block; padding: 5px 10px; border-radius: 3px; }
            .status.healthy { background: #2ecc71; color: white; }
            .status.unhealthy { background: #e74c3c; color: white; }
            button { background: #3498db; color: white; border: none; padding: 10px 20px; border-radius: 3px; cursor: pointer; }
            button:hover { background: #2980b9; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🚀 AutoCloud SaaS Platform</h1>
                <p>Multi-Layer Cloud Infrastructure Management</p>
            </div>
            
            <div class="card">
                <h2>Service Status</h2>
                <div id="status">Loading...</div>
                <button onclick="checkStatus()">Refresh Status</button>
            </div>
            
            <div class="card">
                <h2>Quick Actions</h2>
                <button onclick="deployApp()">Deploy Application</button>
                <button onclick="scaleService()">Scale Service</button>
                <button onclick="viewMetrics()">View Metrics</button>
            </div>
            
            <div class="card">
                <h2>Recent Activity</h2>
                <div id="activity">No recent activity</div>
            </div>
        </div>
        
        <script>
            async function checkStatus() {
                const response = await fetch('/api/status');
                const data = await response.json();
                document.getElementById('status').innerHTML = formatStatus(data);
            }
            
            function formatStatus(data) {
                return Object.entries(data.services).map(([name, status]) => 
                    `<div><strong>${name}:</strong> <span class="status ${status}">${status}</span></div>`
                ).join('');
            }
            
            async function deployApp() {
                alert('Deploying application...');
                const response = await fetch('/api/deploy', { method: 'POST' });
                const data = await response.json();
                alert(data.message);
            }
            
            function scaleService() { alert('Scaling service...'); }
            function viewMetrics() { window.location.href = '/metrics'; }
            
            checkStatus();
            setInterval(checkStatus, 30000);
        </script>
    </body>
    </html>
    ''')

@app.route('/api/status')
def api_status():
    """Get service status"""
    try:
        services = {
            'service-a': check_service(SERVICE_A_URL),
            'service-b': check_service(SERVICE_B_URL),
            'database': 'healthy',
            'cache': 'healthy',
            'queue': 'healthy'
        }
        return jsonify({'services': services, 'timestamp': datetime.now().isoformat()})
    except Exception as e:
        logger.error(f"Status check failed: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/deploy', methods=['POST'])
def api_deploy():
    """Deploy application"""
    return jsonify({
        'message': 'Deployment initiated',
        'deployment_id': 'DEP-' + datetime.now().strftime('%Y%m%d%H%M%S')
    })

@app.route('/metrics')
def metrics():
    """Metrics dashboard"""
    return render_template_string('''
    <html>
    <head><title>Metrics Dashboard</title></head>
    <body>
        <h1>Metrics Dashboard</h1>
        <iframe src="http://grafana:3000" width="100%" height="800px"></iframe>
    </body>
    </html>
    ''')

def check_service(url):
    """Check if service is healthy"""
    try:
        response = requests.get(f"{url}/health", timeout=2)
        return 'healthy' if response.status_code == 200 else 'unhealthy'
    except:
        return 'unhealthy'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
