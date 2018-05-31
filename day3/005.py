# #coding:utf8
# from flask import flash
#
# from flask import Flask
# from flask import redirect
# from flask import render_template
# from flask.ext.sqlalchemy import SQLAlchemy
# from flask.ext.wtf import FlaskForm
# from wtforms import StringField, SubmitField
# from wtforms.validators import DataRequired
#
# app = Flask(__name__)
#
#
# # app.config["SQLALCHEMY_DATABASE_URI"]="mysql://root:mysql@localhost:3306/library"
# # app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
# # app.config["SERECT_KEY"]="DFTYUJYUTREWQasdftTGTYHYJHYRFghyjhtgfdscs"
#
# class Config(object):
#     SQLALCHEMY_DATABASE_URI = "mysql://root:mysql@localhost:3306/library"
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     SECRET_KEY = "dsfghjkhlljhgfds"
#
# app.config.from_object(Config)
# db = SQLAlchemy(app)
#
#
# class Author(db.Model):
#     __tablename__ = "authors"
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(64))
#     books = db.relationship("Book", backref="author", lazy="dynamic")
#
#
# class Book(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.column(db.String(64))
#     author_id = db.Column(db.ForeignKey(Author.id))
#
#
# class BookForm(FlaskForm):
#     bookname = StringField(label=u"书名", validators=[DataRequired()], default=u"请输入用户名")
#     authorname = StringField(u"作者", validators=[DataRequired()], render_kw={"placeholder": u"请输入作者"})
#     sumit = SubmitField(u"提交")
#
#
# @app.route('/')
# def index():
#     form = BookForm()
#     authors = Author.query.all()
#     return render_template("04.html", form =form, authors = authors)
#
#
# @app.route('/add_book')
# def add_book():
#     form = BookForm()
#     if form.validate_on_submit():
#         authorname = form.authorname.data
#         bookname = form.bookname.data
#         author = Author.query.filter(Author.name == authorname).first()
#
#         if author:
#             book = Book.query.filter(Book.name == bookname, Book.author_id == author.id)
#
#             if book:
#                 flash(u"该作者已经有该书了")
#             else:
#                 author = Author(name=authorname, author_id=author.id)
#                 db.session.add(author)
#                 db.session.commit()
#         else:
#             author = Author(name=authorname)
#             db.session.add(author)
#             db.session.commit()
#
#             book = Book(name=authorname, author_id=author.id)
#             db.session.add(book)
#             db.session.commit()
#
#     return redirect("/")
# @app.route('/delete_author/<int:id>')
# def delete_author(id):
#     author=Author.query.get(id)
#     books =author.books
#
#     for book in books:
#         db.session.delete(book)
#     db.session.delete(author)
#     db.session.commit()
#     return redirect("/")
#
# if __name__ == '__main__':
#     db.create_all()
#
#     #添加测试数据
#     # 生成数据
#     au1 = Author(name='老王')
#     au2 = Author(name='老尹')
#     au3 = Author(name='老刘')
#     # 把数据提交给用户会话
#     db.session.add_all([au1, au2, au3])
#     db.session.commit()
#
#     # 提交会话
#     bk1 = Book(name='老王回忆录', author_id=au1.id)
#     bk2 = Book(name='我读书少，你别骗我', author_id=au1.id)
#     bk3 = Book(name='如何才能让自己更骚', author_id=au2.id)
#     bk4 = Book(name='怎样征服美丽少女', author_id=au3.id)
#     bk5 = Book(name='如何征服英俊少男', author_id=au3.id)
#
#     # 把数据提交给用户会话
#     db.session.add_all([bk1, bk2, bk3, bk4, bk5])
#
#     # 提交会话
#     db.session.commit()
#
#     app.run(debug=True)


#coding:utf8

from flask import Flask
from flask import flash
from flask import redirect
from flask import render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)

#数据库配置信息
class Config(object):
    SECRET_KEY = "djkfjkdjfkd"
    SQLALCHEMY_DATABASE_URI = "mysql://root:mysql@localhost:3306/library"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

app.config.from_object(Config)

db = SQLAlchemy(app)

#编写模型类
#一个作者可以写多本书
class Author(db.Model):
    __tablename__ = "authors"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64))
    books = db.relationship("Book",backref="author",lazy="dynamic")

#一本书只有一个作者
class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64))
    author_id = db.Column(db.ForeignKey(Author.id))


#定义表单类
class BookForm(FlaskForm):
    bookname = StringField(label=u'书名',validators=[DataRequired()],default=u'请输入用户名')
    authorname = StringField(u'作者',validators=[DataRequired()],render_kw={"placeholder":u'请输入作者'})
    submit = SubmitField(u'提交')


#展示书籍
@app.route('/')
def index():
    #1.创建表单
    form = BookForm()

    #2.查询数据
    authors = Author.query.all()

    #3.将数据渲染到页面
    return render_template("file04library.html",form=form,authors=authors)

#添加书籍
@app.route('/add_book', methods=['POST'])
def add_book():

    #1.创建表单
    form = BookForm()

    #2.校验表单
    if form.validate_on_submit():

        #获取到参数,作者名,书名
        authorname = form.authorname.data
        bookname = form.bookname.data

        author = Author.query.filter(Author.name == authorname).first()
        #判断
        if author:

            #查询该作者底下,是否有该书名
            book = Book.query.filter(Book.name == bookname,Book.author_id == author.id).first()

            #该书存在
            if book:
                flash(u"该作者已经有该书了!!")
                # return redirect("/")

            else:
                book = Book(name=bookname,author_id=author.id)
                db.session.add(book)
                db.session.commit()
                # return redirect("/")

        else:
            #创建作者,和书,添加到数据库
            author = Author(name=authorname)
            db.session.add(author)
            db.session.commit()

            book = Book(name=bookname,author_id=author.id)
            db.session.add(book)
            db.session.commit()
            # return redirect("/")

    #3.响应
    return redirect("/")

#删除书籍
@app.route('/delete_book/<int:id>')
def delete_book(id):
    #1.根据编号获取到书籍
    book = Book.query.get(id)

    #2.删除,提交
    db.session.delete(book)
    db.session.commit()

    #3.重定向到展示页面
    return redirect("/")

#删除作者和作者所有关联的书籍
@app.route('/delete_author/<int:id>')
def delete_author(id):
    #1.通过编号获取到作者对象
    author = Author.query.get(id)

    #2.获取到作者,所有的书籍
    books = author.books

    #3.删除书籍, 作者,提交
    for book in books:
        db.session.delete(book)

    db.session.delete(author)
    db.session.commit()

    #4.重定向到显示页面
    return redirect("/")


if __name__ == "__main__":

    #为了演示方便,先删除所有的表
    db.drop_all()

    #创建所有表
    db.create_all()

    #添加测试数据
    # 生成数据
    au1 = Author(name='老王')
    au2 = Author(name='老尹')
    au3 = Author(name='老刘')
    # 把数据提交给用户会话
    db.session.add_all([au1, au2, au3])
    db.session.commit()

    # 提交会话
    bk1 = Book(name='老王回忆录', author_id=au1.id)
    bk2 = Book(name='我读书少，你别骗我', author_id=au1.id)
    bk3 = Book(name='如何才能让自己更骚', author_id=au2.id)
    bk4 = Book(name='怎样征服美丽少女', author_id=au3.id)
    bk5 = Book(name='如何征服英俊少男', author_id=au3.id)

    # 把数据提交给用户会话
    db.session.add_all([bk1, bk2, bk3, bk4, bk5])

    # 提交会话
    db.session.commit()

    app.run(debug=True)