from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, FileField, IntegerField, SubmitField, EmailField
from wtforms.validators import Email, EqualTo, DataRequired, ValidationError
import string
from table import Users


class tovars(FlaskForm):
    type = StringField("Тип товара")
    name = StringField("Название товара")
    description = TextAreaField("Описание товара")
    brand = StringField("Бренд")
    price = IntegerField("Цена")
    photo = FileField("Фото")
    submit = SubmitField("Ок")


class   LoginForm(FlaskForm):
    login = StringField("Логин", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    submit = SubmitField("Войти")


class RegistrationForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()])
    email = EmailField('Почта', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password22 = PasswordField('Введите пароль ещё раз', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегестрироваться')


    def validate_password(self, password):

        errorscounter=0

        for i in self.password.data:

            if i in string.ascii_lowercase:
                errorscounter+=1
                break

        for i in self.password.data:

            if i in string.ascii_uppercase:
                errorscounter+=1
                break

        for i in self.password.data:
            if i in string.digits:
                errorscounter+=1
                break
        
        for i in self.password.data:
            if i in string.punctuation:
                errorscounter+=1
                break

        if errorscounter<4:
            raise ValidationError('invalid password! ')




    def validate_username(self, login):
        if self.login.data[0] not in string.ascii_letters:
            raise ValidationError('the first letter in login must be Latin')
        
        for i in self.login.data:
            if i not in string.digits + string.ascii_letters + '_':
                raise ValidationError('invalid characters')

        user = Users.query.filter_by(login=login.data).first()
        if user is not None:
            raise ValidationError('Пользователь с таким именем уже существует!')

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Пользователь с такой почтой уже существует!')


class CommentForm(FlaskForm):
    like = IntegerField(label=("Оценка"), validators=[DataRequired()])
    comment = TextAreaField("Комментарий")
    submit = SubmitField("Оставить комментарий")

    def validate_like(self, like):
        if self.like.data > 5 or self.like.data < 1:
            raise ValidationError('Оценка может быть только от 1 до 5')
