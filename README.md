# Arithmetic Coding

python3 `<input file>` `<option>` `<output file>` 

**Options:**
- `c` - Compression
- `d` - Decompression

**File Paths:**
- `<input file>` - Path to any file containing an image
- `<output file>` - Path to the output comp file (after compression)

## Example Usage:

### Compression and Decompression:
```bash
python3 c alice30.txt alice30.comp
python3 d alice30.comp alice30.txt
