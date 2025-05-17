from flask import Flask, render_template, request, redirect, session, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# 샘플 사용자 데이터
users = {
    'user1': {
        'password': generate_password_hash('pass123'),
        'balance': 1000
    },
    'user2': {
        'password': generate_password_hash('pass123'),
        'balance': 1000
    },
    'user3': {
        'password': generate_password_hash('pass123'),
        'balance': 1000
    },
    
}

# 로그인 페이지
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        userid = request.form['userid']
        password = request.form['password']
        user = users.get(userid)

        if user and check_password_hash(user['password'], password):
            session['user'] = userid
            return redirect(url_for('dashboard'))
        else:
            flash('아이디 또는 비밀번호를 확인해주세요.')
    return render_template('login.html')

# 대시보드 (로그인된 사용자만 접근 가능)
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))

    user = users[session['user']]
    message = ""

    if request.method == 'POST':
        action = request.form['action']
        amount = int(request.form['amount'])

        if action == 'deposit':
            user['balance'] += amount
            message = f"{amount}원이 입금되었습니다."
        elif action == 'withdraw':
            if amount > user['balance']:
                message = "잔액이 부족합니다."
            else:
                user['balance'] -= amount
                message = f"{amount}원이 출금되었습니다."

    return render_template('dashboard.html', user=session['user'], balance=user['balance'], message=message)

# 로그아웃
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template("error.html"), 404

if __name__ == '__main__':
    app.run(debug=True)
