import asyncio
import pytest
from microBeesPy.microbees import MicroBees

microBees = MicroBees("336484291124875","8CeCvvgS2gKv8XUE42DLEZCce677yEu5gRvRE7p3")

@pytest.fixture(scope="module")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.mark.asyncio
async def test_login():
    result =  await microBees.login("test@microbees.com","Testtest1")
    print("Login")
    print(result)
    assert result is not None

@pytest.mark.asyncio
async def test_get_bees():
    result = await microBees.getBees()
    print("getBees")
    print(result)
    assert result is not None

@pytest.mark.asyncio
async def test_send_command():
    result = await microBees.sendCommand(25497,1)
    print("sendCommand")
    print(result)
    assert result is True

@pytest.mark.asyncio
async def test_get_actuator_by_id():
    result = await microBees.getActuatorById(25497)
    print("getActuatorById")
    print(result)
    assert result is not None

@pytest.mark.asyncio
async def test_get_my_bees_by_ids():
    result = await microBees.getMyBeesByIds([24907])
    print("getMyBeesByIds")
    print(result)
    assert result is not None

@pytest.mark.asyncio
async def test_get_my_profile():
    result = await microBees.getMyProfile()
    print("getMyProfile")
    print(result)
    assert result is not None