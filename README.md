## Paletisation Generator

```
usage: generator.py [-h] -t WIDTH,HEIGHT -m WIDTH,HEIGHT -M WIDTH,HEIGHT [-n NUM_BLOCKS] [-s NUM_SAMPLES] [-N] [-f FILE_NAME] [-o]

optional arguments:
  -h, --help            show this help message and exit
  -t WIDTH,HEIGHT, --tray_size WIDTH,HEIGHT
                        tray size
  -m WIDTH,HEIGHT, --min_block_size WIDTH,HEIGHT
                        minimum block size
  -M WIDTH,HEIGHT, --max_block_size WIDTH,HEIGHT
                        maximum block size
  -n NUM_BLOCKS, --num_blocks NUM_BLOCKS
                        number of blocks per tray, if omitted - fill entire area
  -s NUM_SAMPLES, --num_samples NUM_SAMPLES
                        number of samples to generate, default=1 [TODO]
  -N, --multiple_samples
                        enable multiple samples in one file [TODO]
  -f FILE_NAME, --file_name FILE_NAME
                        output file name
  -o, --stdout          print data on stdout
```