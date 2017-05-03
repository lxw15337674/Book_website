from app import db
from app.models import User, Fruits

# user = User(name='123', password='123')
# user1 = User(name='666', password='666')
# db.session.add(user)
# db.session.add(user1)


fruit = Fruits(name='高原小城',
               introduction='高原小城',
               price='2',
               photo= 'https://ss1.bdstatic.com/70cFvXSh_Q1YnxGkpoWK1HF6hhy/it/u=38969419,4246819950&fm=23&gp=0.jpg',
               sales=8)
fruit1 = Fruits(name='生平',
               introduction='生平',
               price='1',
                photo='https://ss3.bdstatic.com/70cFv8Sh_Q1YnxGkpoWK1HF6hhy/it/u=1952262159,1630835076&fm=23&gp=0.jpg',
                sales=5)

db.session.add(fruit)
db.session.add(fruit1)

db.session.commit()