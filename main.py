import classes as cl
from flask import Flask, render_template
from flask_restful import Api


app = Flask(__name__, template_folder='templates')
api = Api(app)


@app.route('/')
def index():
    # html start template
    return render_template('index.html')


api.add_resource(cl.PeopleCounter1, '/1')
api.add_resource(cl.PeopleCounter2, '/2/')
api.add_resource(cl.PeopleCounter3, '/upload')


if __name__ == '__main__':
    app.run(debug=True)
