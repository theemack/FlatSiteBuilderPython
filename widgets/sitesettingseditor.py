#############################################################################
# Copyright (C) 2019 Olaf Japp
#
# This file is part of FlatSiteBuilder.
#
#  FlatSiteBuilder is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  FlatSiteBuilder is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with FlatSiteBuilder.  If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################

import os
from widgets.undoableeditor import UndoableEditor
from widgets.plugins import Plugins
from widgets.generator import Generator
from PySide2.QtWidgets import QLineEdit, QComboBox, QVBoxLayout, QLabel

class SiteSettingsEditor(UndoableEditor):
    def __init__(self, win, site):
        UndoableEditor.__init__(self)
        self.win = win
        self.site = site
        self.title = QLineEdit()
        self.titleLabel.setText("Site Settings")
        self.filename = site.source_path + "/" + site.filename
        self.description = QLineEdit()
        self.copyright = QLineEdit()
        self.keywords = QLineEdit()
        self.author = QLineEdit()
        self.copyright.setPlaceholderText("&copy 2019 Artanidos")
        self.publisher = QComboBox()

        for key in Plugins.publishPluginNames():
            pi = Plugins.getPublishPlugin(key)
            if pi:
                self.publisher.addItem(pi.displayName(), key)
        

        vbox = QVBoxLayout()
        vbox.addStretch()

        self.layout.addWidget(QLabel("Title"), 1, 0)
        self.layout.addWidget(self.title, 2, 0)
        self.layout.addWidget(QLabel("Description"), 3, 0)
        self.layout.addWidget(self.description, 4, 0, 1, 3)
        self.layout.addWidget(QLabel("Copyright"), 5, 0)
        self.layout.addWidget(self.copyright, 6, 0, 1, 3)
        self.layout.addWidget(QLabel("Keywords"), 7, 0)
        self.layout.addWidget(self.keywords, 8, 0, 1, 3)
        self.layout.addWidget(QLabel("Author"), 9, 0)
        self.layout.addWidget(self.author, 10, 0)
        self.layout.addWidget(QLabel("Plugin to be used for publishing"), 11, 0)
        self.layout.addWidget(self.publisher, 12, 0)
        self.layout.addLayout(vbox, 13, 0)

        self.load()

        self.title.editingFinished.connect(self.titleChanged)
        self.description.editingFinished.connect(self.descriptionChanged)
        self.copyright.editingFinished.connect(self.copyrightChanged)
        self.keywords.editingFinished.connect(self.keywordsChanged)
        self.author.editingFinished.connect(self.authorChanged)
        self.publisher.currentIndexChanged.connect(self.publisherChanged)

    def load(self):
        oldTitle = self.site.title
        self.site.load()
        self.title.setText(self.site.title)
        self.description.setText(self.site.description)
        self.copyright.setText(self.site.copyright)
        self.keywords.setText(self.site.keywords)
        self.author.setText(self.site.author)
        index = self.publisher.findData(self.site.publisher)
        self.publisher.setCurrentIndex(index)
        if oldTitle != self.site.title:
            os.rename(Generator.sitesPath() + "/" + oldTitle, Generator.sitesPath() + "/" + self.site.title)
            print("renaming1: " + Generator.sitesPath() + "/" + oldTitle)
            self.win.statusBar().showMessage("Site settings have been loaded. Site should be rebuilded. Output path has been renamed to " + self.site.title())

    def save(self):
        if self.site.title != self.title.text():
            oldTitle = self.site.title
            self.site.title = self.title.text()
            self.site.save()
            os.rename(Generator.sitesPath() + "/" + oldTitle, Generator.sitesPath() + "/" + self.site.title)
            print("renaming2: " + Generator.sitesPath() + "/" + oldTitle)
            self.win.statusBar().showMessage("Site settings have been saved. Site should be rebuilded. Output path has been renamed to " + self.title.text())
        else:
            self.site.setAuthor(self.author.text())
            self.site.setCopyright(self.copyright.text())
            self.site.setDescription(self.description.text())
            self.site.setKeywords(self.keywords.text())
            #self.site.setPublisher(self.publisher.currentData().toString())
            self.site.save()
            self.win.statusBar().showMessage("Site settings have been saved. Site should be rebuilded on the dashboard.")

    def publisherChanged(self, publisher):
        if self.site.publisher != publisher:
            self.contentChanged("publisher changed")
    
    def titleChanged(self):
        if self.site.title != self.title.text():
            self.contentChanged("title changed")
    
    def authorChanged(self):
        if self.site.author != self.author.text():
            self.contentChanged("author changed")
    
    def descriptionChanged(self):
        if self.site.description != self.description.text():
            self.contentChanged("description changed")
    
    def copyrightChanged(self):
        if self.site.copyright != self.copyright.text():
            self.contentChanged("copyright changed")
    
    def keywordsChanged(self):
        if self.site.keywords != self.keywords.text():
            self.contentChanged("keywords changed")
    