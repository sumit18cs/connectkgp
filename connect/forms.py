from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField,SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from connect.models import User
from wtforms.ext.sqlalchemy.fields import QuerySelectField


class MessageForm(FlaskForm):
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=0, max=1000)],render_kw={"placeholder": "Enter Your Message"})
    submit = SubmitField('Send')


class SearchForm(FlaskForm):
    search=SelectField('', choices=[('Select Skill','Select Skill'),('Algorithmic Game theory','Algorithmic Game theory'),('Algorithms','Algorithms'),('Analytical Reasoning','Analytical Reasoning'),('Android Development','Android Development'),('Angular','Angular'),('Architectural Design','Architectural Design'),('Artificial Intelligence','Artificial Intelligence'),('Auto CAD','Auto CAD'),('Bootstrap','Bootstrap'),('Business Analysis','Business Analysis'),('Business Management','Business Management'),('C Programming Language','C Programming Language'),('C #','C #'),('C++','C++'),('Cloud Computing','Cloud Computing'),('Competitive Programming','Competitive Programming'),('Computer Graphics','Computer Graphics'),('Consulting','Consulting'),('CSS','CSS'),('Data Analytics','Data Analytics'),('Data Structures','Data Structures'),('Deep Learning','Deep Learning'),('Digital Marketing','Digital Marketing'),('Django','Django'),('EMCA Script','EMCA Script'),('Economics','Economics'),('Financial Management','Financial Management'),('Flask','Flask'),('Fortran','Fortran'),('Git','Git'),('Hibernate','Hibernate'),('HTML','HTML'),('Java','Java'),('Java Frameworks','Java Frameworks'),('JavaScript','JavaScript'),('Jquery','Jquery'),('JSON','JSON'),('Julia','Julia'),('Kotlin','Kotlin'),('Machine Learning','Machine Learning'),('Marketing Accountability','Marketing Accountability'),('Matlab','Matlab'),('Mobile Development','Mobile Development'),('Natural Language Processing','Natural Language Processing'),('NodeJs','NodeJs'),('Octave','Octave'),('PERL','PERL'),('PHP','PHP'),('Python','Python'),('Python Frameworks','Python Frameworks'),('React','React'),('Ruby','Ruby'),('Ruby on Rails','Ruby on Rails'),('Scala','Scala'),('Software Engineering','Software Engineering'),('SQL','SQL'),('SQLAlchemy','SQLAlchemy'),('Swift','Swift'),('Tensor Flow','Tensor Flow'),('TypeScript','TypeScript'),('Unity','Unity'),('Verilog','Verilog'),('Web Development','Web Development')], validators=[DataRequired()])
    submit=SubmitField('Search')

    def validate_search(self,search):
        if search.data=='Select Skill':
            raise ValidationError('Select appropriate Choice.')


class SkillForm(FlaskForm):
    title = SelectField('', choices=[('Select Skill','Select Skill'),('Algorithmic Game theory','Algorithmic Game theory'),('Algorithms','Algorithms'),('Analytical Reasoning','Analytical Reasoning'),('Android Development','Android Development'),('Angular','Angular'),('Architectural Design','Architectural Design'),('Artificial Intelligence','Artificial Intelligence'),('Auto CAD','Auto CAD'),('Bootstrap','Bootstrap'),('Business Analysis','Business Analysis'),('Business Management','Business Management'),('C Programming Language','C Programming Language'),('C #','C #'),('C++','C++'),('Cloud Computing','Cloud Computing'),('Competitive Programming','Competitive Programming'),('Computer Graphics','Computer Graphics'),('Consulting','Consulting'),('CSS','CSS'),('Data Analytics','Data Analytics'),('Data Structures','Data Structures'),('Deep Learning','Deep Learning'),('Digital Marketing','Digital Marketing'),('Django','Django'),('EMCA Script','EMCA Script'),('Economics','Economics'),('Financial Management','Financial Management'),('Flask','Flask'),('Fortran','Fortran'),('Git','Git'),('Hibernate','Hibernate'),('HTML','HTML'),('Java','Java'),('Java Frameworks','Java Frameworks'),('JavaScript','JavaScript'),('Jquery','Jquery'),('JSON','JSON'),('Julia','Julia'),('Kotlin','Kotlin'),('Machine Learning','Machine Learning'),('Marketing Accountability','Marketing Accountability'),('Matlab','Matlab'),('Mobile Development','Mobile Development'),('Natural Language Processing','Natural Language Processing'),('NodeJs','NodeJs'),('Octave','Octave'),('PERL','PERL'),('PHP','PHP'),('Python','Python'),('Python Frameworks','Python Frameworks'),('React','React'),('Ruby','Ruby'),('Ruby on Rails','Ruby on Rails'),('Scala','Scala'),('Software Engineering','Software Engineering'),('SQL','SQL'),('SQLAlchemy','SQLAlchemy'),('Swift','Swift'),('Tensor Flow','Tensor Flow'),('TypeScript','TypeScript'),('Unity','Unity'),('Verilog','Verilog'),('Web Development','Web Development')], validators=[DataRequired()])
    content = TextAreaField('', validators=[DataRequired()],render_kw={"placeholder": "Tell the Resources/Material from where You Learn this Skill"})
    submit = SubmitField('Add Skill')

    def validate_title(self,title):
        if title.data=='Select Skill':
            raise ValidationError('Select Appropriate Choice.')


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)],render_kw={"placeholder": "Enter Username"})
    password = PasswordField('Password', validators=[DataRequired()],render_kw={"placeholder": "Enter Password"})
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')],render_kw={"placeholder": "Enter Password to Confirm"})
    email = StringField('Email',validators=[DataRequired(), Email()],render_kw={"placeholder": "Enter Your Email ID"})
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That Username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That Email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=100)],render_kw={"placeholder": "Enter Your Username"})
    password = PasswordField('Password', validators=[DataRequired()],render_kw={"placeholder": "Enter Your Password"})
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    name= StringField('Name',validators=[DataRequired(),Length(min=2,max=100)])
    department = SelectField('Department', choices=[('None','None'),('Aerospace Engineering', 'Aerospace Engineering'), ('Agricultural and Food Engineering', 'Agricultural and Food Engineering'),('Architecture and Regional Planning', 'Architecture and Regional Planning'),('Bio Science', 'Bio Science'),('Biotechnology', 'Biotechnology'),('Centre for Computational and Data Sciences', 'Centre for Computational and Data Sciences'),('Centre for Educational Technology', 'Centre for Educational Technology'),('Centre for Theoretical Studies', 'Centre for Theoretical Studies'),('Centre of Excellence in Advanced Manufacturing Technology', 'Centre of Excellence in Advanced Manufacturing Technology'),('Centre of Excellence in Artificial Intelligence', 'Centre of Excellence in Artificial Intelligence'),('Chemical Engineering', 'Chemical Engineering'),('Chemistry', 'Chemistry'),('Civil Engineering', 'Civil Engineering'),('Computer Science and Engineering', 'Computer Science and Engineering'),('Cryogenic Engineering', 'Cryogenic Engineering'),('Electrical Engineering', 'Electrical Engineering'),('Energy Science and Engineering', 'Energy Science and Engineering'),('Environmental Science and Engineering', 'Environmental Science and Engineering'),('Exploration Geophysics', 'Exploration Geophysics'),('Geology and Geophysics', 'Geology and Geophysics'),('Humanities and Social Sciences', 'Humanities and Social Sciences'),('Industrial and Systems Engineering', 'Industrial and Systems Engineering'),('Instrumentation Engineering', 'Instrumentation Engineering'),('Manufacturing Engineering', 'Manufacturing Engineering'),('Mathematics', 'Mathematics'),('Mechanical Engineering', 'Mechanical Engineering'),('Metallurgical and Materials Engineering', 'Metallurgical and Materials Engineering'),('Mining Engineering', 'Mining Engineering'),('Ocean Engg and Naval Architecture', 'Ocean Engg and Naval Architecture'),('Physics', 'Physics'),('Quality Engineering Design and Manufacturing', 'Quality Engineering Design and Manufacturing'),('Rajendra Mishra School of Engg Entrepreneurship', 'Rajendra Mishra School of Engg Entrepreneurship'),('Rajiv Gandhi School of Intellectual Property Law', 'Rajiv Gandhi School of Intellectual Property Law'),('Rubber Technology', 'Rubber Technology'),('Statistics and Informatics', 'Statistics and Informatics'),('Vinod Gupta School of Management', 'Vinod Gupta School of Management')])


    hall = SelectField('Hall of Residence', choices=[('None','None'),('Azad Hall of Residence ', 'Azad Hall of Residence '),('B C Roy Hall of Residence ', 'B C Roy Hall of Residence '),('B R Ambedkar Hall of Residence ', 'B R Ambedkar Hall of Residence '),('Gokhale Hall of Residence ', 'Gokhale Hall of Residence '),('Homi J Bhabha Hall of Residence ', 'Homi J Bhabha Hall of Residence '),(' Jagadish Chandra Bose Hall of Residence ', ' Jagadish Chandra Bose Hall of Residence '),(' Nehru Hall of Residence ', ' Nehru Hall of Residence '),('Lalbahadur Sastry Hall of Residence ', 'Lalbahadur Sastry Hall of Residence '),('Lala Lajpat Rai Hall of Residence ', 'Lala Lajpat Rai Hall of Residence '),('Madan Mohan Malviya Hall of Residence ', 'Madan Mohan Malviya Hall of Residence '),(' Megnad Saha Hall of Residence ', ' Megnad Saha Hall of Residence '),('Mother Teresa Hall of Residence ', 'Mother Teresa Hall of Residence '),('Nivedita Hall of Residence ', 'Nivedita Hall of Residence '),('Patel Hall of Residence ', 'Patel Hall of Residence '),(' Radha Krishnan Hall of Residence', ' Radha Krishnan Hall of Residence'),('Rani Laxmibai Hall of Residence ', 'Rani Laxmibai Hall of Residence '),('Rajendra Prasad Hall of Residence', 'Rajendra Prasad Hall of Residence'),('SAM Hall of Residence ', 'SAM Hall of Residence '),(' Sarojini Naidu - Indira Gandhi Hall of Residence ', ' Sarojini Naidu - Indira Gandhi Hall of Residence '),('Vidyasagar Hall of Residence ', 'Vidyasagar Hall of Residence '),('Zakir Hussain Hall of Residence ', 'Zakir Hussain Hall of Residence ')])
    support = SelectField('Wants to Receive messages from Other User', choices=[('Yes', 'Yes'), ('No', 'No')])
    rollno = StringField('RollNo',validators=[DataRequired(), Length(min=0, max=20)])
    email = StringField('Email',validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','jpeg' ,'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That Username is taken. Please choose a different one.')

    def validate_rollno(self, rollno):
        if rollno.data != current_user.rollno:
            user = User.query.filter_by(rollno=rollno.data).first()
            if user:
                raise ValidationError('That Roll Number is already Registered. Please choose a different one.')            

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That Email is taken. Please choose a different one.')


class PostForm(FlaskForm):
    title = StringField('', validators=[DataRequired()],render_kw={"placeholder": "Title Goes Here !!"})
    content = TextAreaField('', validators=[DataRequired()],render_kw={"placeholder": "Content Goes Here !!"})
    submit = SubmitField('Post')


class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()],render_kw={"placeholder": "Enter Your Email ID"})
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that Email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()],render_kw={"placeholder": "Enter Your Password"})
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')],render_kw={"placeholder": "Enter Password to Confirm"})
    submit = SubmitField('Reset Password')


