import pytest
from alembic.config import Config
from alembic import command
from alembic.script import ScriptDirectory
from alembic.runtime.migration import MigrationContext
from alembic.autogenerate import compare_metadata
from sqlalchemy import create_engine
from app.core.database import Base  # CRITICAL: This must import all your models!
from app.core.config import settings

# Setup a clean engine just for migration tests
# We don't use the standard test fixture because we need raw connection control
@pytest.fixture
def migration_engine():
    # Use generic SQLite for speed in tests, or use settings.DATABASE_URL
    url = "sqlite:///:memory:" 
    engine = create_engine(url, pool_pre_ping=True)
    yield engine
    engine.dispose()

@pytest.fixture
def alembic_config(migration_engine):
    """
    Creates an Alembic configuration object that points to 
    the local alembic.ini and uses our test database connection.
    """
    # Point to the alembic.ini in the backend root
    config = Config("alembic.ini")
    
    # We don't want to use the DB URL from alembic.ini. 
    # We want to use our test memory DB.
    # We inject the connection directly later, but setting main_option helps some internal checks.
    config.set_main_option("sqlalchemy.url", str(migration_engine.url))
    config.set_main_option("script_location", "alembic")
    
    return config

def test_no_missing_migrations(migration_engine, alembic_config):
    """
    Crucial Test:
    1. Spins up an in-memory DB.
    2. Runs all existing migrations (upgrade head).
    3. Compares the DB state against the current SQLAlchemy Models (Base.metadata).
    4. Fails if there are any differences (meaning a migration is missing).
    """
    
    # 1. Establish connection
    with migration_engine.connect() as connection:
        # 2. Tell Alembic to use this connection
        alembic_config.attributes['connection'] = connection
        
        # 3. Run migrations to HEAD
        command.upgrade(alembic_config, "head")
        
        # 4. Configure migration context for comparison
        migration_context = MigrationContext.configure(connection)
        
        # 5. Compare the 'actual' DB (after migrations) vs 'expected' (metadata)
        # Note: We filter out 'alembic_version' table automatically
        diff = compare_metadata(migration_context, Base.metadata)
        
        # 6. Assert no differences found
        # If this fails, it means the developer changed a model but forgot 
        # to run `alembic revision --autogenerate`
        assert not diff, f"Schema mismatch detected! Missing migrations for: {diff}"

def test_migrations_up_down_up(migration_engine, alembic_config):
    """
    Sanity Check:
    Ensures that migrations can be applied, rolled back, and applied again.
    Catches syntax errors in downgrade scripts.
    """
    with migration_engine.connect() as connection:
        alembic_config.attributes['connection'] = connection
        
        # 1. Go Up
        command.upgrade(alembic_config, "head")
        
        # 2. Go Down (to the beginning)
        command.downgrade(alembic_config, "base")
        
        # 3. Go Up Again
        command.upgrade(alembic_config, "head")