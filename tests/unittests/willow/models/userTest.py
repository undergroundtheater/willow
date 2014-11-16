from willow.models import User
import unittest


class Test(unittest.TestCase):

    def test_is_active(self):
        user = User()
        self.assertEquals(user.active, None)
        user.active = False
        self.assertFalse(user.is_active())
        user.active = True
        self.assertTrue(user.is_active())

    def test_is_admin(self):
        user = User()
        self.assertTrue(user.is_admin())


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testIsActive']
    unittest.main()