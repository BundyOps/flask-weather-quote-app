# app/auth.py
from flask import request, jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity
)
from app.models import db, User

def register_auth_routes(app):
    """Register all authentication routes"""
    
    @app.route('/api/auth/register', methods=['POST'])
    def register():
        """Register a new user"""
        try:
            data = request.get_json()
            
            if not data:
                return jsonify({'error': 'No data provided'}), 400
            
            required_fields = ['username', 'email', 'password']
            for field in required_fields:
                if field not in data:
                    return jsonify({'error': f'Missing field: {field}'}), 400
            
            if User.query.filter_by(username=data['username']).first():
                return jsonify({'error': 'Username already taken'}), 409
            
            if User.query.filter_by(email=data['email']).first():
                return jsonify({'error': 'Email already registered'}), 409
            
            user = User(
                username=data['username'],
                email=data['email']
            )
            user.password = data['password']
            db.session.add(user)
            db.session.commit()
            
            access_token = create_access_token(identity=str(user.id))
            refresh_token = create_refresh_token(identity=str(user.id))
            
            return jsonify({
                'message': 'User created successfully',
                'user': user.to_dict(),
                'access_token': access_token,
                'refresh_token': refresh_token
            }), 201
            
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Registration error: {str(e)}")
            return jsonify({'error': 'Registration failed'}), 500
    
    @app.route('/api/auth/login', methods=['POST'])
    def login():
        """Login user and return tokens"""
        try:
            data = request.get_json()
            
            if not data:
                return jsonify({'error': 'No data provided'}), 400
            
            identifier = data.get('username') or data.get('email')
            password = data.get('password')
            
            if not identifier or not password:
                return jsonify({'error': 'Username/email and password required'}), 400
            
            user = User.query.filter(
                (User.username == identifier) | (User.email == identifier)
            ).first()
            
            if not user or not user.is_active:
                return jsonify({'error': 'Invalid credentials'}), 401
            
            if not user.check_password(password):
                return jsonify({'error': 'Invalid credentials'}), 401
            
            access_token = create_access_token(identity=str(user.id))
            refresh_token = create_refresh_token(identity=str(user.id))
            
            return jsonify({
                'message': 'Login successful',
                'user': user.to_dict(),
                'access_token': access_token,
                'refresh_token': refresh_token
            }), 200
            
        except Exception as e:
            app.logger.error(f"Login error: {str(e)}")
            return jsonify({'error': 'Login failed'}), 500
    
    @app.route('/api/auth/refresh', methods=['POST'])
    @jwt_required(refresh=True)
    def refresh():
        """Get new access token using refresh token"""
        try:
            user_id = get_jwt_identity()
            user = User.query.get(int(user_id))
            
            if not user or not user.is_active:
                return jsonify({'error': 'User not found or inactive'}), 401
            
            new_access_token = create_access_token(identity=str(user.id))
            
            return jsonify({
                'access_token': new_access_token
            }), 200
            
        except Exception as e:
            app.logger.error(f"Refresh error: {str(e)}")
            return jsonify({'error': 'Refresh failed'}), 500
    
    @app.route('/api/auth/me', methods=['GET'])
    @jwt_required()
    def get_current_user():
        """Get current user info"""
        try:
            user_id = get_jwt_identity()
            user = User.query.get(int(user_id))
            
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            return jsonify(user.to_dict()), 200
            
        except Exception as e:
            app.logger.error(f"Get user error: {str(e)}")
            return jsonify({'error': 'Failed to get user'}), 500
