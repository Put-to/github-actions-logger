from flask import render_template
from app import create_app

app = create_app()

@app.route('/', methods=['GET'])
def get_app():
    return render_template('index.html')

if __name__ == '__main__': 
    app.run(debug=True)
