#!/bin/env python

import dataClasses
import ROOT
import style
import labels

def drawModules(condition, outputName):

    ROOT.gStyle.SetOptStat(0000000)
    ROOT.gStyle.SetLabelColor(1, "XYZ")
    ROOT.gStyle.SetLabelFont(42, "XYZ")
    ROOT.gStyle.SetLabelOffset(0.007, "XYZ")
    ROOT.gStyle.SetLabelSize(0.04, "XYZ")
    
    canvas = ROOT.TCanvas('canvas', 'canvas', 1000, 400)
    canvas.Divide(2,1)

    thermal_back  = ROOT.TH2Poly('Thermal_Back','Backplane',-40, 135, -22, 68)
    thermal_front = ROOT.TH2Poly('Thermal_Front','Strip sensors',-40, 135, -22, 68)

    sensor_gr  = ROOT.TGraph('drawings/module.dat')
    sensor_bin = thermal_front.AddBin(sensor_gr)
    
    backplate_gr  = ROOT.TGraph('drawings/module.dat')
    backplate_bin = thermal_back.AddBin(backplate_gr)
    
    coolant_supply_gr  = ROOT.TGraph('drawings/coolant_supply.dat')
    coolant_supply_bin = thermal_back.AddBin(coolant_supply_gr)

    coolant_return_gr  = ROOT.TGraph('drawings/coolant_return.dat')
    coolant_return_bin = thermal_back.AddBin(coolant_return_gr)

    tubing_gr = ROOT.TGraph('drawings/tubing.dat')
    tubing_bin = thermal_back.AddBin(tubing_gr)

    triangle_gr = ROOT.TGraph('drawings/triangle.dat')
    triangle_bin = thermal_back.AddBin(triangle_gr)
    
    thermal_back.SetBinContent(backplate_bin, condition.getVal('backplate')[0])
    thermal_back.SetBinContent(coolant_supply_bin, condition.getVal('coolant')[0])
    thermal_back.SetBinContent(coolant_return_bin, condition.getVal('coolant')[0])
    thermal_back.SetBinContent(tubing_bin, condition.getVal('tubing')[0])
    thermal_back.SetBinContent(triangle_bin, condition.getVal('triangle')[0])

    thermal_front.SetBinContent(sensor_bin, condition.getVal('sensor')[0])
#    thermal_front.SetBinContent(coolant_supply2_bin, condition.getVal('sensor')[0])
#    thermal_front.SetBinContent(coolant_return2_bin, condition.getVal('sensor')[0])

    dx = 10.
    ds = (100.-9*dx)/10.
    dy = 15.
    Si_sensor_bin = []
    for i in xrange(9):
        Si_sensor_bin.append(thermal_front.AddBin(ds+(dx+ds)*i, 23-dy/2.,  ds+(dx+ds)*i+dx/2., 23+dy/2.))
    for i,j in enumerate(Si_sensor_bin):
        if i > 6: i=i+2
        else : i=i+1
        thermal_front.SetBinContent(j, condition.getVal('strip_%d' % i)[0])
        
#    thermal_back.GetZaxis().SetRangeUser(-20.,0.)
#    thermal_front.GetZaxis().SetRangeUser(-20.,0.)

    latex = ROOT.TLatex()
    latex.SetTextAlign(22)
    latex.SetTextSize(latex.GetTextSize()*0.75)
    latex.SetNDC(1)
    latex.SetTextAngle(90)
    
    
    canvas.cd(1)
    thermal_back.Draw('COLZ L');
    
    canvas.cd(2)
    thermal_front.Draw('COLZ L');
    latex.DrawLatex(0.15, 0.5, 'GBT side')
    latex.DrawLatex(0.85, 0.5, 'DC-DC side')
    canvas.Print(outputName)
    

def drawEvolution(gr, outputName):
    
    style.setTDRStyle()

    line = ROOT.TLine()
    line.SetLineStyle(ROOT.kDashed)
    line.SetLineWidth(1)
    line.SetLineColor(ROOT.kRed)

    latex = ROOT.TLatex()
    latex.SetTextAlign(22)
    latex.SetTextSize(latex.GetTextSize()*0.50)
    
    canvas = ROOT.TCanvas()
    gr.Draw('ALP')

    for i in xrange(4):
        line.DrawLine(i+1, gr.GetYaxis().GetXmin(), i+1, gr.GetYaxis().GetXmax())

    latex.DrawLatex(0.6, gr.GetYaxis().GetXmin() + 0.85*(gr.GetYaxis().GetXmax()-gr.GetYaxis().GetXmin()), 'Coolant')
    latex.DrawLatex(1.5, gr.GetYaxis().GetXmin() + 0.85*(gr.GetYaxis().GetXmax()-gr.GetYaxis().GetXmin()), 'Tubing')
    latex.DrawLatex(2.5, gr.GetYaxis().GetXmin() + 0.85*(gr.GetYaxis().GetXmax()-gr.GetYaxis().GetXmin()), 'Triangle')
    latex.DrawLatex(3.5, gr.GetYaxis().GetXmin() + 0.85*(gr.GetYaxis().GetXmax()-gr.GetYaxis().GetXmin()), 'CF backplate')
    latex.DrawLatex(4.5, gr.GetYaxis().GetXmin() + 0.85*(gr.GetYaxis().GetXmax()-gr.GetYaxis().GetXmin()), 'Strip sensor')

#    labels.CMS_label('Preliminary', None)

    canvas.Print(outputName)
    return gr
    

def mergeEvolutionGraphs(data, condtitle, outputName):
    
    style.setTDRStyle()
    
    mg = ROOT.TMultiGraph()
    leg = ROOT.TLegend(0.20, 0.35, 0.45, 0.60)
    color = [ROOT.kBlue, ROOT.kRed, ROOT.kGreen+3, ROOT.kMagenta]
    i = 0
    for datum in data.itervalues():
        for condition in datum:
            if condition.title == condtitle:
                uncorrGraph = condition.getUncorrEvolution()
                corrGraph   = condition.getCorrEvolution()
                
                uncorrGraph.SetMarkerColor(color[i])
                uncorrGraph.SetMarkerSize(0)
                uncorrGraph.SetLineColor(color[i])
                uncorrGraph.SetLineStyle(ROOT.kDashed)
                mg.Add(uncorrGraph)
                corrGraph.SetMarkerColor(color[i])
                corrGraph.SetLineColor(color[i])
                mg.Add(corrGraph)
                leg.AddEntry(corrGraph, datum.title, 'LP')
                i = i+1
                
    leg.SetBorderSize(0)
    leg.SetFillColor(0)
        
    mg.Draw('ALP')
    mg.GetXaxis().SetRangeUser(0, 5)
    mg.GetXaxis().SetNdivisions(5)
    mg.GetYaxis().SetTitle('#Delta T (K)')
    mg.SetTitle('')
    
    line = ROOT.TLine()
    line.SetLineStyle(ROOT.kDashed)
    line.SetLineWidth(1)
    line.SetLineColor(ROOT.kRed)

    latex = ROOT.TLatex()
    latex.SetTextAlign(22)
    latex.SetTextSize(latex.GetTextSize()*0.50)

    latex2 = ROOT.TLatex()
    latex2.SetTextSize(latex2.GetTextSize()*0.75)
    latex2.SetNDC(1)
    
    canvas = ROOT.TCanvas()
    mg.Draw('ALP')

    for i in xrange(4):
        line.DrawLine(i+1, mg.GetYaxis().GetXmin(), i+1, mg.GetYaxis().GetXmax())

    latex.DrawLatex(0.6, mg.GetYaxis().GetXmin() + 0.85*(mg.GetYaxis().GetXmax()-mg.GetYaxis().GetXmin()), 'Coolant')
    latex.DrawLatex(1.5, mg.GetYaxis().GetXmin() + 0.85*(mg.GetYaxis().GetXmax()-mg.GetYaxis().GetXmin()), 'Tubing')
    latex.DrawLatex(2.5, mg.GetYaxis().GetXmin() + 0.85*(mg.GetYaxis().GetXmax()-mg.GetYaxis().GetXmin()), 'Triangle')
    latex.DrawLatex(3.5, mg.GetYaxis().GetXmin() + 0.85*(mg.GetYaxis().GetXmax()-mg.GetYaxis().GetXmin()), 'CF backplate')
    latex.DrawLatex(4.5, mg.GetYaxis().GetXmin() + 0.85*(mg.GetYaxis().GetXmax()-mg.GetYaxis().GetXmin()), 'Strip sensor')

    latex2.DrawLatex(0.6, 0.15, 'Power injected: %s' % condtitle.replace('p', '.'))
    leg.Draw()
#    labels.CMS_label('Preliminary', None)
    
    canvas.Print(outputName)
