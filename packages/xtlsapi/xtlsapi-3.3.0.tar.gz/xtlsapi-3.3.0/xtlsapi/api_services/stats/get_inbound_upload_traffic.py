import grpc
from xtlsapi.xray_api.app.stats.command import command_pb2
from .._base import BaseService


class GetInboundUploadTraffic(BaseService):
    def get_inbound_upload_traffic(self, tag, reset=False):
        try:
            return self.stats_stub.GetStats(
                command_pb2.GetStatsRequest(
                    name=f"inbound>>>{tag}>>>traffic>>>uplink", reset=reset
                )
            ).stat.value
        except grpc.RpcError:
            # raise
            return None
