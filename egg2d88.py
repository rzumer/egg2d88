import argparse

parser = argparse.ArgumentParser(description='Convert EGG to D88.')
parser.add_argument('input', metavar='input_file', help='the input EGG file')
parser.add_argument('output', metavar='output_file', nargs='?', default='out.d88', help='the output D88 file')
args = parser.parse_args()
print(args.output)



