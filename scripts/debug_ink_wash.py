#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import sqlite3

# Add project root to path
sys.path.insert(0, os.getcwd())

from mcp_server.tools.element_query import get_db_path

def main():
    db_path = get_db_path()
    print(f"DB Path: {db_path}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("\n--- Categories in 'art' domain ---")
    cursor.execute("SELECT category_id, name, total_elements FROM categories WHERE domain_id = 'art'")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
        
    print("\n--- Sample elements in 'ink_wash_techniques' (if exists) ---")
    try:
        cursor.execute("SELECT element_id, name, keywords FROM elements WHERE category_id = 'ink_wash_techniques'")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
    except Exception as e:
        print(f"Error querying elements: {e}")

    print("\n--- Checking for keyword matches ---")
    keywords = ["ink", "wash", "traditional", "negative", "space"]
    for kw in keywords:
        cursor.execute(f"SELECT element_id, name FROM elements WHERE domain_id='art' AND keywords LIKE '%{kw}%'")
        rows = cursor.fetchall()
        print(f"Keyword '{kw}': {len(rows)} matches")
        if rows:
            print(f"  Sample: {rows[0]}")

    conn.close()

if __name__ == "__main__":
    main()
