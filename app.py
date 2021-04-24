from flask import Flask, render_template, request, abort, flash, url_for, redirect
import config
from database import db
import Controller as ctl
import datetime
import calendar


app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


@app.route('/')
def index():
    items = ctl.getStatusByYM(2021, 4)
    color = ['bg-info', 'bg-success', 'bg-warning', 'bg-danger']
    img = ['ion-bag', 'ion-stats-bars', 'ion-person-add', 'ion-pie-graph']
    for i in range(4):
        items[i]['color'] = color[i]
        items[i]['img'] = img[i]
    return render_template('index.html', items=items)


@app.route('/submit/<userid>')
def submit(userid):
    if request.method == 'GET':
        if request.referrer is None:
            abort(403)
        clock_time = datetime.datetime.now()
        # clock_time = datetime.datetime.fromisoformat('2021-04-23 08:40:31')
        res = ctl.clockIn(int(userid), clock_time)
        if res:
            flash("You have clocked in successfully!")
            return redirect(url_for('index'))
        else:
            abort(400)
    else:
        return "这么喜欢搞事情啊gdx👎"


@app.route('/post', methods=['POST', 'GET'])
def handle():
    if request.method == "GET":
        res = ctl.getAllUsername()
        usernames = []
        for i in res:
            usernames.append({'id': i.id, 'username': i.username})
        daySum = calendar.monthrange(datetime.date.today().year, datetime.date.today().month)[1]
        return render_template('post.html', usernames=usernames, daysum=daySum)
    elif request.method == "POST":
        userid = request.form.get('username')
        year = datetime.date.today().year
        month = datetime.date.today().month
        day = int(request.form.get('day'))
        hour = int(request.form.get('hour'))
        minute = int(request.form.get('minute'))
        clock_time = datetime.datetime(year, month, day, hour, minute, 0)
        res = ctl.clockIn(int(userid), clock_time)
        if res:
            flash("You have paid up successfully!")
            return redirect(url_for('index'))
        else:
            abort(400)


@app.route('/status')
def status():
    items = ctl.getTodayStatus()
    print(items)
    style = {'date': datetime.date.today().isoformat()}
    return render_template('status.html', items=items, style=style)


@app.route('/delete/<record_id>')
def delete(record_id):
    ctl.deleteRecordById(record_id)
    return render_template('delete.html')


@app.errorhandler(400)
def badRequest(error):
    print(error)
    return render_template("error.html")


@app.errorhandler(403)
def Forbidden(error):
    return render_template("403.html")


if __name__ == '__main__':
    app.run()
