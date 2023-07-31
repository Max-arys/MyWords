import json


class Users:
    def __init__(self):
        with open(r'MyWords\src\my_words\data\users.json', 'r') as u:
            self.d_users = json.load(u)
        self.users = self.d_users["users"]
        self.user = self.d_users["user"]

    def save_data(self):
        with open(r'MyWords\src\my_words\data\users.json', 'w') as u:
            self.d_users["users"] = self.users
            self.d_users["user"] = self.user
            json.dump(self.d_users, u)
