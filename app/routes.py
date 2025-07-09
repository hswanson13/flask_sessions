from app import app, db
from flask import session, flash, redirect, url_for, render_template, request
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from sqlalchemy import func
from app.models import User
from app.forms import LoginForm
from sqlakeyset import select_page

@app.route('/')
@app.route('/hello')
def index():
    if "hello_counter" not in session:
        session["hello_counter"] = 0
    session["hello_counter"] += 1
    print("sessoin", session)
    return render_template('index.html', title='Home', user=current_user)

@app.route('/bye')
@login_required
def bye():
    if "bye_counter" not in session:
        session["bye_counter"] = 0
    session["bye_counter"] += 1
    print("sessoin", session)
    return f'<h1>Goodbye, World! {current_user.username} </h1><p>Bye count: {session["bye_counter"]}</p><a href="/"><button>Go to Hello</button></a>'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    print("sessoin", session)
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return f"""
    <h1>Sign In</h1>
    <form action="" method="post" novalidate>
        { form.hidden_tag() }
        <p>
            { form.username.label }<br>
            { form.username(size=32) }
        </p>
        <p>
            { form.password.label }<br>
            { form.password(size=32) }
        </p>
        <p>{ form.remember_me() } { form.remember_me.label }</p>
        <p>{ form.submit() }</p>
    </form>
"""

# create paginated table with the one github repo
#       - 
# create table with 5k rows
@app.route('/api/table')
def table_data():
    # Ref: https://blog.miguelgrinberg.com/post/beautiful-flask-tables-part-2
    query = User.query

    # search filter
    search = request.args.get('search')
    if search:
        query = query.filter(db.or_(
            User.username.like(f'%{search}%'),
            User.email.like(f'%{search}%')
        ))
    total = query.count()
    # pagination
    start = request.args.get('start', type=int, default=-1)
    length = request.args.get('length', type=int, default=-1)
    if start != -1 and length != -1:
        query = query.offset(start).limit(length)

    return {
        'data': [{'username':user.username, 'email': user.email} for user in query],
        'total': total,
    }

@app.route('/api/table_keyset')
def table_data_keyset():
    # Ref: https://blog.miguelgrinberg.com/post/beautiful-flask-tables-part-2
    query = db.select(User).order_by(User.id)

    # search filter
    search = request.args.get('search')
    if search:
        query = query.filter(db.or_(
            User.username.like(f'%{search}%'),
            User.email.like(f'%{search}%')
        ))
    
    count_query = db.select(func.count()).select_from(query.subquery())
    total = db.session.scalar(count_query)
    length = request.args.get('length', 10, type=int)
    start = request.args.get("start", 0, type=int)
    page_num = int(start / length)
    final_page_num, _  = divmod(total, length)

    if page_num == 0 or "prev_page" not in session:
        # First page or corrupted session
        page = select_page(db.session, query, per_page=length)
    elif page_num == final_page_num:
        # Last Page
        # https://github.com/djrobstep/sqlakeyset#page-objects
        page = select_page(
            db.session, 
            query, 
            per_page=length,
            page = (None, True)
        )
    else: 
        # In between pages
        page_diff = page_num - session["prev_page_num"]
        page = select_page(db.session, query, page=session["prev_page"])
        step = 1 if page_diff > 0 else -1
        for _ in range(abs(page_diff)):
            page = select_page(
                db.session, 
                query, 
                page = page.paging.next if step > 0 else page.paging.previous
            )
    session["prev_page"] = page.paging.bookmark_current
    session["prev_page_num"] = page_num

    results = [r[0] for r in page]
    return {
        'data': [{"id": user.id, 'username':user.username, 'email': user.email} for user in results],
        'total': total,
    }

@app.route("/table", methods=["GET", "POST"])
def table():
    return render_template('table.html', title='Table', user=current_user)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))