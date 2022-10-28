import subprocess
import utils.save_and_load_spike_data as sl
import ltspy3  # Python module

dir_XVIIx64 = "C:\Program Files\LTC\LTspiceXVII"

subprocess.call(dir_XVIIx64 + "\XVIIx64.exe -b version1.txt")

raw_data_file="version1.raw"

# ====================  Read data into Python IDE==============================
sd = ltspy3.SimData(raw_data_file) # to create a Python object called sd
name = sd.variables # variable names from .raw data. It is an attribute (data)
print(name)
num_var = sd.novariables
#time_trace = sd.values # transient simulation: time and traces from .raw data
time = sd.values[0] # The first element is the time as a matrix
print(type(time), len(time))
trace = sd.values[1:3] # Indexes: including the first but excluding the last