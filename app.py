from ib_tool import app
from flask import render_template
from application_list import application_list
from flask_login import login_required


@app.route('/')
@login_required
def home_page():
    return render_template('home.html', application_list=application_list)


if __name__ == '__main__':
    app.run(debug=True)
