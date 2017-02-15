from flask import Flask, render_template, request, make_response

app = Flask(__name__)


def valid_login(login, passw):
    result = True
    if login == "" or passw == "":
        result = False     

    return result    
    

@app.route('/')
def index():
    _username = "" if not request.cookies.get('username') else request.cookies.get('username')
    _passw = "" if not request.cookies.get('passw') else request.cookies.get('passw')
    #return 'login: %s, password: %s' % (_username, _passw)
    return render_template('index.html', username=_username, passw=_passw)


@app.route('/login', methods=['POST'])
def login():
    """Авторизация или регистрация пользователя, сохранение cookie|"""
    info = None
    _username = request.form['login']
    _passw = request.form['password']
    if valid_login(_username, _passw):
        info = 'Авторизация прошла успешно. login: %s, password: %s' % (_username, _passw)
    else:
        info = 'Неверный логин или пароль'

    resp = make_response(render_template('index.html', username=_username, passw=_passw, login_info=info))    
    resp.set_cookie('username', _username)
    resp.set_cookie('passw', _passw)

    return resp

if __name__ == '__main__':
    app.run()