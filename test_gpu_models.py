#!/usr/bin/env python3
"""
Test script to verify GPU model switching works without Qt object lifecycle errors.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer

from gpuviz.view3d import GPU3DView
from gpuviz.gpu_models import get_gpu_model

def test_gpu_model_switching():
    """Test switching between different GPU models."""
    print("Testing GPU model switching...")

    # Create QApplication
    app = QApplication(sys.argv)

    # Create a View3D widget
    view3d = GPU3DView()

    # Test switching between different GPU models
    gpu_models = ['RTX 4080', 'RTX 4070', 'RTX 4060', 'RTX 4090', 'RX 7900 XTX', 'RX 7900 XT', 'RX 7900 GRE', 'RX 7800 XT', 'RX 7700 XT', 'RTX 4070 Ti', 'RTX 4060 Ti', 'Ultra Detailed GPU']

    for model_name in gpu_models:
        try:
            print(f"Testing {model_name}...")
            gpu_model = get_gpu_model(model_name, view3d)
            print(f"✓ Successfully created {model_name} model")

            # Skip drawing test since we don't have OpenGL context
            # gpu_model.draw_complete_model(1)
            # print(f"✓ Successfully drew {model_name} model")

            # Clean up
            del gpu_model
            print(f"✓ Successfully cleaned up {model_name} model")

        except Exception as e:
            print(f"✗ Error with {model_name}: {e}")
            return False

    print("All GPU models tested successfully!")
    return True

if __name__ == "__main__":
    success = test_gpu_model_switching()
    sys.exit(0 if success else 1)