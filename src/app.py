from flask import Flask, render_template, request, make_response, redirect, url_for, flash
from database import DB
from datetime import datetime
from smtplib import SMTP
from random import randrange

app = Flask(__name__)
app.secret_key = 'some secret'
local_db = DB()


def valid_login(login, passw):
    """Проверяет, зарегистрирован пользователь или нет"""
    sql = 'select * from users where name = ? and password = ?'
    return False if local_db.__execute__(sql, [login, passw]) == [] else True

def fix_visit(login, passw, time_visit):
    """Фиксирует начало визита пользователя и последний его уход в течение дня"""
    sql = 'select id from users where name = ? and password = ?'
    result = local_db.__execute__(sql, [login, passw])

    if result==[]:
        raise ''
    # Получаем id пользователя
    id = result[0][0]

    # По id ищем записи в таблице "Visits" за текущий день
    sql = 'select * from Visits where user_id=? and datetime(dateFrom) between datetime(?) and datetime(?)'
    result = local_db.__execute__(sql, [id, datetime.strftime(datetime.now(), "%Y-%m-%d 00:00:00"), datetime.strftime(datetime.now(), "%Y-%m-%d 23:59:59")])

    #Если в результате ничего не найдено, тогда добавляем новую запись, 
    #иначе обновляем уже текущую запись
    
    if result == []:
        sql = 'INSERT INTO Visits VALUES (?,?,?)'
        local_db.__execute__(sql, [id, time_visit, ""])
    else:
        sql = 'UPDATE Visits SET dateTo=? where user_id=? and datetime(dateFrom) between datetime(?) and datetime(?)'
        local_db.__execute__(sql, [time_visit, id, datetime.strftime(datetime.now(), "%Y-%m-%d 00:00:00"), datetime.strftime(datetime.now(), "%Y-%m-%d 23:59:59")])

    local_db.connector.commit()

def get_fullName():
    """Формирует полное имя пользователя из составных частей (Ф.И.О)"""
    sb = []
    sb.append(request.form['login_part1']+' ')
    sb.append(request.form['login_part2']+' ')
    sb.append(request.form['login_part3'])

    return ''.join(sb)

def get_nextId():
    result = local_db.__execute__('select id from Users ORDER BY id DESC limit 1')
    id = int(result[0][0]) + 1
    return str(id)

def sendMail(recipient):
    pass


@app.route('/sMail')
@app.route('/sMail/<recipient>')
def get_sendMailForm(recipient=False):
    if not recipient:
        return render_template('sMail_form.html')
    else:
        try:
            sendMail(recipient)
        except
        return redirect('index')    

@app.route('/')
@app.route('/<int:fix_visit>')
def index(fix_visit=0):
    _username = "" if not request.cookies.get('username') else request.cookies.get('username')
    
    return render_template('index.html', username=_username)

@app.route('/login', methods=['POST'])
def login():
    """Авторизация или регистрация пользователя, сохранение cookie"""
    error = None
    _username = request.form['login']
    _passw = request.form['password']
    curr_time = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
    if valid_login(_username, _passw):
        try:
            fix_visit(_username, _passw, curr_time)
        except:
            error = 'Не удалось зафиксировать время. Попробуйте ещё раз!'
        else:
            flash("Ваш визит зафиксирован!")    
            resp = redirect(url_for('index'))
            resp.set_cookie('username', _username, expires = datetime(2020, 12, 31))

            return resp
    else:
        error = "Неверный логин или пароль"

    return render_template('index.html', username=_username, login_info=error)    

@app.route('/reg_form')
def reg_form():
    return render_template('reg_form.html')

@app.route('/reg_user', methods=['POST'])
def reg_user():
    """Регистрирует нового пользователя в системе"""
    sql = 'INSERT INTO Users VALUES (?, ?, ?, ?, ?)'
    param = [get_nextId(), get_fullName(), request.form['password'], request.form['e_mail'], request.form['phone']]
    local_db.__execute__(sql, param)
    local_db.connector.commit()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
    