"""
Main Application
Coordinates the iRacing telemetry client and overlay window
"""
import logging
import threading
import time
from typing import Optional
import tkinter as tk

from telemetry_client import IRacingClient
from overlay_window import OverlayWindow

logger = logging.getLogger(__name__)


class IRacingOverlayApp:
    """Main application class for iRacing Overlay"""
    
    def __init__(self):
        self.client = IRacingClient()
        self.overlay = OverlayWindow()
        self.running = False
        self.telemetry_thread = None
        self.update_interval = 0.1  # Update every 100ms
        
    def start(self):
        """Start the application"""
        logger.info("Starting iRacing Overlay Application")
        self.running = True
        
        # Create overlay window
        self.overlay.create_window()
        
        # Start telemetry update thread
        self.telemetry_thread = threading.Thread(target=self._telemetry_loop, daemon=True)
        self.telemetry_thread.start()
        
        # Start GUI main loop
        try:
            self.overlay.root.mainloop()
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self):
        """Stop the application"""
        logger.info("Stopping iRacing Overlay Application")
        self.running = False
        
        if self.client.is_connected:
            self.client.disconnect()
        
        if self.overlay.root:
            self.overlay.destroy()
    
    def _telemetry_loop(self):
        """Background thread for updating telemetry data"""
        logger.info("Telemetry update loop started")
        
        while self.running:
            try:
                # Try to connect if not connected
                if not self.client.is_running():
                    if not self.client.is_connected:
                        self.client.connect()
                    time.sleep(1)  # Wait before retry
                    continue
                
                # Get telemetry data
                telemetry = self.client.get_telemetry()
                
                # Update overlay (must be done on main thread)
                if telemetry and self.overlay.root:
                    self.overlay.root.after(0, self.overlay.update_data, telemetry)
                
                time.sleep(self.update_interval)
                
            except Exception as e:
                logger.error(f"Error in telemetry loop: {e}")
                time.sleep(1)
        
        logger.info("Telemetry update loop stopped")


def setup_logging():
    """Configure application logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('iracing_overlay.log'),
            logging.StreamHandler()
        ]
    )


def main():
    """Main entry point"""
    setup_logging()
    
    logger.info("=" * 50)
    logger.info("iRacing Overlay Application v0.1.0")
    logger.info("=" * 50)
    
    app = IRacingOverlayApp()
    
    try:
        app.start()
    except Exception as e:
        logger.error(f"Application error: {e}", exc_info=True)
    finally:
        app.stop()


if __name__ == "__main__":
    main()
