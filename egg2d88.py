class Disk:
    def __init__(self):
        self.tracks = []

class Track:
    def __init__(self):
        self.sectors = []

class Sector:
    def __init__(self):
        self.cylinder = 0
        self.head = 0
        self.record = 0
        self.size = 0
        self.data_size = 0

import argparse, struct, os

parser = argparse.ArgumentParser(description='Convert EGG to D88.')
parser.add_argument('input', metavar='input_file', help='the input EGG file')
parser.add_argument('output', metavar='output_file', nargs='?', default='out.d88', help='the output D88 file')
args = parser.parse_args()

# parse
disk_size = os.path.getsize(args.input)
disk = Disk()

with open(args.input, 'rb') as f:
    while True:
        try:
            buf = f.read(4)
            if not buf:
                break

            track = Track()

            # get the number of sectors from the track header
            num_sectors = struct.unpack_from('<I', buf)[0]
            sector_offsets = []

            for s in range(0, num_sectors):
                sector = Sector()
                buf = f.read(4)
                sector_offsets.append(struct.unpack_from('<I', buf)[0])
                track.sectors.append(sector)

            disk.tracks.append(track)
            # TODO: process track contents
            break

        except struct.error:
            break

print(len(disk.tracks), "track(s)")
for t in range(0, len(disk.tracks)):
    print(len(disk.tracks[t].sectors), "sector(s) on track", t)
