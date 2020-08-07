import pytest

from app.main import create_app, DbSession

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

@pytest.yield_fixture(scope="session")
def app():
    """
    Creates a new Flask application for a test duration.
    Uses application factory `create_app`.
    """
    #DEBUG
    #_app = create_app("testingsession", config_object=TestConfig)
    _app = create_app("testingsession", config_object='test') #TestConfig)

    # Base is declarative_base()
    Base.metadata.create_all(bind=_app.engine)
    _app.connection = _app.engine.connect()

    # No idea why, but between this app() fixture and session()
    # fixture there is being created a new session object
    # somewhere.  And in my tests I found out that in order to
    # have transactions working properly, I need to have all these
    # scoped sessions configured to use current connection.
    DbSession.configure(bind=_app.connection)

    yield _app

    # the code after yield statement works as a teardown
    _app.connection.close()
    Base.metadata.drop_all(bind=_app.engine)


@pytest.yield_fixture(scope="function")
def session(app):
    """
    Creates a new database session (with working transaction)
    for a test duration.
    """
    app.transaction = app.connection.begin()

    # pushing new Flask application context for multiple-thread
    # tests to work
    ctx = app.app_context()
    ctx.push()

    session = DbSession()

    yield session

    # the code after yield statement works as a teardown
    app.transaction.close()
    session.close()
    ctx.pop()

@pytest.yield_fixture(scope="function")
def test_client(app):
    yield app.test_client()
