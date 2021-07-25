from asyncio.tasks import create_task
from flask import (Flask, g, redirect, render_template, request, session, url_for)
import os
import qrcode
import string
import random
import time
import asyncio

class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'

users = []
users.append(User(id=1, username='hanif_wp', password='password'))
users.append(User(id=2, username='zaw', password='secret'))
users.append(User(id=3, username='ihp', password='somethingsimple'))

app = Flask(__name__)
app.secret_key = 'somesecretkeythatonlyishouldknow'
PICTURES_FOLDER = 'static/img/'
app.config['PICTURES_FOLDER'] = PICTURES_FOLDER


@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user
        
@app.route('/login', methods=['GET', 'POST'])
async def login():
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        user = [x for x in users if x.username == username][0]

        if user and user.password == password:
            session['user_id'] = user.id
            await qr()
            return redirect(url_for('profile'))

        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/profile')
async def profile():
    await asyncio.sleep(2)
    if not g.user:
        return redirect(url_for('login'))
    
    return render_template("profile.html", img = pict)

async def qr():
    global pict
    localtime = str(time.asctime( time.localtime(time.time()) ))
    qr = qrcode.make(localtime)
    file_name = ''.join(random.choice(string.ascii_letters) for x in range(5))
    name = f"qr-{file_name}.png"
    qr.save(os.path.join(PICTURES_FOLDER, name))
    pict = os.path.join(PICTURES_FOLDER, name)

async def main():
    t1 = create_task(login())
    t2 = create_task(profile())
    t3 = create_task(qr())

    await asyncio.wait([t1,t2,t3])

if __name__ == '__main__':
    app.run(debug=True)
    asyncio.run(main())
    