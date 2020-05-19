import unittest
import serv


class LoginTest(unittest.TestCase):
    def test_login(self):
        password = ''
        with open('password.txt', 'r') as tmp_file:
            password = tmp_file.read()
        self.assertTrue(serv.login(password))


class ParserTest(unittest.TestCase):
    def test_parse(self):
        tmp_process = "ready"
        food_entry = "Username, bread, 1, milk, 3"
        tmp_dict = {
            "Username": {
                "process": tmp_process,
                "bread": 1,
                "milk": 3
            }
        }

        self.assertEqual(tmp_dict, serv.parse_food(food_entry, tmp_process))


class NewParserTest(unittest.TestCase):
    def test_new_parser(self):
        food_entry = 'Bread, 1, Milk, 2, Meat, 3'
        tmp_order = {
            "Bread": 1,
            "Milk": 2,
            "Meat": 3
        }

        self.assertEqual(tmp_order, serv.parse_new_food(food_entry))


if __name__ == "__main__":
    unittest.main()
