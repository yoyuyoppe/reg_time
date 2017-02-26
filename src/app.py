from flask import Flask, render_template, request, make_response
from database import DB
from datetime import datetime

app = Flask(__name__)
local_db = DB()



def valid_login(login, passw):
    """Проверяет, зарегистрирован пользователь или нет"""
    sql = 'select * from users where name = ? and password = ?'
    return False if local_db.__execute__(sql, [login, passw]) == [] else True

def fix_visit(time_visit):
    """Фиксирует начало визита пользователя и последний его уход в течение дня"""
    pass

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

@app.route('/')
def index():
    _username = "" if not request.cookies.get('username') else request.cookies.get('username')

    return render_template('index.html', username=_username)


@app.route('/login', methods=['POST'])
def login():
    """Авторизация или регистрация пользователя, сохранение cookie|"""
    info = None
    _username = request.form['login']
    _passw = request.form['password']
    curr_time = datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S")
    if valid_login(_username, _passw):
        info = 'Авторизация прошла успешно '+ curr_time
        fix_visit(curr_time)
    else:
        info = "Пользователь " + str(_username) + ' не зарегистрирован!'
        return render_template('reg_form.html', login_info=info)

    resp = make_response(render_template('index.html', username=_username, passw=_passw, login_info=info))    
    resp.set_cookie('username', _username)

    return resp

@app.route('/registration')
def reg_user():
    """Регистрирует нового пользователя в системе"""
    sql = 'INSERT INTO Users VALUES (?, ?, ?, ?, ?)'
    param = [get_nextId(), get_fullName(), request.form['password'], request.form['e_mail'], request.form['phone']]
    local_db.__execute__(sql, param)

if __name__ == '__main__':
    app.run()
    