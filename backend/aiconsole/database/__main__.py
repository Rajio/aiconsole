#!/usr/bin/env python
"""
Main entry point for the database module.
"""

import sys

from aiconsole.database.custom_queries import main as custom_queries_main
from aiconsole.database.run_sync import main as sync_main
from aiconsole.database.usage_example import main as usage_example_main


def main():
    """Main function to run the database check and synchronization."""
    if len(sys.argv) < 2:
        print("Usage: python -m aiconsole.database [sync|example|queries]")
        return

    if sys.argv[1] == "sync":
        sync_main()
    elif sys.argv[1] == "example":
        usage_example_main()
    elif sys.argv[1] == "queries":
        custom_queries_main()
    else:
        print("Unknown command. Use 'sync', 'example', or 'queries'.")


if __name__ == "__main__":
    main()
