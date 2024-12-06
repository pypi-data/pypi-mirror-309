#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# Copyright (C) 2024, Ondrej Vanka
# 
# File:         pidbcard.py
# Description:  *.db (Database) PXI Card data structure parser
# Version:      1.00
# Author:       Ondrej Vanka @aknavj <ondrej@vanka.net>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
"""

import re

class PiDbCard:

    def __init__(self, file_path):
        self.file_path = file_path
        self.card_data = {
            "header": None,
            "generation": None,
            "architecture": None,
            "logical_layers": [],
            "subunits": [],
            "physical_layers": [],
        }
        self.line_mapping = {}  # maps line numbers to data locations

    def parse_file(self):
        """Parse the file and populate card_data."""
        with open(self.file_path, "r") as file:
            for line_no, line in enumerate(file):
                line = line.strip()
                if not line or line.startswith("H") or line.startswith("E"):
                    continue

                prefix = line[0]
                if prefix == "P":
                    self.parse_header(line, line_no)
                elif prefix == "G":
                    self.parse_generation(line, line_no)
                elif prefix == "A":
                    self.parse_architecture(line, line_no)
                elif prefix == "S":
                    self.parse_subunits(line, line_no)
                elif prefix == "R":
                    self.parse_relay(line, line_no)

        return self.card_data

    def parse_header(self, line, line_no):
        """Parse the header line."""
        match = re.match(r"(PILPXIDB[0-9]+);([^,]+),([0-9]+),([0-9.]+)", line)
        if match:
            pilpxi_version, card_id, card_sn, fw_version = match.groups()
            pilpxi_version_num = int(pilpxi_version[-3:])  # extract numeric version
            
            # determine if the card is simulated
            is_simulated = card_sn.startswith("1000000")

            self.card_data["header"] = {
                "pilpxi_version": pilpxi_version_num,
                "card_id": card_id,
                "card_sn": card_sn,
                "fw_version": fw_version,
                "is_simulated": is_simulated
            }

            self.line_mapping[line_no] = {"type": "card_id"}

        #match = re.match(r"PILPXIDB([0-9]+);(.*)", line)
        #if match:
        #    version, card_info = match.groups()
        #    self.card_data["header"] = {"version": int(version), "card_info": card_info}
        #    self.line_mapping[line_no] = {"type": "header"}

    def parse_generation(self, line, line_no):
        """Parse the generation line."""
        match = re.match(r"G;([0-9]+)", line)
        if match:
            self.card_data["generation"] = int(match.group(1))
            self.line_mapping[line_no] = {"type": "generation"}

    def parse_architecture(self, line, line_no):
        """Parse the architecture line."""
        match = re.match(r"A;([0-9]+);([^;]+);([0-9]+);([^;]+)", line)
        if match:
            loops, description, num_loops, allocations = match.groups()
            allocations = list(map(int, allocations.split(",")))
            self.card_data["architecture"] = {
                "loops": int(loops),
                "description": description,
                "num_loops": int(num_loops),
                "allocations": allocations,
            }
            self.line_mapping[line_no] = {"type": "architecture"}

            for i, alloc in enumerate(allocations):
                self.card_data["physical_layers"].append({
                    "loop_id": i,
                    "rows": alloc,
                    "cols": 1,
                    "relays": {},
                })

    def parse_subunits(self, line, line_no):
        """Parse the subunit line."""
        match = re.match(r"S;([0-9]+);([0-9]+);([0-9]+);([0-9]+);([0-9]+);([0-9]+);([^;]+)", line)
        if match:
            layer_id, sub_type, rows, cols, components, u2, description = match.groups()
            subunit_id = int(layer_id) + 1
            self.card_data["subunits"].append({
                "layer_id": subunit_id,
                "type": int(sub_type),
                "rows": int(rows),
                "cols": int(cols),
                "num_components": int(components),
                "u2": int(u2),
                "description": description,
                "relays": {},
            })
            self.line_mapping[line_no] = {"type": "subunit", "id": subunit_id}

    def parse_relay(self, line, line_no):
        """Parse the relay line."""
        match = re.match(r"R;([LP]);([SL][0-9]+)BIT([0-9]+);([0-9]+)", line)
        if match:
            layer_type, subunit_or_layer, bit, count = match.groups()
            bit, count = int(bit), int(count)

            if layer_type == "L":
                subunit_id = int(re.sub(r"[^0-9]", "", subunit_or_layer))
                for subunit in self.card_data["subunits"]:
                    if subunit["layer_id"] == subunit_id:
                        cols = subunit["cols"]
                        row, col = (bit - 1) // cols, (bit - 1) % cols
                        subunit["relays"][(row, col)] = count
                        self.line_mapping[line_no] = {"type": "logical", "row": row, "col": col}
                        break

            elif layer_type == "P":
                loop_id = int(re.sub(r"[^0-9]", "", subunit_or_layer))
                for loop in self.card_data["physical_layers"]:
                    if loop["loop_id"] == loop_id:
                        loop["relays"][(bit - 1, 0)] = count
                        self.line_mapping[line_no] = {"type": "physical", "row": bit - 1, "col": 0}
                        break