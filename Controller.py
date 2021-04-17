from Model import Record, Summary, User
from sqlalchemy import and_
from database import db
import datetime
from chinese_calendar import is_holiday


# param: userid int
# clocktime datetime.datetime xx-xx-xx xx:xx:xx
# 在该函数处还需要判断打卡时间，若检测打卡时间为下午，则自动计算当天时长并插入数据库中
def clockIn(userId, clockTime):
    res = Record.query.filter(
        and_(
            Record.time.like('{}%'.format(clockTime.isoformat(' ').split()[0])),
            Record.user_id == userId
        )
    ).order_by(Record.time).all()
    print('a1', res)
    # 判断当天是否已打卡两次
    if len(res) > 1:
        return False
    data = Record(userId, clockTime)
    db.session.add(data)
    # 法定假日
    if is_holiday(clockTime):
        if len(res) == 1:
            res = Record.query.filter(
                and_(
                    Record.time.like('{}%'.format(clockTime.isoformat(' ').split()[0])),
                    Record.user_id == userId
                )
            ).order_by(Record.time).all()
            dura = (res[1].time - res[0].time).total_seconds()
            dura = format(dura / 3600., '.2f')
            data = Summary(res[0].user_id, res[0].time.year, res[0].time.month, res[0].time.day, dura)
            db.session.add(data)
        db.session.commit()
        return True
    else:  # 工作日
        # if clockoff, compute overtime duration
        hms = clockTime.time()
        if hms > datetime.time.fromisoformat('17:00:00'):
            assert len(res) == 1
            res = Record.query.filter(
                and_(
                    Record.time.like('{}%'.format(clockTime.isoformat(' ').split()[0])),
                    Record.user_id == userId
                )
            ).order_by(Record.time).all()
            print("dura: ", res)
            dura = computeDurationPerDay(res[0].time, res[1].time)
            data = Summary(res[0].user_id, res[1].time.year, res[1].time.month, res[1].time.day, dura)
            db.session.add(data)
        db.session.commit()
        return True


# param: start,end datetime
# return: int overwork length(s)
def computeDurationPerDay(start, end):
    dividing_line = 9*60*60 + 40*60
    dura = (end - start).total_seconds()
    if dura < dividing_line:
        return 0
    else:
        return format((dura - dividing_line) / 3600., '.2f')


# param: userid int, year int, month int,
# return: list
def getDurationByUserId(user_id, y, m):
    res = Summary.query.filter_by(user_id=user_id, year=y, month=m).all()
    print([i.duration for i in res])
    return [i.duration for i in res]


def getStatusByYM(y, m):
    res = User.query.filter().all()
    items = []
    for each in res:
        duration = round(sum(getDurationByUserId(each.id, y, m)), 2)
        clock_time = Record.query.filter(
            and_(
                Record.time.like('{}%'.format(datetime.date.today().isoformat())),
                Record.user_id == each.id
            )
        ).order_by(Record.time).all()
        clock_time = [i.time for i in clock_time]
        if len(clock_time) < 1:  # 当日未打卡
            clock_time.append("Haven't clocked in.")
            tol = "Haven't clocked in."
            toe = "Haven't clocked in."
        else:
            tol = clock_time[0] + datetime.timedelta(seconds=(9*60*60 + 600))
            toe = tol + datetime.timedelta(seconds=1800)
        item = {'user_id': each.id, 'username': each.username, 'duration': duration, 'attend': clock_time[0],
                'tol': tol, 'toe': toe}
        if len(clock_time) == 2:
            item['status'] = False
        else:
            item['status'] = True
        items.append(item)
    return items


def getAllUsername():
    return User.query.filter().all()


def getTodayStatus():
    users = getAllUsername()
    res = []
    for each in users:
        temp = {'username': each.username, 'id': '#'}
        res.append(temp)
        clock_time = Record.query.filter(
            and_(
                Record.time.like('{}%'.format(datetime.date.today().isoformat())),
                Record.user_id == each.id
            )
        ).order_by(Record.time).all()
        if len(clock_time) == 0:
            temp['come'] = 'NO DATA'
            temp['leave'] = 'NO DATA'
        elif len(clock_time) == 1:
            temp['come'] = clock_time[0].time.time().isoformat()
            temp['leave'] = 'NO DATA'
        else:
            temp['come'] = clock_time[0].time.time().isoformat()
            temp['leave'] = clock_time[1].time.time().isoformat()
            temp['id'] = clock_time[1].id
    return res


def deleteRecordById(record_id):
    res = Record.query.filter_by(id=record_id).first()
    db.session.delete(res)
    res = Summary.query.filter(
        and_(
            Summary.user_id == res.user_id,
            Summary.year == datetime.date.today().year,
            Summary.month == datetime.date.today().month,
            Summary.day == datetime.date.today().day
        )
    ).first()
    if res:
        db.session.delete(res)
    db.session.commit()
