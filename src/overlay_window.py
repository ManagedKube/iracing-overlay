"""
Overlay Window
Creates a transparent overlay window for displaying race data
"""
import tkinter as tk
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class OverlayWindow:
    """Transparent overlay window for displaying race information"""
    
    def __init__(self, width: int = 400, height: int = 300):
        self.width = width
        self.height = height
        self.root = None
        self.labels = {}
        self.is_visible = True
        
    def create_window(self):
        """Create the overlay window"""
        self.root = tk.Tk()
        self.root.title("iRacing Overlay")
        
        # Configure window to be transparent and always on top
        self.root.attributes('-topmost', True)
        self.root.attributes('-alpha', 0.8)  # Semi-transparent
        self.root.configure(bg='black')
        
        # Remove window decorations
        self.root.overrideredirect(True)
        
        # Set window size and position (top-right corner)
        screen_width = self.root.winfo_screenwidth()
        x_position = screen_width - self.width - 20
        y_position = 20
        self.root.geometry(f"{self.width}x{self.height}+{x_position}+{y_position}")
        
        # Create frame for content
        self.frame = tk.Frame(self.root, bg='black', padx=10, pady=10)
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        # Create title label
        title = tk.Label(
            self.frame,
            text="iRacing Overlay",
            font=('Arial', 14, 'bold'),
            bg='black',
            fg='#00ff00'
        )
        title.pack(pady=(0, 10))
        
        # Create data labels
        self._create_data_labels()
        
        # Bind events for dragging
        self.root.bind('<Button-1>', self._start_drag)
        self.root.bind('<B1-Motion>', self._drag)
        
        logger.info("Overlay window created")
        
    def _create_data_labels(self):
        """Create labels for displaying telemetry data"""
        data_fields = [
            ('speed', 'Speed'),
            ('gear', 'Gear'),
            ('rpm', 'RPM'),
            ('lap', 'Lap'),
            ('position', 'Position'),
            ('fuel', 'Fuel Level'),
        ]
        
        for field_id, field_name in data_fields:
            container = tk.Frame(self.frame, bg='black')
            container.pack(fill=tk.X, pady=2)
            
            label_name = tk.Label(
                container,
                text=f"{field_name}:",
                font=('Arial', 10),
                bg='black',
                fg='#cccccc',
                width=15,
                anchor='w'
            )
            label_name.pack(side=tk.LEFT)
            
            label_value = tk.Label(
                container,
                text="--",
                font=('Arial', 10, 'bold'),
                bg='black',
                fg='#00ff00',
                anchor='w'
            )
            label_value.pack(side=tk.LEFT)
            
            self.labels[field_id] = label_value
    
    def _start_drag(self, event):
        """Start dragging the window"""
        self._drag_start_x = event.x
        self._drag_start_y = event.y
    
    def _drag(self, event):
        """Drag the window"""
        x = self.root.winfo_x() + event.x - self._drag_start_x
        y = self.root.winfo_y() + event.y - self._drag_start_y
        self.root.geometry(f"+{x}+{y}")
    
    def update_data(self, telemetry: Optional[Dict[str, Any]]):
        """
        Update overlay with telemetry data
        Args:
            telemetry: Dictionary containing telemetry data
        """
        if not telemetry or not self.root:
            return
        
        try:
            # Update speed (convert to mph)
            if 'speed' in telemetry and telemetry['speed'] is not None:
                speed_mph = telemetry['speed'] * 2.23694  # m/s to mph
                self.labels['speed'].config(text=f"{speed_mph:.0f} mph")
            
            # Update gear
            if 'gear' in telemetry and telemetry['gear'] is not None:
                gear = telemetry['gear']
                gear_text = 'R' if gear == -1 else ('N' if gear == 0 else str(gear))
                self.labels['gear'].config(text=gear_text)
            
            # Update RPM
            if 'rpm' in telemetry and telemetry['rpm'] is not None:
                self.labels['rpm'].config(text=f"{telemetry['rpm']:.0f}")
            
            # Update lap
            if 'lap' in telemetry and telemetry['lap'] is not None:
                self.labels['lap'].config(text=str(telemetry['lap']))
            
            # Update position
            if 'position' in telemetry and telemetry['position'] is not None:
                self.labels['position'].config(text=str(telemetry['position']))
            
            # Update fuel
            if 'fuel_level' in telemetry and telemetry['fuel_level'] is not None:
                self.labels['fuel'].config(text=f"{telemetry['fuel_level']:.1f}L")
        
        except Exception as e:
            logger.error(f"Error updating overlay: {e}")
    
    def toggle_visibility(self):
        """Toggle overlay visibility"""
        if self.is_visible:
            self.root.withdraw()
            self.is_visible = False
        else:
            self.root.deiconify()
            self.is_visible = True
    
    def destroy(self):
        """Destroy the overlay window"""
        if self.root:
            self.root.destroy()
            logger.info("Overlay window destroyed")
