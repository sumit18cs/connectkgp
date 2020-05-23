import os
from os import urandom
from datetime import datetime
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from connect import app, db, bcrypt, mail
from connect.forms import RegistrationForm, LoginForm, UpdateAccountForm,PostForm, RequestResetForm, ResetPasswordForm, SkillForm, SearchForm, MessageForm
from connect.models import User, Doubt, Skill, Comment, Chat, Job, Jobcomment, Collab, Collabcomment
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
import json

#############################################################
#HOME PAGE
#############################################################
@app.route("/")
@app.route("/home", methods=['GET', 'POST'])
@login_required
def home():
    page = request.args.get('page', 1, type=int)
    doubts = Doubt.query.filter_by(author=current_user).order_by(Doubt.date_posted.desc()).paginate(page=page, per_page=5)
    jobs = Job.query.filter_by(author=current_user).order_by(Job.date_posted.desc()).paginate(page=page, per_page=5)
    collabs = Collab.query.filter_by(author=current_user).order_by(Collab.date_posted.desc()).paginate(page=page, per_page=5)
    user_list = []
    title='Connect KGP'
    form = SearchForm()
    if form.validate_on_submit():   
        title=form.search.data
        users=User.query.join(Skill,User.skills).filter_by(title=form.search.data).all()
        user_2d=[]
        for user in users:
            add=(user,user.followers.count())
            user_2d.insert(0,add)
            user_list.append(user)
        user_2d.sort(key=lambda x:x[1])
        user_list1=[]
        for i in user_2d:
            user_list1.append(i[0])
        user_list = user_list1[::-1]  
    # print('################################')
    # for user in user_list:
    #     # print(user.username)
    #     for skill in user.skills:
    #         print(skill.title)
    #         # print(skill.content)
    # print('####################################')
    allskill=[]
    skills=Skill.query.all()
    for skill in skills:
        allskill.append(skill.title)
    allskill.sort()

    # for skill in allskill:
    #     print(skill)
    # print('######################################')
    allskill_2d=[]
    t=''
    allskill.append('abc')
    for a in range(0,len(allskill),1):
        s=1
        if allskill[a]!=t:
            for b in range(a+1,len(allskill),1):
                if allskill[a]==allskill[b]:
                    s=s+1
                else:
                    add=(s,allskill[b-1])
                    allskill_2d.append(add)
                    break
            t=allskill[a]
    # print('##########################################')
    
    # print('#######################################')
    allskill_2d.sort(key=lambda x:x[0])
    allskill_2d.reverse()
    # for skill in allskill_2d:
    #     print(skill[0])
    #     print(skill[1])
    showskill=[]
    s=0
    for a in allskill_2d:
        showskill.append(a[1])
        s=s+1
        if s==3:
            break
    # print('##########################################')
    return render_template('home.html',form=form,doubts=doubts,jobs=jobs,collabs=collabs,title=title,user_list=user_list,showskill=showskill,info='Trending Skills')


###########################################################
#REGISTER, LOGIN, LOGOUT, ABOUT
###########################################################
@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password,email=form.email.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
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
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check Username and Password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/about")
@login_required
def about():
    return render_template('about.html')

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


def save_picture(form_picture):
    random_hex = urandom(8).hex()
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

###############################################################
#USER DETAIL, ACCOUNT, FRIEND
###############################################################
@app.route("/user_detail/<string:username>")
@login_required
def user_detail(username): 
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    doubts = Doubt.query.filter_by(author=user).paginate(page=page, per_page=5)
    jobs = Job.query.filter_by(author=user).paginate(page=page, per_page=5)
    collabs = Collab.query.filter_by(author=user).paginate(page=page, per_page=5)
    #print('###########################################')
    # print(user.followed.count())
    # for use in user.followed:
    #     print(use.username)
    # print(followers.follower_id)
    #print('#############################################')
    image_file = url_for('static', filename='profile_pics/' + user.image_file)
    return render_template('user_detail.html', title='Account',image_file=image_file,user=user,doubts=doubts,jobs=jobs,collabs=collabs)
    # info='If you like the resources/material provided by this user, click follow button which ultimately help others to access these resources/ material easily'


@app.route("/friend")
@login_required
def friend():
    users=User.query.all()
    #print('##########################')
    t=len(users)
    #print(len(users))
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('friend.html',image_file=image_file,users=users,t=t,title='Following')


@app.route("/account")
@login_required
def account(): 
    #print('###########################################')
    #print(current_user.followers.count())
    #print('###########################################')
    page = request.args.get('page', 1, type=int)
    skills = Skill.query.order_by(Skill.date_posted.desc()).paginate(page=page)
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',image_file=image_file,skills=skills)

@app.route("/edit_account", methods=['GET', 'POST'])
@login_required
def edit_account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.department = form.department.data
        current_user.support=form.support.data
        current_user.name=form.name.data
        current_user.rollno = form.rollno.data
        current_user.hall = form.hall.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated !!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.support.data=current_user.support
        form.name.data=current_user.name
        form.department.data = current_user.department
        form.hall.data = current_user.hall
        form.rollno.data = current_user.rollno
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('edit_account.html', title='EditAccount',
                           image_file=image_file, form=form)


#######################################################
#DOUBT AND DISCUSSIONS
#######################################################
@app.route("/doubt/new", methods=['GET', 'POST'])
@login_required
def new_doubt():
    page = request.args.get('page', 1, type=int)
    doubts = Doubt.query.order_by(Doubt.date_posted.desc()).paginate(page=page, per_page=5)
    form = PostForm()
    if form.validate_on_submit():
        doubt = Doubt(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(doubt)
        db.session.commit()
        flash('Your Doubt Post has been created !!', 'success')
        return redirect(url_for('home'))
    return render_template('create_doubt.html', title='New Doubt',form=form, legend='New Doubt',doubts=doubts)


@app.route("/doubt/<int:doubt_id>",methods=['POST','GET'])
@login_required
def doubt(doubt_id):
    doubt = Doubt.query.get_or_404(doubt_id)
    comments = Comment.query.filter_by(doubt_id=doubt_id).order_by(Comment.date_posted.desc()).all() 
    # print('######################################################')
    #  print(str(comments))
    # print('######################################################')
    #print(str(comments.message))
    # for comment in comments:
    #      print(current_user.username)
    #      print(comment.user_name)
    #     print(comment.message)
    #     print(comment.id)
    #  print(doubt_id)
    # print('######################################################')

    if request.method=='POST':
        # print("current user is"+str(current_user))
        #user_name=current_user
        message=request.form.get('message')
        #user = User.query.filter_by(username=username).first_or_404()
        comment=Comment(message=message,user_name=current_user.username,doubt_id=doubt_id)
        # print('#######################################')
        # print(str(comment))
        # print('#######################################')
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been submitted !!','success')
        return redirect(url_for('doubt',doubt_id=doubt_id))
    
    return render_template('doubt.html', doubt=doubt,comments=comments)


@app.route("/doubt/<int:comment_id>/<int:doubt_id>/delete", methods=['POST'])
@login_required
def delete_comment(comment_id,doubt_id):
    # print(comment_id)
    comments=Comment.query.get_or_404(comment_id)
    # print('#######################################')
    
    # print(comments.message)
    # print('#######################################')
    comment = Comment.query.get_or_404(comment_id)
    if comment.user_name != current_user.username:
        abort(403)
    db.session.delete(comment)
    db.session.commit()
    flash('Your Coment has been deleted !!', 'info')
    return redirect(url_for('doubt',doubt_id=doubt_id))




@app.route("/doubt/<int:doubt_id>/update", methods=['GET', 'POST'])
@login_required
def update_doubt(doubt_id):
    page = request.args.get('page', 1, type=int)
    doubts = Doubt.query.order_by(Doubt.date_posted.desc()).paginate(page=page, per_page=5)
    doubt = Doubt.query.get_or_404(doubt_id)
    if doubt.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        doubt.title = form.title.data
        doubt.content = form.content.data
        db.session.commit()
        flash('Your Doubt Post has been updated !!', 'success')
        return redirect(url_for('doubt', doubt_id=doubt.id))
    elif request.method == 'GET':
        form.title.data = doubt.title
        form.content.data = doubt.content
    return render_template('create_doubt.html', title='Update Doubt',
                           form=form, legend='Update Doubt',doubts=doubts)


@app.route("/doubt/<int:doubt_id>/delete", methods=['POST'])
@login_required
def delete_doubt(doubt_id):
    doubt = Doubt.query.get_or_404(doubt_id)
    comments = Comment.query.filter_by(doubt_id=doubt_id).all()

    if doubt.author != current_user:
        abort(403)
    db.session.delete(doubt)
    for comment in comments:
        db.session.delete(comment)
    
    db.session.commit()
    flash('Your Doubt Post has been deleted !!', 'info')
    return redirect(url_for('home'))


@app.route("/user/doubt/<string:username>")
@login_required
def user_doubts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    doubts = Doubt.query.filter_by(author=user)\
        .order_by(Doubt.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_doubt.html', doubts=doubts, user=user)




#######################################################
#JOBS/INTERNSHIP
#######################################################
@app.route("/job/new", methods=['GET', 'POST'])
@login_required
def new_job():
    page = request.args.get('page', 1, type=int)
    jobs = Job.query.order_by(Job.date_posted.desc()).paginate(page=page, per_page=5)
    form = PostForm()
    if form.validate_on_submit():
        job = Job(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(job)
        db.session.commit()
        flash('Your Job/Internship Post has been created !!', 'success')
        return redirect(url_for('home'))
    return render_template('create_job.html', title='New Job',form=form, legend='New Job/Internship Post',jobs=jobs)


@app.route("/job/<int:job_id>",methods=['POST','GET'])
@login_required
def job(job_id):
    job = Job.query.get_or_404(job_id)
    comments = Jobcomment.query.filter_by(job_id=job_id).order_by(Jobcomment.date_posted.desc()).all()
    # print('######################################################')
    # print(str(comments))
    # print('######################################################')
    if request.method=='POST':
        # print("current user is"+str(current_user))
        #user_name=current_user
        message=request.form.get('message')
        #user = User.query.filter_by(username=username).first_or_404()
        comment=Jobcomment(message=message,user_name=current_user.username,job_id=job_id)
        # print('#######################################')
        # print(str(comment))
        # print('#######################################')
        db.session.add(comment)
        db.session.commit()
        flash('Your Comment has been submitted !!','success')
        return redirect(url_for('job',job_id=job_id)) 
    return render_template('job.html', job=job,comments=comments)


@app.route("/job/<int:jobcomment_id>/<int:job_id>/delete", methods=['POST'])
@login_required
def delete_jobcomment(jobcomment_id,job_id):
    comment = Jobcomment.query.get_or_404(jobcomment_id)
    if comment.user_name != current_user.username:
        abort(403)
    db.session.delete(comment)
    db.session.commit()
    flash('Your Comment has been deleted !!', 'info')
    return redirect(url_for('job',job_id=job_id))




@app.route("/job/<int:job_id>/update", methods=['GET', 'POST'])
@login_required
def update_job(job_id):
    page = request.args.get('page', 1, type=int)
    jobs = Job.query.order_by(Job.date_posted.desc()).paginate(page=page, per_page=5)
    job = Job.query.get_or_404(job_id)
    if job.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        job.title = form.title.data
        job.content = form.content.data
        db.session.commit()
        flash('Your Job/Internship Post has been updated !!', 'success')
        return redirect(url_for('job', job_id=job.id))
    elif request.method == 'GET':
        form.title.data = job.title
        form.content.data = job.content
    return render_template('create_job.html', title='Update Job',
                           form=form, legend='Update Job/Internship Post',jobs=jobs)


@app.route("/job/<int:job_id>/delete", methods=['POST'])
@login_required
def delete_job(job_id):
    job = Job.query.get_or_404(job_id)
    comments = Jobcomment.query.filter_by(job_id=job_id).all()
    if job.author != current_user:
        abort(403)
    db.session.delete(job)
    for comment in comments:
        db.session.delete(comment)
    db.session.commit()
    flash('Your Job/Internship Post has been deleted !!', 'info')
    return redirect(url_for('home'))


@app.route("/user/job/<string:username>")
@login_required
def user_jobs(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    jobs = Job.query.filter_by(author=user)\
        .order_by(Job.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_job.html', jobs=jobs, user=user)




#######################################################
#COLLABORATION POST
#######################################################
@app.route("/collab/new", methods=['GET', 'POST'])
@login_required
def new_collab():
    page = request.args.get('page', 1, type=int)
    collabs = Collab.query.order_by(Collab.date_posted.desc()).paginate(page=page, per_page=5)
    form = PostForm()
    if form.validate_on_submit():
        collab = Collab(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(collab)
        db.session.commit()
        flash('Your Post for Collaboration has been created !!', 'success')
        return redirect(url_for('home'))
    return render_template('create_collab.html', title='New Collab',form=form, legend='New Collaboration Post',collabs=collabs)


@app.route("/collab/<int:collab_id>",methods=['POST','GET'])
@login_required
def collab(collab_id):
    collab = Collab.query.get_or_404(collab_id)
    comments = Collabcomment.query.filter_by(collab_id=collab_id).order_by(Collabcomment.date_posted.desc()).all()
    # print('######################################################')
    # print(str(comments))
    # print('######################################################')
    if request.method=='POST':
        # print("current user is"+str(current_user))
        #user_name=current_user
        message=request.form.get('message')
        #user = User.query.filter_by(username=username).first_or_404()
        comment=Collabcomment(message=message,user_name=current_user.username,collab_id=collab_id)
        # print('#######################################')
        # print(str(comment))
        # print('#######################################')
        db.session.add(comment)
        db.session.commit()
        flash('Your Comment has been submitted !!','success')
        return redirect(url_for('collab',collab_id=collab_id)) 
    return render_template('collab.html', collab=collab,comments=comments)


@app.route("/collab/<int:collabcomment_id>/<int:collab_id>/delete", methods=['POST'])
@login_required
def delete_collabcomment(collabcomment_id,collab_id):
    comment = Collabcomment.query.get_or_404(collabcomment_id)
    if comment.user_name != current_user.username:
        abort(403)
    db.session.delete(comment)
    db.session.commit()
    flash('Your Comment has been deleted !!', 'info')
    return redirect(url_for('collab',collab_id=collab_id))


@app.route("/collab/<int:collab_id>/update", methods=['GET', 'POST'])
@login_required
def update_collab(collab_id):
    page = request.args.get('page', 1, type=int)
    collabs = Collab.query.order_by(Collab.date_posted.desc()).paginate(page=page, per_page=5)
    collab = Collab.query.get_or_404(collab_id)
    if collab.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        collab.title = form.title.data
        collab.content = form.content.data
        db.session.commit()
        flash('Your Post for Collaboration has been updated !!', 'success')
        return redirect(url_for('collab', collab_id=collab.id))
    elif request.method == 'GET':
        form.title.data = collab.title
        form.content.data = collab.content
    return render_template('create_collab.html', title='Update Collaboration Post',
                           form=form, legend='Update Collaboration Post',collabs=collabs)



@app.route("/collab/<int:collab_id>/delete", methods=['POST'])
@login_required
def delete_collab(collab_id):
    collab = Collab.query.get_or_404(collab_id)
    comments = Collabcomment.query.filter_by(collab_id=collab_id).all()
    if collab.author != current_user:
        abort(403)
    db.session.delete(collab)
    for comment in comments:
        db.session.delete(comment)
    db.session.commit()
    flash('Your Post for Collaboration has been deleted!', 'info')
    return redirect(url_for('home'))


@app.route("/user/collab/<string:username>")
@login_required
def user_collabs(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    collabs = Collab.query.filter_by(author=user)\
        .order_by(Collab.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_collab.html', collabs=collabs, user=user)



#######################################################
#RESET PASSWORD THROUGH E MAIL VERIFICATION
#######################################################
def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='connectkgp.iitkgp@gmail.com',
                  recipients=[user.email])
    msg.body = 'To reset your password, visit the link: \n'+ url_for('reset_token', token=token, _external=True)+'\n If you did not make this request then simply ignore this mail and no changes will be made.' 

    mail.send(msg)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    flash('This Function is not available in trial version. Please Register with another account','info')
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        ##################
        return redirect(url_for('login'))
        ##################
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An Email has been sent with instructions to reset your Password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)



#######################################################
#SKILLS 
#######################################################
@app.route("/skill/new", methods=['GET', 'POST'])
@login_required
def new_skill():
    form = SkillForm()
    if form.validate_on_submit():   
        skills = Skill.query.filter_by(author=current_user)
        for skill in skills:
            if skill.title==form.title.data:
                flash('Selected Option is already Chosen !!','danger')
                return redirect(url_for('account'))

        skill = Skill(title=form.title.data,content=form.content.data, author=current_user)
        db.session.add(skill)
        db.session.commit()
        flash('Your Skill has been added !!', 'success')
        return redirect(url_for('account'))
                
    return render_template('create_skill.html',form=form, legend='New Skill',title='New Skills')


@app.route("/skill/<int:skill_id>")
@login_required
def skill(skill_id):
    skill = Skill.query.order_by(Skill.date_posted.desc()).get_or_404(skill_id)
    return render_template('skill.html', title=skill.title, skill=skill)


@app.route("/skill/<int:skill_id>/update", methods=['GET', 'POST'])
@login_required
def update_skill(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    if skill.author != current_user:
        abort(403)
    form = SkillForm()
    if form.validate_on_submit():
        skills = Skill.query.filter_by(author=current_user)
        for skilla in skills:
            if skilla.title==form.title.data:
                if skilla.title!=skill.title:
                    flash('Selected option is already Chosen','danger')
                    return redirect(url_for('account'))

        skill.title = form.title.data
        skill.content = form.content.data
        db.session.commit()
        flash('Your Skills related information has been updated !!', 'success')
        return redirect(url_for('skill', skill_id=skill.id))
    elif request.method == 'GET':
        form.title.data = skill.title
        form.content.data = skill.content
    return render_template('create_skill.html', title='Update Skill',
                           form=form, legend='Update Skill')


@app.route("/skill/<int:skill_id>/delete", methods=['POST'])
@login_required
def delete_skill(skill_id):
    # print('##########################################')
    skill = Skill.query.get_or_404(skill_id)
    # print(skill)
    # print('############################################')
    if skill.author != current_user:
        abort(403)
    db.session.delete(skill)
    db.session.commit()
    flash('Your Skill has been deleted !!', 'info')
    return redirect(url_for('account'))



#######################################################
#FOLLOWERS AND FOLLOWING
#######################################################
@app.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('user_detail'))
    if user == current_user:
        flash('You cannot follow yourself!')
        return redirect(url_for('user_detail', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are following {}!'.format(username),'success')
    return redirect(url_for('user_detail', username=username))

@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('user_detail'))
    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('user_detail', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following {}.'.format(username),'success')
    return redirect(url_for('user_detail', username=username))



#######################################################
#CHAT MESSAGES
#######################################################
@app.route('/send_message/<recipient>', methods=['GET', 'POST'])
@login_required
def send_message(recipient):
    user = User.query.filter_by(username=recipient).first_or_404()
    form = MessageForm()
    if form.validate_on_submit():
        if current_user.support=='No':
            flash('You are not allowed to send Message','danger')
            return redirect(url_for('messages'))
        elif user.support=='No':
            flash('You are not allowed to send Message','danger')
            return redirect(url_for('messages'))
        else:
            msg = Chat(recipient=user,body=form.message.data,author=current_user)
            db.session.add(msg)
            db.session.commit()
            flash('Your Message has been sent !!','success')
            return redirect(url_for('messages'))
    return render_template('send_message.html',title='Send Message', legend=recipient,form=form, recipient=recipient)


@app.route('/messages')
@login_required
def messages():
    user_list=[]
    user_list1=[]
    current_user.last_message_read_time = datetime.now()
    db.session.commit()
    messages = current_user.messages_received.order_by(Chat.timestamp.asc())
    # print('####################################')
    #print(messages)
    r=messages.count()
    for message in messages:
        user=User.query.get_or_404(message.sender_id)
        add=(user,message)
        user_list.insert(0,add)

    messages = current_user.messages_sent.order_by(Chat.timestamp.asc())
    # print('####################################')
    # print(messages.count())
    s=messages.count()
    # print('######################################')
    for message in messages:
        user=User.query.get_or_404(message.recipient_id)
        add=(user,message,message.id)
        # print(message.id)
        user_list1.insert(0,add)

    return render_template('messages.html',user_list=user_list,user_list1=user_list1,r=r,s=s,title='Messages')



@app.route('/messages/<string:username>')
@login_required
def personalchat(username):
    user_list=[]
    user_list1=[]
    user=User.query.filter_by(username=username).first()
    current_user.last_message_read_time = datetime.now()
    db.session.commit()
    messages = current_user.messages_received.order_by(Chat.timestamp.asc())
   
    for message in messages:
        user1=User.query.get_or_404(message.sender_id)
        if user1.username==user.username :
            add=(user,message)
            user_list.insert(0,add)
    # print("##############################")
    # print(len(user_list))
    r=len(user_list)
    # print('############################')
    messages = current_user.messages_sent.order_by(Chat.timestamp.asc())
    
    for message in messages:
        user1=User.query.get_or_404(message.recipient_id)
        if user1.username==user.username :    
            add=(user,message,message.id)
            user_list1.insert(0,add)
    s=len(user_list1)
    return render_template('messages.html',user_list=user_list,user_list1=user_list1,r=r,s=s,title='Messages with '+username )



@app.route("/messages/<int:chat_id>/delete", methods=['POST'])
@login_required
def delete_chat(chat_id):
    chat=Chat.query.get_or_404(chat_id)
    if chat.sender_id != current_user.id:
        abort(403)
    print(chat.sender_id)
    print(current_user.id)
    db.session.delete(chat)
    db.session.commit()
    flash('Message has been deleted !!', 'success')
    return redirect(url_for('messages'))