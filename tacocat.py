from flask import Flask,g , render_template, redirect, url_for, flash
from flask.ext.bcrypt import check_password_hash
from flask.ext.login import LoginManager, login_required, login_user, logout_user, current_user
from models import DATABASE, initialize, User, Taco, DoesNotExist
from forms import SignUpForm, LoginForm, TacoForm

app = Flask(__name__)
app.secret_key = "hhbjbhjbkhbk13hb4kj1.j1k23l4bé1kl23j4b..1234$$$$@$"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@app.before_request
def before_request():
    g.db = DATABASE.connect()


@app.after_request
def after_request(response):
    DATABASE.close()
    return response


@login_manager.user_loader
def load_user(userid):
    try:
        return User.get(User.id == userid)
    except DoesNotExist:
        return None


@app.route("/register", methods=('GET', 'POST'))
def register():
    form = SignUpForm()
    if form.validate_on_submit():
        User.create_user(form.email.data, form.password.data)
        return redirect(url_for("index"))

    return render_template("register.html", form=form)


@app.route("/login", methods=('GET', 'POST'))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = User.get(User.email == form.email.data)
        except DoesNotExist:
            flash("Email or Password invalid", "error")
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("You're successfully logued in", "success")
                return redirect(url_for("index"))
            else:
                flash("Email or Password invalid", "error")

    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/taco", methods=('GET', 'POST'))
@login_required
def taco():
    form = TacoForm()
    if form.validate_on_submit():
        Taco.create(
            protein=form.protein.data,
            shell=form.shell.data,
            cheese=form.cheese.data,
            extras=form.extras.data,
            user=current_user._get_current_object()
        )
        return redirect(url_for("index"))

    return render_template("taco.html", form=form)


@app.route("/")
def index():
    return render_template("index.html", tacos=Taco.select())


if __name__ == "__main__":
    initialize()
    app.run(port=8000,debug=True, host="localhost")