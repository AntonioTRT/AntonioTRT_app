"""
TRT Core Module - Motor de comunicación y abstracción para hardware
"""

from .trtmsg import TRTMessageHandler, get_trt_handler

__all__ = ['TRTMessageHandler', 'get_trt_handler']
