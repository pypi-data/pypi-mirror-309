from t1cicd.cicd.server.factory import create_app


def main():
    # Pass the desired configuration when creating the app
    app = create_app(config_name="DevelopmentConfig")
    app.run(debug=False)
