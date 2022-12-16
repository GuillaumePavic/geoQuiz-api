from dbConnect import connection

createUserSchema = {
    'type': 'object',
    'properties': {
        'email': {'type': 'string'},
        'password': {'type': 'string'},
        'username': {'type': 'string'}
    },
    'required': ['email', 'password', 'username']
}

loginSchema = {
    'type': 'object',
    'properties': {
        'email': {'type': 'string'},
        'password': {'type': 'string'},
    },
    'required': ['email', 'password']
}

class User:
    @staticmethod
    def createUser(email, password, username):
        sql = """
        INSERT INTO "user"("email", "password", "username") 
        VALUES (%s, %s, %s)
        """

        with connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, (email, password, username))
    
    @staticmethod
    def getUser(email):
        sql="""
        SELECT * FROM "user" WHERE "email" = 'guillaume.pa@outlook.fr';
        """

        with connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, (email))
                results = cursor.fetchone()
                if results is None:
                    return None
                user = {
                    "id": results[0],
                    "email": results[1],
                    "password": results[2],
                    "isAdmin": results[4]
                }
                return user
