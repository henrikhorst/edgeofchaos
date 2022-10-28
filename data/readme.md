# Purpose of data folder

The data folder combines the saved LTSpice results
in their most natural form. Hence, in .raw or .txt
data files. Each folder is basically named after its
circuit. In each folder there is another readme.md
to describe the circuit and the obtained data

The dataloader.py file contains utility functions
for loading the native LTSpice data and convert it
into some more useful for our further Python processing
chain. 

The Fireflies20.ipynb is just a small case study
for how the obtained data can be processed. It is a relic from the early days of the project