
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Game(Base):
    __tablename__ = 'games'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    platform = Column(String)
    genre = Column(String)
    price = Column(Integer)
    reviews = relationship('Review', backref='game')

class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True)
    score = Column(Integer)
    comment = Column(String)
    game_id = Column(Integer, ForeignKey('games.id'))

# test_game.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Game, Review

class TestGame:
    '''Class Game in models.py'''

    # start session, reset db
    Session = sessionmaker(bind=engine)
    session = Session()

    # add test data
    mario_kart = Game(
        title="Mario Kart",
        platform="Switch",
        genre="Racing",
        price=60
    )

    session.add(mario_kart)
    session.commit()

    mk_review_1 = Review(
        score=10,
        comment="Wow, what a game",
        game_id=mario_kart.id
    )

    mk_review_2 = Review(
        score=8,
        comment="A classic",
        game_id=mario_kart.id
    )

    session.bulk_save_objects([mk_review_1, mk_review_2])
    session.commit()


class TestReview:
    '''Class Review in models.py'''

    # start session, reset db
    engine = create_engine()
    Session = sessionmaker(bind=engine)
    session = Session()

    # add test data
    skyrim = Game(
        title="The Elder Scrolls V: Skyrim",
        platform="PC",
        genre="Adventure",
        price=20
    )

    session.add(skyrim)
    session.commit()

    skyrim_review = Review(
        score=10,
        comment="Wow, what a game",
        game_id=skyrim.id
    )

    session.add(skyrim_review)
    session.commit()

    def test_review_has_correct_attributes(self):
        '''has attributes "id", "score", "comment", "game_id".'''
        assert all(
            hasattr(TestReview.skyrim_review, attr)
            for attr in ["id", "score", "comment", "game_id"]
        )

    def test_knows_about_associated_game(self):
        '''has attribute "game" that is the "Game" object associated with its game_id.'''
        assert TestReview.skyrim_review.game == TestReview.skyrim
