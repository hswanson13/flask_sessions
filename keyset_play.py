from app import app, db
from flask import session, flash, redirect, url_for, render_template, request
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from sqlalchemy import func
from app.models import User
from app.forms import LoginForm
from flask_sqlakeyset import select_page

with app.app_context():
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

    # gets the first page
    page1 = select_page(db.session, query, per_page=20)

    # gets the key for the next page
    next_page = page1.paging.next

    # gets the second page
    page2 = select_page(db.session, query, per_page=20, page=next_page)
    print(page1)
