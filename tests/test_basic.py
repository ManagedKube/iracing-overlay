"""
Simple tests for iRacing Overlay Application
Tests basic module imports and class instantiation
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


def test_imports():
    """Test that all modules can be imported"""
    try:
        import telemetry_client
        import overlay_window
        import main
        print("✓ All modules imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False


def test_telemetry_client_creation():
    """Test IRacingClient can be instantiated"""
    try:
        from telemetry_client import IRacingClient
        client = IRacingClient()
        assert client is not None
        assert hasattr(client, 'connect')
        assert hasattr(client, 'get_telemetry')
        assert hasattr(client, 'is_running')
        print("✓ IRacingClient instantiated successfully")
        return True
    except Exception as e:
        print(f"✗ Error creating IRacingClient: {e}")
        return False


def test_overlay_window_creation():
    """Test OverlayWindow can be instantiated"""
    try:
        from overlay_window import OverlayWindow
        overlay = OverlayWindow()
        assert overlay is not None
        assert hasattr(overlay, 'create_window')
        assert hasattr(overlay, 'update_data')
        print("✓ OverlayWindow instantiated successfully")
        return True
    except Exception as e:
        print(f"✗ Error creating OverlayWindow: {e}")
        return False


def test_app_creation():
    """Test IRacingOverlayApp can be instantiated"""
    try:
        from main import IRacingOverlayApp
        app = IRacingOverlayApp()
        assert app is not None
        assert hasattr(app, 'start')
        assert hasattr(app, 'stop')
        print("✓ IRacingOverlayApp instantiated successfully")
        return True
    except Exception as e:
        print(f"✗ Error creating IRacingOverlayApp: {e}")
        return False


def run_tests():
    """Run all tests"""
    print("=" * 50)
    print("Running iRacing Overlay Tests")
    print("=" * 50)
    print()
    
    tests = [
        ("Module Imports", test_imports),
        ("Telemetry Client", test_telemetry_client_creation),
        ("Overlay Window", test_overlay_window_creation),
        ("Main Application", test_app_creation),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"Testing {test_name}...")
        result = test_func()
        results.append(result)
        print()
    
    print("=" * 50)
    passed = sum(results)
    total = len(results)
    print(f"Tests Passed: {passed}/{total}")
    
    if passed == total:
        print("✓ All tests passed!")
        return 0
    else:
        print("✗ Some tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(run_tests())
