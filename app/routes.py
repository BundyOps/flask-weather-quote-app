# app/routes.py
from flask import request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils import get_weather, get_random_quote
from app.models import User
import time

def register_routes(app):
    """Register all routes with the app"""
    
    @app.before_request
    def log_request_info():
        current_app.logger.info(f"Request: {request.method} {request.url}")
    
    @app.after_request
    def log_response_info(response):
        current_app.logger.info(f"Response: {response.status_code} - {request.method} {request.url}")
        return response
    
    # Public routes (no authentication)
    
    @app.route('/my-ip', methods=['GET'])
    def get_my_ip():
        """Return the client's IP address (public)"""
        ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        if ip and ',' in ip:
            ip = ip.split(',')[0].strip()
        
        return jsonify({
            'ip': ip,
            'timestamp': time.time()
        })
    
    @app.route('/weather', methods=['GET'])
    def weather():
        """Return weather information (public)"""
        location = request.args.get('location')
        
        if not location:
            return jsonify({'error': 'Location parameter is required'}), 400
        
        weather_data = get_weather(location)
        
        if 'error' in weather_data:
            return jsonify(weather_data), 404
        
        return jsonify(weather_data)
    
    @app.route('/quote', methods=['GET'])
    def quote():
        """Return a random quote (public)"""
        quote_data = get_random_quote()
        return jsonify(quote_data)
    
    @app.route('/health', methods=['GET'])
    def health_check():
        """Health check endpoint (public)"""
        return jsonify({'status': 'healthy', 'timestamp': time.time()})
    
    # Protected routes (require authentication)
    
    @app.route('/api/protected/profile', methods=['GET'])
    @jwt_required()
    def get_profile():
        """Get current user profile (protected)"""
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify(user.to_dict()), 200
    
    @app.route('/api/protected/weather', methods=['GET'])
    @jwt_required()
    def protected_weather():
        """Get weather with user info (protected)"""
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        location = request.args.get('location')
        if not location:
            return jsonify({'error': 'Location parameter is required'}), 400
        
        weather_data = get_weather(location)
        
        if 'error' in weather_data:
            return jsonify(weather_data), 404
        
        # Add who requested it
        weather_data['requested_by'] = user.username
        
        return jsonify(weather_data)
    
    
    @app.route('/favicon.ico')
    def favicon():
        """Serve favicon.ico"""
        return '', 204
