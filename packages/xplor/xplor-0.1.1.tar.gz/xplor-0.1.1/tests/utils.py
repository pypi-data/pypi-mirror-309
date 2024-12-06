import gurobipy as gp
import pytest
import xplor  # noqa: F401


@pytest.fixture
def model():
    env = gp.Env()
    model = gp.Model(env=env)
    yield model
    model.close()
    env.close()
