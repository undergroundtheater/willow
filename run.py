import os
from willow.app import create_app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5002))
    app.run('0.0.0.0', port=port, debug=True)
