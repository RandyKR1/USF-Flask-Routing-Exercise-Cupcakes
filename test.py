from unittest import TestCase

from app import app
from models import db, Cupcake

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes_test'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

db.drop_all()
db.create_all()


CUPCAKE_DATA = {
    "flavor": "TestFlavor",
    "size": "TestSize",
    "rating": 5,
    "image": "http://test.com/cupcake.jpg"
}

CUPCAKE_DATA_2 = {
    "flavor": "TestFlavor2",
    "size": "TestSize2",
    "rating": 10,
    "image": "http://test.com/cupcake2.jpg"
}

class CupcakeTestCase(TestCase):
    
    def setUp(self):
        Cupcake.query.delete()
        
        cupcake=Cupcake(**CUPCAKE_DATA)
        db.session.add(cupcake)
        db.session.commit()
        
        self.cupcake = cupcake
        
    def tearDown(self):
        db.session.rollback()
    
    def test_list_cupcakes(self):
        with app.test_client() as client:
            resp = client.get("/api/cupcakes")

            self.assertEqual(resp.status_code, 200)
            
    def test_delete_route(self):
        with app.test_client() as client:
            resp = client.delete(f"/api/cupcakes/{self.cupcake.id}")
            
            self.assertEqual(resp.status_code, 200)

            data = resp.json
            self.assertEqual(data, {"message": "deleted"})
            
            self.assertEqual(Cupcake.query.count(), 0)
    
    def test_updated_cupcake(self):
        with app.test_client() as client:
            url = f"api/cupcakes/{self.cupcake.id}"
            resp = client.patch(url, json=CUPCAKE_DATA_2)
            
            self.assertEqual(resp.status_code, 200)
            
            data = resp.json
            
            self.assertEqual(data, {
            "cupcake": {
                    "id": self.cupcake.id,
                    "flavor": "TestFlavor2",
                    "size": "TestSize2",
                    "rating": 10,
                    "image": "http://test.com/cupcake2.jpg"
                }
            })

            self.assertEqual(Cupcake.query.count(), 1)