import abc
from typing import Protocol, Any

class TrafficProxy(Protocol):

    # 使用場境
    # - subscription 付款時
    def redirect(self, url: str) -> Any: ...
    def SyncPost(self) -> Any: ...
    def AsyncPost(self) -> Any: ...
        # ReturnImmediately



class PaymentGateway(abc.ABC):

    def __init__(self, traffic_proxy: TrafficProxy) -> None:
        super().__init__()
        self.traffic_proxy: TrafficProxy = traffic_proxy

    @classmethod
    def _generate_transaction_id(cls) -> str:
        return 

    def redirect(self, url: str):
        return self.traffic_proxy.redirect(url)
    
    def get_billing_info(self):
        return 

    # @abc.abstractmethod
    # def 