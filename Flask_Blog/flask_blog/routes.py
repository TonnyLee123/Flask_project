import os
import secrets
# from PIL import Image(for resizing pic)
from flask import render_template, url_for, flash, redirect, request, abort
from flask_blog import app, db, bcrypt
from flask_blog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, GoalForm, RecordForm, TestForm
from flask_blog.models import User, Post, Goal
from flask_login import login_user, current_user, logout_user, login_required
import re

@app.route("/")
@app.route("/home")
def home():
    page = request.args.get('page', 1, type=int)#url設名為page的variable 從url_bar取的page的值
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=5, page=page)# 新文排到舊文，然後再分頁
    return render_template('home.html', posts=posts)


@app.route("/about", methods=['GET', 'POST'])
def about():
    form = TestForm()
    s="F"
    if form.validate_on_submit():
        s="T"
    return render_template('about.html', form=form, s=s)


@app.route("/register", methods=['GET', 'POST'])
def register():
    # 如果已經登入了，又嘗試進入註冊頁面。則會重新導向到主頁
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('創建成功!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('無法登入，請確認使用者名稱及密碼', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8) #產生8bytes亂數
    #grab file extention(123.jpg -> 123, .jpg)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    form_picture.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data: #如果有更新頭像
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        #current_user.email = form.email.data
        db.session.commit()
        flash('更新成功!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        #form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id) # give me the post with this ID, if it doesn't exist then return a 404(page doesn't exist)
    return render_template('post.html', title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user: # 如果不是文章本人進行修改
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data 
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET': # 顯示原有的title
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))


@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)


@app.route("/goal/new", methods=['GET', 'POST'])
# @login_required
def new_goal():
    form = GoalForm()
    if form.validate_on_submit():
        goal = Goal(object=form.object.data, 
                    key_result=form.key_result.data, amount=form.amount.data,
                    key_result2=form.key_result2.data, amount2=form.amount2.data,
                    key_result3=form.key_result3.data, amount3=form.amount3.data,
                    note=form.note.data, 
                    author=current_user)
        db.session.add(goal)
        db.session.commit()
        flash('建立成功', 'success')
        return redirect(url_for('home'))
    return render_template('create_goal.html', title='New Goal', form=form, legend='New Goal')
"""
@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_goal(goal_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user: # 如果不是文章本人進行修改
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data 
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET': # 顯示原有的title
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')
"""

# single goal
@app.route("/goal/<int:goal_id>", methods=['GET', 'POST'])
@login_required
def goal(goal_id):
    form=RecordForm()
    goal = Goal.query.get_or_404(goal_id)
    if form.validate_on_submit():
        goal.mon=form.mon.data
        goal.tue=form.tue.data
        goal.wed=form.wed.data
        goal.thu=form.thu.data
        goal.fri=form.fri.data
        goal.sat=form.sat.data
        goal.sun=form.sun.data
        goal.state=form.state.data
        if goal.key_result2:
            goal.mon2=form.mon2.data
            goal.tue2=form.tue2.data
            goal.wed2=form.wed2.data
            goal.thu2=form.thu2.data
            goal.fri2=form.fri2.data
            goal.sat2=form.sat2.data
            goal.sun2=form.sun2.data
            goal.state=form.state.data
            if goal.key_result3:
                goal.mon3=form.mon3.data
                goal.tue3=form.tue3.data
                goal.wed3=form.wed3.data
                goal.thu3=form.thu3.data
                goal.fri3=form.fri3.data
                goal.sat3=form.sat3.data
                goal.sun3=form.sun3.data
                goal.state=form.state.data
                db.session.commit()
            else: 
                db.session.commit()
                flash('紀錄成功!', 'success')
        else: db.session.commit()
    elif request.method == 'GET': # 顯示之前記錄好的data
        form.mon.data = goal.mon
        form.tue.data = goal.tue
        form.wed.data = goal.wed
        form.thu.data = goal.thu
        form.fri.data = goal.fri
        form.sat.data = goal.sat
        form.sun.data = goal.sun
        if goal.key_result2:
            form.mon2.data = goal.mon2
            form.tue2.data = goal.tue2
            form.wed2.data = goal.wed2
            form.thu2.data = goal.thu2
            form.fri2.data = goal.fri2
            form.sat2.data = goal.sat2
            form.sun2.data = goal.sun2
        if goal.key_result3:
            form.mon3.data = goal.mon3
            form.tue3.data = goal.tue3
            form.wed3.data = goal.wed3
            form.thu3.data = goal.thu3
            form.fri3.data = goal.fri3
            form.sat3.data = goal.sat3
            form.sun3.data = goal.sun3

    # progress (key result1)
    if goal.key_result:
        current=int(form.mon.data)+int(form.tue.data)+int(form.wed.data)+int(form.thu.data)+int(form.fri.data)+int(form.sat.data)+int(form.sun.data)
        # 把3km變成3(key result1)
        total = goal.amount # 3km
        formate = re.compile("([+-]?[0-9]+\.?[0-9]*)([a-zA-Z]+)")
        res = formate.match(total).groups()
        num =  float(res[0]) # no unit -> 3

        if current<num:
            goal.progress = str(round(current/num, 1)*100) + "%"
            db.session.commit()
        else:
            goal.progress = "100%"

    # progress (key result2)
    if goal.key_result2:
        current2=float(form.mon2.data)+float(form.tue2.data)+float(form.wed2.data)+float(form.thu2.data)+float(form.fri2.data)+float(form.sat2.data)+float(form.sun2.data)
        total2 = goal.amount2 # 3kmfloat
        formate2 = re.compile("([+-]?[0-9]+\.?[0-9]*)([a-zA-Z]+)")
        res2 = formate.match(total2).groups()
        num2=  float(res2[0])

        if current2<num2:
            goal.progress2 = str(round(current2/num2, 1)*100) + "%"
            db.session.commit()
        else:
            goal.progress2 = "100%"

    # progress (key result3)
    if goal.key_result3:
        current3=float(form.mon3.data)+float(form.tue3.data)+float(form.wed3.data)+float(form.thu3.data)+float(form.fri3.data)+float(form.sat3.data)+float(form.sun3.data)
        # 把3km變成3(key result3)
        total3 = goal.amount # 3km
        formate3 = re.compile("([+-]?[0-9]+\.?[0-9]*)([a-zA-Z]+)")
        res3 = formate.match(total3).groups()
        num3 =  float(res3[0]) # no unit -> 3

        if current3<num3:
            goal.progress3 = str(round(current3/num3, 1)*100) + "%"
            db.session.commit()
            # percent_progress3 =  str(goal.progress3*100) + "%"
        else:
            goal.progress3 = "100%"
    if goal.key_result:
        if goal.key_result2:
            if goal.key_result3:
                if ((round(current3/num3, 1)*100)+(round(current2/num2, 1)*100)+(round(current/num, 1)*100))/3<100:
                    goal.final_score= ((round(current3/num3, 1)*100)+(round(current2/num2, 1)*100)+(round(current/num, 1)*100))/3
                else: goal.final_score = 100
                db.session.commit()
            else:
                if ((round(current2/num2, 1)*100)+(round(current/num, 1)*100))/2<100:
                    goal.final_score = ((round(current2/num2, 1)*100)+(round(current/num, 1)*100))/2
                else: goal.final_score = 100
                db.session.commit()
        else:       
            if (round(current/num, 1)*100)<100:
                goal.final_score = (round(current/num, 1)*100)
            else: goal.final_score = 100
            db.session.commit()

    return render_template('goal.html', object=goal.object, goal=goal, title=goal.object, form=form)

@app.route("/goal/<int:goal_id>/update", methods=['GET', 'POST'])
@login_required
def update_goal(goal_id):
    goal = Goal.query.get_or_404(goal_id)
    if goal.author != current_user: # 如果不是本人進行修改
        abort(403)
    form = GoalForm()
    if form.validate_on_submit():
        goal.object=form.object.data
        goal.key_result=form.key_result.data 
        goal.amount=form.amount.data
        # if goal.key_result2:
        goal.key_result2=form.key_result2.data
        goal.amount2=form.amount2.data
        # if goal.key_result3:
        goal.key_result3=form.key_result3.data
        goal.amount3=form.amount3.data
        goal.note=form.note.data

        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('goal', goal_id=goal.id))
    elif request.method == 'GET': # 顯示原有的
        form.object.data = goal.object

        form.key_result.data = goal.key_result
        form.amount.data = goal.amount
        form.key_result2.data = goal.key_result2
        form.amount2.data = goal.amount2
        form.key_result3.data = goal.key_result3
        form.amount3.data = goal.amount3
        form.note.data = goal.note
    return render_template('create_goal.html', title='Update Goal',
                           form=form, legend='Update Goal') 
@app.route("/goal/<int:goal_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_goal(goal_id):
    goal = Goal.query.get_or_404(goal_id)
    if goal.author != current_user:
        abort(403)
    db.session.delete(goal)
    db.session.commit()
    flash('成功刪除', 'success')
    return redirect(url_for('home'))

@app.route("/dashboard", methods=['GET', 'POST'])
@login_required
def dashboard():
    form=RecordForm()
    user = User.query.filter_by(username=current_user.username).first_or_404() # 先找user(=現在登入的user)
    goals = Goal.query.filter_by(author=user, state="progressing").all()                            # 再透過這user的名稱找這個人的所有goals; return "list of goals" ->[Goal('test_goal', '2022-06-10 15:27:48.788870'), Goal('test_goal2', '2022-06-10 18:10:07.187977')]
    # goals = Goal.query.filter_by(author=current_user
  
    return render_template('dashboard.html', title='myDashboard', form=form, user=user, goals=goals)

@app.route("/dashboard_end", methods=['GET', 'POST'])
@login_required
def dashboard_end():
    form=RecordForm()
    user = User.query.filter_by(username=current_user.username).first_or_404() # 先找user(=現在登入的user)
    goals_s = Goal.query.filter_by(author=user, state="successed").all()
    goals_f = Goal.query.filter_by(author=user, state="failed").all()
    # goals = Goal.query.filter_by(author=current_user
  
    return render_template('dashboard_end.html', title='myDashboard', form=form, user=user, goals_s=goals_s, goals_f=goals_f)
