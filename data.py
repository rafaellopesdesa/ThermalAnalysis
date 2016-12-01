from dataClasses import dataInfo
import channels

''' 
     The lines here follow an EXCEL style: the first line in the CSV file is number 2 and the first and last line are included in the averages  
     You create a new data taking period by using

        dataInfo(title, csvfile, channels)
     
     and then the method

        addCondition(power, firstLine, lastLine)

     Channels encodes the entries as defined in the labview code used to acquire the data. It is written in the channels.py file with a ROOT tree notation.
     Temperature measurments are encoded by the channels defined above. The following have to be defined:

        coolant
        tubing
        triangle
        backplate
        sensor
        module
        ambient
     
'''

data = {}

data['TiltedBarrelA'] = dataInfo('TiltedBarrelA', 'data/TiltedBarrelA_062416_151324.csv', channels.channelsTiltedBarrelA)
data['TiltedBarrelA'].addCondition('0W', 0., 127, 139)
data['TiltedBarrelA'].addCondition('7p7W', 7.7, 111, 117)

data['TiltedBarrelA'].setFormula('coolant', '((supply_copper_tubing+return_copper_tubing)/2.)')
data['TiltedBarrelA'].setFormula('tubing', '((supply_copper_tubing+return_copper_tubing)/2.)')
data['TiltedBarrelA'].setFormula('triangle', '(Al_CF_triangle)')
data['TiltedBarrelA'].setFormula('backplate', '(CF_backplate_1)')
# For consistency with Stefan's table
#data['TiltedBarrelA'].setFormula('sensor', '((strip_1+strip_2+strip_3+strip_4+strip_5+strip_6+strip_7+strip_9+strip_10+RTD_11_near_center_of_top_long_side_of_module+RTD_12_center_module+RTD_13_near_center_of_bottom_long_side_of_module+RTD_14_near_center_of_bottom_long_side_of_module)/13.)')
data['TiltedBarrelA'].setFormula('sensor', '((strip_1+strip_2+strip_3+strip_4+strip_5+strip_6+strip_7+strip_9+strip_10)/9.)')
data['TiltedBarrelA'].setFormula('module', '(((%s)+(%s))/2.)' % (data['TiltedBarrelA'].getFormula('sensor'), data['TiltedBarrelA'].getFormula('backplate')))
data['TiltedBarrelA'].setFormula('ambient', '((ambient_below_module+ambient_above_module)/2.)')

data['TiltedBarrel2'] = dataInfo('TiltedBarrel2', 'data/TiltedBarrel2_102616_175243.csv', channels.channelsTiltedBarrel2)
data['TiltedBarrel2'].addCondition('0W', 0., 207, 215)
data['TiltedBarrel2'].addCondition('7p7W', 7.56, 237, 245)
data['TiltedBarrel2'].addCondition('15p0W', 15.,276, 285)

data['TiltedBarrel2'].setFormula('coolant', '((supply_copper_tubing+return_copper_tubing)/2.)')
data['TiltedBarrel2'].setFormula('tubing', '((thin_supply_tubing+thin_return_tubing)/2.)')
data['TiltedBarrel2'].setFormula('triangle', '(Al_CF_triangle)')
data['TiltedBarrel2'].setFormula('backplate', '((CF_backplate_1+CF_backplate_2)/2.)')
data['TiltedBarrel2'].setFormula('sensor', '((strip_1+strip_2+strip_3+strip_4+strip_5+strip_6+strip_7+strip_9+strip_10+RTD_11_near_center_of_top_long_side_of_module+RTD_12_center_module+RTD_13_near_center_of_bottom_long_side_of_module+RTD_14_near_center_of_bottom_long_side_of_module)/13.)')
data['TiltedBarrel2'].setFormula('module', '(((%s)+(%s))/2.)' % (data['TiltedBarrel2'].getFormula('sensor'), data['TiltedBarrel2'].getFormula('backplate')))
data['TiltedBarrel2'].setFormula('ambient', '((ambient_above_module+ambient_below_module)/2.)')

data['TiltedBarrel3'] = dataInfo('TiltedBarrel3', 'data/TiltedBarrel3_20161027_175304.csv', channels.channelsTiltedBarrel3)
data['TiltedBarrel3'].addCondition('0W', 0., 76, 78)
data['TiltedBarrel3'].addCondition('7p7W', 7.56, 38, 40)
data['TiltedBarrel3'].addCondition('15p0W', 15., 54, 56)

data['TiltedBarrel3'].setFormula('coolant', '((supply_copper_tubing+return_copper_tubing)/2.)')
data['TiltedBarrel3'].setFormula('tubing', '((thin_supply_tubing+thin_return_tubing)/2.)')
data['TiltedBarrel3'].setFormula('triangle', '(Al_CF_triangle)')
data['TiltedBarrel3'].setFormula('backplate', '((CF_backplate_1+CF_backplate_2)/2.)')
data['TiltedBarrel3'].setFormula('sensor', '((strip_1+strip_2+strip_3+strip_4+strip_5+strip_6+strip_7+strip_9+strip_10+RTD_11_near_center_of_top_long_side_of_module+RTD_12_center_module+RTD_13_near_center_of_bottom_long_side_of_module+RTD_14_near_center_of_bottom_long_side_of_module)/13.)')
data['TiltedBarrel3'].setFormula('module', '(((%s)+(%s))/2.)' % (data['TiltedBarrel3'].getFormula('sensor'), data['TiltedBarrel3'].getFormula('backplate')))
data['TiltedBarrel3'].setFormula('ambient', '((ambient_above_module+ambient_below_module)/2.)')

data['TiltedBarrel3liq'] = dataInfo('TiltedBarrel3liq', 'data/TiltedBarrel3_20161027_175304.csv', channels.channelsTiltedBarrel3)
data['TiltedBarrel3liq'].addCondition('0W', 0., 96, 98)
data['TiltedBarrel3liq'].addCondition('7p7W', 7.56, 112, 114)

data['TiltedBarrel3liq'].setFormula('coolant', '((supply_copper_tubing+return_copper_tubing)/2.)')
data['TiltedBarrel3liq'].setFormula('tubing', '((thin_supply_tubing+thin_return_tubing)/2.)')
data['TiltedBarrel3liq'].setFormula('triangle', '(Al_CF_triangle)')
data['TiltedBarrel3liq'].setFormula('backplate', '((CF_backplate_1+CF_backplate_2)/2.)')
data['TiltedBarrel3liq'].setFormula('sensor', '((strip_1+strip_2+strip_3+strip_4+strip_5+strip_6+strip_7+strip_9+strip_10+RTD_11_near_center_of_top_long_side_of_module+RTD_12_center_module+RTD_13_near_center_of_bottom_long_side_of_module+RTD_14_near_center_of_bottom_long_side_of_module)/13.)')
data['TiltedBarrel3liq'].setFormula('module', '(((%s)+(%s))/2.)' % (data['TiltedBarrel3liq'].getFormula('sensor'), data['TiltedBarrel3liq'].getFormula('backplate')))
data['TiltedBarrel3liq'].setFormula('ambient', '((ambient_above_module+ambient_below_module)/2.)')



                               

