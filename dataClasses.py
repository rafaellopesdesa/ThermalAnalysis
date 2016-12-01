import ROOT

class tempMeasurements:

    def __init__(self):
        self.coolant     = ''
        self.tubing      = ''
        self.triangle    = ''
        self.backplate   = ''
        self.sensor      = ''
        self.module      = ''
        self.ambient     = ''
        
class conditionInfo:

    def __init__(self, _title, _power, _firstLine, _lastLine, _comment = ''):
        self.title     = _title
        self.power     = _power
        self.firstLine = _firstLine
        self.lastLine  = _lastLine
        self.comment   = ''

        self.vals = {'coolant': [],
                     'tubing': [],
                     'triangle': [],
                     'backplate': [],
                     'sensor': [],
                     'module': [],
                     'ambient': []}

        self.uncorrEvolution = ROOT.TGraphErrors(5)
        self.corrEvolution = ROOT.TGraphErrors(5)
        self.powerToCoolant = 0.
        self.powerToAmbient = 0.
        
    def __iter__(self):
        return iter(self.vals)

    def getTitle(self):
        return self.title
    
    def setVal(self, measurement, val):
        self.vals[measurement] = val

    def getVal(self, measurement):
        return self.vals[measurement]

    def setUncorrEvolution(self, gr):
        self.uncorrEvolution = gr

    def setCorrEvolution(self, gr):
        self.corrEvolution = gr

    def getUncorrEvolution(self):
        return self.uncorrEvolution

    def getCorrEvolution(self):
        return self.corrEvolution

    def setPowerToCoolant(self, val):
        self.powerToCoolant = val

    def setPowerToAmbient(self, val):
        self.powerToAmbient = val
        
    def getPowerToCoolant(self):
        return self.powerToCoolant

    def getPowerToAmbient(self):
        return self.powerToAmbient

    def makeEvolution(self):
        
        self.uncorrEvolution.SetPoint(0, 0.5, 0)
        self.uncorrEvolution.SetPointError(0, 0, 0.)
        
        self.uncorrEvolution.SetPoint(1, 1.5, (self.getVal('tubing')[0]-self.getVal('coolant')[0]))
        self.uncorrEvolution.SetPointError(1, 0, ROOT.TMath.Sqrt(self.getVal('tubing')[1]*self.getVal('tubing')[1]+self.getVal('coolant')[1]*self.getVal('coolant')[1]))
        
        self.uncorrEvolution.SetPoint(2, 2.5, (self.getVal('triangle')[0]-self.getVal('coolant')[0]))
        self.uncorrEvolution.SetPointError(2, 0, ROOT.TMath.Sqrt(self.getVal('triangle')[1]*self.getVal('triangle')[1]+self.getVal('coolant')[1]*self.getVal('coolant')[1]))
        
        self.uncorrEvolution.SetPoint(3, 3.5, (self.getVal('backplate')[0]-self.getVal('coolant')[0]))
        self.uncorrEvolution.SetPointError(3, 0, ROOT.TMath.Sqrt(self.getVal('backplate')[1]*self.getVal('backplate')[1]+self.getVal('coolant')[1]*self.getVal('coolant')[1]))
        
        self.uncorrEvolution.SetPoint(4, 4.5, (self.getVal('sensor')[0]-self.getVal('coolant')[0]))
        self.uncorrEvolution.SetPointError(4, 0, ROOT.TMath.Sqrt(self.getVal('sensor')[1]*self.getVal('sensor')[1]+self.getVal('coolant')[1]*self.getVal('coolant')[1]))
        
        self.uncorrEvolution.SetMarkerStyle(20)
        self.uncorrEvolution.SetLineWidth(2)
    
        self.uncorrEvolution.Draw('ALP')
        self.uncorrEvolution.GetXaxis().SetRangeUser(0, 5)
        self.uncorrEvolution.GetXaxis().SetNdivisions(5)
        self.uncorrEvolution.GetYaxis().SetTitle('#Delta T (K)')
        self.uncorrEvolution.SetTitle('')

        return self.uncorrEvolution
        
    def correctEvolution(self):

        corr = 1.0
        if self.powerToCoolant != 0:
            corr = (self.power/self.powerToCoolant)
        
        gr = ROOT.TGraphErrors(5)
        
        self.corrEvolution.SetPoint(0, 0.5, 0)
        self.corrEvolution.SetPointError(0, 0, 0.)
        
        self.corrEvolution.SetPoint(1, 1.5, (self.getVal('tubing')[0]-self.getVal('coolant')[0]))
        self.corrEvolution.SetPointError(1, 0, ROOT.TMath.Sqrt(self.getVal('tubing')[1]*self.getVal('tubing')[1]+self.getVal('coolant')[1]*self.getVal('coolant')[1]))
        
        self.corrEvolution.SetPoint(2, 2.5, (self.getVal('triangle')[0]-self.getVal('coolant')[0]))
        self.corrEvolution.SetPointError(2, 0, ROOT.TMath.Sqrt(self.getVal('triangle')[1]*self.getVal('triangle')[1]+self.getVal('coolant')[1]*self.getVal('coolant')[1]))
        
        self.corrEvolution.SetPoint(3, 3.5, (corr*(self.getVal('backplate')[0]-self.getVal('coolant')[0])))
        self.corrEvolution.SetPointError(3, 0, ROOT.TMath.Sqrt(self.getVal('backplate')[1]*self.getVal('backplate')[1]+self.getVal('coolant')[1]*self.getVal('coolant')[1]))
        
        self.corrEvolution.SetPoint(4, 4.5, (corr*(self.getVal('sensor')[0]-self.getVal('coolant')[0])))
        self.corrEvolution.SetPointError(4, 0, ROOT.TMath.Sqrt(self.getVal('sensor')[1]*self.getVal('sensor')[1]+self.getVal('coolant')[1]*self.getVal('coolant')[1]))
        
        self.corrEvolution.SetMarkerStyle(20)
        self.corrEvolution.SetLineWidth(2)
    
        self.corrEvolution.Draw('ALP')
        self.corrEvolution.GetXaxis().SetRangeUser(0, 5)
        self.corrEvolution.GetXaxis().SetNdivisions(5)
        self.corrEvolution.GetYaxis().SetTitle('#Delta T (K)')
        self.corrEvolution.SetTitle('')

        return self.corrEvolution
            
class dataInfo:

    
    def __init__(self, _title, _csvfile, _channellist):

        self.title               = _title
        self.csvfile             = _csvfile
        self.channellist         = _channellist
        self.conditions          = []
        self.temperatures        = tempMeasurements()
        self.resistanceToCoolant = 0.
        self.resistanceToAmbient = 0.
        
    def addCondition(self, _title, _power, _firstLine, _lastLine, _comment = ''):
        self.conditions.append(conditionInfo(_title, _power, _firstLine, _lastLine, _comment))

    def setFormula(self, measurement, formula):
        setattr(self.temperatures, measurement, formula)
        
    def getFormula(self, measurement):
        return getattr(self.temperatures, measurement)
    
    def __iter__(self):
        return iter(self.conditions)
    
    
