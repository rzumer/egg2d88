# egg2d88

Convert EGG files to D88 format.

Not all disk features are supported, but the program will attempt to detect discrepancies.

## Dependencies

- [Python](https://www.python.org/) in the system or user path (both 2.x and 3.x should work)
- [QuickBMS](https://aluigi.altervista.org/quickbms.htm)
- [Executable extraction script](http://aluigi.altervista.org/bms/project_egg.bms)

## Usage

The QuickBMS source package appears to be missing files, so only a Batch script for Windows is provided.

1. Extract the QuickBMS executable, the `project_egg.bms` script, and input EGG files (with the `exe` extension) in the same directory.
2. Call `egg2d88.bat <input_file>`, where `<input_file>` is the name of the executable you wish to extract.
3. If QuickBMS asks to create an output directory, say yes.
