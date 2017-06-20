import os
import unittest
import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *
import logging

#
# mod
#

class mod(ScriptedLoadableModule):
  """Uses ScriptedLoadableModule base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = "mod" # TODO make this more human readable by adding spaces
    self.parent.categories = ["Examples"]
    self.parent.dependencies = []
    self.parent.contributors = ["John Doe"] # replace with "Firstname Lastname (Organization)"
    self.parent.helpText = """
    This is an example of scripted loadable module bundled in an extension.
    It performs a simple thresholding on the input volume and optionally captures a screenshot.
    """
    self.parent.acknowledgementText = """
    This file was originally developed by Jean-Christophe Fillion-Robin, Kitware Inc.
    and Steve Pieper, Isomics, Inc. and was partially funded by NIH grant 3P41RR013218-12S1.
""" # replace with organization, grant and thanks.

#
# modWidget
#

class modWidget(ScriptedLoadableModuleWidget):

  def setup(self):
    ScriptedLoadableModuleWidget.setup(self)

    #
    # Parameters 
    #
  
    modelSelector = ctk.ctkCollapsibleButton()
    modelSelector.text = "Models Selector"
    self.layout.addWidget(modelSelector)

    # Layout within the dummy collapsible button
	
    modelsFormLayout = qt.QFormLayout(modelSelector)

	# Input model
   
    self.modelsSelector = slicer.qMRMLNodeComboBox()
    self.modelsSelector.nodeTypes = ["vtkMRMLModelNode"]
    self.modelsSelector.selectNodeUponCreation = True
    self.modelsSelector.addEnabled = False
    self.modelsSelector.removeEnabled = True
    self.modelsSelector.noneEnabled = True
    self.modelsSelector.showHidden = False
    self.modelsSelector.showChildNodeTypes = False
    self.modelsSelector.setMRMLScene( slicer.mrmlScene )
    self.modelsSelector.setToolTip( "Input model selection" )
    modelsFormLayout.addRow("Input model: ", self.modelsSelector)

	# Opacity
    
    self.opacitySlider = ctk.ctkSliderWidget()
    self.opacitySlider.singleStep = 1
    self.opacitySlider.minimum = 0
    self.opacitySlider.maximum = 100
    self.opacitySlider.value = 50
    self.opacitySlider.setToolTip("Opacity selection")
    modelsFormLayout.addRow("Set opacity:", self.opacitySlider)	

	# Show / Hide

    self.showHideButton = qt.QPushButton("Show / Hide")
    self.showHideButton.toolTip = "Show or hide the model"
    self.showHideButton.enabled = True
    modelsFormLayout.addRow(self.showHideButton)
    
	# Add vertical spacer
    self.layout.addStretch(5)
	
	
	
	
	#
    # connections
	#
	
    self.showHideButton.connect('clicked(bool)', self.onShowHideButton)
    self.opacitySlider.connect('valueChanged(double)', self.onSliderValueChanged)


	# Definitions 
	
  def cleanup(self):
  
    pass


  def onShowHideButton(self):
  
    logic = modLogic()
    logic.showModel(self.modelsSelector.currentNode())

  def onSliderValueChanged(self):
  
    logic = modLogic()
    opacityValue = self.opacitySlider.value
    logic.changeOpacity(self.modelsSelector.currentNode(), opacityValue)
  
  

#
# modLogic
#

class modLogic(ScriptedLoadableModuleLogic):


  def isValidModelData(self, modelNode):
    """Validates if the model is empty
      """
    if not modelNode:
      logging.debug('isValidAllData failed: no model node defined')
      return False
    return True

  def changeOpacity(self, model, opacityVal):
    if not self.isValidModelData( model):
      slicer.util.errorDisplay('Please set proper input model')
      return False
    n = model.GetDisplayNode()
    n.SetOpacity(opacityVal/100)
    return True

  def showModel(self, model):
    if not self.isValidModelData( model):
      slicer.util.errorDisplay('Please set proper input model')
      return False
    node = model.GetDisplayNode()
    visibility = node.GetVisibility()
    if (visibility==0):
      node.SetVisibility(1)
    else:
      node.SetVisibility(0)


class modTest(ScriptedLoadableModuleTest):
  """
  This is the test case for your scripted module.
  Uses ScriptedLoadableModuleTest base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setUp(self):
    """ Do whatever is needed to reset the state - typically a scene clear will be enough.
    """
    slicer.mrmlScene.Clear(0)

  def runTest(self):
    """Run as few or as many tests as needed here.
    """
    self.setUp()
    self.test_mod1()

  def test_mod1(self):
    """ Ideally you should have several levels of tests.  At the lowest level
    tests should exercise the functionality of the logic with different inputs
    (both valid and invalid).  At higher levels your tests should emulate the
    way the user would interact with your code and confirm that it still works
    the way you intended.
    One of the most important features of the tests is that it should alert other
    developers when their changes will have an impact on the behavior of your
    module.  For example, if a developer removes a feature that you depend on,
    your test should break so they know that the feature is needed.
    """

    