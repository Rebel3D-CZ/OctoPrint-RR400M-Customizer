class LCDTFT:
  def printStart(self, printer):
    printer.commands("M118 A1 P2 action:print_start")
    return

  def printEnd(self, printer):
    printer.commands("M118 A1 P2 action:print_end")
    return

  def printPause(self, printer):
    printer.commands("M118 A1 P2 action:pause")
    return

  def printResume(self, printer):
    printer.commands("M118 A1 P2 action:resume")
    return

  def updateProgress(self, printer, progressPerc):
    printer.commands("M118 A1 P0 action:notification Data Left {}/100".format(progressPerc))
    return

  def notify(self, printer, message):
    printer.commands("M118 A1 P2 action:notification %s" % (message))
    return
