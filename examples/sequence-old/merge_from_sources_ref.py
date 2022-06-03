#!/usr/bin/env python3

#
# Configure logging
#
import logging
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--debug", action="store_true", help="Show debugging output.")
args = parser.parse_args()
log_level = logging.DEBUG if args.debug else logging.INFO
logging.basicConfig(level=log_level, format='[%(levelname)8s] %(name)-15s : %(message)s')

#
# The following example shows how to construct a new sequence
# that is the result of merging two other sequences. The data is
# not copied, but only referenced.
#

#
# Generate a sequence
#
import os

print()

print("Running: \"python3 ./write_from_files.py > /dev/null\"")
os.system("python3 ./write_from_files.py > /dev/null")
print()

print("Running: \"python3 ./write_from_tensor.py > /dev/null\"")
os.system("python3 ./write_from_tensor.py > /dev/null")
print()

#
# Merge the two sequences
#
from itypes import Sequence

# NOTE: The merged seuqence will be kept in memory
# (alternatively you could write it directly by specifying
# filename=... to the sequence).
# NOTE: The source sequences in this case come from disk,
# but they can equally be from memory or on-demand.

seq1 = Sequence('out_write_from_files/data.gridseq').read()
seq2 = Sequence('out_write_from_tensor/data.gridseq').read()

# NOTE: source_mode="copy" will create local copies of the sequences
# when writing the new sequences. source_mode="ref" will only create references.
new_seq = Sequence(source_mode="ref")

# NOTE: "linear" merging in ignores scene and frame names but relies
# on the linear index. "structured" merging relies on scene and frame names
# and igonres the linear index. If your sequences are of equal scene lengths,
# you can safely rely on "linear", which is the default value.

# First row: show images
with new_seq.grid.new_row() as row:
    # You can speicfy source_id=... if the source id is different
    # In the example we switch image0 and image1
    row.add_cell('image', 'image0', source_seq=seq1, source_id="image1", source_method="linear")
    row.add_cell('image', 'image1', source_seq=seq1, source_id="image0", source_method="structured")
    row.add_cell('flow',  'flow',   source_seq=seq2) # source_method is "linear" by default

# Second row: show flow and occlusions
with new_seq.grid.new_row() as row:
    row.skip_cell()
    row.skip_cell()
    row.add_cell('image', 'occ',    source_seq=seq2) # source_method is "linear" by default

# We now need fill in the frames from the sources
new_seq.fill_from_sources()

# TODO
# In future you will be able to directly visualize the data without ever writing it to disk:
# iviz.visualize(new_seq)

# Write the entire sequence to disk.
# This will write data.gridseq and the images.
new_seq.write(filename='out_merge_from_sources_ref/data.gridseq')

print("To view run: \"iviz out_merge_from_sources_ref/data.gridseq\"")
print()


