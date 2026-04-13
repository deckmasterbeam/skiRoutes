import xml.etree.ElementTree as ET
from typing import List
import os
import math

WAYPOINT_TOLERANCE_M = 20.0

def _local_name(tag: str) -> str:
    if tag is None:
        return ""
    if "}" in tag:
        return tag.split("}", 1)[1]
    return tag

def filename_to_tree(file_path: str) -> ET.ElementTree[ET.Element]:
    """Parse a GPX file into an ElementTree, with error handling."""
    try:
        tree = ET.parse(file_path)
        return tree
    except ET.ParseError as e:
        print(f"{file_path}: ERROR parsing XML: {e}")
        raise
    except Exception as e:
        print(f"{file_path}: ERROR: {e}")
        raise

def get_waypoints_from_tree(tree: ET.ElementTree[ET.Element]) -> List[dict]:
    """Extract all waypoints from a GPX tree of a route file.
    
    Returns a list of dicts with keys: lat, lon, name (if present)
    """
    root = tree.getroot()
    if root is None:
        return []
    waypoints = []
    
    for elem in root.iter():
        if _local_name(elem.tag).lower() == "wpt":
            wpt = {
                "lat": elem.get("lat"),
                "lon": elem.get("lon"),
                "name": None
            }
            # Check for name child element
            for child in elem:
                if _local_name(child.tag).lower() == "name":
                    if child.text:
                        wpt["name"] = child.text.strip()
                    break
            waypoints.append(wpt)
    
    return waypoints


def get_trackpoints_from_tree(tree: ET.ElementTree[ET.Element]) -> List[dict]:
    """Extract all trackpoints from a candidate GPX tree.
    
    Returns a list of dicts with keys: lat, lon, name (if present), time (if present)
    """
    root = tree.getroot()
    trackpoints = []
    
    for elem in root.iter():
        if _local_name(elem.tag).lower() == "trkpt":
            trkpt = {
                "lat": elem.get("lat"),
                "lon": elem.get("lon"),
                "name": None,
                "time": None
            }
            # Check for name and time child elements
            for child in elem:
                tag_name = _local_name(child.tag).lower()
                if tag_name == "name":
                    if child.text:
                        trkpt["name"] = child.text.strip()
                elif tag_name == "time":
                    if child.text:
                        trkpt["time"] = child.text.strip()
            trackpoints.append(trkpt)
    
    return trackpoints


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate the distance between two coordinates in meters using the haversine formula."""
    R = 6371000  # Earth's radius in meters
    
    lat1_rad = math.radians(float(lat1))
    lat2_rad = math.radians(float(lat2))
    delta_lat = math.radians(float(lat2) - float(lat1))
    delta_lon = math.radians(float(lon2) - float(lon1))
    
    a = math.sin(delta_lat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    
    return R * c


def get_hit_waypoints(waypoints: List[dict], trackpoints: List[dict], tolerance_m: float) -> List[dict]:
    """Check which waypoints have been hit by trackpoints within the tolerance distance.
    
    Returns a list of dicts with keys: lat, lon, name, first_hit_time
    """
    hit_waypoints = []
    
    for waypoint in waypoints:
        wpt_lat = float(waypoint["lat"])
        wpt_lon = float(waypoint["lon"])
        
        for trackpoint in trackpoints:
            trkpt_lat = float(trackpoint["lat"])
            trkpt_lon = float(trackpoint["lon"])
            
            distance = haversine_distance(wpt_lat, wpt_lon, trkpt_lat, trkpt_lon)
            
            if distance <= tolerance_m:
                hit_waypoints.append({
                    "lat": waypoint["lat"],
                    "lon": waypoint["lon"],
                    "name": waypoint["name"],
                    "first_hit_time": trackpoint["time"]
                })
                break
    
    return hit_waypoints

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)

# one run
# candidate_user_submission_filename = os.path.join(project_root, 'testUserSubmissions', '2-6-26-ZermattMatterhorn-JoshOneRun.gpx')
# all day
# candidate_user_submission_filename = os.path.join(project_root, 'testUserSubmissions', '2-6-26-ZermattMatterhorn-JoshAllDay.gpx')
# mission ridge, no waypoints hit
candidate_user_submission_filename = os.path.join(project_root, 'testUserSubmissions', '3-23-2026-MissionRidge-Josh.gpx')
target_route = os.path.join(project_root, 'routes', 'testRoute.gpx')

def main():
    candidate_user_submission = filename_to_tree(candidate_user_submission_filename)
    candidate_trackpoints = get_trackpoints_from_tree(candidate_user_submission)
    # print out the first 5 trackpoints for debugging
    print(f"\nCandidate trackpoints ({len(candidate_trackpoints)}):")
    for i, trkpt in enumerate(candidate_trackpoints[:5], 1):
        name_str = f" - {trkpt['name']}" if trkpt['name'] else ""
        print(f"  {i}. ({trkpt['lat']}, {trkpt['lon']}){name_str}")
    
    target_route_tree = filename_to_tree(target_route)
    waypoints_to_hit = get_waypoints_from_tree(target_route_tree)
    print(f"\nWaypoints to hit ({len(waypoints_to_hit)}):")
    for i, wpt in enumerate(waypoints_to_hit, 1):
        name_str = f" - {wpt['name']}" if wpt['name'] else ""
        print(f"  {i}. ({wpt['lat']}, {wpt['lon']}){name_str}")
    
    # Check which waypoints were hit
    hit_waypoints = get_hit_waypoints(waypoints_to_hit, candidate_trackpoints, WAYPOINT_TOLERANCE_M)
    print(f"\nWaypoints hit ({len(hit_waypoints)} out of {len(waypoints_to_hit)}):")
    for i, wpt in enumerate(hit_waypoints, 1):
        name_str = f" - {wpt['name']}" if wpt['name'] else ""
        time_str = f" at {wpt['first_hit_time']}" if wpt['first_hit_time'] else " (no timestamp)"
        print(f"  {i}. ({wpt['lat']}, {wpt['lon']}){name_str}{time_str}")

    return hit_waypoints

if __name__ == "__main__":
    main()
