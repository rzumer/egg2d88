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
        self.data = None

import argparse, os, struct

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
            track = Track()
            track_offset = f.tell()

            # get the number of sectors from the track header
            num_sectors = struct.unpack_from('<I', f.read(4))[0]
            sector_offsets = []

            # process sector offsets
            for s in range(0, num_sectors):
                sector = Sector()
                sector_offsets.append(struct.unpack_from('<I', f.read(4))[0])
                track.sectors.append(sector)

            # process track contents
            for o, s in zip(sector_offsets, track.sectors):
                f.seek(track_offset + o, os.SEEK_SET)
                s.cylinder = struct.unpack('B', f.read(1))[0]
                s.head = struct.unpack('B', f.read(1))[0]
                s.record = struct.unpack('B', f.read(1))[0]
                s.size = struct.unpack('B', f.read(1))[0]
                f.seek(8, os.SEEK_CUR) # skip the remainder of the header
                # TODO: find out the meaning of the unhandled sector header bits
                s.data = f.read(128 << s.size)

            disk.tracks.append(track)

        except struct.error:
            break

print(len(disk.tracks), "track(s)")
for t in range(0, len(disk.tracks)):
    print(len(disk.tracks[t].sectors), "sector(s) on track", t)
    for s in range(0, len(disk.tracks[t].sectors)):
        print("size of sector", s, ":", len(disk.tracks[t].sectors[s].data))
