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

@app.route('/')
def index():
    _username = "" if not request.cookies.get('username') else request.cookies.get('username')
    _passw = "" if not request.cookies.get('passw') else request.cookies.get('passw')

    return render_template('index.html', username=_username, passw=_passw)


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
        info = 'Неверный логин или пароль'

    resp = make_response(render_template('index.html', username=_username, passw=_passw, login_info=info))    
    resp.set_cookie('username', _username)
    resp.set_cookie('passw', _passw)

    return resp

if __name__ == '__main__':
    app.run()
    