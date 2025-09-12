from app_init import create_app


if __name__ == "__main__":
    app = create_app()
    
    # Running the app on host '0.0.0.0' makes it accessible
    # from outside the Docker container.
    app.run(host='0.0.0.0', port=5000, debug=True)


