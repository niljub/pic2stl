import unittest
import os
import numpy as np
from PIL import Image
from pic2stl import image_to_stl
import trimesh

class TestPic2Stl(unittest.TestCase):
    def setUp(self):
        self.test_img = "test_img.png"
        self.test_stl = "test_out.stl"
        # Create a simple 2x2 image
        img = Image.new('L', (2, 2), color=0)
        img.putpixel((0,0), 255)
        img.save(self.test_img)

    def tearDown(self):
        if os.path.exists(self.test_img):
            os.remove(self.test_img)
        if os.path.exists(self.test_stl):
            os.remove(self.test_stl)

    def test_basic_conversion(self):
        image_to_stl(self.test_img, self.test_stl, 5)
        self.assertTrue(os.path.exists(self.test_stl))
        mesh = trimesh.load(self.test_stl)
        # 1 pixel = 1 box = 12 faces
        self.assertEqual(len(mesh.faces), 12)
        # Bounds: [0,0,0] to [1,1,5] (approx)
        self.assertAlmostEqual(mesh.bounds[1][2], 5)

    def test_with_base(self):
        image_to_stl(self.test_img, self.test_stl, 5, add_base=True, base_thickness=2)
        mesh = trimesh.load(self.test_stl)
        # Base (12 faces) + Pixel (12 faces) = 24 faces
        self.assertEqual(len(mesh.faces), 24)
        # Total height 2 + 5 = 7
        self.assertAlmostEqual(mesh.bounds[1][2], 7)

if __name__ == '__main__':
    unittest.main()
