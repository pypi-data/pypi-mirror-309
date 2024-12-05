import dif as difPy
import unittest
import os
import sys

class difTester(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up the directory paths
        cls.directory = "C:/Users/elise/Pictures/difPy Testing/"
        cls.dir1 = os.path.join(cls.directory, "test1")
        cls.dir2 = os.path.join(cls.directory, "test2")
        
        # Verify the directories exist
        for dir_path in [cls.directory, cls.dir1, cls.dir2]:
            if not os.path.exists(dir_path):
                raise ValueError(f"Directory {dir_path} does not exist")

    def test_build_and_search(self):
        """Test building and searching functionality"""
        # Test without in_folder
        dif = difPy.build(self.directory, show_progress=False)
        self.assertEqual(dif.stats["total_files"], 52)
        self.assertEqual(dif.stats["invalid_files"]["count"], 8)
        self._run_search_tests(dif)

        # Test with in_folder=True
        dif = difPy.build(self.directory, in_folder=True)
        self.assertEqual(dif.stats["total_files"], 52)
        self.assertEqual(dif.stats["invalid_files"]["count"], 8)
        self._run_search_tests(dif)

    def test_non_recursive_build(self):
        """Test building with non-recursive folder scanning"""
        # Build with in_folder=True and recursive=False
        dif = difPy.build(self.dir1, self.dir2, in_folder=True, recursive=False, show_progress=False)
        
        # Verify build stats
        self.assertEqual(dif.stats["total_files"], 46, "Total files count mismatch")
        self.assertEqual(dif.stats["invalid_files"]["count"], 6, "Invalid files count mismatch")
        
        # Search and verify search stats
        search = difPy.search(dif, show_progress=False)
        self.assertEqual(search.stats["process"]["search"]["matches_found"]["duplicates"], 
                        2, "Duplicates count mismatch")
        self.assertEqual(len(search.lower_quality), 2, "Lower quality matches count mismatch")

    def test_directory_comparison(self):
        """Test directory comparison functionality with different methods"""
        # Test with list of directories
        dif = difPy.build([self.dir1, self.dir2], show_progress=False)
        self._verify_results(dif, expected_duplicates=24)

        # Test with multiple directory arguments
        dif = difPy.build(self.dir1, self.dir2, show_progress=False)
        self._verify_results(dif, expected_duplicates=24)

        # Test with in_folder=True
        dif = difPy.build(self.dir1, self.dir2, in_folder=True)
        self._verify_results(dif, expected_duplicates=4)

    def _verify_results(self, dif, expected_duplicates):
        """Helper method to verify directory comparison results"""
        # Verify build stats
        self.assertEqual(dif.stats["total_files"], 52, "Total files count mismatch")
        self.assertEqual(dif.stats["invalid_files"]["count"], 8, "Invalid files count mismatch")
        
        # Search and verify search stats
        search = difPy.search(dif, show_progress=False)
        self.assertEqual(search.stats["process"]["search"]["files_searched"], 44, 
                        "Files searched count mismatch")
        self.assertEqual(search.stats["process"]["search"]["matches_found"]["duplicates"],
                        expected_duplicates, "Duplicates count mismatch")
        self.assertEqual(len(search.lower_quality), expected_duplicates, 
                        "Lower quality matches count mismatch")

    def _run_search_tests(self, dif):
        """Helper method to run search tests"""
        ## Duplicates ##
        test_cases = [
            ("1", {}),
            ("2", {"rotate": False, "show_progress": False}),
            ("3", {"lazy": False, "show_progress": False}),
            ("4", {"processes": 5, "show_progress": False}),
            ("5", {"chunksize": 50, "show_progress": False}),
        ]
        
        # Run duplicate test cases
        for label, kwargs in test_cases:
            print(label)
            search = difPy.search(dif, **kwargs)
            self.assertEqual(search.stats["process"]["search"]["files_searched"], 44)
            self.assertEqual(search.stats["process"]["search"]["matches_found"]["duplicates"], 24)
            self.assertEqual(len(search.lower_quality), 24, 
                           f"Lower quality matches count mismatch for case {label}")

        ## Similar ##
        similar_test_cases = [
            ("A", {"similarity": "similar"}),
            ("B", {"similarity": "similar", "rotate": False, "show_progress": False}),
            ("C", {"similarity": "similar", "lazy": False, "show_progress": False}),
            ("D", {"similarity": "similar", "processes": 5, "show_progress": False}),
            ("E", {"similarity": "similar", "chunksize": 50, "show_progress": False}),
        ]
        
        # Run similar test cases
        for label, kwargs in similar_test_cases:
            print(label)
            search = difPy.search(dif, **kwargs)
            self.assertEqual(search.stats["process"]["search"]["files_searched"], 44)
            self.assertEqual(search.stats["process"]["search"]["matches_found"]["duplicates"], 20)
            self.assertEqual(search.stats["process"]["search"]["matches_found"]["similar"], 8)
            self.assertEqual(len(search.lower_quality), 28,  # 20 duplicates + 8 similar
                           f"Lower quality matches count mismatch for similar case {label}")

def run_tests():
    """Run the tests in a way that works in both regular Python and IPython"""
    try:
        # Create a test suite
        suite = unittest.TestLoader().loadTestsFromTestCase(difTester)
        
        # Run the tests
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        
        # Return appropriate exit code
        return 0 if result.wasSuccessful() else 1
    except Exception as e:
        print(f"An error occurred: {e}")
        return 1

if __name__ == '__main__':
    # Check if we're running in IPython
    if 'IPython' in sys.modules:
        # If in IPython, just run the tests without system exit
        run_tests()
    else:
        # If running as a regular Python script, exit with appropriate code
        sys.exit(run_tests())