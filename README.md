# iRacing Overlay

A Windows application that creates real-time overlays for iRacing simulator data. This application runs in the background and displays live telemetry data from iRacing on a transparent overlay window during races.

## Features

- **Real-time Telemetry Display**: Shows live data from iRacing including:
  - Speed (MPH)
  - Current Gear
  - RPM
  - Current Lap
  - Race Position
  - Fuel Level
  
- **Transparent Overlay**: Semi-transparent window that overlays on top of iRacing
- **Draggable Window**: Click and drag the overlay to position it anywhere on screen
- **Auto-Connect**: Automatically connects to iRacing when it's running
- **Background Operation**: Runs quietly in the background while racing

## Requirements

- Windows OS (iRacing is Windows-only)
- Python 3.8 or higher
- iRacing simulator installed and running

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/ManagedKube/iracing-overlay.git
   cd iracing-overlay
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Start iRacing and load into a session (practice, qualifying, or race)

2. Run the overlay application:
   ```bash
   cd src
   python main.py
   ```

3. The overlay window will appear in the top-right corner of your screen

4. You can drag the overlay to any position by clicking and dragging it

5. The overlay will automatically update with live telemetry data from iRacing

## Configuration

You can customize the overlay by editing `config.ini`:

- **Display Settings**: Window size, transparency, update frequency
- **Telemetry Settings**: Connection timeout, auto-reconnect
- **Appearance**: Colors, fonts, and styling

To create a custom configuration:
```bash
cp config.ini config.local.ini
# Edit config.local.ini with your preferences
```

## How It Works

The application consists of three main components:

1. **Telemetry Client** (`telemetry_client.py`): Connects to iRacing's SDK via shared memory to retrieve real-time telemetry data

2. **Overlay Window** (`overlay_window.py`): Creates a transparent, always-on-top window using tkinter to display the data

3. **Main Application** (`main.py`): Coordinates the telemetry client and overlay window, running the telemetry updates in a background thread

### iRacing Data Connection

iRacing exposes telemetry data through a memory-mapped file when running. The `pyirsdk` library provides easy access to this data. The application:
- Automatically detects when iRacing is running
- Connects to the telemetry stream
- Updates the overlay 10 times per second (configurable)
- Automatically reconnects if the connection is lost

## Troubleshooting

**Overlay not appearing:**
- Make sure iRacing is running and you're in a session (not in the UI)
- Check that Python and dependencies are correctly installed
- Look for error messages in `iracing_overlay.log`

**No data showing:**
- Verify iRacing is actively running a session
- The overlay shows "--" for unavailable data
- Check the log file for connection errors

**Performance issues:**
- Increase the `update_interval` in config.ini (e.g., 0.2 for 5 updates/sec)
- Reduce window transparency if GPU performance is affected

## Development

### Project Structure
```
iracing-overlay/
├── src/
│   ├── __init__.py
│   ├── main.py              # Application entry point
│   ├── telemetry_client.py  # iRacing SDK connection
│   └── overlay_window.py    # Overlay UI
├── config.ini               # Default configuration
├── requirements.txt         # Python dependencies
└── README.md
```

### Adding New Telemetry Fields

To add new data fields to the overlay:

1. Update `telemetry_client.py` to fetch the new data in the `get_telemetry()` method
2. Add the field to `overlay_window.py` in `_create_data_labels()`
3. Add update logic in `update_data()`

See the [iRacing SDK documentation](https://github.com/kutu/pyirsdk) for available telemetry variables.

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- [pyirsdk](https://github.com/kutu/pyirsdk) - Python iRacing SDK implementation
- iRacing for providing the telemetry API
