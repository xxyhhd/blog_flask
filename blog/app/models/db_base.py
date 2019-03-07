from app.extensions import db


# db操作的类
class DB:
    # 添加一条数据的方法
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except:
            db.session.rollback()

    # 添加多条数据的方法
    def save_all(*args):
        try:
            db.session.add_all(args)
            db.session.commit()
        except:
            db.session.rollback()

    # 删除数据的方法
    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            db.session.rollback()
