from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(64), nullable=False)
    address = db.Column(db.String(64))
    phone = db.Column(db.String(128))
    email = db.Column(db.String(64))
    pay = db.Column(db.String(6))
    admin = db.Column(db.Boolean, default=False)
    orders = db.relationship('Order', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % self.name

    def __init__(self, name, pay, password, address, phone, email, admin):
        self.name = name
        self.pay = pay
        self.password = password
        self.address = address
        self.phone = phone
        self.email = email
        self.admin = admin

    # 是否被认证
    def is_authenticated(self):
        return True

    # 是否有效,除非用户被禁止
    def is_active(self):
        return True

    # 是否匿名
    def is_anonymous(self):
        return False

    # 是否是管理员
    def is_admin(self):
        return self.admin

    def get_id(self):
        return str(self.id)


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    introduction = db.Column(db.String(1000))
    photo = db.Column(db.String(140))
    price = db.Column(db.Integer)
    sales = db.Column(db.Integer)

    def __init__(self, name, introduction, price, photo, sales=0):
        self.name = name
        self.introduction = introduction
        self.price = price
        self.photo = photo
        self.sales = sales

    # 头像
    def avatar(self):
        book = Books.query.filter_by(id=self.id).first()
        img = book.photo
        return img


# 订单
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cost = db.Column(db.Integer)
    time = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    address = db.Column(db.String(30))
    status = db.Column(db.String(5))  # 订单属性:购物车,未支付,待发货,已发货,完成
    items = db.relationship('OrderItem', backref='order', lazy='dynamic')

    def __init__(self, user_id):
        # 初始化用户的购物车(首先检查用户是否有购物车, 没有就添加)
        self.user_id = user_id
        self.status = "购物车"
        self.address = ''
        self.cost = '0'

    # 更新价格
    def updatecost(self):
        cost = 0
        for a in self.items:
            cost += a.cost
        self.cost = cost


class Assess(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer)
    body = db.Column(db.String(64))
    time = db.Column(db.DateTime)

    def __init__(self,book_id,body,time):
        self.book_id = book_id
        self.body = body
        self.time = time

# 订单的单个商品
class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer)
    book_name = db.Column(db.String(64))
    price = db.Column(db.Integer)
    num = db.Column(db.Integer)
    cost = db.Column(db.Integer)
    Order_id = db.Column(db.Integer, db.ForeignKey('order.id'), )

    # 添加商品到购物车
    def add(self, book_id, num, order_id):
        self.book_id = book_id
        self.book_name = Books.query.filter_by(id=book_id).first().name
        self.price = Books.query.filter_by(id=book_id).first().price
        self.num = num
        self.cost = self.price * self.num
        self.Order_id = order_id

    # 改变商品数量
    def changenum(self, num):
        self.num += num
        self.cost = self.price * self.num
