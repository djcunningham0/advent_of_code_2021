from __future__ import annotations

from shared import read_text_file
from typing import List
from functools import reduce


HEX_TO_BIN = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111",
}


def parse_data(path: str) -> str:
    data = read_text_file(path)
    return data[0]


def hex_to_bin(s: str) -> str:
    for hex, bin in HEX_TO_BIN.items():
        s = s.replace(hex, bin)
    return s


def bin_to_int(bin_string: str) -> int:
    return int(bin_string, 2)


class Packet:
    def __init__(self, s: str):
        self.s = s
        self.version = bin_to_int(s[:3])
        self.type_ = bin_to_int(s[3:6])

        self.literal_value = None
        self.leftover_bits = ""
        self.subpackets: List[Packet] = []

        self.process_packet()

    def __len__(self) -> int:
        return len(self.s)

    def __repr__(self):
        return f"Packet(version={self.version}, type={self.type_}, length={len(self)}, subpackets={len(self.subpackets)})"

    def process_packet(self):
        if self.type_ == 4:
            self.process_type_4()
        else:
            self.process_operator_packet()

    def process_type_4(self):
        last = False
        groups = []
        i = 6
        while not last:
            if self.s[i] == "0":
                last = True
            group = self.s[i+1:i+5]
            groups.append(group)
            i += 5

        end = i
        if any(x != "0" for x in self.s[i:end]):
            raise ValueError(f"Found nonzero trailing bits in {self.s[:end]}")
        self.leftover_bits = self.s[end:]
        self.s = self.s[:end]
        self.literal_value = bin_to_int("".join(groups))

    def process_operator_packet(self):
        length_type = self.s[6]
        if length_type == "0":
            self.process_length_type_0()
        elif length_type == "1":
            self.process_length_type_1()

    def process_length_type_0(self):
        length = bin_to_int(self.s[7:22])
        total_subpacket_length = 0
        start = 22
        while total_subpacket_length < length:
            s = self.s[start:]
            packet = Packet(s)
            self.subpackets.append(packet)
            total_subpacket_length += len(packet)
            start += len(packet)
        self.leftover_bits = self.s[22+length:]
        self.s = self.s[:22+length]

    def process_length_type_1(self):
        n_packets = bin_to_int(self.s[7:18])
        s = self.s[18:]
        for _ in range(n_packets):
            packet = Packet(s)
            self.subpackets.append(packet)
            s = packet.leftover_bits
        self.leftover_bits = s
        self.s = self.s[:len(self.s) - len(self.leftover_bits)]

    def sum_versions(self):
        version_sum = self.version
        for p in self.subpackets:
            version_sum += p.sum_versions()
        return version_sum

    def get_packet_value(self):
        value = 0
        if self.type_ == 4:
            return self.literal_value
        elif self.type_ == 0:
            return sum(p.get_packet_value() for p in self.subpackets)
        elif self.type_ == 1:
            values = [p.get_packet_value() for p in self.subpackets]
            return reduce(lambda a, b: a * b, values)
        elif self.type_ == 2:
            return min(p.get_packet_value() for p in self.subpackets)
        elif self.type_ == 3:
            return max(p.get_packet_value() for p in self.subpackets)
        elif self.type_ == 5:
            return 1 if self.subpackets[0].get_packet_value() > self.subpackets[1].get_packet_value() else 0
        elif self.type_ == 6:
            return 1 if self.subpackets[0].get_packet_value() < self.subpackets[1].get_packet_value() else 0
        elif self.type_ == 7:
            return 1 if self.subpackets[0].get_packet_value() == self.subpackets[1].get_packet_value() else 0
        return value


def get_packet_from_string(s: str) -> Packet:
    s = hex_to_bin(s)
    return Packet(s)


if __name__ == "__main__":
    data = parse_data("data/16.txt")

    ### Part 1
    packet = get_packet_from_string(data)
    version_sum = packet.sum_versions()
    print(f"Solution 16a: {version_sum}")

    ### Part 2
    packet_value = packet.get_packet_value()
    print(f"Solution 16b: {packet_value}")
