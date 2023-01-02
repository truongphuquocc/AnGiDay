# from crypt import methods
from flask import render_template, redirect, flash, url_for
from app import app
from app.forms import LoginForm
from flask_login import login_user, current_user, logout_user, login_required
from app.models import User, MonAn
from flask import request, session
from werkzeug.urls import url_parse
import random
from app import db
from sqlalchemy import func


@app.route('/')
@app.route('/index')
# @login_required
def index():
    # return "Hello, World"
    session["client"] = []
    user = current_user
    return render_template('index.html', user=user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/danhsach')
@login_required
def danhsach():
    allmonan = MonAn.query.all()
    return render_template('danhsach.html', title='Quản lý món ăn', mon=allmonan)


@app.route('/danhsachclient')
def danhsachclient():
    allmonan = MonAn.query.all()
    return render_template('danhsachclient.html', title='Danh sách món ăn', mon=allmonan)


@app.route('/ngaunhien', methods=['GET', 'POST'])
def ngaunhien():
    slphu = request.form.get('slphu')
    slchinh = request.form.get('slchinh')

    if (slphu is None):
        slp = 0
    else:
        slp = int(slphu)

    if (slchinh is None):
        slc = 0
    else:
        slc = int(slchinh)

    monchinh = MonAn.query.filter(MonAn.maloai == 'monchinh').all()
    monphu = MonAn.query.filter(MonAn.maloai == 'monphu').all()

    random.shuffle(monchinh)
    randomchinh = monchinh[0:slc]

    random.shuffle(monphu)
    randomphu = monphu[0:slp]

    rdlist2 = randomphu + randomchinh
# region
    #rdlist = []
    # ic = 1
    # while (ic <= slc):
    #     rd = round(random.random()*(len(monchinh)-1))
    #     mc = monchinh[rd]
    #     for i in rdlist:
    #         if i.tenmon == monchinh[rd].tenmon:
    #             #rd = round(random.random()*(len(monchinh)-1))
    #             break
    #         else:
    #             rd = round(random.random()*(len(monchinh)-1))
    #             mc = monchinh[rd]
    #     rdlist.append(mc)
    #     ic += 1
    #rdmonchinh = []

    # ip = 1
    # i = 1
    # while (ip <= slp):
    #     rd = round(random.random()*(len(monphu)-1))
    #     mn = monphu[rd]
    #     for i in rdlist:
    #         if i.tenmon == monphu[rd].tenmon:
    #             rd = round(random.random()*(len(monphu)-1))
    #         else:
    #             mn = monphu[rd]
    #             # rdlist.append(mn)
    #     rdlist.append(mn)
    #     ip += 1
# endregion

    return render_template('random.html', dsrandom=rdlist2)


@app.route('/update', methods=['GET', 'POST'])
@login_required
def update():
    if request.method == 'POST':
        my_data = MonAn.query.get(request.form.get('id'))
        print(my_data)
        test = request.form.get('tenmon')
        my_data.tenmon = request.form.get('tenmon')
        print(my_data.tenmon)

        if (request.form.get('mm') is not None):
            #my_data.maloai = 'monphu'
            my_data.maloai = request.form.get('mm')
        print(my_data.maloai)
        db.session.commit()
        flash(f"sửa thành công")
        return redirect(url_for('danhsach'))
    return render_template('danhsach.html')


@app.route('/insert', methods=['GET', 'POST'])
@login_required
def insert():
    if request.method == 'POST':

        tenmon = request.form.get('tenmon')
        maloai = request.form.get('mm')

        allmonan = MonAn.query.filter(func.lower(MonAn.tenmon) == func.lower(tenmon)).all()
        if len(allmonan) == 0:
            print("Danh sach")
            print(allmonan)
            print("end Danh sach")
            insert = MonAn(maloai, tenmon)
            db.session.add(insert)
            db.session.commit()
            flash(f"Thêm thành công!")
            return redirect(url_for('insert'))
        else:
            flash(f"Món đã có trong hệ thống!")
    return render_template('themmon.html', title='Thêm món ăn',)


@app.route('/delete/<id>/', methods=['GET', 'POST'])
@login_required
def delete(id):

    delete = MonAn.query.get(id)
    db.session.delete(delete)
    db.session.commit()
    flash(f"xoá thành công")
    return redirect(url_for('danhsach'))


@app.route('/client', methods=['GET', 'POST'])
def client():
    #session["client"] = []

    dssession = session["client"]
    if dssession == []:
        session["client"] = []

    print(type(dssession))

    return render_template('client.html', client=dssession)


@app.route('/insertclient', methods=['GET', 'POST'])
def insertclient():

    tenmon = request.form.get('tenmon')
    maloai = request.form.get('mm')

    dict = {
        'tenmon': tenmon,
        'maloai': maloai,
    }
    if "client" in session:
        client = session["client"]

    check = 0

    for x in client:
        print(x["tenmon"])
        if x["tenmon"].lower() == tenmon.lower():
            check = 1
            break
    if check == 0 and tenmon is not None:
        client.append(dict)
    elif tenmon is not None :
        flash(f"Món ăn bị trùng")
    session["client"] = client

    return render_template('client.html', client=session["client"])


@app.route('/deleteclient/<tenmon>/<maloai>/', methods=['GET', 'POST'])
def deleteclient(tenmon, maloai):

    dict = {
        'tenmon': tenmon,
        'maloai': maloai,
    }
    client = session["client"]
    for x in client:
        if x["tenmon"] == tenmon:
            client.remove(dict)
            flash(f"Xoá thành công")
    session["client"] = client
    return redirect(url_for('client'))


@app.route('/randomclient', methods=['GET', 'POST'])
def randomclient():

    slphu = request.form.get('slphu')
    slchinh = request.form.get('slchinh')

    if (slphu is None):
        slp = 0
    else:
        slp = int(slphu)

    if (slchinh is None):
        slc = 0
    else:
        slc = int(slchinh)

    session["slc"] = slc
    session["slp"] = slp
    client = session["client"]

    monchinh = []
    monphu = []

    for x in client:
        if x["maloai"] == 'monchinh':
            monchinh.append({"tenmon": x["tenmon"], "maloai": x["maloai"]})
        else:
            monphu.append({"tenmon": x["tenmon"], "maloai": x["maloai"]})
    print("ds mon chinh")
    print(monchinh)

    random.shuffle(monchinh)
    randomchinh = monchinh[0:slc]

    random.shuffle(monphu)
    randomphu = monphu[0:slp]

    rdlist2 = randomphu + randomchinh
    return render_template('client.html', dsrandom=rdlist2, client=client)
