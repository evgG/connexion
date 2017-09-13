import connexion
from model import Hero, User, init_db
from flask import jsonify
from flask_jwt import JWT, jwt_required, current_identity

db_uri = 'sqlite:///app.sqlite'


# jwt helpers
def authenticate(username, password=None):
    user = (db_session.query(User).
            filter(User.login == username).
            filter(User.password == password).one_or_none())
    return user


def identity(payload):
    # print(payload)
    return (db_session.query(User).
            filter(User.id == payload['identity']).one_or_none())


def post_greeting(name):
    return 'Hello {name}'.format(name=name)


def get_greeting():
    return dict(name='John')


def get_all():
    heroes = db_session.query(Hero).all()
    # heroes = hero.Hero.query.all()
    return [h.serialize() for h in heroes]


def post_hero(name):
    db_session.add(Hero(name=name))
    db_session.commit()
    return connexion.NoContent, 201


def get_hero(id):
    q = (db_session.query(Hero).
         filter(Hero.id == id).one_or_none())
    if q:
        return q.serialize(), 200
    return connexion.NoContent, 404


def put_hero(id, name):
    q = (db_session.query(Hero).
         filter(Hero.id == id).one_or_none())
    if q:
        q.name = name
        db_session.commit()
        return connexion.NoContent, 201
    return connexion.NoContent, 404


def delete_hero(id):
    q = (db_session.query(Hero).
         filter(Hero.id == id).one_or_none())
    if q:
        db_session.query(Hero).filter(Hero.id == id).delete()
        db_session.commit()
        return connexion.NoContent, 204
    return connexion.NoContent, 404


app = connexion.FlaskApp(__name__, specification_dir='swagger/')
# app = connexion.FlaskApp(__name__, specification_dir='swagger/',
#                          swagger_ui=False)
db_session = init_db(db_uri)
app.add_api('your_api.yaml')


@app.route('/unprotected')
def unprotected():
    return jsonify({
        'message': 'This is an unprotected resource.'
    })


@app.route('/protected')
@jwt_required()
def protected():
    return jsonify({
        'message': 'This is a protected resource.',
        'current_identity': str(current_identity)
    })


app.app.debug = True
app.app.config['SECRET_KEY'] = 'super-secret'

jwt = JWT(app.app, authenticate, identity)

app.run(port=8080)
