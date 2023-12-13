from ib_aitool import app
from flask import Blueprint,render_template
from ib_aitool.admin.decorators import has_permission
from decorators import xr_login_required,current_user

dashboard_blueprint = Blueprint('dashboard',__name__)
@dashboard_blueprint.route('/',endpoint='index')
@xr_login_required
@has_permission('Dashboard')
def index():
	current_user_obj = current_user()
	return render_template('admin/dashboard/index.html',current_user=current_user_obj)


app.register_blueprint(dashboard_blueprint,url_prefix='/admin/dashboard')