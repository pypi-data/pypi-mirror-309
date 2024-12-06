from ..models import EventTrack, EventTrackLane, TimeMode, Keyframe, ConcreteSchemaType
from .instance import InstanceProxy
from typing import List, Dict
from uuid import uuid4

class EventTrackArgs:
    def __init__(self, name: str, short_id: str, time_mode: TimeMode):
        self.name = name
        self.short_id = short_id
        self.time_mode = time_mode


class KeyframeArgs:
    def __init__(self, time: float, data: any):
        self.time = time
        self.data = data
        

class EventTrackLaneArgs:
    def __init__(self, short_id: str, name: str, type: ConcreteSchemaType, keys: List[KeyframeArgs]):
        self.short_id = short_id
        self.name = name
        self.type = type
        self.keys = keys


class KeyframeArgs:
    def __init__(self, time: float, data: any):
        self.time = time
        self.data = data


class EventTrackProxy:
    def __init__(self, instance: InstanceProxy, client, args: EventTrackArgs):
        self.client = client
        self.args = args
        self.instance = instance
        self.lanes: Dict[str, EventTrackLaneProxy] = {}
   
    def id(self) -> str:
        return f"{self.instance.args.service_id}:{self.args.short_id}"
    
    async def add_lane(self, args: EventTrackLaneArgs) -> 'EventTrackLaneProxy':
        p = EventTrackLaneProxy(self.instance, self.client, args, self)
        self.lanes[p.id()] = p
        await self.save()
        return p
    
    async def save(self):
        event_track = EventTrack(
            id=self.id(),
            name=self.args.name,
            time_mode=self.args.time_mode,
        )

        if event_track.id not in self.client.event_tracks or self.client.event_tracks[event_track.id] != event_track.hash:
            await self.client.set_data(event_track, 'Event Track')
            self.client.event_tracks[event_track.id] = event_track

    async def save_all(self):
        await self.save()
        for lane in self.lanes.values():
            await lane.save()


class EventTrackLaneProxy:
    def __init__(self, instance: InstanceProxy, client, args: EventTrackLaneArgs, track: EventTrackProxy, sent: Dict[str, Keyframe]):
        self.client = client
        self.args = args
        self.track = track
        self.sent = sent

    def id(self) -> str:
        return f"{self.track.id()}:{self.args.short_id}"
    
    async def save(self):
        tx = str(uuid4())

        frames = [
            Keyframe(
                event_track_id=self.track.id(),
                data_type=self.args.type,
                id=f"{self.track.id()}-{key.time}",
                layer_id=self.id(),
                time=key.time,
                value=key.data,
            )
            for key in self.args.keys
        ]

        # transcode groupBy()
        grouped_by_lanes = {}
        for frame in frames:
            if frame.layer_id not in grouped_by_lanes:
                grouped_by_lanes[frame.layer_id] = []
            grouped_by_lanes[frame.layer_id].append(frame)

        # transcode map()
        lanes = [
            EventTrackLane(
                id=layer_id,
                name=self.args.name,
                event_track_id=self.track.id(),
                type=self.args.type,
            )
            for layer_id in grouped_by_lanes
        ]
        for lane in lanes:
            await self.client.send_event(lane, tx)

        to_delete = set(self.sent.keys())
        for frame in frames:
            to_delete.discard(frame.id)

        self.sent.clear()

        for frame in frames:
            self.sent[frame.id] = frame
            await self.client.send_event(frame, tx)
        
        for frame_id in to_delete:
            await self.client.delete_data(frame_id, tx)

        self.sent.clear()