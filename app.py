from flask_blog_app import create_app

app = create_app()

if __name__ == '__main__':
    # APP.run(host='0.0.0.0', port=5000, debug=True)
    app.run(debug=False)
