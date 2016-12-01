import ROOT

def CMS_label(text="Preliminary 2012", sqrts=8, pad=None):
    """ Add a 'CMS Preliminary' style label to the current Pad.

    The blurbs are drawn in the top margin.  The label "CMS " + text is drawn
    in the upper left.  If sqrts is None, it will be omitted.  Otherwise, it
    will be drawn in the upper right.
    """
    if pad is None:
        pad = ROOT.gPad.func()
        pad.cd()
        left_margin = pad.GetLeftMargin()
        top_margin = pad.GetTopMargin()
        ypos = 1 - top_margin / 2.
        l = ROOT.TLatex(left_margin, ypos, "CMS " + text)
        l.SetTextAlign(12) # left-middle
        l.SetNDC()
        # The text is 90% as tall as the margin it lives in.
        l.SetTextSize(0.90 * top_margin)
        l.Draw()
        # Draw sqrt(s) label, if desired
        if sqrts:
            right_margin = pad.GetRightMargin()
            p = ROOT.TLatex(1 - right_margin, ypos,
                            "#sqrt{{s}}={0:d}TeV".format(sqrts))
            p.SetTextAlign(32) # right-middle
            p.SetNDC()
            p.SetTextSize(0.90 * top_margin)
            p.Draw()
        else:
            p = None
        pad.Modified()
        pad.Update()
    return l, p
