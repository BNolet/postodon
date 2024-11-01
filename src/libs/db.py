from .models import *

from functools import wraps
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import NoResultFound
from sqlalchemy import select, exists, create_engine


class DB():
    def __init__(self,):
        self.engine = create_engine('sqlite:///database/postodon.db', echo=True)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()



    def session_scope(func):
        @wraps(func)
        def wrapper(self,*args, **kwargs):
            with self.session as session:
                try:
                    result = func(self, *args, **kwargs)
                    print("Committing changes")
                    session.commit()
                    return result
                except Exception as e:
                    print(f'Exception encounered{repr(e)}')
                    print('Rolling back changes')
                    session.rollback()
                    raise
                finally:
                    print('Closing session')
                    session.close()
        return wrapper
    
    # User
    @session_scope
    def create_user(self,email:str, 
                    display_name:str, 
                    username:str, 
                    password:str, 
                    is_admin:bool=False, 
                    is_active:bool=False, 
                    requesting_user_id:str=None):
        try:
            if not requesting_user_id:
                query = select(User)
                if not self.session.execute(query).first():
                    pass
                else:
                    raise PermissionError
            
            if username and password:
                print('Creating user')
                user = User(username=username,
                        password=password,
                        display_name=display_name,
                        email=email,
                        is_admin=is_admin,
                        is_active=is_active)

                self.session.add(user)
            return user
        except PermissionError:
            print(f"You are not permitted to create users")
            raise
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            raise

    @session_scope
    def get_user(self, 
                 username:str=None,
                 user_id:str=None):
        if username:
            query = select(User).where(User.username == username) 
        elif user_id:
            query = select(User).where(User.id == user_id)
        else:
            query = select(User).where(User.id.isnot(None))

        try:
            result = self.session.execute(query).first()
            if result:
                user = result[0]
            else:
                raise NoResultFound
            self.session.expunge_all()
            return user
        except NoResultFound:
            print(f"No user found with ID {user_id}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            raise

        
    @session_scope
    def update_user(self, 
                    user_id, 
                    updated_user):
        try:
            query = select(User).where(User.id == user_id)
            user = self.session.execute(query)

            for key, value in updated_user.items():
                if hasattr(user, key) and key != "id" and key != "password":
                    setattr(user, key, value)
            
            self.session.commit()
            return user
        
        except NoResultFound:
            print("No user found with ID {user_id}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            raise

    @session_scope
    def delete_user(self, 
                    user_id):
        try:
            query = select(User).where(User.id == user_id)
            user = self.session.execute(query).first()

            self.session.delete(user)
            return True
        except NoResultFound:
            print(f"A user with ID {user_id} does not exist.")
            return None
        except Exception as e:
            print(f"An unexpected error occurred")
            raise
        
    # Post
    @session_scope
    def create_post(self, 
                    content:str, 
                    created_by_email:str, 
                    date_posted:DateTime=datetime.now(UTC),
                    recurring:bool=False):
        # Default timing is temporary. Scope for now is for "recurring" posts.
        if content and created_by_email:
            user = self.session.execute(select(User).where(User.email == created_by_email)).first()
            post = Post(
                content=content,
                created_by=user[0].id,
                date_posted=date_posted,
                recurring=recurring)

            self.session.add(post)
        
    @session_scope
    def get_post(self, 
                 post_id):
        if post_id:
            query = select(Post).where(Post.id == post_id)
            return self.session.execute(query)
    
    @session_scope
    def get_posts_by_user(self, 
                          user_id:str, 
                          date_posted:DateTime=None):
        if user_id:
            query = select(Post).where(Post.created_by == user_id)
            posts = self.session.execute(query).scalars().all()
            posts = [post.dict for post in posts]
            return posts
        
    @session_scope
    def update_post(self, 
                    user_id:str, 
                    post_id:str, 
                    content:str=None, 
                    date_posted:DateTime=None):
        query = select(Post).where(Post.created_by == user_id, Post.id == post_id)
        post = self.session.execute(query).first()

        if not post:
            return None

        if content:
            post.content = content

        if date_posted:
            post.date_posted = date_posted

        return post
    
    @session_scope
    def delete_post(self, 
                    user_id:str, 
                    post_id:str):
        query = select(Post).where(Post.created_by == user_id, Post.id == post_id)
        post = self.session.execute(query).first()[0]

        try:
            self.session.delete(post)
            return True
        except Exception as e:
            return False
        
    #Social

    @session_scope
    def create_social(self, 
                    username: str, 
                    access_token: str, 
                    server: str, 
                    instance_user_id:str, 
                    user_id:str):
        new_social = Social(
            username=username,
            access_token=access_token,
            instance_domain=server,
            instance_user_id=instance_user_id,
            user_id=user_id
        )
        try:
            self.session.add(new_social)
            print(f"Added social entry for user: {username}")
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise

    @session_scope
    def update_social(self, 
                      updated_social:Social):
        try:
            query = select(Social).where(Social.id == updated_social.id)
            social = self.session.execute(query)

            for key, value in updated_social.items():
                if hasattr(social, key) and key != "id":
                    setattr(social, key, value)

        except NoResultFound:
            print(f"No social found with ID {updated_social.id}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise

    @session_scope
    def delete_social(self, user_id, social_id):
        try:
            query = select(Social).where(Social.id == social_id)
            social = self.session.execute(query)

            if social.user_id != user_id:
                raise PermissionError

            self.session.delete(social)

        except NoResultFound:
            print(f"No social found with ID {social_id}")
            return None
        except PermissionError:
            print(f"User of ID {user_id} is not permitted to delete this social")

    @session_scope
    def get_social(self, 
                   user_id): 
        query = select(Social).where(Social.user_id == user_id)
        result = self.session.execute(query).first()
        if result:
            social = result[0]
        else:
            return False
        self.session.expunge_all()
        return social.dict


    # Version
    @session_scope
    def create_version(self, 
                       major:int, 
                       minor:int, 
                       patch:int):
        version = Version(major=major,minor=minor,patch=patch)
        self.session.add(version)

    # Instance

    @session_scope
    def create_instance(self, 
                        domain:str, 
                        client_id:str, 
                        client_secret:str):
        instance = Instance(domain=domain,
                            client_id=client_id,
                            client_secret=client_secret)
        self.session.add(instance)
        id = instance.id
        return id

    @session_scope
    def get_instance(self, 
                     domain:str):
        query = select(Instance).where(Instance.domain == domain)
        instance = self.session.execute(query).first()

        if instance:
            self.session.expunge_all()
            return instance[0]
        else:
            return False
        
    @session_scope
    def update_instance(self,
                        domain:str,
                        new_domain:str):
        query = select(Instance).where(Instance.domain == domain)
        instance = self.session.execute(query).first()

        if instance:
            instance.domain == new_domain
            self.session.commit()
            return instance
        else:
            return False