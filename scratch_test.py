import os
from PIL import Image
import numpy as np
import sys
sys.path.append(os.path.dirname(__file__))
from src.image.ela_processor import compute_ela

def test_variance():
    real_dir = "data/images/real"
    fake_dir = "data/images/fake"
    
    real_files = [os.path.join(real_dir, f) for f in os.listdir(real_dir) if f.endswith('.jpg')][:10]
    fake_files = [os.path.join(fake_dir, f) for f in os.listdir(fake_dir) if f.endswith('.jpg')][:10]
    
    print("REAL:")
    for f in real_files:
        ela = compute_ela(f)
        if ela:
            arr = np.array(ela.convert('L'))
            print(f"{os.path.basename(f)} - StdDev: {np.std(arr):.2f}, Mean: {np.mean(arr):.2f}, Max: {np.max(arr)}")
            
    print("\nFAKE:")
    for f in fake_files:
        ela = compute_ela(f)
        if ela:
            arr = np.array(ela.convert('L'))
            print(f"{os.path.basename(f)} - StdDev: {np.std(arr):.2f}, Mean: {np.mean(arr):.2f}, Max: {np.max(arr)}")

if __name__ == "__main__":
    test_variance()
