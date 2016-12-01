#!/bin/env python

import ROOT
import numpy
import array
import style
import labels

histnum = 1

power_vec = []
module_vec = []
ambient_vec = []
coolant_vec = []

def calculateAverage(dataTree, formula, firstEvent, lastEvent):
    global histnum
    histname = 'hist_%d' % histnum
    histnum = histnum+1
    dataTree.Draw('%s >> %s' % (formula, histname), 'Entry$ > %d && Entry$ < %d' %(firstEvent-3, lastEvent-1)) # the -3 comes from the fact that excel starts at 2
    htemp = ROOT.gDirectory.Get(histname)
    mean = htemp.GetMean()
    rms  = htemp.GetMeanError()
    return [mean, rms]

def fcn( npar, gin, f, par, iflag ):

    global power_vec
    global module_vec
    global ambient_vec
    global coolant_vec

    chisq, delta = 0., 0.
    
    for i in xrange(len(power_vec)):
        Tma_vec = module_vec[i] - ambient_vec[i]
        Tmc_vec = module_vec[i] - coolant_vec[i]
        
        delta  = (power_vec[i]-Tma_vec/par[0]-Tmc_vec/par[1])
        chisq += delta*delta
        
    f[0] = chisq
   
def calculateThermalConductivity(datum, outputName1, outputName2):

    style.setTDRStyle()

    global power_vec
    global module_vec
    global ambient_vec
    global coolant_vec

    power_vec   = []
    module_vec  = []
    ambient_vec = []
    coolant_vec = []
    
    for condition in datum:
        power_vec.append(condition.power)
        module_vec.append(condition.getVal('module')[0])
        coolant_vec.append(condition.getVal('coolant')[0])
        ambient_vec.append(condition.getVal('ambient')[0])

    gMinuit = ROOT.TMinuit(2)
    gMinuit.SetPrintLevel(-1)
    gMinuit.SetGraphicsMode(ROOT.kFALSE)
    gMinuit.SetFCN(fcn)

    arglist = array.array( 'd', 10*[0.] )
    ierflg = ROOT.Long()
    
    arglist[0] = 1
    gMinuit.mnexcm( "SET ERR", arglist, 1, ierflg )

    vstart = array.array( 'd', [ 1.0, 1.0 ] )
    step   = array.array( 'd', [ 0.001, 0.001 ] )
    gMinuit.mnparm( 0, "Rmc", vstart[0], step[0], 0, 0, ierflg )
    gMinuit.mnparm( 1, "Rma", vstart[1], step[1], 0, 0, ierflg )
    
    arglist[0] = 500
    arglist[1] = 1.
    gMinuit.mnexcm( "MIGRAD", arglist, 2, ierflg )
        
    par_c, err_c = ROOT.Double(), ROOT.Double()    
    par_a, err_a = ROOT.Double(), ROOT.Double()    
    gMinuit.GetParameter( 0, par_a, err_a )
    gMinuit.GetParameter( 1, par_c, err_c )

    latex = ROOT.TLatex()
    latex.SetTextSize(latex.GetTextSize()*0.75)

    gr_a = ROOT.TGraph()
    gr_a.SetMarkerStyle(20)
    gr_a.SetPoint(0, 0., 0.)

    gr_c = ROOT.TGraph()
    gr_c.SetMarkerStyle(20)
    gr_c.SetPoint(0, 0., 0.)

    idx = 1    
    for p, m, a, c in zip(power_vec[1:], module_vec[1:], ambient_vec[1:], coolant_vec[1:]):
        
        tma = m-a
        tmc = m-c
        
        tma0 = module_vec[0]-ambient_vec[0]
        tmc0 = module_vec[0]-coolant_vec[0]
        p0 = power_vec[0]
        det = tma0*tmc-tmc0*tma

        ra = det/(tmc*p0-tmc0*p)
        rc = det/(-tma*p0+tma0*p)

        pma = tma/ra
        pmc = tmc/rc
        
        gr_a.SetPoint(idx, pma, tma)        
        gr_c.SetPoint(idx, pmc, tmc)
        idx = idx+1

    f_a = ROOT.TF1('f_a', '[0]*x', -100., 100.)
    f_a.SetParameter(0, par_a)

    f_c = ROOT.TF1('f_c', '[0]*x', -100., 100.)
    f_c.SetParameter(0, par_c)

    datum.resistanceToCoolant = par_c
    datum.resistanceToAmbient = par_a
    for condition in datum:
        condition.setPowerToCoolant((condition.getVal('module')[0]-condition.getVal('coolant')[0])/par_c)
        condition.setPowerToAmbient((condition.getVal('module')[0]-condition.getVal('ambient')[0])/par_a)
        
    canvas = ROOT.TCanvas('c1', 'c1', 600, 600)
    canvas.SetGridx()
    canvas.SetGridy()

    relshift = 0.03

    gr_c.Draw('AP')
    shift = relshift*(gr_c.GetXaxis().GetXmax()-gr_c.GetXaxis().GetXmin())
    gr_c.SetTitle(';Power Module #rightarrow Coolant (W); #Delta T_{Module #rightarrow Coolant (K)}')
    f_c.Draw('SAME')
#    latex.DrawLatex(gr_c.GetX()[0]+shift, gr_c.GetY()[0], '(REF)')
    for i, p in enumerate(power_vec[1:]):
        latex.DrawLatex(gr_c.GetX()[i+1]+shift, gr_c.GetY()[i+1], '%.2f W' % p)
    canvas.Print(outputName1)
    
    gr_a.Draw('AP')
    shift = relshift*(gr_a.GetXaxis().GetXmax()-gr_a.GetXaxis().GetXmin())
    gr_a.SetTitle(';Power Module #rightarrow Ambient (W); #Delta T_{Module #rightarrow Ambient (K)}')
    f_a.Draw('SAME')
#    latex.DrawLatex(gr_a.GetX()[0]+shift, gr_a.GetY()[0], '(REF)')
    for i, p in enumerate(power_vec[1:]):
        latex.DrawLatex(gr_a.GetX()[i+1]+shift, gr_a.GetY()[i+1], '%.2f W' % p)

    canvas.Print(outputName2)
    return gr_a, gr_c

