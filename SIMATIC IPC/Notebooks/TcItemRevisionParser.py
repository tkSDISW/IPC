# SPDX-FileCopyrightText: © Siemens AG
# SPDX-License-Identifier: Apache-2.0
"""
TcItemRevision Parser
~~~~~~~~~~~~~~~~~~~~~

This module defines the `TcItemRevisionParser` class, which extracts and manages
`smw:TcItemRevision` elements from a `.capella` file associated with a given `.aird` file.

This project is compliant with the REUSE Specification Version 3.0.

Copyright Siemens AG, licensed under Apache 2.0 (see full text in LICENSES/Apache-2.0.txt)

Dot-files are licensed under CC0-1.0 (see full text in LICENSES/CC0-1.0.txt)


Typical usage example:
    parser = TcItemRevisionParser("/path/to/model.aird")
    revision = parser.get_by_id("some-uuid")
    print(revision["itemId"])

The parser identifies elements by their `xsi:type="smw:TcItemRevision"` attribute and collects
the following fields if present:
- id
- tcuid
- stableTcId
- itemId
- revisionId

Author: Anthony Komar
"""

import os
import xml.etree.ElementTree as ET

class TcItemRevisionParser:
    """
    A parser class to extract smw:TcItemRevision entries from a .capella file
    located in the same directory as a given .aird file.

    Attributes:
        aird_file_path (str): Path to the .aird file.
        capella_file_path (str): Path to the associated .capella file.
        items (dict): Dictionary mapping IDs to extracted TcItemRevision metadata.
    """

    def __init__(self, aird_file_path):
        """
        Initialize the parser with the path to a .aird file. Automatically locates
        the corresponding .capella file and extracts TcItemRevision entries.

        Args:
            aird_file_path (str): Path to the .aird file.
        """
        self.aird_file_path = aird_file_path
        self.capella_file_path = self._find_capella_file()
        self.items = {}

        if self.capella_file_path:
            self._parse_capella_file()

    def _find_capella_file(self):
        """
        Search for a .capella file in the same directory as the .aird file.

        Returns:
            str or None: Path to the .capella file if found, else None.
        """
        base_dir = os.path.dirname(self.aird_file_path)
        for file in os.listdir(base_dir):
            if file.endswith(".capella"):
                return os.path.join(base_dir, file)
        return None

    def _parse_capella_file(self):
        """
        Parse the .capella XML and extract elements with xsi:type="smw:TcItemRevision".
        Populates the items dictionary using the element 'id' as the key.
        """
        tree = ET.parse(self.capella_file_path)
        root = tree.getroot()

        for elem in root.iter():
            # Identify TcItemRevision by xsi:type while ignoring namespace in tag
            if elem.tag == "ownedExtensions" and elem.attrib.get("{http://www.w3.org/2001/XMLSchema-instance}type") == "smw:TcItemRevision":
                item = {
                    'id': elem.attrib.get('id'),
                    'tcuid': elem.attrib.get('tcuid'),
                    'stableTcId': elem.attrib.get('stableTcId'),
                    'itemId': elem.attrib.get('itemId'),
                    'revisionId': elem.attrib.get('revisionId')
                }
                if item['id']:
                    self.items[item['id']] = item

    def get_by_id(self, item_id):
        """
        Retrieve a specific TcItemRevision entry by its ID.

        Args:
            item_id (str): The 'id' attribute of the TcItemRevision element.

        Returns:
            dict or None: The corresponding TcItemRevision data, or None if not found.
        """
        return self.items.get(item_id)

    def all_items(self):
        """
        Retrieve all parsed TcItemRevision entries.

        Returns:
            list: A list of all TcItemRevision dictionaries.
        """
        return list(self.items.values())