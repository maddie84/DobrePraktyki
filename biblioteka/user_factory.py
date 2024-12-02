class User:
    def __init__(self, name, user_type):
        self.name = name
        self.user_type = user_type

    def __str__(self):
        return f"{self.user_type} {self.name}"

    # Metoda potrzebna do wzorca Observer
    def update(self, message):
        print(f"{self.name} ({self.user_type}) received notification: {message}")


class UserFactory:
    @staticmethod
    def create_user(name, user_type):
        if user_type.lower() in ["student", "teacher", "librarian"]:
            return User(name, user_type.capitalize())
        else:
            raise ValueError(f"Unknown user type: {user_type}")


# Test Factory
if __name__ == "__main__":
    user1 = UserFactory.create_user("Alice", "student")
    user2 = UserFactory.create_user("Bob", "teacher")
    print(user1)
    print(user2)
