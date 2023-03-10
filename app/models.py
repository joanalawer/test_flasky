# ...

from werkzeug.security import generate_password_hash, check_password_hash
from . import login_manager
from flask.ext.login import login_required

class User(UserMixin, db.Model):
# ...
	# user loader callback function
	@login_manager.user_loader
	def load_user(user_id):
		return User.query.get(int(user_id))

	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(64), unique=True, index=True)
	username = db.Column(db.String(64), unique=True, index=True)
	password_hash = db.Column(db.String(128))
	role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

	def __repr__(self):
		return '<User %r>' % self.username
	
	password_hash = db.Column(db.String(128))
	
	@app.route('/secret')
	@login_required
	def secret():
		return 'Only authenticated users are allowed!'

	@property
	def password(self):
		raise AttributeError('password is not a readable attribute')
		
	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)
		
	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)
