from flask import Flask, render_template, request, make_response, redirect, url_for
from database import DB
from datetime import datetime

app = Flask(__name__)
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

    """
    Если в результате ничего не найдено, тогда добавляем новую запись, 
    иначе обновляем уже текущую запись
    """
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

def get_fix_info(fix_status):
    info = ''
    if fix_status == 1:
        info = "Ваш визит зафиксирован!"
    elif fix_status == 2:
        info = "Не удалось зафиксировать ваш визит!"
    elif fix_status == 3:
        info = "Неверный логин или пароль!"

    return info

@app.route('/send_mail/<type>')
def send_mail(type=''):
    return redirect(url_for('index'))

@app.route('/')
@app.route('/<int:fix_visit>')
def index(fix_visit=0):
    _username = "" if not request.cookies.get('username') else request.cookies.get('username')
    info = get_fix_info(fix_visit)
    
    return render_template('index.html', username=_username, login_info = info)

@app.route('/login', methods=['POST'])
def login():
    """Авторизация или регистрация пользователя, сохранение cookie"""
    info = None
    _username = request.form['login']
    _passw = request.form['password']
    curr_time = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
    fix_success = 0
    if valid_login(_username, _passw):
        try:
            fix_visit(_username, _passw, curr_time)
            fix_success = 1
        except:
            info = 'Не удалось зафиксировать время. Попробуйте ещё раз!'
            fix_success = 2
    else:
        fix_success = 3
        info = "Неверный логин или пароль"

    resp = redirect(url_for('index', fix_visit=fix_success))
    resp.set_cookie('username', _username, expires = datetime(2020, 12, 31))

    return resp

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
    