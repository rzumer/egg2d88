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
parser.add_argument('input', metavar='input_prefix', help='the input EGG image file name prefix')
parser.add_argument('output', metavar='output_file', nargs='?', default='out.d88', help='the output D88 file')
args = parser.parse_args()

disk = Disk()

# get matching input files
base_path = os.path.dirname(args.input)
file_prefix = os.path.basename(args.input)
input_files = []

for f in os.listdir(base_path):
    full_path = os.path.join(base_path, f)
    if os.path.isfile(full_path) and f.startswith(file_prefix):
        try:
            track_number = int(os.path.splitext(f)[0].split('-')[-1])
            input_files.append( (track_number, full_path) ) # add as tuple
        except ValueError:
            pass

if len(input_files) == 0:
    print("No matching input files found.")
    exit(0)

# add entries for missing tracks and sort on track number
for t in range(0, max(input_files, key=lambda tup: tup[0])[0]):
    if not any([item[0] == t for item in input_files]):
        input_files.append( (t, None) )

input_files.sort(key=lambda tup: tup[0]) # sort on track number

# parse EGG input
for t in input_files:
    track = Track()

    if t[1] is not None:
        with open(t[1], 'rb') as f:
            try:

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
                    f.seek(o, os.SEEK_SET)

                    # read sector header
                    s.cylinder = struct.unpack_from('B', f.read(1))[0]
                    s.head = struct.unpack_from('B', f.read(1))[0]
                    s.record = struct.unpack_from('B', f.read(1))[0]
                    s.size = struct.unpack_from('B', f.read(1))[0]

                    # TODO: find out the meaning of the unhandled sector header bits
                    # for now, assert that the values of the next 8 bytes are those expected
                    magic_bits = struct.unpack_from('<I', f.read(4))[0]
                    assert magic_bits == 1
                    magic_bits = struct.unpack_from('<I', f.read(4))[0]
                    assert magic_bits == 128 << s.size # seems to correspond

                    # read sector content
                    s.data = f.read(128 << s.size)

            except struct.error:
                print("Error reading input data.")
                exit(-1)

    disk.tracks.append(track)

# write D88 output
with open(args.output, 'wb') as f:
    # write disk header
    disk_header_size = 688; # TODO: confirm that this is always valid
    sector_header_size = 16;
    f.write('\0' * 16 + '\0') # disk name/comment and terminator
    f.write('\0' * 9) # reserved bits
    f.write('\0') # write protect flag
    f.write('\0') # media flag, hardcoded as 2D
    # TODO: detect the media and write the correct flag

    # compute and write the total output disk size
    output_disk_size = sum([len(s.data) + sector_header_size
        for t in disk.tracks
        for s in t.sectors]) + disk_header_size

    f.write(struct.pack('<I', output_disk_size))

    # write the track table
    track_offset = disk_header_size;
    for track in disk.tracks:
        if not any(track.sectors):
            f.write('\0' * 4) # null track
        else:
            f.write(struct.pack('<I', track_offset))
            track_offset += sum([len(s.data) + sector_header_size
                for s in track.sectors])

    # pad the disk header
    while f.tell() < disk_header_size:
        f.write('\0' * 4) # null track

    # write sector contents
    for track in disk.tracks:
        if not any(track.sectors):
            continue # skip null tracks
        for sector in track.sectors:
            f.write(struct.pack('B', sector.cylinder))
            f.write(struct.pack('B', sector.head))
            f.write(struct.pack('B', sector.record))
            f.write(struct.pack('B', sector.size))
            f.write(struct.pack('<H', len(track.sectors)))
            f.write('\0') # density, hardcoded as double
            # TODO: detect single/double density
            f.write('\0') # DDAM flag, hardcoded as normal
            # TODO: detect deleted data
            f.write('\0') # FDC status, hardcoded as normal
            # TODO: detect FDC status
            f.write('\0' * 5) # reserved bits
            f.write(struct.pack('<H', len(sector.data)))
            f.write(sector.data)

print("Wrote {:d} tracks and {:d} sectors.".format(len(disk.tracks),
    sum([len(track.sectors) for track in disk.tracks])))
