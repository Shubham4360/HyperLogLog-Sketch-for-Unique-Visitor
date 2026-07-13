class ExactCounter:

    def __init__(self):
        self.users = set()

    def add(self, user_id):
        self.users.add(user_id)

    def count(self):
        return len(self.users)