"""
This file provides classes to create in a most automatically way Netlist files for LTSpice.
The mother class SpiceNetlist contains the attribute 'netlist' which is at the beginning an empty
list which is then filed with entries where each entry is a line of the Netlist. To keep track
of how many of each component already exist counter attributes are introduced. E.g. for the
Number of Voltage sources self.num_V .
As one daughter class the Fireflies class is build. This class is especially useful for leaky fire integrated
oscillators which are coupled in several ways.
"""

import pickle


class SpiceNetlist:  # extend it to your needs :)

    def __init__(self):
        self.netlist = []
        self.num_V = 0  # counter for number of independent voltage sources
        self.num_I = 0  # counter for number of independent current sources
        self.num_R = 0  # counter for number of resistors
        self.num_C = 0  # counter for number of capacitors
        self.num_L = 0  # counter for number of inductors
        self.num_M = 0  # counter for number of mosfets
        self.num_X = 0  # counter for number of subcircuits

    def create_start(self, circuit_name="Edge of Chaos"):
        """
        Creates start of the netlist. This is necessary since LTSpice considers the first line
        of the created Netlist always as the name
        """
        self.netlist.append(f'*  {circuit_name}\n'.encode('ascii'))

    def create_end(self):
        """ Creates end of the Netlist file"""
        self.netlist.append('.backanno\n'.encode('ascii'))
        self.netlist.append('.end\n'.encode('ascii'))

    def add_libs(self):
        """
        lib files have to be in the ltspice_automation folder to be found
        """
        run_path = '../../../ltspice_automation/'
        self.netlist.append('.model NMOS NMOS\n'.encode('ascii'))
        self.netlist.append('.model PMOS PMOS\n'.encode('ascii'))
        self.netlist.append(f'.lib {run_path}2N6027.LIB\n'.encode('ascii'))
        self.netlist.append(f'.lib {run_path}standard.mos\n'.encode('ascii'))


    def add_simulation(self, start_time=0, stop_time=180, save_time="1E-3", set_startup=True):
        """
        Add the simulation line in the Netlist

        :param start_time: Obvious
        :param stop_time: Obvious
        :param save_time: Obvious
        :param set_startup: start external DC supply voltages at 0 Volt -> necessary for reproducible
        simulation results
        :return: None
        """
        if set_startup:
            startup = "startup"

        else:
            startup = ''
        self.netlist.append(f'.tran {start_time} {stop_time} {save_time} {startup}\n'.encode('ascii'))

    def add_voltage_source(self, plus_node, minus_node, voltage):
        """

        :param plus_node: Obvious
        :param minus_node: Obvious
        :param voltage: Value of the Voltage source e.g 10
        :return: None
        """
        self.num_V += 1  # increment by one to create a unique name
        self.netlist.append(
            (' '.join(('V' + str(self.num_V), str(plus_node), str(minus_node), str(voltage))) + '\n').encode('ascii'))

    def add_resistor(self, plus_node, minus_node, value):
        """

        :param plus_node: Obvious
        :param minus_node: Obvious
        :param value: Value of the resistor e.g. 1k
        :return: None
        """
        self.num_R += 1  # increment by one to create a unique name
        self.netlist.append(
            (' '.join(('R' + str(self.num_R), str(plus_node), str(minus_node), str(value))) + '\n').encode('ascii'))

    def add_capacitor(self, plus_node, minus_node, value):
        """

        :param plus_node: Obvious
        :param minus_node: Obvious
        :param value: Value of the capacitor e.g. 1u
        :return: None
        """
        self.num_C += 1
        self.netlist.append(
            (' '.join(('C' + str(self.num_C), str(plus_node), str(minus_node), str(value))) + '\n').encode('ascii'))

    def add_mosfet(self, drain, gate, source, bulk, name):
        """
        Here a three terminal device is assumed. Enhance functionality yourself if needed :)
        :param anode: Obvious
        :param gate: Obvious
        :param cathode:
        :param name: type of the mosfet i.e. NMOS or PMOS
        :return: None
        """
        self.num_M += 1
        self.netlist.append(
            (' '.join(('M' + str(self.num_M), str(drain), str(gate), str(source), str(bulk), str(name))) + '\n').encode('ascii'))


    def add_subcircuit(self, anode, gate, cathode, name):
        """
        Here a three terminal device is assumed. Enhance functionality yourself if needed :)
        :param anode: Obvious
        :param gate: Obvious
        :param cathode:
        :param name: name of the subcircuit e.g 2N6027
        :return: None
        """
        self.num_X += 1
        self.netlist.append(
            (' '.join(('XU' + str(self.num_X), str(anode), str(gate), str(cathode), str(name))) + '\n').encode('ascii'))

    def return_netlist_file(self):
        """
        Takes the Netlist ( i.e. self.netlist) which is a list with each element a single line
        for the final Netlist file and concatenates the single lines(i.e. list elements) to
        a single (binary) string

        :return: string in ascii format -> ascii is needed for LTSpice
        """
        return ''.encode('ascii').join([item for item in self.netlist])


class Fireflies(SpiceNetlist):
    """
    For the correct functionality of this class it is absolutely necessary to provide a config dictionary
    file in the correct format. For an example of a correct format see end of this file or even better in
    the Test.ipynb in this folder.
    """
    def __init__(self, config_file):
        super().__init__()
        # reads in the config file for the circuit and assigns the read in config object to an attribute
        with open(config_file, 'rb') as config_dictionary_file:
            self.config = pickle.load(config_dictionary_file)  # self.config is a really nested dictionary

        self.num_O = 0  # counter for number of oscillators
        self.num_Coupling = 0  # counter for number of oscillator couplings  (or other)

    def create_coupling_to_ground(self, value):
        """
        The famous coupling resistor a lot of our sweeps are done with to drive a circuit towards
        and away from criticality
        :param value: value of the coupling to ground resistor e.g. 5k
        :return: None
        """
        self.add_resistor('central', '0', value)

    def create_oscillator(self, oscillator_config):
        """
        This oscillator is the standard leaky fire integrator without internal voltage source fot the membrane
        potential

        :param oscillator_config: dictionary with component values as key-value pairs and connections also
         saved as key and corresponding value
        :return:
        """
        self.num_O += 1
        self.add_resistor(oscillator_config['input_connection'], 'anode' + str(self.num_O), oscillator_config['Rin_a'])
        self.add_capacitor('anode' + str(self.num_O), '0', oscillator_config['Ca_gnd'])
        self.add_resistor('cathode' + str(self.num_O), '0', oscillator_config['Rc_gnd'])
        self.add_resistor(oscillator_config['input_connection'], 'gate' + str(self.num_O), oscillator_config['Rin_g'])
        self.add_resistor('gate' + str(self.num_O), '0', oscillator_config['Rg_gnd'])
        self.add_subcircuit('anode' + str(self.num_O), 'gate' + str(self.num_O), 'cathode' + str(self.num_O), '2N6027')
        for elem in oscillator_config['output_connection']:
            self.create_coupling('gate' + str(self.num_O), elem, oscillator_config['output_connection'])

    def create_coupling(self, input, output, config):
        """

        :param input: input node/connection
        :param output: output node/connection
        :param config: nested dict with all output connection information saved in it
        :return:
        """
        self.num_Coupling += 1

        if config[output][0] == 'excitatory':
            self.add_capacitor(input, 'cr' + str(self.num_Coupling), config[output][1]['C_coupling'])
            self.add_resistor('cr' + str(self.num_Coupling), 'gate' + output, config[output][1]['R_coupling'])

        elif config[output][0] == 'inhibitory':
            self.add_mosfet('mr' + str(self.num_Coupling), input.replace('gate', 'cathode'), 0, 0, 'NMOS')
            self.add_resistor('mr' + str(self.num_Coupling), 'anode' + output, config[output][1]['R_coupling'])


        else:
            # this is a relict for the simplest test case of two coupled oscillators
            self.add_capacitor(input, 'cr' + str(self.num_Coupling), '1u')
            self.add_resistor('cr' + str(self.num_Coupling), 'rc' + str(self.num_Coupling), '1k')
            self.add_capacitor('rc' + str(self.num_Coupling), output, '1u')

    def create_netlist(self):
        """
        This function finally fills the (empty) netlist with entries
        :return: None
        """
        self.create_start()
        for i in range(self.config['V']['num_Vs']):
            self.add_voltage_source('V' + str(i + 1), '0', self.config['V']['values'][i])
        # self.create_coupling_to_ground(self.config['R_coup'])
        for j in range(self.config['O']['num_Os']):
            self.create_oscillator(self.config['O']['values'][j])
        self.add_simulation()
        self.add_libs()
        self.create_end()
