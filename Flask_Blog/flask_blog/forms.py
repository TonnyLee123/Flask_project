from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from flask_blog.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    #email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('密碼', validators=[DataRequired()])
    confirm_password = PasswordField('確認密碼',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('註冊')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('此用戶名稱已註冊過，請更換一個，謝謝!。')
    # 客製化validation(查詢用戶username是否已經註冊(存在在db))   
    # def validate_field(self, field):
        #if true:
            #raise ValidationError('...')      

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('密碼', validators=[DataRequired()])
    remember = BooleanField('記住我')
    submit = SubmitField('登入')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    picture = FileField('更新頭貼', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

class PostForm(FlaskForm):
    title = StringField('標題', validators=[DataRequired()])
    content = TextAreaField('內容', validators=[DataRequired()])
    submit = SubmitField('Post')


class GoalForm(FlaskForm):
    object = StringField('目標', validators=[DataRequired()])
    # planning = TextAreaField('任務', validators=[DataRequired()])
    key_result = StringField('任務1', validators=[DataRequired()])
    key_result2 = StringField('任務2')
    key_result3 = StringField('任務3')
    amount = StringField('數量(單位)', validators=[DataRequired(), Length(max=20)])
    amount2 = StringField('數量(單位)', validators=[Length(max=20)])
    amount3 = StringField('數量(單位)', validators=[Length(max=20)])
    # week = SelectMultipleField('時間', choices =[('Mon', '一'), ('Tue', '二'), ('Wed', '三'), ('Thu', '四'), ('Fri', '五'), ('Sat', '六'), ('Sun', '日')])
    note = TextAreaField('note')
    submit = SubmitField('建立')

class RecordForm(FlaskForm):

    test = StringField('Test')
    mon = StringField('mon')
    tue = StringField('tue')
    wed = StringField('wed')
    thu = StringField('thu')
    fri = StringField('fri')
    sat = StringField('sat')
    sun = StringField('sun')

    mon2 = StringField('mon2')
    tue2 = StringField('tue2')
    wed2 = StringField('wed2')
    thu2 = StringField('thu2')
    fri2 = StringField('fri2')
    sat2 = StringField('sat2')
    sun2 = StringField('sun2')

    mon3 = StringField('mon3')
    tue3 = StringField('tue3')
    wed3 = StringField('wed3')
    thu3 = StringField('thu3')
    fri3 = StringField('fri3')
    sat3 = StringField('sat3')
    sun3 = StringField('sun3')
    state = SelectField('狀態', choices=[('progressing', '進行中'), ('successed', '成功'), ('failed', '失敗')])
    submit = SubmitField('紀錄')

    # start_date = DateField('開始日期', format='%m/%d/%Y', render_kw={"placeholder": "10/03/2001"}) #  有format 不需要 validators=[DataRequired()]
    #end_date = DateField('結束日期', format='%m/%d/%Y', render_kw={"placeholder": "月月/日日/年年年年"})

    #repeat = SelectMultipleField('星期幾', choices =[('Mon', '一'), ('Tue', '二'), ('Wed', '三'), ('Thu', '四'), ('Fri', '五'), ('Sat', '六'), ('Sun', '日')])
    #time = TimeField('執行時間') # 因為timefield有版本問題因此用html
 


class TestForm(FlaskForm):
    mon = StringField('mon')
    tue = StringField('tue')
    wed = StringField('wed')
    thu = StringField('thu')
    fri = StringField('fri')
    sat = StringField('sat')
    sun = StringField('sun')
    sub = SubmitField('提交')
