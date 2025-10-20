import unittest
import sys
import os

# Add parent directory to path to import pow module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pow import mine, difficulty


class TestProofOfWork(unittest.TestCase):
    """Minimal test cases for the Proof of Work mining functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_prev_hash = "0000000000000000000000000000000000000000000000000000000000000000"
        self.test_data = "Test transaction data"
    
    def test_basic_mining(self):
        """Test that mining produces a valid hash."""
        block_hash, nonce, mining_time, block = mine(self.test_prev_hash, self.test_data)
        print(block)

        # Verify hash starts with required number of zeros
        self.assertTrue(block_hash.startswith("0" * difficulty))
        
        # Verify return types
        self.assertIsInstance(nonce, int)
        self.assertIsInstance(mining_time, float)
        self.assertEqual(len(block_hash), 64)
    
    def test_different_data_produces_different_hash(self):
        """Test that different data produces different hashes."""
        hash1, _, _, _ = mine(self.test_prev_hash, "Data 1")
        hash2, _, _, _ = mine(self.test_prev_hash, "Data 2")
        
        self.assertNotEqual(hash1, hash2)
    
    def test_empty_inputs_raise_error(self):
        """Test that empty inputs raise ValueError."""
        with self.assertRaises(ValueError):
            mine("", self.test_data)
        
        with self.assertRaises(ValueError):
            mine(self.test_prev_hash, "")
    
    def test_hash_format(self):
        """Test that hash is valid hex format."""
        block_hash, _, _, _ = mine(self.test_prev_hash, self.test_data)
        
        # Should be 64 character hex string
        self.assertTrue(all(c in '0123456789abcdef' for c in block_hash))


if __name__ == '__main__':
    unittest.main(verbosity=2)
