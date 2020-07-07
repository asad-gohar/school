try:
    from flask_socketio import SocketIO, send
    import os
    from flask import Flask, render_template, request, redirect, url_for, g, session, jsonify, json, send_file
    from flask_sqlalchemy import SQLAlchemy
    from flask_sqlalchemy import SQLAlchemy
    from sqlalchemy import and_, desc, func
    from sqlalchemy import or_
    from click import File
    import smtplib
    import smtplib
    from email.message import EmailMessage
    import stripe
    import random
    import datetime

    print("found")
except:
    print("not found d")

print("aaa")
myApp = Flask(__name__)
myApp.secret_key = os.urandom(24)
socketio = SocketIO(myApp)
project_dir = os.path.abspath(os.path.dirname(__file__))
print(project_dir)
print("=" * 100)

database_file = "sqlite:///{}".format(os.path.join(project_dir, "School.db"))
myApp.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(myApp)


class Admin(db.Model):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    email = db.Column(db.String(40), unique=False, nullable=False)
    password = db.Column(db.String(40), unique=False, nullable=False)
    img = db.Column(db.String(40), unique=False, nullable=True)


class User(db.Model):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    email = db.Column(db.String(40), unique=False, nullable=False)
    password = db.Column(db.String(40), unique=False, nullable=False)
    img = db.Column(db.String(40), unique=False, nullable=True)
    first_name = db.Column(db.String(40), unique=False, nullable=False)
    last_name = db.Column(db.String(40), unique=False, nullable=False)
    phone = db.Column(db.String(40), unique=False, nullable=False)
    account_username = db.Column(db.String(40), unique=False, nullable=False)


class Exam(db.Model):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    subject = db.Column(db.String(40), unique=False, nullable=False)
    question = db.Column(db.String(40), unique=False, nullable=False)
    A = db.Column(db.String(40), unique=False, nullable=True)
    B = db.Column(db.String(40), unique=False, nullable=False)
    C = db.Column(db.String(40), unique=False, nullable=False)
    D = db.Column(db.String(40), unique=False, nullable=False)
    E = db.Column(db.String(40), unique=False, nullable=False)


class Notification(db.Model):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    notifications = db.Column(db.Integer, unique=False, nullable=False)
    price = db.Column(db.Integer, unique=False, nullable=False)
    mail = db.Column(db.Integer, unique=False, nullable=False)


class News(db.Model):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    Name = db.Column(db.Integer, unique=False, nullable=False)
    img = db.Column(db.String(40), unique=False, nullable=True)
    date = db.Column(db.String(40), unique=False, nullable=True)
    Description = db.Column(db.String(40), unique=False, nullable=True)


class Store(db.Model):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    name = db.Column(db.Integer, unique=False, nullable=False)
    img = db.Column(db.String(40), unique=False, nullable=True)
    file = db.Column(db.String(40), unique=False, nullable=True)
    catagory = db.Column(db.String(40), unique=False, nullable=True)
    Price = db.Column(db.String(40), unique=False, nullable=True)


class Comment(db.Model):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    post_id = db.Column(db.Integer, unique=False, nullable=False)
    message = db.Column(db.String(500), unique=False, nullable=False)
    user = db.Column(db.String(500), unique=False, nullable=False)
    img = db.Column(db.String(40), unique=False, nullable=True)
    email = db.Column(db.String(40), unique=False, nullable=False)


db.create_all()


@socketio.on('message')
def handleMessage(msg, post, user, img, email):
    if img == "":
        img = None

    print('img=', img)
    message = Comment(message=msg, post_id=post, user=user, img=img, email=email)
    if msg != "User has connected!":
        db.session.add(message)
        db.session.commit()

    send(msg, broadcast=True)


@myApp.route('/comment')
def all_data():
    # dates = Movie.query.filter_by(movie_name="asad").all()

    all_data = Comment.query.order_by(-Comment.id).limit(1).first()
    dataArray = []
    Obj = {}
    Obj["message"] = all_data.message
    Obj["user"] = all_data.user
    Obj["pic"] = all_data.img
    Obj["email"] = all_data.email
    dataArray.append(Obj)
    return jsonify({'all_data': dataArray})


@myApp.route('/')
def home():
    check = -1
    totalnumber = 0
    currentnum = 0
    session["check"] = check

    session["totalnumber"] = totalnumber

    session["currentnum"] = currentnum
    postNum = News.query.all()
    userNum = User.query.all()
    postNumber = len(postNum)
    userNumber = len(userNum)

    posts = News.query.order_by(-News.id).limit(10).all()
    user = User.query.filter_by(email=g.User).first()

    if g.User:
        if user.img is None or user.img == "":
            src = "https://img.icons8.com/metro/100/000000/user-male-circle.png"
            return render_template("index.html", src=src, Login="", Logout="d-none", post=posts, name=user.first_name,
                                   postNumber=postNumber, userNumber=userNumber)
        userpic = g.User
        userpic = userpic.split("@")
        userpic = userpic[0]
        scr = "../static/profile_pic/" + userpic + "/" + user.img
        return render_template("index.html", Login="", Logout="d-none", src=scr, post=posts, user=user,
                               name=user.first_name, postNumber=postNumber, userNumber=userNumber)
    return render_template("index.html", Login="d-none", Logout="", post=posts, postNumber=postNumber,
                           userNumber=userNumber)


@myApp.route('/signup', methods=["POST", "GET"])
def signup():
    if request.method == "POST":

        session['OPT'] = random.randint(1000, 9999)
        print(session['OPT'])
        g.OPT = session['OPT']

        user1 = User.query.all()
        # img = request.files["ProfilPic"]

        # img = request.files["ProfilPic"]
        # user.img = img.filename

        session['Fname'] = request.form["fname"]
        session['lname'] = request.form["lname"]
        session['Phone'] = request.form["Phone"]
        session['Account'] = request.form["Account"]
        session['Signupmail'] = request.form["Email"]
        session['Signupass'] = request.form["password"]

        for u in user1:
            if u.email == g.Signupmail:
                return render_template("signup.html", email=g.Signupmail, error="Email Exist")

        session['Singup_user'] = g.Signupmail
        EMAIL_ADDRESS = "rock44576@gmail.com"
        EMAIL_PASSWORD = "yahoo.com.12"

        msg = EmailMessage()
        msg['Subject'] = 'Mr. Asad Massage you'
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = request.form["Email"]

        msg.set_content('Your one time OPT is  ' + '<b>' + str(g.OPT) + '</b>', subtype='html')

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)

        return render_template("confirm.html")
    return render_template("signup.html")


@myApp.route('/upload-Exam', methods=["POST", "GET"])
def upload_Exam():
    if request.method == "POST":
        subject = request.form["subject"]

        return redirect(url_for("upload", subject=subject))
    return render_template("404.html")


@myApp.route('/upload-Exam/<subject>', methods=["POST", "GET"])
def upload(subject):
    print(subject)
    return render_template("examform.html", subject=subject)


@myApp.route('/Exam-post', methods=["POST", "GET"])
def Exampost():
    if request.method == "POST":
        exam = Exam()
        subject = request.form["subject"]
        print(subject)
        Question = request.form["Question"]
        A = request.form["A"]
        B = request.form["B"]
        C = request.form["C"]
        D = request.form["D"]
        E = request.form["E"]
        exam.subject = subject
        exam.question = Question
        exam.A = A
        exam.B = B
        exam.C = C
        exam.D = D
        exam.E = E
        db.session.add(exam)
        db.session.commit()

        return redirect(url_for("upload", subject=subject))
    return render_template("404.html")


@myApp.route('/resentOPt')
def resentOPt():
    print('=', g.Signupmail)
    if g.Signupmail:
        g.OPT = random.randint(1000, 9999)
        EMAIL_ADDRESS = "rock44576@gmail.com"
        EMAIL_PASSWORD = "yahoo.com.12"

        msg = EmailMessage()
        msg['Subject'] = 'Mr. Asad Massage you'
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = g.Signupmail

        msg.set_content('Your first time OPT is  ' + '<b>' + str(g.OPT) + '</b>', subtype='html')

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)

        return render_template("confirm.html")
    return render_template("404.html")


@myApp.route('/comfirm', methods=['POST', 'GET'])
def comfirm():
    if g.Signupmail:
        userpic = g.Signupmail
        userpic = userpic.split("@")
        userpic = userpic[0]
        print(userpic)

        target_img = os.path.join(project_dir, 'static/profile_pic/' + userpic)
        if not os.path.isdir(target_img):
            os.mkdir(target_img)

        if g.OPT == int(request.form["OPT"]):
            user = User()
            # img = request.files["ProfilPic"]
            # user.img = img.filename

            user.email = g.Signupmail
            user.password = g.Signupass
            user.first_name = g.fname
            user.last_name = g.lname
            user.phone = g.Phone
            user.account_username = g.Account
            db.session.add(user)
            db.session.commit()
            notifi = Notification.query.filter_by(id=1).first()
            notifi.notifications = notifi.notifications + 1
            db.session.add(notifi)

            # signup mail
            EMAIL_ADDRESS = "rock44576@gmail.com"
            EMAIL_PASSWORD = "yahoo.com.12"

            msg = EmailMessage()
            msg['Subject'] = 'Mr. Asad Massage you'
            msg['From'] = EMAIL_ADDRESS
            msg['To'] = g.Signupmail

            msg.set_content('<b>' + "singu" + '</b>', subtype='html')

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                smtp.send_message(msg)
            # destination = "/".join([target_img, user.img])
            # img.save(destination)
            g.OPT = 0
            return redirect(url_for("signup"))
        return render_template("confirm.html", msg="invalid")
    return redirect(url_for("signup"))


# login
@myApp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        Email = request.form["Email"]
        password = request.form["password"]
        password2 = request.form.get('rememberme')
        print("password2:", password2)
        Adminuser = Admin.query.filter_by(email=Email).first()
        user = User.query.filter_by(email=Email).first()

        if Adminuser:
            if Adminuser.password == password:
                session['AdminUser'] = request.form["Email"]
                return redirect(url_for("MyAdmin"))
            else:

                return render_template("login.html", msg="Invalid Passowrd")
        elif user:

            if user.password == password:
                session['User'] = request.form["Email"]

                session['first_name'] = user.first_name
                print(" name=", session['first_name'])
                if g.Post_id:
                    print("Post_id=", g.Post_id)
                    return redirect(url_for("posts"))
                return redirect(url_for("profile"))

            else:

                return render_template("login.html", msg="Invalid Passowrd")
        else:
            return render_template("login.html", msg1="Invalid Email")

    return render_template("login.html")


@myApp.route('/logout')
def logout():
    if g.User:
        session.pop("User", None)
    if g.AdminUser:
        session.pop("AdminUser", None)
    return redirect(url_for("home"))


@myApp.route('/profile')
def profile():
    if g.User:
        user = User.query.filter_by(email=g.User).first()

        userpic = g.User
        userpic = userpic.split("@")
        userpic = userpic[0]
        print(userpic)
        if user.img is None:
            src = "https://img.icons8.com/metro/100/000000/user-male-circle.png"
            return render_template("userdashboard.html", src=src, name=user.first_name, user=user)

        scr = "../static/profile_pic/" + userpic + "/" + user.img
        return render_template("userdashboard.html", src=scr, name=user.first_name, user=user)
    return redirect(url_for("login"))


@myApp.route('/MyAdmin')
def MyAdmin():
    if g.AdminUser:
#         userpic = g.AdminUser
#         userpic = userpic.split("@")
#         userpic = userpic[0]
#         admin = Admin.query.filter_by(email=g.AdminUser).first()
 
# #         if admin.img is None:
# #             src = "https://img.icons8.com/metro/100/000000/user-male-circle.png"
# #             return render_template("Myadmin.html", admin=admin, src=src, name=userpic)

        
        return render_template("Myadmin.html", admin=admin, src="aa", name=userpic)
    return redirect(url_for("login"))


@myApp.route('/post', methods=['GET', 'POST'])
def post():
    if request.method == 'POST':
        target_img = os.path.join(project_dir, 'static/Post')
        if not os.path.isdir(target_img):
            os.mkdir(target_img)
        news = News()
        news.Name = request.form["name"]
        img = request.files["photo"]
        news.img = img.filename
        news.date = request.form["Release_Date"]
        news.Description = request.form["textarea"]

        db.session.add(news)
        db.session.commit()
        destination = "/".join([target_img, news.img])
        img.save(destination)
        return redirect(url_for("MyAdmin"))
    return render_template("404.html")


@myApp.route('/News', methods=['GET', 'POST'])
def news():
    if request.method == 'GET':
        return redirect(url_for("posts"))
    news_id = request.form["id"]
    print("id=", news_id)
    session['Post_id'] = news_id
    if request.method == 'POST':
        if g.User:

            user = User.query.filter_by(email=g.User).first()
            userpic = g.User
            userpic = userpic.split("@")
            userpic = userpic[0]
            name = user.first_name
            img = user.img
            print(g.User, img)
            news1 = News.query.filter_by(id=news_id).first()
            messsage = Comment.query.filter_by(post_id=news_id).all()

            if img is None:
                src = "https://img.icons8.com/metro/100/000000/user-male-circle.png"

                return render_template("news.html", news=news1, messsage=messsage, Login="", Logout="d-none", scr=src,
                                       news_id=news_id, user=name,
                                       email=userpic)

            scr = "../static/profile_pic/" + userpic + "/" + img

            return render_template("news.html", news=news1, scr=scr, messsage=messsage, Login="", Logout="d-none",
                                   news_id=news_id, user=name, img=img,
                                   email=userpic)
        return redirect(url_for("login"))
    return redirect(url_for("home"))


@myApp.route('/news')
def posts():
    if g.User:

        user = User.query.filter_by(email=g.User).first()
        userpic = g.User
        userpic = userpic.split("@")
        userpic = userpic[0]
        name = user.first_name
        img = user.img
        print(g.User, img)
        news1 = News.query.filter_by(id=g.Post_id).first()
        messsage = Comment.query.filter_by(post_id=g.Post_id).all()

        if img is None:
            src = "https://img.icons8.com/metro/100/000000/user-male-circle.png"

            return render_template("news.html", news=news1, messsage=messsage, Login="", Logout="d-none", scr=src,
                                   news_id=g.Post_id, user=name,
                                   email=userpic)

        scr = "../static/profile_pic/" + userpic + "/" + img

        return render_template("news.html", news=news1, scr=scr, messsage=messsage, Login="", Logout="d-none",
                               news_id=g.Post_id, user=name, img=img,
                               email=userpic)
    return redirect(url_for("login"))


@myApp.route('/subject/<v>')
def subject(v):
    jamb = ["Accounts", "Agricultural Science", "Biology", "Chemistry", "Christian Religious Knowledge", "Commerce",
            "Economics", "English Language", "Fine Arts", "French", "Geography", "Government", "Hausa"
        , "History", "Home Economics", "Igbo", "Islamic Religious Knowledge", "Literature In English", "Mathematics",
            "Physics", "Sweet Sixteen", "Yoruba"]

    waec = ["Accounts", "Agricultural Science", " Biology", "Chemistry", "Christian Religious Knowledge", "Commerce",
            "Computer Studies", "Economics", "English Language", "Geography", "Government",
            "Literature In English", "Mathematics", "Physics"]

    neco = ["Biology", "Chemistry", "Commerce", "Computer Studies",
            "Economics", "English Language", "Government", "Mathematics",
            "Physics"]

    subject = []
    if v == "jamb":
        subject = jamb
        return jsonify(subject)
    elif v == "waec":
        subject = waec
        return jsonify(subject)
    else:
        subject = neco
        return jsonify(subject)


@myApp.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        form = request.form
        search_value = form['search_string']
        search = "%{0}%".format(search_value)
        posts = News.query.filter(News.Name.like(search)).all()
        user = User.query.filter_by(email=g.User).first()
        if len(posts) == 0:
            return render_template("404.html")

        if g.User:
            if user.img is None or user.img == "":
                src = "https://img.icons8.com/metro/100/000000/user-male-circle.png"
                return render_template("latestnews.html", src=src, Login="", Logout="d-none", post=posts,
                                       name=user.first_name)
            userpic = g.User
            userpic = userpic.split("@")
            userpic = userpic[0]
            scr = "../static/profile_pic/" + userpic + "/" + user.img
            return render_template("latestnews.html", Login="", Logout="d-none", src=scr, post=posts, user=user,
                                   name=user.first_name)
        return render_template("latestnews.html", Login="d-none", Logout="", post=posts)
    return render_template("latestnews.html", Login="d-none", Logout="")


@myApp.route('/Exam', methods=['GET', 'POST'])
def test():
    if request.method == "POST":
        user = User.query.filter_by(email=g.User).first()
        exam = request.form["exam_body"]
        time = request.form["exam_mode"]
        subject = request.form["subject"]
        list_subject = request.form.getlist('Chaked')
        print(list_subject)
        print(subject)
        if subject == "1":
            if exam == "jamb":
                list_subject.insert(0, "English Language")
                print("bh=", list_subject)

                print(list_subject[0])
            question = Exam.query.filter_by(subject=list_subject[0]).order_by(func.random()).all()
            subject1 = list_subject
            paper = list_subject[0]

            list_subject.remove(list_subject[0])
            print("pr=", list_subject)

            print("paper=", paper)
        else:
            question = Exam.query.filter_by(subject=subject).order_by(func.random()).all()
            subject1 = list_subject
            paper = subject
            list_subject.remove(subject)
            print("pr=", list_subject)

            print("paper=", paper)

        if subject == "0" or subject == 0:
            return str(g.totalnumber)

        if len(list_subject) == 0:
            list_subject = "0"
            if g.User:
                if user.img is None or user.img == "":
                    src = "https://img.icons8.com/metro/100/000000/user-male-circle.png"
                    return render_template("index.html", src=src, Login="", Logout="d-none", post=posts,
                                           name=user.first_name)
                userpic = g.User
                userpic = userpic.split("@")
                userpic = userpic[0]
                scr = "../static/profile_pic/" + userpic + "/" + user.img
                return render_template("exam.html", Login="", Logout="d-none", src=scr, list=list_subject,
                                       question=question, time=time, exam=paper, exam_body=exam, v="hidden", user=user,
                                       name=user.first_name)
            return render_template("exam.html", Login="d-none", Logout="", list=list_subject, question=question,
                                   time=time, exam=paper, exam_body=exam, v="hidden")

        if g.User:
            if user.img is None or user.img == "":
                src = "https://img.icons8.com/metro/100/000000/user-male-circle.png"
                return render_template("index.html", src=src, Login="", Logout="d-none", post=posts,
                                       name=user.first_name)
            userpic = g.User
            userpic = userpic.split("@")
            userpic = userpic[0]
            scr = "../static/profile_pic/" + userpic + "/" + user.img
            return render_template("exam.html", Login="", Logout="d-none", src=scr, list=list_subject,
                                   question=question, time=time, exam=paper, exam_body=exam, v="visible", user=user,
                                   name=user.first_name)
        return render_template("exam.html", Login="d-none", Logout="", list=list_subject, question=question, time=time,
                               exam=paper, exam_body=exam, v="visible")

    return redirect(url_for("profile"))


@myApp.route('/quit', methods=['GET', 'POST'])
def quit():
    return render_template("scroce.html",totalnumber="g.totalnumber")


@myApp.route('/Examevaluation', methods=['GET', 'POST'])
def Examevaluation():
    if request.method == "POST":
        answer = request.form["answer"]
        subject_id = request.form["subject_id"]
        print(g.check)

        if subject_id != g.check:
            option = Exam.query.filter_by(id=subject_id).first()
            session["check"] = option.id
            g.check = session["check"]
            print("g.check=", g.check)
            if option.E == answer:
                session["currentnum"] = 2
                g.currentnum = session["currentnum"]
                session["totalnumber"] = g.totalnumber + g.currentnum
                g.totalnumber = session["totalnumber"]

                print("g.totalnumber=", g.totalnumber)
            else:
                session["currentnum"] = 0
                g.currentnum = session["currentnum"]

        return jsonify("hello wprld")
    return render_template("404.html")


@myApp.route('/evaluation', methods=['GET', 'POST'])
def evaluation():
    session["totalnumber"] = g.totalnumber - g.currentnum
    print("g.totalnumber - =", g.totalnumber)
    answer = request.form["answer"]
    subject_id = request.form["subject_id"]
    option = Exam.query.filter_by(id=subject_id).first()
    if option.E == answer:

        session["currentnum"] = 2
        g.currentnum = session["currentnum"]
        session["totalnumber"] = g.totalnumber + g.currentnum
        g.totalnumber = session["totalnumber"]

        print("g.totalnumber=", g.totalnumber)
    else:
        session["currentnum"] = 0
        g.currentnum = session["currentnum"]

    return jsonify("hello wprld")


@myApp.route('/search_store', methods=['GET', 'POST'])
def search_store():
    if request.method == 'POST':
        form = request.form
        search_value = form['search_string']
        search = "%{0}%".format(search_value)
        store = Store.query.filter(Store.name.like(search)).all()
        user = User.query.filter_by(email=g.User).first()
        if len(store) == 0:
            return render_template("404.html")

        if g.User:
            if user.img is None or user.img == "":
                src = "https://img.icons8.com/metro/100/000000/user-male-circle.png"
                return render_template("store.html", src=src, Login="", Logout="d-none", store=store,
                                       name=user.first_name)
            userpic = g.User
            userpic = userpic.split("@")
            userpic = userpic[0]
            scr = "../static/profile_pic/" + userpic + "/" + user.img
            return render_template("store.html", Login="", Logout="d-none", store=store, src=scr, user=user,
                                   name=user.first_name)
        return redirect(url_for("home"))
    return redirect(url_for("home"))


@myApp.route('/Library', methods=['GET', 'POST'])
def Library():
    user = User.query.filter_by(email=g.User).first()

    library = Store.query.filter_by(Price="free").order_by(-Store.id).all()


    if g.User:
        if user.img is None or user.img == "":
            src = "https://img.icons8.com/metro/100/000000/user-male-circle.png"
            return render_template("library.html", src=src, Login="", Logout="d-none", name=user.first_name,
                                   library=library
                                   )
        userpic = g.User
        userpic = userpic.split("@")
        userpic = userpic[0]
        scr = "../static/profile_pic/" + userpic + "/" + user.img
        return render_template("library.html", Login="", Logout="d-none", src=scr, user=user,
                               name=user.first_name, library=library)
    return render_template("library.html", Login="d-none", Logout="", user=user, library=library)


@myApp.route('/store', methods=['GET', 'POST'])
def store():
    user = User.query.filter_by(email=g.User).first()
    store = Store.query.order_by(-Store.id).all()
    Stories = Store.query.filter_by(catagory="Stories").order_by(-Store.id).all()
    Novel = Store.query.filter_by(catagory="Novel").order_by(-Store.id).all()
    Text_books = Store.query.filter_by(catagory="Text books").order_by(-Store.id).all()
    Softwares = Store.query.filter_by(catagory="Softwares").order_by(-Store.id).all()

    if g.User:
        if user.img is None or user.img == "":
            src = "https://img.icons8.com/metro/100/000000/user-male-circle.png"
            return render_template("store.html", src=src, Login="", Logout="d-none", store=store, name=user.first_name,
                                   Stories=Stories, Novel=Novel, Text_books=Text_books, Softwares=Softwares)
        userpic = g.User
        userpic = userpic.split("@")
        userpic = userpic[0]
        scr = "../static/profile_pic/" + userpic + "/" + user.img
        return render_template("store.html", Login="", Logout="d-none", store=store, src=scr, user=user,
                               name=user.first_name, Stories=Stories, Novel=Novel, Text_books=Text_books,
                               Softwares=Softwares)
    return redirect(url_for("home"))


@myApp.route('/store_item', methods=['GET', 'POST'])
def store_item():
    if request.method == "POST":
        target_img = os.path.join(project_dir, 'static/images/store/images')
        if not os.path.isdir(target_img):
            os.mkdir(target_img)
        target_file = os.path.join(project_dir, 'static/images/store/files')
        if not os.path.isdir(target_file):
            os.mkdir(target_file)
        store = Store()
        store.name = request.form["name"]
        img = request.files["item"]
        store.img = img.filename
        file = request.files["file"]
        store.catagory = request.form["Category"]
        store.Price = request.form["price"]
        store.file = file.filename
        db.session.add(store)
        db.session.commit()
        destination = "/".join([target_img, store.img])
        destination1 = "/".join([target_file, store.file])
        img.save(destination)
        file.save(destination1)
        return redirect(url_for("MyAdmin"))
    return render_template("404.html")


@myApp.route('/latest_news', methods=['GET', 'POST'])
def latesnew():
    posts = News.query.order_by(-News.id).all()
    user = User.query.filter_by(email=g.User).first()

    if g.User:
        if user.img is None or user.img == "":
            src = "https://img.icons8.com/metro/100/000000/user-male-circle.png"
            return render_template("latestnews.html", src=src, Login="", Logout="d-none", post=posts,
                                   name=user.first_name)
        userpic = g.User
        userpic = userpic.split("@")
        userpic = userpic[0]
        scr = "../static/profile_pic/" + userpic + "/" + user.img
        return render_template("latestnews.html", Login="", Logout="d-none", src=scr, post=posts, user=user,
                               name=user.first_name)
    return render_template("latestnews.html", Login="d-none", Logout="", post=posts)


@myApp.route('/download', methods=['GET', 'POST'])
def download():
    if request.method == "POST":
        file_id = request.form["file_id"]
        file = Store.query.filter_by(id=file_id).first()

        path = "static/images/store/files/" + file.file

        return send_file(path, as_attachment=True)
    return render_template("404.html")


@myApp.route('/update', methods=["POST", "GET"])
def update():
    if request.method == "POST":
        if g.User:
            userpic = g.User
            userpic = userpic.split("@")
            userpic = userpic[0]
        else:
            userpic = g.AdminUser
            userpic = userpic.split("@")
            userpic = userpic[0]

        target_img = os.path.join(project_dir, 'static/profile_pic/' + userpic)
        if not os.path.isdir(target_img):
            os.mkdir(target_img)

        if g.User:
            user = User.query.filter_by(email=g.User).first()
            removepic = user.img
            user.password = request.form["confirm"]
            user.first_name = request.form["fname"]
            user.last_name = request.form["lname"]
            user.account_username = request.form["Account"]
            user.phone = request.form["Phone"]
            user.email = request.form["Email"]
            user_pic = request.files["photo"]
            user.img = user_pic.filename
            print(removepic)
            print("user.img=", user.img)

            if user.img == "":
                user.img = removepic
                db.session.add(user)
                db.session.commit()
                return redirect(url_for("profile"))
            db.session.add(user)
            db.session.commit()
            if removepic is None or removepic == "":
                print("nome")
                destination = "/".join([target_img, user.img])
                user_pic.save(destination)
                return redirect(url_for("profile"))
            os.remove(target_img + '/' + removepic)
            destination = "/".join([target_img, user.img])
            user_pic.save(destination)
            return redirect(url_for("profile"))

        if g.AdminUser:
            admin = Admin.query.filter_by(email=g.AdminUser).first()
            removepic = admin.img
            admin.password = request.form["confirm"]
            admin_pic = request.files["photo"]
            admin.img = admin_pic.filename
            if admin.img == "":
                admin.img = removepic
                db.session.add(admin)
                db.session.commit()
                return redirect(url_for("MyAdmin"))

            print(removepic)
            db.session.add(admin)
            db.session.commit()
            if removepic == None:
                destination = "/".join([target_img, admin.img])
                admin_pic.save(destination)
                return redirect(url_for("MyAdmin"))
            os.remove(target_img + '/' + removepic)
            destination = "/".join([target_img, admin.img])
            admin_pic.save(destination)
            return redirect(url_for("MyAdmin"))
    return render_template("404.html")


@myApp.route('/404')
def not_fond():
    return render_template("404.html")


# put user in seesion
@myApp.before_request
def before_request():
    g.User = None
    g.AdminUser = None
    g.fname = None
    g.lname = None
    g.Account = None
    g.Phone = 0
    g.OPT = 0
    g.first_name = None
    g.Post_id = 0
    g.Signupmail = None
    g.Signupass = None
    g.check = -1
    g.totalnumber = 0
    g.currentnum = 0
    if 'totalnumber' in session:
        g.totalnumber = session["totalnumber"]
    if 'currentnum' in session:
        g.currentnum = session["currentnum"]

    if 'check' in session:
        g.check = session["check"]
    if 'Post_id' in session:
        g.Post_id = session['Post_id']
    if 'first_name' in session:
        g.first_name = session['first_name']
        print("names=", g.first_name)
    if 'Fname' in session:
        g.fname = session['Fname']
    if 'lname' in session:
        g.lname = session['lname']
    if 'Phone' in session:
        g.Phone = session['Phone']
    if 'Account' in session:
        g.Account = session['Account']

    if 'Signupass' in session:
        g.Signupass = session['Signupass']
    if 'Signupmail' in session:
        g.Signupmail = session['Signupmail']
    if 'OPT' in session:
        g.OPT = session['OPT']
        print(g.OPT)
    if 'AdminUser' in session:
        g.AdminUser = session['AdminUser']
    if 'User' in session:
        g.User = session['User']


if __name__ == "__main__":
    socketio.run(myApp)
