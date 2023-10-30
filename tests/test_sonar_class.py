import unittest
from sonarlight import Sonar
import pandas as pd
import numpy as np

class TestMyModule(unittest.TestCase):
    def setUp(self):
        self.sl2 = Sonar("example_files/example_sl2_file.sl2")
        self.sl3 = Sonar("example_files/example_sl3_file.sl3")
        self.sl2_augment = Sonar("example_files/example_sl2_file.sl2", augment_coords=True)
        self.sl3_augment = Sonar("example_files/example_sl3_file.sl3", augment_coords=True)

    def test_class(self):
        self.assertIsInstance(self.sl2, Sonar)
        self.assertIsInstance(self.sl3, Sonar)

    def test_class_with_augment(self):
        self.assertIsInstance(self.sl2_augment, Sonar)
        self.assertIsInstance(self.sl3_augment, Sonar)

    def test_shape_with_augment(self):
        #Does augmented dataframe shape with four new columns match non-augmented frame?
        sl2_shape = list(self.sl2.df.shape)
        sl2_aug_shape = list(self.sl2_augment.df.shape)
        sl2_shape[1] += 4

        sl3_shape = list(self.sl3.df.shape)
        sl3_aug_shape = list(self.sl3_augment.df.shape)
        sl3_shape[1] += 4

        self.assertEqual(sl2_shape, sl2_aug_shape)
        self.assertEqual(sl3_shape, sl3_aug_shape)

    def test_sl2_version(self):
        self.assertEqual(self.sl2.version, 2)

    def test_sl3_version(self):
        self.assertEqual(self.sl3.version, 3)

    def test_sl2_frame_version(self):
        self.assertEqual(self.sl2.frame_version, 8)

    def test_sl3_frame_version(self):
        self.assertEqual(self.sl3.frame_version, 10)
    
    def test_sl2_pandas(self):
        self.assertIsInstance(self.sl2.df, pd.DataFrame)

    def test_sl3_pandas(self):
        self.assertIsInstance(self.sl3.df, pd.DataFrame)

    def test_sl2_image(self):

        with self.assertRaises(ValueError):
            self.sl2.image("typo")

        image_primary = self.sl2.image("primary")
        self.assertIsInstance(image_primary, np.ndarray)
        self.assertEqual(image_primary.shape, (1288, 3072))

        image_secondary = self.sl2.image("secondary")
        self.assertIsInstance(image_secondary, np.ndarray)
        self.assertEqual(image_secondary.shape, (1288, 3072))

        image_downscan = self.sl2.image("downscan")
        self.assertIsInstance(image_downscan, np.ndarray)
        self.assertEqual(image_downscan.shape, (1288, 1400))

        image_sidescan = self.sl2.image("sidescan")
        self.assertIsInstance(image_sidescan, np.ndarray)
        self.assertEqual(image_sidescan.shape, (1287, 2800))

    def test_sl3_image(self):

        with self.assertRaises(ValueError):
            self.sl3.image("typo")

        image_primary = self.sl3.image("primary")
        self.assertIsInstance(image_primary, np.ndarray)
        self.assertEqual(image_primary.shape, (1281, 3072))

        image_secondary = self.sl3.image("secondary")
        self.assertIsInstance(image_secondary, np.ndarray)
        self.assertEqual(image_secondary.shape, (1281, 3072))

        image_downscan = self.sl3.image("downscan")
        self.assertIsInstance(image_downscan, np.ndarray)
        self.assertEqual(image_downscan.shape, (1282, 1400))

        image_sidescan = self.sl3.image("sidescan")
        self.assertIsInstance(image_sidescan, np.ndarray)
        self.assertEqual(image_sidescan.shape, (1281, 2800))

    def test_sl2_xyz(self):
        self.assertIsInstance(self.sl2.sidescan_xyz(), pd.DataFrame)

    def test_sl3_xyz(self):
        self.assertIsInstance(self.sl3.sidescan_xyz(), pd.DataFrame)

    def test_sl2_water(self):

        pixels=300

        with self.assertRaises(ValueError):
            self.sl2.water("sidescan", pixels)

        with self.assertRaises(ValueError):
            self.sl2.water("typo", pixels)

        water_primary = self.sl2.water("primary", pixels)
        self.assertIsInstance(water_primary, np.ndarray)
        self.assertEqual(water_primary.shape[1], pixels)

        water_secondary = self.sl2.water("secondary", pixels)
        self.assertIsInstance(water_secondary, np.ndarray)
        self.assertEqual(water_secondary.shape[1], pixels)

        water_downscan = self.sl2.water("downscan", pixels)
        self.assertIsInstance(water_downscan, np.ndarray)
        self.assertEqual(water_downscan.shape[1], pixels)

    def test_sl3_water(self):

        pixels=300

        with self.assertRaises(ValueError):
            self.sl3.water("sidescan", pixels)

        with self.assertRaises(ValueError):
            self.sl3.water("typo", pixels)

        water_primary = self.sl3.water("primary", pixels)
        self.assertIsInstance(water_primary, np.ndarray)
        self.assertEqual(water_primary.shape[1], pixels)

        water_secondary = self.sl3.water("secondary", pixels)
        self.assertIsInstance(water_secondary, np.ndarray)
        self.assertEqual(water_secondary.shape[1], pixels)

        water_downscan = self.sl3.water("downscan", pixels)
        self.assertIsInstance(water_downscan, np.ndarray)
        self.assertEqual(water_downscan.shape[1], pixels)

    def test_sl2_bottom(self):

        with self.assertRaises(ValueError):
            self.sl2.bottom("sidescan")

        with self.assertRaises(ValueError):
            self.sl2.bottom("typo")

        bottom_primary = self.sl2.bottom("primary")
        self.assertIsInstance(bottom_primary, np.ndarray)

        bottom_secondary = self.sl2.bottom("secondary")
        self.assertIsInstance(bottom_secondary, np.ndarray)

        bottom_downscan = self.sl2.bottom("downscan")
        self.assertIsInstance(bottom_downscan, np.ndarray)

    def test_sl3_bottom(self):

        with self.assertRaises(ValueError):
            self.sl3.bottom("sidescan")

        with self.assertRaises(ValueError):
            self.sl3.bottom("typo")

        bottom_primary = self.sl3.bottom("primary")
        self.assertIsInstance(bottom_primary, np.ndarray)

        bottom_secondary = self.sl3.bottom("secondary")
        self.assertIsInstance(bottom_secondary, np.ndarray)

        bottom_downscan = self.sl3.bottom("downscan")
        self.assertIsInstance(bottom_downscan, np.ndarray)
