from unittest import TestCase
from app import app
from models import db, User, Post

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test_db'
app.config['SQLALCHEMY_ECHO']=False
app.config['TESTING']=True
db.drop_all()
db.create_all()

class UserModelTestCase(TestCase):
    def setUp(self):
        User.query.delete()
        Post.query.delete()
        user = User(first_name="Test_First", last_name="Test_Last", image_url = "https://scontent-ort2-2.xx.fbcdn.net/v/t1.0-9/92392533_1929214157209094_5872836043148886016_o.jpg?_nc_cat=107&ccb=3&_nc_sid=09cbfe&_nc_ohc=vWSVf2t0ZkcAX_SCvtJ&_nc_oc=AQmJz-rO5dcOYX7bJvVOxu2DutdTyItvJLCht69zvDThLk8f7kNBWCYKJn62Ys_lXKk&_nc_ht=scontent-ort2-2.xx&oh=20151e96f7714259582a3f9a1372fcb6&oe=60515C2E")
        db.session.add(user)
        db.session.commit()
        self.user_id = user.id

    def tearDown(self):
        db.session.rollback()

    def test_users(self):
        with app.test_client() as client:
            resp = client.get('/users')
            # html = resp.get_data(as_text=True)
            # self.assertEqual(resp.status_code, 200)
            # self.assertIn('Test_First Test_Last', html)

    def test_add_user(self):
        with app.test_client() as client:
            resp = client.get('/users/new')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("""<form action="/users/new" method="POST">
    First Name <input type="text" name="first_name" placeholder="first_name" required>
    <br>
    <br>
    Last Name <input type="text" name="last_name" placeholder="last_name" required>
    <br>
    <br>
    Image URL <input type="text" name="image_url" placeholder="image_url"> optional
    <br>
    <br>
    <button>Submit</button>
</form>""", html)

    def test_post_add_user(self):
        with app.test_client() as client:
            d = {'first_name': "TestFirst2", "last_name": "TestLast2", "image_url": "https://media-exp1.licdn.com/dms/image/C4E03AQGK_Maz9GsuJg/profile-displayphoto-shrink_800_800/0/1609805687427?e=1619049600&v=beta&t=DmSHrp9_SKK-FyhbVpcB8kgBprbaZgfrRxBwQ1xgeCI"}
            resp = client.post('/users/new', data = d, follow_redirects = True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("TestFirst2 TestLast2", html)

    def test_post_form(self):
        with app.test_client() as client:
            resp = client.get(f'/users/{self.user_id}/posts/new')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Title <input", html)
            self.assertIn("Content <textarea", html)
            self.assertIn("<button>Add", html)
            self.assertIn("<button>Cancel", html)

    def test_post_form_handle(self):
        with app.test_client() as client:
            d = {"title": "TestTitle", "content": "TestContent"}
            resp = client.post(f'/users/{self.user_id}/posts/new', data=d, follow_redirects=True)
            html = resp.get_data(as_text = True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestTitle', html)

    def test_delete_user(self):
        with app.test_client() as client:
            resp = client.get(f'/users/{self.user_id}/delete', follow_redirects= True)
            html = resp.get_data(as_text = True)
            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('Test_First Test_Last', html)

