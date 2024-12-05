from ...core.grpc_client import rpc_client
from ...common.utils import *
from ...common.grpc import grpc_pb2
from ...core.grpc_client import get_tcp_calls
from .pluto_wrapper import WrapperMeta

# class rx_def:
#     pass

# class tx_def:
#     pass

# class rx_tx_def(rx_def, tx_def):
#     pass

# class ad9364(rx_tx_def):
#     pass

class Pluto(metaclass=WrapperMeta): # client
    
    def __init__(self, token='', debug=False):
        self.token = token
        # self.try_set(function_name="ip", value=grpc_pb2.Argument(string_value=ip))
        
        if debug:
            print("Pluto Remote Client Initialized.")
        
    def api_token(self, token:str) -> None:
        self.token = token
        
    def try_get(self, *, function_name):
        try:
            return unmap_arg(rpc_client(function_name=f"Pluto:{function_name}:GET", args={'a':map_arg(self.token)}).results[function_name])
        except Exception as e:
            input(f"Error: {e}\nHit enter to continue...")
            return None

    def try_set(self, *, function_name, value):
        try:
            rpc_client(function_name=f"Pluto:{function_name}:SET", args={function_name: map_arg(value), 'a':map_arg(self.token)})
        except Exception as e:
            input(f"Error: {e}\nHit enter to continue...")
            
    # def test_print(self):
    #     if self.debug == True and get_tcp_calls() % 50 == 0:
    #         print(f'TCP Call Number: {get_tcp_calls()}')

    #region ad9364

    @property
    def filter(self):
        pass
        # return self.try_get(function_name="filter")
    
    @filter.setter
    def filter(self, value):
        pass
        # self.try_set(function_name="filter", value=grpc_pb2.Argument(int64_value=value))
        
    @property
    def loopback(self):
        pass
        # return self.try_get(function_name="loopback")
    
    @loopback.setter
    def loopback(self, value):
        pass
        # self.try_set(function_name="loopback",  value=grpc_pb2.Argument(int64_value=value))
        
    @property
    def gain_control_mode_chan0(self):
        pass
        # return self.try_get(function_name="gain_control_mode_chan0")
    
    @gain_control_mode_chan0.setter
    def gain_control_mode_chan0(self, value):
        pass
        # self.try_set(function_name="gain_control_mode_chan0",  value=grpc_pb2.Argument(int64_value=value))
        
    @property
    def rx_hardwaregain_chan0(self):
        pass
        # return self.try_get(function_name="rx_hardwaregain_chan0")
    
    @rx_hardwaregain_chan0.setter
    def rx_hardwaregain_chan0(self, value):
        pass
        # self.try_set(function_name="rx_hardwaregain_chan0",  value=grpc_pb2.Argument(int64_value=value))
        
    @property
    def tx_hardwaregain_chan0(self):
        pass
        # return self.try_get(function_name="tx_hardwaregain_chan0")
    
    @tx_hardwaregain_chan0.setter
    def tx_hardwaregain_chan0(self, value):
        pass
        # self.try_set(function_name="tx_hardwaregain_chan0", value=grpc_pb2.Argument(int64_value=value))
        
    @property
    def rx_rf_bandwidth(self):
        pass
        # return unmap_arg(self.try_get(function_name="rx_rf_bandwidth"))
    
    @rx_rf_bandwidth.setter
    def rx_rf_bandwidth(self, value):
        pass
        # print("Setting RX RF Bandwidth")
        # self.try_set(function_name="rx_rf_bandwidth",  value=grpc_pb2.Argument(int64_value=value))
        
    @property
    def tx_rf_bandwidth(self):
        pass
        # return self.try_get(function_name="tx_rf_bandwidth")
    
    @tx_rf_bandwidth.setter
    def tx_rf_bandwidth(self, value):
        pass
        # self.try_set(function_name="tx_rf_bandwidth",  value=grpc_pb2.Argument(int64_value=value))
        
    @property
    def sample_rate(self):
        pass
        # return self.try_get(function_name="sample_rate")
    
    @sample_rate.setter
    def sample_rate(self, value):
        pass
        # self.try_set(function_name="sample_rate",  value=grpc_pb2.Argument(int64_value=value))
        
    @property
    def rx_lo(self):
        pass
        # return self.try_get(function_name="rx_lo").int64_value
    
    @rx_lo.setter
    def rx_lo(self, value):
        pass
        # self.try_set(function_name="rx_lo", value=grpc_pb2.Argument(int64_value=value))
        
    @property
    def tx_lo(self):
        pass
        # return self.try_get(function_name="tx_lo").int64_value
    
    @tx_lo.setter
    def tx_lo(self, value):
        pass
        # self.try_set(function_name="tx_lo", value=grpc_pb2.Argument(int64_value=value))
        
    #endregion
    
    #region rx_def
    
    @property
    def rx(self):
        pass
        # return unmap_arg(self.try_get(function_name="rx"))
    
    @property
    def rx_buffer_size(self):
        pass
        # return self.try_get(function_name="rx_buffer_size").int64_value
    
    @rx_buffer_size.setter
    def rx_buffer_size(self, value):
        pass
        # self.try_set(function_name="rx_buffer_size", value=grpc_pb2.Argument(int64_value=value))
    
    #endregion
    
    #region tx_def
    
    #endregion
 