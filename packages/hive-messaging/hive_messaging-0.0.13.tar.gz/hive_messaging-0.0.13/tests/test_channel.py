import json
import re

from pika import BasicProperties, DeliveryMode

from hive.messaging import Channel


class MockPika:
    def __getattr__(self, attr):
        if attr == "_prefetch_count":
            raise AttributeError(attr)
        raise NotImplementedError(attr)


class MockMethod:
    def __init__(self, *, returns=None):
        self.call_log = []
        self._returns = returns

    def __call__(self, *args, **kwargs):
        self.call_log.append((args, kwargs))
        return self._returns


expect_properties = BasicProperties(
    content_type="application/json",
    delivery_mode=DeliveryMode.Persistent,
)


def test_publish_request():
    mock = MockPika()
    mock.exchange_declare = MockMethod()
    mock.basic_publish = MockMethod()

    channel = Channel(pika=mock)
    channel.publish_request(
        message={
            "hello": "world",
        },
        routing_key="hallo.wereld",
    )

    assert mock.exchange_declare.call_log == [((), {
        "exchange": "hive.requests",
        "exchange_type": "direct",
        "durable": True,
    })]
    assert mock.basic_publish.call_log == [((), {
        "exchange": "hive.requests",
        "routing_key": "hallo.wereld",
        "body": b'{"hello": "world"}',
        "properties": expect_properties,
        "mandatory": True,
    })]


def test_consume_requests():
    mock = MockPika()
    mock.exchange_declare = MockMethod()
    mock.basic_qos = MockMethod()
    mock.queue_declare = MockMethod(
        returns=type("Result", (), dict(
            method=type("Method", (), dict(
                queue="TeStQuEu3")))))
    mock.queue_bind = MockMethod()
    mock.basic_consume = MockMethod()
    on_message_callback = MockMethod()
    mock.basic_ack = MockMethod()

    channel = Channel(pika=mock)
    channel.consume_requests(
        queue="arr.pirates",
        on_message_callback=on_message_callback,
    )

    assert mock.exchange_declare.call_log == [((), {
        "exchange": "hive.requests",
        "exchange_type": "direct",
        "durable": True,
    }), ((), {
        "exchange": "hive.dead.letter",
        "exchange_type": "direct",
        "durable": True,
    })]
    assert mock.basic_qos.call_log == [((), {
        "prefetch_count": 1,
    })]
    assert mock.queue_declare.call_log == [((
        "x.arr.pirates",
    ), {
        "durable": True,
    }), ((
        "arr.pirates",
    ), {
        "durable": True,
        "arguments": {
            "x-dead-letter-exchange": "hive.dead.letter",
        },
    })]
    assert mock.queue_bind.call_log == [((), {
        "queue": "x.arr.pirates",
        "exchange": "hive.dead.letter",
        "routing_key": "arr.pirates",
    }), ((), {
        "queue": "arr.pirates",
        "exchange": "hive.requests",
        "routing_key": "arr.pirates",
    })]

    assert len(mock.basic_consume.call_log) == 1
    assert len(mock.basic_consume.call_log[0]) == 2
    got_callback = mock.basic_consume.call_log[0][1]["on_message_callback"]
    assert mock.basic_consume.call_log == [((), {
        "queue": "arr.pirates",
        "on_message_callback": got_callback,
    })]
    assert on_message_callback.call_log == []
    assert mock.basic_ack.call_log == []

    method = type("method", (), {"delivery_tag": 5})
    got_callback(channel._pika, method, hello="W0RLD")

    assert on_message_callback.call_log == [((
        channel,
        method,
    ), {
        "hello": "W0RLD",
    })]
    assert mock.basic_ack.call_log == [((), {"delivery_tag": 5})]


def test_publish_mandatory_event():
    mock = MockPika()
    mock.exchange_declare = MockMethod()
    mock.basic_publish = MockMethod()

    channel = Channel(pika=mock)
    channel.publish_event(
        message={
            "hello": "world",
        },
        routing_key="hoolloo.wooreled",
        mandatory=True,
    )

    assert mock.exchange_declare.call_log == [((), {
        "exchange": "hive.events",
        "exchange_type": "direct",
        "durable": True,
    })]
    assert mock.basic_publish.call_log == [((), {
        "exchange": "hive.events",
        "routing_key": "hoolloo.wooreled",
        "body": b'{"hello": "world"}',
        "properties": expect_properties,
        "mandatory": True,
    })]


def test_consume_mandatory_events():
    mock = MockPika()
    mock.exchange_declare = MockMethod()
    mock.basic_qos = MockMethod()
    mock.queue_declare = MockMethod(
        returns=type("Result", (), dict(
            method=type("Method", (), dict(
                queue="TeStQuEu3")))))
    mock.queue_bind = MockMethod()
    mock.basic_consume = MockMethod()
    on_message_callback = MockMethod()
    mock.basic_ack = MockMethod()

    channel = Channel(pika=mock)
    channel.consume_events(
        queue="arr.pirates",
        on_message_callback=on_message_callback,
        mandatory=True,
    )

    assert mock.exchange_declare.call_log == [((), {
        "exchange": "hive.events",
        "exchange_type": "direct",
        "durable": True,
    }), ((), {
        "exchange": "hive.dead.letter",
        "exchange_type": "direct",
        "durable": True,
    })]
    assert mock.basic_qos.call_log == [((), {
        "prefetch_count": 1,
    })]
    assert mock.queue_declare.call_log == [((
        "x.arr.pirates",
    ), {
        "durable": True,
    }), ((
        "arr.pirates",
    ), {
        "durable": True,
        "arguments": {
            "x-dead-letter-exchange": "hive.dead.letter",
        },
    })]
    assert mock.queue_bind.call_log == [((), {
        "queue": "x.arr.pirates",
        "exchange": "hive.dead.letter",
        "routing_key": "arr.pirates",
    }), ((), {
        "queue": "arr.pirates",
        "exchange": "hive.events",
        "routing_key": "arr.pirates",
    })]

    assert len(mock.basic_consume.call_log) == 1
    assert len(mock.basic_consume.call_log[0]) == 2
    got_callback = mock.basic_consume.call_log[0][1]["on_message_callback"]
    assert mock.basic_consume.call_log == [((), {
        "queue": "arr.pirates",
        "on_message_callback": got_callback,
    })]
    assert on_message_callback.call_log == []
    assert mock.basic_ack.call_log == []

    method = type("method", (), {"delivery_tag": 5})
    got_callback(channel._pika, method, hello="W0RLD")

    assert on_message_callback.call_log == [((
        channel,
        method,
    ), {
        "hello": "W0RLD",
    })]
    assert mock.basic_ack.call_log == [((), {"delivery_tag": 5})]


def test_publish_fanout_event():
    mock = MockPika()
    mock.exchange_declare = MockMethod()
    mock.basic_publish = MockMethod()

    channel = Channel(pika=mock)
    channel.publish_event(
        message={
            "bonjour": "madame",
        },
        routing_key="egg.nog",
    )

    assert mock.exchange_declare.call_log == [((), {
        "exchange": "hive.egg.nog",
        "exchange_type": "fanout",
        "durable": True,
    })]
    assert mock.basic_publish.call_log == [((), {
        "exchange": "hive.egg.nog",
        "routing_key": "",
        "body": b'{"bonjour": "madame"}',
        "properties": expect_properties,
        "mandatory": False,
    })]


def test_consume_fanout_events():
    mock = MockPika()
    mock.exchange_declare = MockMethod()
    mock.basic_qos = MockMethod()
    mock.queue_declare = MockMethod(
        returns=type("Result", (), dict(
            method=type("Method", (), dict(
                queue="TeStQuEu3")))))
    mock.queue_bind = MockMethod()
    mock.basic_consume = MockMethod()
    on_message_callback = MockMethod()
    mock.basic_ack = MockMethod()

    channel = Channel(pika=mock)
    channel.consume_events(
        queue="arr.pirates",
        on_message_callback=on_message_callback,
    )

    assert mock.exchange_declare.call_log == [((), {
        "exchange": "hive.arr.pirates",
        "exchange_type": "fanout",
        "durable": True,
    }), ((), {
        "exchange": "hive.dead.letter",
        "exchange_type": "direct",
        "durable": True,
    })]
    assert mock.basic_qos.call_log == [((), {
        "prefetch_count": 1,
    })]
    assert mock.queue_declare.call_log == [((
        "x.pytest.arr.pirates",
    ), {
        "durable": True,
    }), ((
        "pytest.arr.pirates",
    ), {
        "exclusive": True,
        "arguments": {
            "x-dead-letter-exchange": "hive.dead.letter",
        },
    })]
    assert mock.queue_bind.call_log == [((), {
        "queue": "x.pytest.arr.pirates",
        "exchange": "hive.dead.letter",
        "routing_key": "pytest.arr.pirates",
    }), ((), {
        "queue": "TeStQuEu3",
        "exchange": "hive.arr.pirates",
    })]

    assert len(mock.basic_consume.call_log) == 1
    assert len(mock.basic_consume.call_log[0]) == 2
    got_callback = mock.basic_consume.call_log[0][1]["on_message_callback"]
    assert mock.basic_consume.call_log == [((), {
        "queue": "TeStQuEu3",
        "on_message_callback": got_callback,
    })]
    assert on_message_callback.call_log == []
    assert mock.basic_ack.call_log == []

    method = type("method", (), {"delivery_tag": 5})
    got_callback(channel._pika, method, hello="W0RLD")

    assert on_message_callback.call_log == [((
        channel,
        method,
    ), {
        "hello": "W0RLD",
    })]
    assert mock.basic_ack.call_log == [((), {"delivery_tag": 5})]


def test_tell_user():
    mock = MockPika()
    mock.exchange_declare = MockMethod()
    mock.basic_publish = MockMethod()

    channel = Channel(pika=mock)
    channel.tell_user("bonjour!")

    assert mock.exchange_declare.call_log == [((), {
        "exchange": "hive.chat.messages",
        "exchange_type": "fanout",
        "durable": True,
    })]

    assert len(mock.basic_publish.call_log) == 1
    assert len(mock.basic_publish.call_log[0]) == 2
    got_body = mock.basic_publish.call_log[0][1]["body"]
    assert mock.basic_publish.call_log == [((), {
        "exchange": "hive.chat.messages",
        "routing_key": "",
        "body": got_body,
        "properties": expect_properties,
        "mandatory": False,
    })]

    assert isinstance(got_body, bytes)
    message = json.loads(got_body)

    uuid = message.pop("uuid")
    assert isinstance(uuid, str)
    uuid_re = "-".join(f"[0-9a-f]{{{n}}}" for n in (8, 4, 4, 4, 12))
    uuid_re = f"^{uuid_re}$"
    assert re.match(uuid_re, uuid)

    timestamp = message.pop("timestamp")
    assert isinstance(timestamp, str)
    timestamp_re = r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d{6}\+00:00$"
    assert re.match(timestamp_re, timestamp)

    assert message == {
        "sender": "hive",
        "text": "bonjour!",
    }
