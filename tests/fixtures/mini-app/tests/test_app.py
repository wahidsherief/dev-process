import unittest, db, app

class T(unittest.TestCase):
    def test_list_orders(self):
        c = db.connect(":memory:"); db.init(c)
        c.execute("INSERT INTO customers VALUES (1,'Ada','a@x.io')")
        c.execute("INSERT INTO orders VALUES (1,1,10.0,'2026-01-01')")
        self.assertEqual(app.list_orders(c)[0]["customer"], "Ada")

if __name__ == "__main__":
    unittest.main()
