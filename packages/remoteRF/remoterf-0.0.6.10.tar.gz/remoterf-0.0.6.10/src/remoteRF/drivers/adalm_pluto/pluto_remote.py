from ...core.grpc_client import rpc_client
from ...common.utils import *
from ...common.grpc import grpc_pb2
from ...core.grpc_client import get_tcp_calls

def try_get(function_name, token):
    try:
        return unmap_arg(rpc_client(function_name=f"Pluto:{function_name}:GET", args={'a':map_arg(token)}).results[function_name])
    except Exception as e:
        input(f"Error: {e}\nHit enter to continue...")
    return None

def try_set(function_name, value, token):
    try:
        rpc_client(function_name=f"Pluto:{function_name}:SET", args={function_name: map_arg(value), 'a':map_arg(token)})
    except Exception as e:
        input(f"Error: {e}\nHit enter to continue...")

class rx_def:
    pass

class tx_def:
    pass

class rx_tx_def(rx_def, tx_def):
    pass

class ad9364(rx_tx_def):
    pass

class Pluto: # client
    
    def __init__(self, token='', debug=False):
        self.token = token
        # self.try_set(function_name="ip", value=grpc_pb2.Argument(string_value=ip))
        
        if debug:
            print("Pluto Remote Client Initialized.")
        
    def api_token(self, token:str) -> None:
        self.token = token
        
    # def try_get(self, *, function_name):
    #     try:
    #         return rpc_client(function_name=f"Pluto:{function_name}:GET", args={'a':map_arg(self.token)}).results[function_name]
    #     except Exception as e:
    #         input(f"Error: {e}\nHit enter to continue...")
    #         return None

    # def try_set(self, *, function_name, value):
    #     try:
    #         rpc_client(function_name=f"Pluto:{function_name}:SET", args={function_name: value, 'a':map_arg(self.token)})
    #     except Exception as e:
    #         input(f"Error: {e}\nHit enter to continue...")
            
    # def test_print(self):
    #     if self.debug == True and get_tcp_calls() % 50 == 0:
    #         print(f'TCP Call Number: {get_tcp_calls()}')
    
    """AD9364 Transceiver"""

    @property
    def filter(self):
        return try_get("filter", self.token)

    @filter.setter
    def filter(self, value):
        try_set("filter", value, self.token)

    @property
    def loopback(self):
        """loopback: Set loopback mode. Options are:
        0 (Disable), 1 (Digital), 2 (RF)"""
        return try_get("loopback", self.token)

    @loopback.setter
    def loopback(self, value):
        try_set("loopback", value, self.token)

    @property
    def gain_control_mode_chan0(self):
        """gain_control_mode_chan0: Mode of receive path AGC. Options are:
        slow_attack, fast_attack, manual"""
        return try_get("gain_control_mode_chan0", self.token)

    @gain_control_mode_chan0.setter
    def gain_control_mode_chan0(self, value):
        try_set("gain_control_mode_chan0", value, self.token)

    @property
    def rx_hardwaregain_chan0(self):
        """rx_hardwaregain_chan0: Gain applied to RX path. Only applicable when
        gain_control_mode is set to 'manual'"""
        return try_get("rx_hardwaregain_chan0", self.token)

    @rx_hardwaregain_chan0.setter
    def rx_hardwaregain_chan0(self, value):
        try_set("rx_hardwaregain_chan0", value, self.token)

    @property
    def tx_hardwaregain_chan0(self):
        """tx_hardwaregain_chan0: Attenuation applied to TX path"""
        return try_get("tx_hardwaregain_chan0", self.token)

    @tx_hardwaregain_chan0.setter
    def tx_hardwaregain_chan0(self, value):
        try_set("tx_hardwaregain_chan0", value, self.token)

    @property
    def rx_rf_bandwidth(self):
        """rx_rf_bandwidth: Bandwidth of front-end analog filter of RX path"""
        return try_get("rx_rf_bandwidth", self.token)

    @rx_rf_bandwidth.setter
    def rx_rf_bandwidth(self, value):
        try_set("rx_rf_bandwidth", value, self.token)

    @property
    def tx_rf_bandwidth(self):
        """tx_rf_bandwidth: Bandwidth of front-end analog filter of TX path"""
        return try_get("tx_rf_bandwidth", self.token)

    @tx_rf_bandwidth.setter
    def tx_rf_bandwidth(self, value):
        try_set("tx_rf_bandwidth", value, self.token)

    @property
    def sample_rate(self):
        """sample_rate: Sample rate RX and TX paths in samples per second"""
        return try_get("sample_rate", self.token)

    @sample_rate.setter
    def sample_rate(self, rate):
        try_set("sample_rate", rate, self.token)

    @property
    def rx_lo(self):
        """rx_lo: Carrier frequency of RX path"""
        return try_get("rx_lo", self.token)

    @rx_lo.setter
    def rx_lo(self, value):
        try_set("rx_lo", value, self.token)

    @property
    def tx_lo(self):
        """tx_lo: Carrier frequency of TX path"""
        return try_get("tx_lo", self.token)

    @tx_lo.setter
    def tx_lo(self, value):
        try_set("tx_lo", value, self.token)

    #region ad9364

    # @property
    # def filter(self):
    #     return self.try_get(function_name="filter")
    
    # @filter.setter
    # def filter(self, value):
    #     self.try_set(function_name="filter", value=grpc_pb2.Argument(int64_value=value))
        
    # @property
    # def loopback(self):
    #     return self.try_get(function_name="loopback")
    
    # @loopback.setter
    # def loopback(self, value):
    #     self.try_set(function_name="loopback",  value=grpc_pb2.Argument(int64_value=value))
        
    # @property
    # def gain_control_mode_chan0(self):
    #     return self.try_get(function_name="gain_control_mode_chan0")
    
    # @gain_control_mode_chan0.setter
    # def gain_control_mode_chan0(self, value):
    #     self.try_set(function_name="gain_control_mode_chan0",  value=grpc_pb2.Argument(int64_value=value))
        
    # @property
    # def rx_hardwaregain_chan0(self):
    #     return self.try_get(function_name="rx_hardwaregain_chan0")
    
    # @rx_hardwaregain_chan0.setter
    # def rx_hardwaregain_chan0(self, value):
    #     self.try_set(function_name="rx_hardwaregain_chan0",  value=grpc_pb2.Argument(int64_value=value))
        
    # @property
    # def tx_hardwaregain_chan0(self):
    #     return self.try_get(function_name="tx_hardwaregain_chan0")
    
    # @tx_hardwaregain_chan0.setter
    # def tx_hardwaregain_chan0(self, value):
    #     self.try_set(function_name="tx_hardwaregain_chan0", value=grpc_pb2.Argument(int64_value=value))
        
    # @property
    # def rx_rf_bandwidth(self):
    #     return unmap_arg(self.try_get(function_name="rx_rf_bandwidth"))
    
    # @rx_rf_bandwidth.setter
    # def rx_rf_bandwidth(self, value):
    #     print("Setting RX RF Bandwidth")
    #     self.try_set(function_name="rx_rf_bandwidth",  value=grpc_pb2.Argument(int64_value=value))
        
    # @property
    # def tx_rf_bandwidth(self):
    #     return self.try_get(function_name="tx_rf_bandwidth")
    
    # @tx_rf_bandwidth.setter
    # def tx_rf_bandwidth(self, value):
    #     self.try_set(function_name="tx_rf_bandwidth",  value=grpc_pb2.Argument(int64_value=value))
        
    # @property
    # def sample_rate(self):
    #     return self.try_get(function_name="sample_rate")
    
    # @sample_rate.setter
    # def sample_rate(self, value):
    #     self.try_set(function_name="sample_rate",  value=grpc_pb2.Argument(int64_value=value))
        
    # @property
    # def rx_lo(self):
    #     return self.try_get(function_name="rx_lo").int64_value
    
    # @rx_lo.setter
    # def rx_lo(self, value):
    #     self.try_set(function_name="rx_lo", value=grpc_pb2.Argument(int64_value=value))
        
    # @property
    # def tx_lo(self):
    #     return self.try_get(function_name="tx_lo").int64_value
    
    # @tx_lo.setter
    # def tx_lo(self, value):
    #     self.try_set(function_name="tx_lo", value=grpc_pb2.Argument(int64_value=value))
        
    #endregion
    
    #region rx_def
    
    def rx(self):
        return unmap_arg(self.try_get(function_name="rx"))
    
    @property
    def rx_buffer_size(self):
        return self.try_get(function_name="rx_buffer_size").int64_value
    
    @rx_buffer_size.setter
    def rx_buffer_size(self, value):
        self.try_set(function_name="rx_buffer_size", value=grpc_pb2.Argument(int64_value=value))
    
    #endregion
    
    #region tx_def
    
    #endregion
 