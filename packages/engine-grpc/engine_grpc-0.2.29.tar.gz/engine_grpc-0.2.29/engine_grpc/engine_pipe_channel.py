from __future__ import annotations
import os
import asyncio
from dataclasses import dataclass
from compipe.utils.singleton import Singleton
from compipe.runtime_env import Environment as env
from compipe.utils.logging import logger
from grpclib.client import Channel
from grpclib.config import Configuration
from ugrpc_pipe import UGrpcPipeStub

from .engine_pipe_abstract import EngineAbstract


class GrpcCacheConfig(metaclass=Singleton):
    host: str = None
    port: int = 0

    def update(self, host: str, port: int):
        self.host = host
        self.port = port

    @property
    def channel(self):
        return None if self.host == None or self.port == 0 else f"{self.host}:{self.port}"


@dataclass
class GrpcChannelConfig:
    description: str = "message_length = 100*1024*1024"
    channel: str = None
    max_msg_length: int = 104857600

    @classmethod
    def retrieve_grpc_cfg(cls, engine: str) -> GrpcChannelConfig:
        if (grpc_cfg_json := env().get_value_by_path(['grpc', engine], None)) == None:
            raise ValueError(
                f"Not found matched grpc config for engine: {engine}")

        return GrpcChannelConfig(**grpc_cfg_json)


@dataclass
class base_channel(object):

    engine: EngineAbstract

    channel: str = None

    def __post_init__(self):

        self.grpc_cfg: GrpcChannelConfig = GrpcChannelConfig.retrieve_grpc_cfg(
            engine=self.engine.engine_platform)

        if self.engine.channel != None:
            self.channel = self.engine.channel
        elif (channel := os.environ.get(f"{self.engine.engine_platform.upper()}_GRPC_CHANNEL", None)) != None:
            # try to load specific channel from system environment
            # allow user to dynamically change the channel by setting the environment variable
            self.channel = channel
        else:
            self.channel = self.grpc_cfg.channel
            # logger.warning(f"Initialize gRPC channel by passing default values {self.channel}")

        if ':' not in self.channel:
            raise ValueError(
                'The specified channel content is invalid. Only accept format <ip>:<port> e.g., 127.0.0.1:50051')

        # declare the maximum message length by passing the values from config
        cfg = Configuration(http2_stream_window_size=self.grpc_cfg.max_msg_length,
                            http2_connection_window_size=self.grpc_cfg.max_msg_length)

        # parse host address and port from the specified channel definition

        host, port = tuple(self.channel.split(':'))
        # construct a channel instance
        self.grpc_channel = Channel(
            host=host, port=port, config=cfg, loop=self.engine.event_loop)

        logger.debug(f"Established gRPC channel with channel: {self.channel}")

    def __enter__(self):
        raise NotImplementedError

    def __exit__(self, exc_type, exc_val, exc_tb):
        # make sure the grpc channel gets closed
        self.grpc_channel.close()


class general_channel(base_channel):

    def __post_init__(self):
        # try to retrieve the existing event loop. or create a new one.
        try:
            self.engine.event_loop = asyncio.get_event_loop()
        except RuntimeError:
            self.engine.event_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.engine.event_loop)

        super().__post_init__()

    def __enter__(self):
        # make a grpc stub and return it
        self.engine.stub = UGrpcPipeStub(channel=self.grpc_channel)
