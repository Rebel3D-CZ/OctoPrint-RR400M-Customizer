class RDSC(LCDNull):
  def notify(self, printer, message):
    printer.commands("M117 %s" % (message))
    return
