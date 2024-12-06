# fiscus_config.py

import sys
import os

# Add the 'src' directory to the Python path for access to the SDK
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from fiscus import FiscusClient, FiscusUser, FiscusLogLevel

# Initialize Fiscus client
client = FiscusClient(
    api_key='fiscus_production_394a5d73_f3cbabd01364dde698bea9bb8125d1f7cab7606c429d644ebc7869651a094e92',
    user_id="12345",
    logging_level=FiscusLogLevel.DEBUG
)

# Initialize Fiscus user for stateful environment
user = FiscusUser(
    user_id="12345",
    client=client
)
