"""
Script for doing impedance matching for our diamond problem

Set up script and run it to test
"""
from GIM import IM

#create the experiments
experiment = IM()

#add materials to the experiments
experiment.add_material("diamond", "hyades")
experiment.add_material("quartz", "desjarlais_quartz")

#finalize setup, solve & plot
experiment.finalize_setup()
experiment.solve(Us = 15.44) #solve this impedance matching problem for a measures shock velocity of 16km/s
experiment.plot_results(show_hugoniots=False, 
                        label_initial_measurement=False, 
                        label_final_measurement=False,
                        label_appendix="ASBO1")
experiment.solve(Us = 15.62)
experiment.plot_results(title = "s38635 Impedance Matching", label_appendix = "ASBO2")
experiment.show_plot()