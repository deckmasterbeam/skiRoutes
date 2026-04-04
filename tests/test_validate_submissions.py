"""Tests for validateUserSubmissionAgainstRoute module."""

import os
import sys
import unittest

# Add src directory to path
src_dir = os.path.join(os.path.dirname(__file__), '..', 'src')
sys.path.insert(0, src_dir)

from validateUserSubmissionAgainstRoute import (
    filename_to_tree,
    get_trackpoints_from_tree,
    get_waypoints_from_tree,
    get_hit_waypoints,
    haversine_distance,
    WAYPOINT_TOLERANCE_M,
)

class TestGPXParsing(unittest.TestCase):
    """Test GPX file parsing and waypoint/trackpoint extraction."""

    # ========== Setup ==========

    def setUp(self):
        """Set up test fixtures."""
        self.project_root = os.path.dirname(os.path.dirname(__file__))

    # ========== Helper Methods ==========

    def _verify_gpx_files_exists(self, target_route_filename, submission_filename):
        """Test that target route file and submission file exist."""
        self.assertTrue(os.path.exists(target_route_filename))
        self.assertTrue(os.path.exists(submission_filename))

    def _verify_waypoints_extracted_from_route(self, waypoints):
        """Test that waypoints are extracted from route."""
        self.assertGreater(len(waypoints), 0)
        # Check waypoint structure
        for wpt in waypoints:
            self.assertIn('lat', wpt)
            self.assertIn('lon', wpt)
            self.assertIn('name', wpt)

    def _verify_trackpoints_extracted_from_submission(self, trackpoints):
        """Test that trackpoints are extracted from submission file."""
        self.assertGreater(len(trackpoints), 0, f"No trackpoints in submission file")
        # Check trackpoint structure
        for trkpt in trackpoints[:1]:  # Check first trackpoint
            self.assertIn('lat', trkpt)
            self.assertIn('lon', trkpt)
            self.assertIn('time', trkpt)

    # ========== Test Methods ==========

    def test_haversine_distance(self):
        """Test haversine distance calculation."""
        # Same point should be 0 distance
        distance = haversine_distance(0, 0, 0, 0)
        self.assertAlmostEqual(distance, 0, places=1)
        
        # Test a known distance (roughly 111km per degree at equator)
        distance = haversine_distance(0, 0, 1, 0)
        self.assertGreater(distance, 100000)  # > 100km
        self.assertLess(distance, 120000)  # < 120km

    def test_josh_one_route_hits_waypoints(self):
        """Test that Josh's one run route hits expected waypoints."""
        target_route = os.path.join(
            self.project_root, 'routes', 'testRoute.gpx'
        )
        submission_file = os.path.join(
            self.project_root, 'testUserSubmissions', '2-6-26-ZermattMatterhorn-JoshOneRun.gpx'
        )
        self._verify_gpx_files_exists(target_route, submission_file)

        target_route_tree = filename_to_tree(target_route)
        submission_tree = filename_to_tree(submission_file)

        waypoints = get_waypoints_from_tree(target_route_tree)
        trackpoints = get_trackpoints_from_tree(submission_tree)

        self._verify_waypoints_extracted_from_route(waypoints)
        self._verify_trackpoints_extracted_from_submission(trackpoints)

        hit_waypoints = get_hit_waypoints(waypoints, trackpoints, WAYPOINT_TOLERANCE_M)
        self.assertEqual(len(hit_waypoints), 3, f"Expected 3 waypoints hit, got {len(hit_waypoints)}")

    def test_josh_all_day_route_hits_waypoints(self):
        """Test that Josh's all day route hits expected waypoints."""
        target_route = os.path.join(
            self.project_root, 'routes', 'testRoute.gpx'
        )
        submission_file = os.path.join(
            self.project_root, 'testUserSubmissions', '2-6-26-ZermattMatterhorn-JoshAllDay.gpx'
        )
        self._verify_gpx_files_exists(target_route, submission_file)

        target_route_tree = filename_to_tree(target_route)
        submission_tree = filename_to_tree(submission_file)

        waypoints = get_waypoints_from_tree(target_route_tree)
        trackpoints = get_trackpoints_from_tree(submission_tree)

        self._verify_waypoints_extracted_from_route(waypoints)
        self._verify_trackpoints_extracted_from_submission(trackpoints)

        hit_waypoints = get_hit_waypoints(waypoints, trackpoints, WAYPOINT_TOLERANCE_M)
        self.assertEqual(len(hit_waypoints), 3, f"Expected 3 waypoints hit, got {len(hit_waypoints)}")

    def test_josh_mission_ridge_route_hits_no_waypoints(self):
        """Test that Josh's Mission Ridge route hits no waypoints."""
        target_route = os.path.join(
            self.project_root, 'routes', 'testRoute.gpx'
        )
        submission_file = os.path.join(
            self.project_root, 'testUserSubmissions', '3-23-2026-MissionRidge-Josh.gpx'
        )
        self._verify_gpx_files_exists(target_route, submission_file)

        target_route_tree = filename_to_tree(target_route)
        submission_tree = filename_to_tree(submission_file)

        waypoints = get_waypoints_from_tree(target_route_tree)
        trackpoints = get_trackpoints_from_tree(submission_tree)

        self._verify_waypoints_extracted_from_route(waypoints)
        self._verify_trackpoints_extracted_from_submission(trackpoints)

        hit_waypoints = get_hit_waypoints(waypoints, trackpoints, WAYPOINT_TOLERANCE_M)
        self.assertEqual(len(hit_waypoints), 0, f"Expected 0 waypoints hit, got {len(hit_waypoints)}")

if __name__ == '__main__':
    unittest.main()
