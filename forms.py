# -*- encoding: utf-8 -*-
from includes import *

USERNAME_MIN_LEN = 4
USERNAME_MAX_LEN = 25


PASSWORD_MIN_LEN = 12
PASSWORD_MAX_LEN = 255

### SignIn 

class SignInForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=USERNAME_MIN_LEN, max=USERNAME_MAX_LEN)])
    password = PasswordField(validators=[InputRequired(), Length(min=PASSWORD_MIN_LEN, max=PASSWORD_MAX_LEN)])
    signin = SubmitField("Giriş Yap")

class ForgotMyPasswordForm(FlaskForm):
    email_address = StringField(validators=[InputRequired(), Length(min=8, max=50), Email()])
    send = SubmitField("Devam Et")

class NewPasswordForm(FlaskForm):
    new_password = PasswordField(validators=[InputRequired(), Length(min=PASSWORD_MIN_LEN, max=PASSWORD_MAX_LEN)])
    new_password_confirm = PasswordField(validators=[InputRequired(), Length(min=PASSWORD_MIN_LEN, max=PASSWORD_MAX_LEN)])
    change = SubmitField("Değiştir")

### SignUp 

class SignUpForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=USERNAME_MIN_LEN, max=USERNAME_MAX_LEN)])
    password = PasswordField(validators=[InputRequired(), Length(min=PASSWORD_MIN_LEN, max=PASSWORD_MAX_LEN)])
    email_address = StringField(validators=[InputRequired(), Length(min=8, max=50), Email()])
    recaptcha = RecaptchaField()
    signup = SubmitField("Kayıt Ol")

class NewProfileForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=USERNAME_MIN_LEN, max=USERNAME_MAX_LEN)])
    password = PasswordField(validators=[Length(max=PASSWORD_MAX_LEN)])
    create = SubmitField('Oluştur')

class WhoIsWatchingPasswordForm(FlaskForm):
    password = PasswordField(validators=[Length(max=PASSWORD_MAX_LEN)])
    enter = SubmitField('Giriş Yap')

### SettingsProfile

class SettingsProfileChangePasswordForm(FlaskForm):
    old_password = PasswordField(validators=[Length(max=PASSWORD_MAX_LEN)])
    new_password = PasswordField(validators=[Length(max=PASSWORD_MAX_LEN)])
    confirm_password = PasswordField(validators=[Length(max=PASSWORD_MAX_LEN)])
    change = SubmitField('Kaydet')

class SettingsProfileChangeUsernameForm(FlaskForm):
    new_username = StringField(validators=[InputRequired(), Length(min=USERNAME_MIN_LEN, max=USERNAME_MAX_LEN)])
    change = SubmitField('Kaydet')

class SettingsProfileCustomizationForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=USERNAME_MIN_LEN, max=USERNAME_MAX_LEN)])
    biography = TextAreaField(validators=[Length(max=PASSWORD_MAX_LEN)])
    change = SubmitField('Kaydet')

class SettingsProfileDropProfileConfirmationForm(FlaskForm):
    password = PasswordField(validators=[Length(max=PASSWORD_MAX_LEN)])
    drop = SubmitField('Profilimi Sil')

### SettingsAccount

class SettingsAccountConfirmEnterForm(FlaskForm):
    security_password = PasswordField(validators=[InputRequired(), Length(min=PASSWORD_MIN_LEN, max=PASSWORD_MAX_LEN)])
    enter = SubmitField('Devam Et')

class SettingsAccountChangePasswordForm(FlaskForm):
    old_password = PasswordField(validators=[InputRequired(), Length(min=PASSWORD_MIN_LEN, max=PASSWORD_MAX_LEN)])
    new_password = PasswordField(validators=[InputRequired(), Length(min=PASSWORD_MIN_LEN, max=PASSWORD_MAX_LEN)])
    confirm_password = PasswordField(validators=[InputRequired(), Length(min=PASSWORD_MIN_LEN, max=PASSWORD_MAX_LEN)])
    change = SubmitField('Değişiklikleri Kaydet')

class SettingsAccountChangeUsernameEmailForm(FlaskForm):
    new_username = StringField(validators=[InputRequired(), Length(min=USERNAME_MIN_LEN, max=USERNAME_MAX_LEN)])
    new_email_address = StringField(validators=[InputRequired(), Length(min=8, max=50), Email()])
    change = SubmitField('Değişiklikleri Kaydet')

class SettingsAccountChangeSecurityPasswordForm(FlaskForm):
    old_security_password = PasswordField(validators=[InputRequired(), Length(min=PASSWORD_MIN_LEN, max=PASSWORD_MAX_LEN)])
    new_security_password = PasswordField(validators=[InputRequired(), Length(min=PASSWORD_MIN_LEN, max=PASSWORD_MAX_LEN)])
    confirm_security_password = PasswordField(validators=[InputRequired(), Length(min=PASSWORD_MIN_LEN, max=PASSWORD_MAX_LEN)])
    change = SubmitField('Değişiklikleri Kaydet')

class SettingsAccountDropAccountConfirmationForm(FlaskForm):
    password = PasswordField(validators=[Length(max=PASSWORD_MAX_LEN)])
    drop = SubmitField('Hesabımı Sil')

### Collection 

class CollectionDiscoverSearchForm(FlaskForm):
    query = StringField("Aradığın oynatma listesinin adını veya etiketini gir.")
    search = SubmitField("Ara")

class NewCollectionForm(FlaskForm):
    title = StringField(validators=[InputRequired(), Length(min=USERNAME_MIN_LEN, max=USERNAME_MAX_LEN)])
    overview = TextAreaField(validators=[Length(max=PASSWORD_MAX_LEN)])
    create = SubmitField('Oluştur')

class CollectionEditForm(FlaskForm):
    new_title = StringField(validators=[InputRequired(), Length(min=USERNAME_MIN_LEN, max=USERNAME_MAX_LEN)])
    new_overview = StringField(validators=[Length(max=PASSWORD_MAX_LEN + 255)])
    change = SubmitField('Değiştir')

### Watch 

class WatchCommentForm(FlaskForm):
    text = TextAreaField(validators=[InputRequired(), Length(max=PASSWORD_MAX_LEN)])
    comment = SubmitField('Yorum Yap')

### Contact

class ContactForm(FlaskForm):
    name = StringField(validators=[InputRequired(), Length(min=USERNAME_MIN_LEN, max=USERNAME_MAX_LEN)])
    email_address = StringField(validators=[InputRequired(), Length(min=8, max=50), Email()])
    title = StringField(validators=[InputRequired(), Length(min=USERNAME_MIN_LEN, max=USERNAME_MAX_LEN)])
    message = TextAreaField(validators=[Length(max=PASSWORD_MAX_LEN)])
    recaptcha = RecaptchaField()
    send = SubmitField("Gönder")
