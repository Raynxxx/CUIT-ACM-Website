# coding=utf-8
from __init__ import *
from dao.dbBook import BookStatus, Borrowinfo, Book, BorrowStatus


def add_book(bookForm):
    one = Book(bookForm.name.data,bookForm.introduce.data,bookForm.isbn.data,bookForm.shortcut.data)
    one.save()

def del_book(id):
    has = Book.query.filter(Book.id == id).with_lockmode('update').first()
    if not has:
        raise Exception(u'该书不存在')
    has.delete()

def modify_book(isbn, bookForm):
    has = Book.query.filter(Book.isbn == isbn).with_lockmode('update').first()
    if not has:
        raise Exception(u'该书不存在')
    has.name = bookForm.name.data
    has.introduce = bookForm.introduce.data
    has.isbn = bookForm.isbn.data
    has.shortcut = bookForm.shortcut.data
    has.status = bookForm.status.data
    has.save()

def list_bool_all(offset=0,limit=20):
    return Book.query.offset(offset).limit(limit)

def list_book(offset=0, limit=20, status=BookStatus.Normal):
    return Book.query.filter(Book.status == status).offset(offset).limit(limit)


def borrow_book(isbn, user):
    has = Book.query.filter(Book.isbn == isbn).with_lockmode('update').first()
    if not has:
        raise Exception(u'该书不存在')
    if has.user or (has.status == BookStatus.Borrowed):
        raise Exception(u'该书已经借出')
    borrow_info = Borrowinfo()
    borrow_info.book = has
    borrow_info.borrow_time = datetime.datetime.now()
    borrow_info.user = user
    borrow_info.status = BookStatus.Normal
    borrow_info.save()
    has.user = user
    has.borrow_count = has.borrow_count + 1
    has.save()

def return_book(isbn, user):
    has = user.book.query.filter(Book.isbn == isbn).with_lockmode('update').first()
    borrow_info = user.borrowinfo.filter(Borrowinfo.status == BorrowStatus.Normal).with_lockmode('update').first()
    if (not has) or (not borrow_info):
        raise Exception(u'没有借书记录')
    borrow_info.return_time = datetime.datetime.now()
    borrow_info.status = BorrowStatus.Finished
    has.status = BookStatus.Normal
    has.user = None
    has.save()
    borrow_info.save()

def list_borrow_info(user,offset=0,limit=20):
    return user.borrowinfo.query.offset(offset).limit(limit)