from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail

db.create_all()

app = Flask(__name__)

ENV = "prod"

if ENV == "dev":
    app.debug = True
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = "postgresql://postgres:Treynanhal@localhost/lexus"
else:
    app.debug = False
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = "postgres://zyjmontqioiyyr:0b7d38d45f1124f23978ed1002d4ca8a52d79c750864d13704d2a0436051c41a@ec2-52-1-115-6.compute-1.amazonaws.com:5432/d5qvmhbd5iej3a"


app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Feedback(db.Model):
    __tablename__ = "feedback"
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(200), unique=True)
    dealer = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())

    def __init__(self, customer, dealer, rating, comments):
        self.customer = customer
        self.dealer = dealer
        self.rating = rating
        self.comments = comments


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    if request.method == "POST":
        customer = request.form["customer"]
        dealer = request.form["dealer"]
        rating = request.form["rating"]
        comments = request.form["comments"]
        # print(customer, dealer, rating, comments)
        if customer == "" or dealer == "":
            return render_template("index.html", message="Enter required fields")
        if (
            db.session.query(Feedback).filter(Feedback.customer == customer).count()
            == 0
        ):
            data = Feedback(customer, dealer, rating, comments)
            db.session.add(data)
            db.session.commit()
            send_mail(customer, dealer, rating, comments)
            return render_template("success.html")
        return render_template(
            "index.html", message="You have already submitted feedback."
        )


if __name__ == "__main__":
    app.run()
