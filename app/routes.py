# app/routes.py
from flask import request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils import get_weather, get_random_quote
from app.models import User
from app.decorators.log_decorator import log_route
from app.logger import get_logger, get_business_logger
import time

def register_routes(app):
    """Register all routes with the app"""
    
    # === PUBLIC ROUTES ===
    
    @app.route('/my-ip', methods=['GET'])
    @log_route(
        level='INFO',
        include_request_body=False,
        event_type='IP_LOOKUP'
    )
    def get_my_ip():
        """Return the client's IP address (public)"""
        ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        if ip and ',' in ip:
            ip = ip.split(',')[0].strip()
        
        return jsonify({
            'ip': ip,
            'timestamp': time.time()
        })
    
    @app.route('/health', methods=['GET'])
    @log_route(
        level='INFO',
        include_request_body=False,
        event_type='HEALTH_CHECK'
    )
    def health_check():
        """Health check endpoint (public)"""
        # Check database connection
        try:
            from app.models import db
            db.session.execute('SELECT 1')
            status = 'healthy'
            db_status = 'connected'
        except Exception as e:
            status = 'unhealthy'
            db_status = 'disconnected'
            current_app.logger.error(f"Health check failed: {e}")
        
        return jsonify({
            'status': status,
            'database': db_status,
            'timestamp': time.time()
        }), 200 if status == 'healthy' else 503
    
    @app.route('/favicon.ico')
    @log_route(level='DEBUG', include_request_body=False)
    def favicon():
        """Serve favicon.ico"""
        return '', 204
    
    # === PROTECTED ROUTES ===
    
    @app.route('/api/weather', methods=['GET'])
    @log_route(
        level='INFO',
        include_request_body=False,
        log_to_business=True,
        event_type='WEATHER_REQUEST'
    )
    @jwt_required()
    def protected_weather():
        """Get weather with user info (protected)"""
        business_logger = get_business_logger()
        
        try:
            user_id = get_jwt_identity()
            user = User.query.get(int(user_id))
            
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            # Set user context for logging
            request.user_id = user.id
            request.username = user.username
            
            location = request.args.get('location')
            if not location:
                return jsonify({'error': 'Location parameter is required'}), 400
            
            # Log the request
            business_logger.info({
                'event': 'WEATHER_REQUEST_START',
                'user_id': user.id,
                'username': user.username,
                'location': location,
                'request_id': getattr(request, 'request_id', None)
            })
            
            start_time = time.time()
            weather_data = get_weather(location)
            response_time = round((time.time() - start_time) * 1000, 2)
            
            if 'error' in weather_data:
                business_logger.warning({
                    'event': 'WEATHER_REQUEST_FAILED',
                    'user_id': user.id,
                    'username': user.username,
                    'location': location,
                    'error': weather_data['error'],
                    'response_time_ms': response_time,
                    'request_id': getattr(request, 'request_id', None)
                })
                return jsonify(weather_data), 404
            
            # Add who requested it
            weather_data['requested_by'] = user.username
            
            business_logger.info({
                'event': 'WEATHER_REQUEST_SUCCESS',
                'user_id': user.id,
                'username': user.username,
                'location': location,
                'temperature': weather_data.get('temperature'),
                'response_time_ms': response_time,
                'request_id': getattr(request, 'request_id', None)
            })
            
            return jsonify(weather_data), 200
            
        except Exception as e:
            current_app.logger.error(f"Weather error: {str(e)}")
            return jsonify({'error': 'Failed to get weather'}), 500
    
    @app.route('/api/quotes', methods=['GET'])
    @log_route(
        level='INFO',
        include_request_body=False,
        log_to_business=True,
        event_type='QUOTE_REQUEST'
    )
    @jwt_required()
    def protected_quote():
        """Return a random quote (protected)"""
        business_logger = get_business_logger()
        
        try:
            user_id = get_jwt_identity()
            user = User.query.get(int(user_id))
            
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            # Set user context for logging
            request.user_id = user.id
            request.username = user.username
            
            quote_data = get_random_quote()
            
            business_logger.info({
                'event': 'QUOTE_REQUEST_SUCCESS',
                'user_id': user.id,
                'username': user.username,
                'author': quote_data.get('author'),
                'request_id': getattr(request, 'request_id', None)
            })
            
            return jsonify(quote_data)
            
        except Exception as e:
            current_app.logger.error(f"Quote error: {str(e)}")
            return jsonify({'error': 'Failed to get quote'}), 500
    
    # === CRASH ROUTE (debug only) ===
    
    if app.debug:
        @app.route('/crash')
        @log_route(level='ERROR', include_request_body=False)
        def crash():
            """Intentionally crash to test debugger"""
            result = 1 / 0
            return jsonify({'result': result})