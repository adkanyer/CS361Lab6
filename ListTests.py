import unittest
from ListUI import *


class UserDoesNotExistException(Exception):
    pass


class TestList(unittest.TestCase):
    def setUp(self):
        self.listui = ListUI()
        self.listui.users = [{"username": "ExistingUser", "password": "12345", "current": False, "wishlist": []}]

    def get_user_names(self):
        usernames = []
        for user in self.listui.users:
            usernames.append(user['username'])
        return usernames

    def get_user(self, username):
        for user in self.listui.users:
            if user['username'] == username:
                return user
        raise UserDoesNotExistException()

    def test_add(self):
        self.assertNotIn("TestUser", self.get_user_names())
        response = self.listui.command("add TestUser 12345")
        self.assertEqual(response, "User TestUser added.")
        self.assertIn("TestUser", self.get_user_names())
        self.assertEqual(self.get_user("TestUser")["password"], "12345")

    def test_add_missing_args(self):
        users_before_add = self.listui.users
        self.listui.command("add")
        self.assertEqual(users_before_add, self.listui.users)

        self.listui.command("add justOneArg")
        self.assertEqual(users_before_add, self.listui.users)

    def test_add_existing_user(self):
        self.listui.command("add ExistingUser 12345")
        response = self.listui.command("add ExistingUser 12345")
        self.assertEqual(response, "Failed. User exists.")
        self.assertEqual(self.get_password("ExistingUser"), "12345")
        self.assertEqual(self.get_user_names().count("ExisitngUser"), 1)

    def test_login(self):
        response = self.listui.command("login ExistingUser 12345")
        self.assertEqual(response, "ExistingUser logged in.")
        self.assertTrue(self.get_user("ExistingUser")['current'])

    def test_login_nonexisting_user(self):
        response = self.listui.command("login NonexistingUser 12345")
        self.assertEqual(response, "Failed. Username or password invalid.")

    def test_login_wrong_password(self):
        response = self.listui.command("login ExistingUser wrong_pass")
        self.assertEqual(response, "Failed. Username or password invalid.")

