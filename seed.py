from models import User, db
from app import app

db.drop_all()
db.create_all()

ethan = User(first_name='Ethan', last_name='Schreur', image_url='https://scontent-ort2-2.xx.fbcdn.net/v/t1.0-9/92392533_1929214157209094_5872836043148886016_o.jpg?_nc_cat=107&ccb=3&_nc_sid=09cbfe&_nc_ohc=vWSVf2t0ZkcAX_SCvtJ&_nc_oc=AQmJz-rO5dcOYX7bJvVOxu2DutdTyItvJLCht69zvDThLk8f7kNBWCYKJn62Ys_lXKk&_nc_ht=scontent-ort2-2.xx&oh=20151e96f7714259582a3f9a1372fcb6&oe=60515C2E')
db.session.add(ethan)
db.session.commit()