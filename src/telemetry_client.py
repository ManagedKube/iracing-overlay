"""
iRacing Telemetry Client
Connects to iRacing SDK to retrieve real-time telemetry data
"""
import irsdk
import time
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class IRacingClient:
    """Client for connecting to iRacing telemetry"""
    
    def __init__(self):
        self.ir = irsdk.IRSDK()
        self.is_connected = False
        
    def connect(self) -> bool:
        """
        Attempt to connect to iRacing
        Returns True if connected, False otherwise
        """
        try:
            if self.ir.startup():
                self.is_connected = True
                logger.info("Connected to iRacing")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to connect to iRacing: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from iRacing"""
        if self.is_connected:
            self.ir.shutdown()
            self.is_connected = False
            logger.info("Disconnected from iRacing")
    
    def is_running(self) -> bool:
        """Check if iRacing is currently running"""
        return self.ir.is_initialized and self.ir.is_connected
    
    def get_telemetry(self) -> Optional[Dict[str, Any]]:
        """
        Get current telemetry data
        Returns dictionary with telemetry data or None if not available
        """
        if not self.is_running():
            return None
        
        try:
            # Freeze data to prevent changes during read
            self.ir.freeze_var_buffer_latest()
            
            # Get essential telemetry data
            data = {
                'speed': self.ir['Speed'],
                'gear': self.ir['Gear'],
                'rpm': self.ir['RPM'],
                'lap': self.ir['Lap'],
                'lap_distance': self.ir['LapDistPct'],
                'session_time': self.ir['SessionTime'],
                'fuel_level': self.ir['FuelLevel'],
                'fuel_use_per_hour': self.ir['FuelUsePerHour'],
                'position': self.ir['PlayerCarPosition'],
                'car_class_position': self.ir['PlayerCarClassPosition'],
            }
            
            return data
        except Exception as e:
            logger.error(f"Error reading telemetry: {e}")
            return None
    
    def wait_for_connection(self, timeout: int = 30) -> bool:
        """
        Wait for iRacing to be available
        Args:
            timeout: Maximum time to wait in seconds
        Returns:
            True if connected within timeout, False otherwise
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self.connect():
                return True
            time.sleep(1)
        return False
