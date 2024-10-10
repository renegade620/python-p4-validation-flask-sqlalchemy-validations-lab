from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators
    @validates("name")
    def validate_name(self, key, name):
        if not name:
            raise ValueError("All authors have a name")
        if Author.query.filter(Author.name == name).first():
            raise ValueError("Name already exists")
        return name
    
    @validates('phone_number')
    def validate_phone_num(self, key, phone_number):
        if len(phone_number) != 10 or not phone_number.isdigit():
            raise ValueError("Phone number must be exactly 10 digits and numeric")
        return phone_number
        

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates("content")
    def validate_content(self, key, content):
        if len(content) < 250:
            raise ValueError("Post content should be at least 250 characters long")
        return content
    
    @validates("summary")
    def validate_summary(self, key, summary):
        if len(summary) > 250:
            raise ValueError("Post summary should be at most 250 characters long")
        return summary
    
    @validates("category")
    def validate_category(self, key, category):
        if category != "Fiction" or category != "Non-Fiction":
            raise ValueError("Post category is either Fiction or Non-Fiction")
        return category
    
    @validates("title")
    def validate_title(self, key, title):
        if not title:
            raise ValueError("Post must cotain title") 
             
        clickbait = ["Won't Believe", "Secret", "Top", "Guess"]

        if any(word in title for word in clickbait):
            raise ValueError("Title is insufficiently clickbait-y")
        
        return title

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
