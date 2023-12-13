from ib_tool import app
from flask import render_template,redirect
from application_list import application_list
from decorators import xr_login_required


@app.route('/',endpoint='home_page')
@xr_login_required
def home_page():
    # return render_template('home.html', application_list=application_list)
    return redirect("/smart-interview-assessment")

if __name__ == '__main__':
    app.run(debug=True)
