from app.config.mysqlconnection import connectToMySQL

class Pet:

    def __init__(self, data):

        self.id = data['id']
        self.name = data['name']
        self.type = data['type']
        self.age = data['age']
        self.hobby = data['hobby']
        self.user_id = data['user_id']
        self.favorite_snack = data['favorite_snack']
        self.image_path = data['image_path']
        self.likes_count = data['likes_count']
        self.liked_by_current_user = data['pet_id'] is not None # boolean
        self.likes=[]
   
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'age': self.age,
            'hobby': self.hobby,
            'user_id': self.user_id,
            'favorite_snack': self.favorite_snack,
            'likes_count': self.likes_count,
            'liked_by_current_user': self.liked_by_current_user,
            'likes': self.likes
        }

    def is_liked_by(self, user_id):
        for like in self.likes:
            if like['id'] == user_id:
                return True
        return False
          
    @classmethod
    def get_all(cls, user_id=None):
        
        query = """
            SELECT
                *,
                (
					SELECT COUNT(*) FROM user_like_pet WHERE user_like_pet.pet_id = pets.id
				) AS likes_count

            FROM
                pets
			
				LEFT JOIN user_like_pet ON user_like_pet.pet_id = pets.id AND user_like_pet.user_id = %(user_id)s
				LEFT JOIN users ON users.id = user_like_pet.user_id
                ;
        """

        results = connectToMySQL('dec_22_exm_review').query_db(query, {'user_id': user_id})
        
        return [cls(character) for character in results] # list comprehension

    @classmethod
    def destroy(cls, id):

        query  = """
            DELETE FROM 
                pets 
            WHERE 
                id = %(id)s;
        """
        
        return connectToMySQL('dec_22_exm_review').query_db(query, {'id': id})

    @classmethod
    def save(cls, data):

        query = """
            INSERT INTO 
                pets 
                (name, type, age, hobby, favorite_snack, user_id, image_path) 
            VALUES 
                (%(name)s, %(type)s, %(age)s, %(hobby)s, %(favorite_snack)s, %(user_id)s, %(image_path)s);
        """

        result = connectToMySQL('dec_22_exm_review').query_db(query, data)

        return result

    @classmethod
    def get_one(cls, id):

        query  = """
            SELECT 
                * ,
                (SELECT COUNT(*) FROM user_like_pet WHERE user_like_pet.pet_id = pets.id) AS likes_count

            FROM 
                pets 
            
            LEFT JOIN user_like_pet ON user_like_pet.pet_id = pets.id
            LEFT JOIN users ON users.id = user_like_pet.user_id

            WHERE 
                pets.id = %(id)s;
        """

        result = connectToMySQL('dec_22_exm_review').query_db(query, {'id': id})

        if not result:
            return None

        pet = cls(result[0])

        for row in result:
            if row['users.id']:
                pet.likes.append({
                    'id': row['users.id'],
                    'first_name': row['first_name'],
                    'last_name': row['last_name'],
                    'password': row['password']
                })

        return pet

    @classmethod
    def update(cls, data):

        query = """
            UPDATE 
                pets 
            SET 
                name=%(name)s,
                type=%(type)s,
                age=%(age)s,
                hobby=%(hobby)s,
                favorite_snack=%(favorite_snack)s
                
            WHERE 
                id = %(id)s;
        """

        return connectToMySQL('dec_22_exm_review').query_db(query, data)

    @classmethod
    def like(cls, pet_id, user_id):

        query = """
            INSERT INTO 
                user_like_pet 
                (pet_id, user_id) 
            VALUES 
                (%(pet_id)s, %(user_id)s);
        """

        result = connectToMySQL('dec_22_exm_review').query_db(query, {
            'pet_id': pet_id,
            'user_id': user_id
        })

        return result

    @classmethod
    def unlike(cls, pet_id, user_id):

        query  = """
            DELETE FROM 
                user_like_pet 
            WHERE 
                pet_id = %(pet_id)s AND user_id = %(user_id)s ;
        """
        
        return connectToMySQL('dec_22_exm_review').query_db(query, {
            'user_id': user_id,
            'pet_id': pet_id
            })