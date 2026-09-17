from flask import Flask
from .config import Config
from .extensions import db, jwt

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    jwt.init_app(app)

    from .routes.health import health_bp
    from .routes.auth import auth_bp
    from .routes.products import products_bp
    from .routes.orders import orders_bp
    from .routes.payments import payments_bp

    app.register_blueprint(health_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(products_bp, url_prefix="/products")
    app.register_blueprint(orders_bp, url_prefix="/orders")
    app.register_blueprint(payments_bp, url_prefix="/payments")

    with app.app_context():
        db.create_all()

    return app
