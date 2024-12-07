import asyncio
import pytest
import microBeesPy

microBees = microBeesPy.MicroBees("336484291124875","8CeCvvgS2gKv8XUE42DLEZCce677yEu5gRvRE7p3")

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

@pytest.mark.asyncio
async def test_mqtt_client_connect():
    mqtt_client = microBeesPy.MicrobeesMqtt(host="mqtt.example.com", port=1883, username="mqtt_user", password="mqtt_password")
    print("mqtt_client_connect")
    print(mqtt_client)
    assert mqtt_client is not None

@pytest.mark.asyncio
async def test_mqtt_client_subscribe():
    mqtt_client = microBeesPy.MicrobeesMqtt(host="mqtt.example.com", port=1883, username="mqtt_user", password="mqtt_password")
    await mqtt_client.connect()
    await mqtt_client.subscribe("microbees/sensor/data", handle_message)
    print("mqtt_client_subscribe")
    print(mqtt_client)
    assert mqtt_client is not None

def handle_message(json_data):
    """Gestisce i messaggi JSON ricevuti."""
    print(f"Handling received JSON message: {json_data}")