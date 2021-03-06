from Orange.widgets import widget, settings, gui

from Orange.data import Table
from Orange.regression.mean import MeanLearner, MeanModel
from Orange.widgets.utils.owlearnerwidget import OWProvidesLearner


class OWMean(OWProvidesLearner, widget.OWWidget):
    name = "Mean Learner"
    description = "Regression to the average class value from the training set."
    icon = "icons/Mean.svg"

    LEARNER = MeanLearner

    inputs = [("Data", Table, "set_data")] + OWProvidesLearner.inputs
    outputs = [("Learner", LEARNER),
               ("Predictor", MeanModel)]

    learner_name = settings.Setting("Mean Learner")

    want_main_area = False
    resizing_enabled = False

    def __init__(self):
        super().__init__()

        self.data = None
        self.preprocessors = None

        box = gui.widgetBox(self.controlArea, "Learner Name")
        gui.lineEdit(box, self, "learner_name")
        gui.button(self.controlArea, self, "Apply",
                   callback=self.apply, default=True)
        self.controlArea.layout().addWidget(self.report_button)
        self.apply()

    def set_data(self, data):
        self.data = data
        if data is not None:
            self.apply()

    def apply(self):
        learner = self.LEARNER(preprocessors=self.preprocessors)
        learner.name = self.learner_name
        predictor = None
        if self.data is not None:
            self.error(0)
            if not learner.check_learner_adequacy(self.data.domain):
                self.error(0, learner.learner_adequacy_err_msg)
            else:
                predictor = learner(self.data)
                predictor.name = learner.name

        self.send("Learner", learner)
        self.send("Predictor", predictor)

    def send_report(self):
        self.report_items((("Name", self.learner_name),))


if __name__ == "__main__":
    import sys
    from PyQt4.QtGui import QApplication

    a = QApplication(sys.argv)
    ow = OWMean()
    d = Table('housing')
    ow.set_data(d)
    ow.show()
    a.exec_()
    ow.saveSettings()
