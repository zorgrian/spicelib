#!/usr/bin/python

import sys, os
import ConfigParser
import pygtk
pygtk.require('2.0')
import gtk

from spicelibconf import *
import testlibrary


class SpicelibTestGui:
    def __init__(self, lib_filename):
        self.filename = lib_filename
        self.library = testlibrary.modellibrary(self.filename)
        self.create_gui()
        self.load_models()

    def main(self):
        gtk.main()

    def create_gui(self):
        # create a new window
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)
        self.window.set_border_width(5)

        ## container for all elements
        vbox = gtk.VBox()
        self.window.add(vbox)

        ## upper hbox with devices and buttons
        hbox = gtk.HBox()
        hbox.set_homogeneous(True)
        vbox.pack_start(hbox, True, True, 5)

        ## upper left vbox with devices
        vbox1 = gtk.VBox()
        hbox.pack_start(vbox1, True, True, 5)
        scroll1 = gtk.ScrolledWindow()
        self.window.set_geometry_hints(vbox1, min_width=100)
        vbox1.pack_start(scroll1)

        ## Model text view
        self.model_text = gtk.TextView()
        self.model_text_buffer = gtk.TextBuffer()
        self.model_text_buffer.set_text('Hello World1!')
        self.model_text.set_buffer(self.model_text_buffer)
        scroll2 = gtk.ScrolledWindow()
        hbox.pack_start(scroll2, True, True, 5)
        scroll2.add(self.model_text)
        
        ## upper right vbox with model definition and test buttons
        vbox2 = gtk.VBox()
        hbox.pack_start(vbox2, True, True, 5)
        
        ## treeview for the model list
        self.model_list = gtk.ListStore(str)
        self.model_tree = gtk.TreeView(self.model_list)
        tvcolumn = gtk.TreeViewColumn('Device')
        self.model_tree.append_column(tvcolumn)
        cell = gtk.CellRendererText()
        tvcolumn.pack_start(cell,True)
        tvcolumn.add_attribute(cell, 'text', 0)
        scroll1.add(self.model_tree)
        self.model_tree.connect('cursor-changed', self.callback_select, None)

        ## device definition text view
        self.device_text = gtk.TextView()
        self.device_text_buffer = gtk.TextBuffer()
        self.device_text_buffer.set_text('Hello World2!')
        self.device_text.set_buffer(self.device_text_buffer)
        scroll3 = gtk.ScrolledWindow()
        vbox2.pack_start(scroll3, True, True, 5)
        scroll3.add(self.device_text)

        ## tester buttons
        button_prev = gtk.Button("<<")
        button_prev.connect("clicked", self.callback_move, -1)
        button_next = gtk.Button(">>")
        button_next.connect("clicked", self.callback_move, +1)
        button_test = gtk.Button("test model definition")
        button_test.connect("clicked", self.callback_test, None)
        hbox_test = gtk.HBox()
        hbox_test.pack_start(button_prev, False, False, 0)
        hbox_test.pack_start(button_test, True, True, 0)
        hbox_test.pack_start(button_next, False, False, 0)
        vbox2.pack_start(hbox_test, False, False, 5)


        ## simulator action buttons in a widget table
        self.testwidgets = {}
        table = gtk.Table(5,len(SIMULATORS))
        for n, sim in enumerate(SIMULATORS):
            headline = gtk.Label(sim + ':')
            table.attach(headline,n,n+1,0,1)
            status = gtk.Entry()
            self.testwidgets[(sim,'status')] = status
            table.attach(status,n,n+1,1,2)
            for m,action in enumerate(['good', 'broken','view']):
                button = gtk.Button(action)
                table.attach(button,n,n+1,2+m,3+m)
                button.connect('clicked', self.callback_simulator_action, (sim,action))
        vbox2.pack_start(table, False, False, 5)
        
        ## update checksum button
        hbox2 = gtk.HBox()
        vbox2.pack_start(hbox2, False, False, 5)
        self.entry_checksum = gtk.Entry()
        hbox2.pack_start(self.entry_checksum, True, True, 5)
        button_sign = gtk.Button('sign checksum')
        button_sign.connect("clicked", self.callback_sign, None)
        hbox2.pack_start(button_sign, True, True, 5)

        ## logging window in the bottom
        # TBD

        # The final step is to display this newly created widgets
        self.window.show_all()

    def load_models(self):
        for model in self.library.get_devices():
            self.model_list.append([model])

    def callback_select(self, treeview, data=None):
        path = treeview.get_cursor()[0]
        device = self.model_list[path][0]
        devicetext = self.library.get_devicetext(device)
        self.device_text_buffer.set_text(devicetext)
        modeltext = self.library.get_modeltext(device)
        self.model_text_buffer.set_text(modeltext)
        self.update_teststatus()

    def callback_test(self, widget, data=None):
        path = self.model_tree.get_cursor()[0]
        model = self.model_list[path][0]
        self.library.test_single(model)
        self.update_teststatus()

    def callback_move(self, widget, data):
        path = self.model_tree.get_cursor()[0]
        newnr = path[0] + data
        if newnr >= 0 and newnr < len(self.model_list):
           self.model_tree.set_cursor((newnr,))
        

    def callback_simulator_action(self, widget, data):
        sim, action = data
        path = self.model_tree.get_cursor()[0]
        device = self.model_list[path][0]
        if action == 'broken':
            print sim, action, device
        elif action == 'good':
            print sim, action, device
        elif action == 'view':
            resultfile = os.path.join(self.library.testdir, device,
                                      SIMULATORS[sim]['folder'], 'index.html')
            os.system('firefox '+resultfile)

    def callback_sign(self, widget, data=None):
        path = self.model_tree.get_cursor()[0]
        device = self.model_list[path][0]
        self.library.sign_checksum(device)


    def update_teststatus(self):
        path = self.model_tree.get_cursor()[0]
        device = self.model_list[path][0]
        statusfile = os.path.join(self.library.testdir, device, 'status.cfg')
        if os.path.exists(statusfile):
            status = ConfigParser.RawConfigParser()
            status.read(statusfile)
            for sim in SIMULATORS:
                s = status.get('simulators', sim)
                self.testwidgets[(sim,'status')].set_text(s)
                c = COLORS.get(s,'#777777')
                self.testwidgets[(sim,'status')].modify_base(gtk.STATE_NORMAL,
                                                             gtk.gdk.color_parse(c))
            s = status.get('checksum','checksum')
            self.entry_checksum.set_text('checksum=' + s)
            c = COLORS.get(s,'#777777')
            self.entry_checksum.modify_base(gtk.STATE_NORMAL,
                                            gtk.gdk.color_parse(c))
        else:
            for sim in SIMULATORS:
                self.testwidgets[(sim,'status')].set_text('None')
                self.testwidgets[(sim,'status')].modify_base(gtk.STATE_NORMAL,
                                                             gtk.gdk.color_parse("#FFFFFF"))
            self.entry_checksum.set_text('None')
            self.entry_checksum.modify_base(gtk.STATE_NORMAL,
                                            gtk.gdk.color_parse("#FFFFFF"))

    def out_of_range(self):
        d = gtk.MessageDialog(parent=self.window, flags=gtk.DIALOG_MODAL,
                              type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE,
                              message_format='Point number out of range')

        d.run()
        d.destroy()

    def delete_event(self, widget, event, data=None):
        return False

    def destroy(self, widget, data=None):
        print "destroy signal occurred"
        gtk.main_quit()


if __name__ == "__main__":
    filename = sys.argv[1]
    app = SpicelibTestGui(filename)
    app.main()
