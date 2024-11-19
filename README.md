# LVM Int Ass

## What is it?
LVM Int Ass is a assembler and interpreter for a learning virtual machine

## Flags
**CLI flags are set:**
- mode - assembler or interpreter mode (assemble, interpret)
- input_file (txt) - your txt file with data
- output_file (bin) - your output file (if it doesn't exist, the program will create it)
- log_file (xml) - your log file (if it doesn't exist, the program will create it)
- result_file (xml) - your file with results (if it doesn't exist, the program will create it)
- memory_range [start:end] - memory range for interpreter

## Examples

### Input File
```
A=30, B=1, C=51
A=1, B=1, C=817
A=7, B=6, C=3
A=45, B=0, C=7, D=2
```
### Example for interpreter
```
python intass.py interpret input.txt output.bin log.xml --result_file=result.xml --memory_range=0:10
```
or
```
intass.py interpret input.txt output.bin log.xml --result_file=result.xml --memory_range=0:10
```
### Example for assembler
```
python intass.py assemble input.txt output.bin log.xml
```
or
```
python intass.py assemble input.txt output.bin log.xml
```
