import csv
import os
from pathlib import Path
from typing import Any

from conductor.client import worker_task

from task_logging.task_logger import get_task_logger

MAX_ROW_IN_CSV = 6

task_logger = get_task_logger()


def get_script_files(vlan_directory: Path) -> tuple[list[str], bool]:
    """
    Check if VLAN directory exists and get all script files in alphabetical order.

    Args:
        vlan_directory (str): Path to the VLAN directory

    Returns:
        tuple: (script_files, directory_exists) where:
            - script_files: Sorted list of script filenames
            - directory_exists: Boolean indicating if directory exists
    """
    if os.path.exists(vlan_directory) and os.path.isdir(vlan_directory):
        # Get all files in the directory (excluding subdirectories)
        files = [f for f in os.listdir(vlan_directory) if os.path.isfile(os.path.join(vlan_directory, f))]
        # Return files sorted alphabetically and True for directory exists
        return sorted(files), True
    else:
        return [], False


def create_first_file(path: Path, input_file: str, vlan_groups: dict[str, list[str]]) -> Any:
    # Create the first file as .sh with comments
    first_output_file_name = input_file.replace(".csv", "_vlan_empty_users.sh")
    first_output_file = path / first_output_file_name
    with open(first_output_file, "w", newline="") as f1:
        f1.write("#!/bin/bash\n")
        f1.write("# VLANs with empty users field and mode not equal to p2p\n\n")

        for vlan, script_files in vlan_groups.items():
            if script_files:  # Only write if there are script files
                f1.write(f"# VLAN: {vlan}\n")
                for script_file in script_files:
                    f1.write(f"{vlan}/{script_file}\n")
                f1.write("\n")

    # Make both scripts executable
    os.chmod(first_output_file, 0o755)
    return first_output_file.name


def create_second(path: Path, input_file: str, all_vlans: set[str], vlan_empty_user: dict[str, list[str]]) -> Any:
    # Create the second file as .sh with comments
    second_output_file_name = input_file.replace(".csv", "_vlan_remaining.sh")
    second_output_file = path / second_output_file_name

    with open(second_output_file, "w", newline="") as f2:
        f2.write("#!/bin/bash\n")
        f2.write("# VLANs with non-empty users field OR mode equal to p2p\n\n")

        for vlan in all_vlans:
            # Check if this VLAN was not included in the first file
            if vlan not in vlan_empty_user:
                # Get all script files for this VLAN directory
                script_files, directory_exists = get_script_files(path / vlan)

                if script_files:  # Only write if there are script files
                    f2.write(f"# VLAN: {vlan}\n")
                    for script_file in script_files:
                        f2.write(f"{vlan}/{script_file}\n")
                    f2.write("\n")

    os.chmod(second_output_file, 0o755)

    return second_output_file.name


def process_csv(path: Path, input_file: str) -> None:
    """
    Process the CSV file and generate two output files with VLAN/script paths.
    First file: VLANs where users field is empty and mode is not "p2p"
    Second file: All other VLANs not included in the first file
    """
    # Dictionary to group paths by VLAN for the first file
    vlan_groups_first_file = {}
    # Set for all unique VLANs (to avoid duplicates)
    all_vlans = set()
    # List to track missing directories for warnings
    missing_directories = []

    with open(path / input_file, newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=";")

        for row in reader:
            # Check if the row has enough columns
            if len(row) < MAX_ROW_IN_CSV:
                continue

            vlan = row[1].strip()  # Column 2 - VLAN
            users = row[4].strip()  # Column 5 - Users
            mode = row[5].strip()  # Column 6 - Mode

            # Save all unique VLANs
            if vlan:
                all_vlans.add(vlan)

            # Conditions for the first file
            if vlan and not users and mode != "p2p":
                # Get all script files for this VLAN directory
                script_files, directory_exists = get_script_files(path / vlan)
                # Store files grouped by VLAN
                vlan_groups_first_file[vlan] = script_files
                # Track missing directories
                if not directory_exists:
                    missing_directories.append(vlan)

    # Count VLANs for second file (those not in first file)
    vlan_count_second = 0
    for vlan in all_vlans:
        if vlan not in vlan_groups_first_file:
            # Get all script files for this VLAN directory
            script_files, directory_exists = get_script_files(path / vlan)

            if script_files:  # Only count if there are script files
                vlan_count_second += 1
            # Track missing directories for second file VLANs too
            if not directory_exists:
                missing_directories.append(vlan)

    # Create the first file as .sh with comments
    first_output_file = create_first_file(path, input_file, vlan_groups_first_file)

    # Create the second file as .sh with comments
    second_output_file = create_second(path, input_file, all_vlans, vlan_groups_first_file)

    # Print summary with VLAN counts only
    vlan_count_first = len([vlan for vlan in vlan_groups_first_file if vlan_groups_first_file[vlan]])
    task_logger.info(f"1. {first_output_file} - {vlan_count_first} VLANs")
    task_logger.info(f"2. {second_output_file} - {vlan_count_second} VLANs")

    # Print warnings for missing directories if any found
    if missing_directories:
        unique_missing = sorted(set(missing_directories))
        task_logger.info(f"\nWARNING: {len(unique_missing)} VLAN directories do not exist:")
        for vlan in unique_missing:
            task_logger.info(f"  - {vlan}")


@worker_task(
    task_definition_name="create_svlan_bash_scripts",
    register_task_def=True,  # Auto-register on startup
)
def create_svlan_bash_scripts(path: str, svlan_extraction_csv: str) -> None:
    csv_path = Path(Path("fm_outputs") / f"{path}")

    process_csv(csv_path, svlan_extraction_csv)
