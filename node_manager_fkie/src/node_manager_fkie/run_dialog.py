# Software License Agreement (BSD License)
#
# Copyright (c) 2012, Fraunhofer FKIE/US, Alexander Tiderko
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of Fraunhofer nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from PySide import QtGui
from PySide import QtCore

import os

import node_manager_fkie as nm
from detailed_msg_box import WarningMessageBox


class RunDialog(QtGui.QDialog):
  '''
  A dialog to run a ROS node without configuration
  '''

  def __init__(self, host, parent=None):
    QtGui.QDialog.__init__(self, parent)
    self.host = host
    self.setWindowTitle('Run')
    self.verticalLayout = QtGui.QVBoxLayout(self)
    self.verticalLayout.setObjectName("verticalLayout")

    self.content = QtGui.QWidget()
    self.contentLayout = QtGui.QFormLayout(self.content)
    self.contentLayout.setVerticalSpacing(0)
    self.verticalLayout.addWidget(self.content)

    # fill the input fields
    self.root_paths = [os.path.normpath(p) for p in os.getenv("ROS_PACKAGE_PATH").split(':')]
    self.packages = {}
    for p in self.root_paths:
      ret = self._getPackages(p)
      self.packages = dict(ret.items() + self.packages.items())

    package_label = QtGui.QLabel("Package:", self.content)
    self.package_field = QtGui.QComboBox(self.content)
    self.package_field.setInsertPolicy(QtGui.QComboBox.InsertAlphabetically)
    self.package_field.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed))
    self.package_field.setEditable(True)
    self.contentLayout.addRow(package_label, self.package_field)
    binary_label = QtGui.QLabel("Binary:", self.content)
    self.binary_field = QtGui.QComboBox(self.content)
#    self.binary_field.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
    self.binary_field.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed))
    self.binary_field.setEditable(True)
    self.contentLayout.addRow(binary_label, self.binary_field)
    ns_name_label = QtGui.QLabel("NS/Name:", self.content)
    self.ns_field = QtGui.QComboBox(self.content)
    self.ns_field.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed))
    self.ns_field.setEditable(True)
    ns_history = nm.history().cachedParamValues('run_dialog/NS')
    ns_history.insert(0, '/')
    self.ns_field.addItems(ns_history)
    self.name_field = QtGui.QLineEdit(self.content)
    self.name_field.setEnabled(False)
    horizontalLayout = QtGui.QHBoxLayout()
    horizontalLayout.addWidget(self.ns_field)
    horizontalLayout.addWidget(self.name_field)
    self.contentLayout.addRow(ns_name_label, horizontalLayout)
    args_label = QtGui.QLabel("Args:", self.content)
    self.args_field = QtGui.QComboBox(self.content)
    self.args_field.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToMinimumContentsLength)
#    self.args_field.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed))
    self.args_field.setEditable(True)
    self.contentLayout.addRow(args_label, self.args_field)
    args_history = nm.history().cachedParamValues('run_dialog/Args')
    args_history.insert(0, '')
    self.args_field.addItems(args_history)
    
    host_label = QtGui.QLabel("Host:", self.content)
    self.host_field = QtGui.QComboBox(self.content)
#    self.host_field.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
    self.host_field.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed))
    self.host_field.setEditable(True)
    host_label.setBuddy(self.host_field)
    self.contentLayout.addRow(host_label, self.host_field)
    self.host_history = host_history = nm.history().cachedParamValues('/Host')
    if self.host in host_history:
      host_history.remove(self.host)
    host_history.insert(0, self.host)
    self.host_field.addItems(host_history)

    master_label = QtGui.QLabel("ROS Master URI:", self.content)
    self.master_field = QtGui.QComboBox(self.content)
    self.master_field.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed))
    self.master_field.setEditable(True)
    master_label.setBuddy(self.host_field)
    self.contentLayout.addRow(master_label, self.master_field)
    self.master_history = master_history = nm.history().cachedParamValues('/Optional Parameter/ROS Master URI')
    self.masteruri = "ROS_MASTER_URI"
    if self.masteruri in master_history:
      master_history.remove(self.masteruri)
    master_history.insert(0, self.masteruri)
    self.master_field.addItems(master_history)
    
    self.buttonBox = QtGui.QDialogButtonBox(self)
    self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok|QtGui.QDialogButtonBox.Cancel)
    self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
    self.buttonBox.setObjectName("buttonBox")
    self.verticalLayout.addWidget(self.buttonBox)
    
    QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), self.accept)
    QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), self.reject)
    QtCore.QMetaObject.connectSlotsByName(self)
    self.package_field.activated[str].connect(self.on_package_selected)
    self.package_field.textChanged.connect(self.on_package_selected)
    self.binary_field.activated[str].connect(self.on_binary_selected)
    
    self.package_field.setFocus(QtCore.Qt.TabFocusReason)
    self.package = ''
    self.binary = ''

    packages = self.packages.keys()
    packages.sort()
    self.package_field.addItems(packages)
    if packages:
      self.on_package_selected(packages[0])
    
  def runSelected(self):
    '''
    Runs the selected node, or do nothing. 
    '''
    self.binary = self.binary_field.currentText()
    self.host = self.host_field.currentText() if self.host_field.currentText() else self.host
    self.masteruri = self.master_field.currentText() if self.master_field.currentText() else self.masteruri
    if not self.host in self.host_history and self.host != 'localhost' and self.host != '127.0.0.1':
      nm.history().add2HostHistory(self.host)
    ns = self.ns_field.currentText()
    if ns and ns != '/':
      nm.history().addParamCache('run_dialog/NS', ns)
    args = self.args_field.currentText()
    if args:
      nm.history().addParamCache('run_dialog/Args', args)
    if self.package and self.binary:
      nm.history().addParamCache('/Host', self.host)
      try:
        nm.starter().runNodeWithoutConfig(self.host, self.package, self.binary, str(self.name_field.text()), str(''.join(['__ns:=', ns, ' ', args])).split(' '), None if self.masteruri == 'ROS_MASTER_URI' else self.masteruri)
      except Exception as e:
        WarningMessageBox(QtGui.QMessageBox.Warning, "Run node", 
                          ''.join(['Run node ', str(self.binary), '[', str(self.package), '] failed!']),
                          str(e)).exec_()

  def _getPackages(self, path):
    result = {}
    if os.path.isdir(path):
      fileList = os.listdir(path)
      if 'manifest.xml' in fileList:
        return {os.path.basename(path) : path}
      for f in fileList:
        ret = self._getPackages(os.path.sep.join([path, f]))
        result = dict(ret.items() + result.items())
    return result

  def _getBinaries(self, path):
    result = {}
    if os.path.isdir(path):
      fileList = os.listdir(path)
      for f in fileList:
        if f and f[0] != '.' and not f in ['build'] and not f.endswith('.cfg') and not f.endswith('.so'):
          ret = self._getBinaries(os.path.sep.join([path, f]))
          result = dict(ret.items() + result.items())
    elif os.path.isfile(path) and os.access(path, os.X_OK):
      # create a selection for binaries
      return {os.path.basename(path) : path}
    return result

  def on_package_selected(self, package):
    self.binary_field.clear()
    if self.packages.has_key(package):
      self.binary_field.setEnabled(True)
      self.args_field.setEnabled(True)
      self.ns_field.setEnabled(True)
      self.name_field.setEnabled(True)
      path = self.packages[package]
      binaries = self._getBinaries(path).keys()
      binaries.sort()
      self.binary_field.addItems(binaries)
      self.package = package
      root, ext = os.path.splitext(os.path.basename(self.binary_field.currentText()))
      self.name_field.setText(root)

  def on_binary_selected(self, binary):
    root, ext = os.path.splitext(os.path.basename(binary))
    self.name_field.setText(root)
