from app import app, db
from flask import session, flash, redirect, url_for, render_template, request
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from sqlalchemy import func
from app.models import User
from app.forms import LoginForm
from sqlakeyset import select_page

# with app.app_context():
#     page_num = 0
#     page_length = 10

#     fake_session = {}

#     query = db.select(User).order_by(User.id)

#     count_query = db.select(func.count()).select_from(query.subquery())
#     total = db.session.scalar(count_query)
#     final_page_num, _  = divmod(total, page_length)
#     print("final page num", final_page_num)

#     if page_num == final_page_num:
#         page = select_page(db.session, query.order_by(User.id.desc()), per_page=page_length)
#     elif page_num == 0 or "prev_page" not in fake_session:
#         page = select_page(db.session, query, per_page=page_length)
#     else:
#         page_diff = page_num - fake_session["prev_page_num"]
#         prev_page = select_page(db.session, query, page=fake_session["prev_page"])
#         if page_diff > 0:
#             while page_diff != 0:
#                 page = page.paging.next
#                 page_diff -= 1
#         else:
#             raise NotImplementedError("not yet")

#         page = select_page(db.session, query, per_page=page_length)

#     fake_session["prev_page"] = page.paging.bookmark_current
#     fake_session["prev_page_num"] = page_num

#     print(page)


with app.app_context():

    length=10

    page = select_page(
        db.session, 
        db.select(User).order_by(User.id), 
        per_page=length,
        page = (None, True)
    )

    print("Last Page:", page)
    # print("------\n")

    # start_id = page[-1][0].id
    # print(start_id)
    # page = select_page(
    #     db.session,
    #     db.select(User).where(User.id >= start_id),
    #     per_page=length
    # )
    # print("last page, reversed", page)
    # print("------\n")
    # page = select_page(
    #     db.session,
    #     db.select(User).order_by(User.id),
    #     per_page=length,
    #     page=page.paging.previous
    # )
    print("saved page")
    print(page)
    print("---------\n")

    print(page.paging.bookmark_current)
    print(page.paging.bookmark_previous)
    print(page.paging.bookmark_next)
    print(page.paging.bookmark_current_backwards)



