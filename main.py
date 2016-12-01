#!/bin/env python

import ROOT
import numpy
import calculate
import draw

from data import data

def readFile(datum):
    dataTree = ROOT.TTree('dataTree', 'dataTree')
    dataTree.ReadFile(datum.csvfile, datum.channellist,',')
    
    for condition in datum:
        channels = [x.split('/')[0] for x in datum.channellist.strip().split(':')]
        for formula in condition:
            condition.setVal(formula, calculate.calculateAverage(dataTree, datum.getFormula(formula), condition.firstLine, condition.lastLine))
        for channel in channels:
            condition.setVal(channel, calculate.calculateAverage(dataTree, channel, condition.firstLine, condition.lastLine))        
            

if __name__ == '__main__':

    ROOT.gErrorIgnoreLevel = ROOT.kError
    
    uncorrEvolutionPlots = {}
    corrEvolutionPlots = {}
    resistancePlots = {}
    for datum in data.itervalues():
        print datum.title
        readFile(datum)

    for datum in data.itervalues():        
        for condition in datum:
            draw.drawModules(condition, 'figures/module_%s_%s.png' % (datum.title, condition.title))

    for datum in data.itervalues():            
        resistancePlots[datum.title] = calculate.calculateThermalConductivity(datum, 'figures/thermalResistModel_%s_coolant.png' % datum.title, 'figures/thermalResistModel_%s_ambient.png' % datum.title)
        print 'Summary for %s' % datum.title
        print ' Power +   Rmc|Rma   +   Pmc|Pma   +   Tsc|corr  '
        print '-------+-------------+-------------+-------------'
        for condition in datum:
            condition.makeEvolution()
            condition.correctEvolution()
            draw.drawEvolution(condition.getUncorrEvolution(),
                               'figures/deltaT_%s_%s.png' % (datum.title, condition.title))
            draw.drawEvolution(condition.getCorrEvolution(),
                               'figures/corr_deltaT_%s_%s.png' % (datum.title, condition.title))

            if condition.power != 0.:
                print ' %5.2f | %5.2f %5.2f | %5.2f %5.2f | %5.2f %5.2f' % (condition.power,
                                                                            datum.resistanceToCoolant,
                                                                            datum.resistanceToAmbient,
                                                                            condition.powerToCoolant,
                                                                            condition.powerToAmbient,
                                                                            condition.getUncorrEvolution().GetY()[4],
                                                                            condition.getCorrEvolution().GetY()[4])
        print '-------+-------------+-------------+-------------'

    draw.mergeEvolutionGraphs(data, '7p7W', 'figures/delta_temp_7p7W.png')
    draw.mergeEvolutionGraphs(data, '15p0W', 'figures/delta_temp_15p0W.png')
