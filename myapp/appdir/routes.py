from flask import render_template, flash, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from appdir import app, db
from appdir.forms import LoginForm, SignupForm, ProfileForm, PostForm
from appdir.models import User,Post, Profile
from appdir.config import Config
from appdir import moment
from datetime import datetime

import os

@app.route('/')
@app.route('/index')
def index():
	prev_posts = Post.query.filter().order_by(db.desc(Post.timestamp)).all()
	list=[]
	for post in prev_posts:
		user=User.query.filter(User.id == post.user_id).first()
		name=user.username
		dic=[post,name]
		print(dic)
		list.append(dic)
	username = session.get("USERNAME")
	user=User.query.filter(User.username == username).first()
	print(list)
	profile=User.profile
	return render_template('index.html', title='Home', dict=list, profile=profile, user=user,current_time=datetime.utcnow())


@app.route('/doc')
def doc():
	form = PostForm()
	user=session.get("USERNAME")
	if not user is None:
		if form.validate_on_submit():
			body = form.postbody.data
			user_in_db = User.query.filter(User.username == session.get("USERNAME")).first()
			post = Post(body=body, author=user_in_db)
			db.session.add(post)
			db.session.commit()
			return redirect(url_for('post'))
		else:
			user_in_db = User.query.filter(User.username == session.get("USERNAME")).first()
			prev_posts = Post.query.filter(Post.user_id == user_in_db.id).all()
			print("Checking for user: {} with id: {}".format(user_in_db.username, user_in_db.id))
			return render_template('doc.html', title='User Posts',user=user_in_db, prev_posts=prev_posts, form=form)
	else:
		flash("User needs to either login or signup first")
		return redirect(url_for('login'))


@app.errorhandler(404)
def error(error):
        return render_template('404.html'), 404

@app.errorhandler(500)
def exception(error):
        return render_template('404.html'), 500







# reference 1: part of below code from the assignment of week 13
@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user_in_db = User.query.filter(User.username == form.username.data).first()
		if not user_in_db:
			flash('No user found with username: {}'.format(form.username.data))
			return redirect(url_for('login'))
		if (check_password_hash(user_in_db.password_hash, form.password.data)):
			flash('Login success!')
			session["USERNAME"] = user_in_db.username
			return redirect(url_for('doc'))
		flash('Incorrect Password')
		return redirect(url_for('login'))
	return render_template('login.html', title='Sign In', form=form)
	
@app.route('/signup', methods=['GET', 'POST'])
def signup():
	form = SignupForm()
	if form.validate_on_submit():
		if form.password.data != form.password2.data:
			flash('Passwords do not match!')
			return redirect(url_for('signup'))
		passw_hash = generate_password_hash(form.password.data)
		user = User(username=form.username.data, email=form.email.data, password_hash=passw_hash)
		db.session.add(user)
		db.session.commit()
		flash('User registered with username:{}'.format(form.username.data))
		session["USERNAME"] = user.username
		return redirect(url_for('doc'))
	return render_template('signup.html', title='Register a new user', form=form)
# endReference


@app.route('/profile', methods=['GET', 'POST'])
def profile():
	form = ProfileForm()
	if not session.get("USERNAME") is None:
		user = User.query.filter(User.username == session.get("USERNAME")).first()
		if form.validate_on_submit():
			user_in_db = User.query.filter(User.username == session.get("USERNAME")).first()
			stored_profile = Profile.query.filter(Profile.user == user_in_db).first()
			if not stored_profile:
				profile = Profile(dob=form.dob.data, gender=form.gender.data, user=user_in_db)
				db.session.add(profile)
			else:
				stored_profile.dob = form.dob.data
				stored_profile.gender = form.gender.data
			db.session.commit()
			return redirect(url_for('index'))
		else:

			user_in_db = User.query.filter(User.username == session.get("USERNAME")).first()
			stored_profile = Profile.query.filter(Profile.user == user_in_db).first()
			if not stored_profile:
				return render_template('profile.html', title='Add your profile',user=user_in_db,form=form)
			else:
				form.dob.data = stored_profile.dob
				form.gender.data = stored_profile.gender
				return render_template('profile.html', title='Modify your profile',user=user_in_db, form=form)

	else:
		flash("User needs to either login or signup first")
		return redirect(url_for('login'))
		

		
@app.route('/post', methods=['GET', 'POST'])
def post():
	form = PostForm()
	if not session.get("USERNAME") is None:
		if form.validate_on_submit():
			flash("Commited")
			body = form.postbody.data
			title = form.postTitle.data
			user_in_db = User.query.filter(User.username == session.get("USERNAME")).first()
			post = Post(body=body, title=title, author = user_in_db)
			db.session.add(post)
			db.session.commit()
			return redirect(url_for('index'))
		else:
			user_in_db = User.query.filter(User.username == session.get("USERNAME")).first()
			prev_posts = Post.query.filter(Post.user_id == user_in_db.id).all()
			flash("Checking for user: {} with id: {}".format(user_in_db.username, user_in_db.id))
			return render_template('post.html', title='User Posts', prev_posts=prev_posts,user=user_in_db,form=form)
	else:
		flash("User needs to either login or signup first")
		return redirect(url_for('login'))
		
@app.route('/logout')
def logout():
	session.pop("USERNAME", None)
	return redirect(url_for('login'))