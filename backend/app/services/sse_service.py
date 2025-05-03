from flask import Response, current_app
import json
import redis
from typing import Dict, Any


class SSEService:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=current_app.config["REDIS_HOST"],
            port=current_app.config["REDIS_PORT"],
            db=current_app.config["REDIS_DB"],
        )
        self.pubsub = self.redis_client.pubsub()

    def publish_event(self, user_id: int, event_type: str, data: Dict[str, Any]):
        """Publish an event to Redis"""
        channel = f"user:{user_id}"
        event_data = {"type": event_type, "data": data}
        self.redis_client.publish(channel, json.dumps(event_data))

    def subscribe_to_user_events(self, user_id: int):
        """Subscribe to user events and yield them as SSE"""
        channel = f"user:{user_id}"
        self.pubsub.subscribe(channel)

        def event_stream():
            try:
                for message in self.pubsub.listen():
                    if message["type"] == "message":
                        yield f"data: {message['data'].decode('utf-8')}\n\n"
            except Exception as e:
                current_app.logger.error(f"SSE Error: {str(e)}")
                yield f"data: {json.dumps({'error': str(e)})}\n\n"

        return Response(
            event_stream(),
            mimetype="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",
            },
        )
