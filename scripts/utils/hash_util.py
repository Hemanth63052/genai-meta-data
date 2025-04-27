import bcrypt

class HashUtil:

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash the password using bcrypt.
        :param password:
        :return:
        """
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode()

    @staticmethod
    def compare_password(password: str, hashed_password: str) -> bool:
        """
        Compare the password with the hashed password.
        :param password:
        :param hashed_password:
        :return:
        """
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
