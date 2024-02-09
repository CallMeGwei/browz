# window.py
#
# Copyright 2020 Kavya Gokul
#
# Copyright 2024 Andrew D. Anderson
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import os
import sys

from gi.repository import Gdk, Gio, GLib, Gtk, Pango


class BrowzWindow(Gtk.ApplicationWindow):
    __gtype_name__ = "BrowzWindow"
    browsers = []
    entry = Gtk.Entry()

    def __init__(self, app):
        super().__init__(title="Browz", application=app)

        # Set it to open in center
        self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)

        # Set to not be resizable
        self.set_resizable(False)

        self.connect("key-release-event", self.keyboard_handle, app)

        settings = Gtk.Settings.get_default()
        settings.set_property("gtk-application-prefer-dark-theme", True)

        # Applying the custom css to the app
        style_provider = Gtk.CssProvider()
        style_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "style.css"
        )
        style_provider.load_from_path(style_path)

        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )

        # Create headerbar and add to window as titlebar
        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.set_name("headerbar")
        hb.props.title = ""
        self.set_titlebar(hb)

        Gtk.StyleContext.add_class(hb.get_style_context(), Gtk.STYLE_CLASS_FLAT)

        # Create an entry, put the url argument in the entry, and add to headerbar
        self.entry.set_icon_from_icon_name(Gtk.EntryIconPosition.PRIMARY, "web-browser")
        try:
            self.entry.set_text(sys.argv[1])
        except IndexError:
            print("No url provided")

        self.entry.set_width_chars(35)
        hb.add(self.entry)

        # Create an options button
        options_button = Gtk.MenuButton.new()
        try:
            options_button.add(
                Gtk.Image.new_from_icon_name(
                    "settings-symbolic", Gtk.IconSize.LARGE_TOOLBAR
                )
            )
        except:
            options_button.add(
                Gtk.Image.new_from_icon_name(
                    "preferences-system", Gtk.IconSize.LARGE_TOOLBAR
                )
            )
        hb.pack_end(options_button)

        options_menu = Gtk.Menu.new()
        options_menu.set_name("options_menu")
        options_button.set_popup(options_menu)

        about_menu_item = Gtk.MenuItem.new()
        about_menu_item.set_label("About")
        about_menu_item.connect("activate", app.on_about)
        options_menu.append(about_menu_item)

        # quit_menu_item = Gtk.MenuItem.new()
        # quit_menu_item.set_label("Quit")
        # quit_menu_item.connect("activate", self.quit_app, app)
        # options_menu.append(quit_menu_item)

        options_menu.show_all()

        # outer_box
        outer_box = Gtk.Box()
        outer_box.set_orientation(Gtk.Orientation.VERTICAL)

        self.add(outer_box)

        # create a horizontal box to hold browser buttons
        hbox = Gtk.Box()
        hbox.set_name("mainbox")
        hbox.set_orientation(Gtk.Orientation.HORIZONTAL)
        hbox.set_spacing(10)
        hbox.set_homogeneous(True)

        outer_box.add(hbox)

        # Create an info_bar to help the user set Browz as default
        info_bar = Gtk.InfoBar()
        info_bar.set_message_type(Gtk.MessageType.QUESTION)
        info_bar.set_show_close_button(True)
        info_bar.connect("response", self.on_infobar_response, app)

        info_label = Gtk.Label("Set Browz as your default browser")
        content = info_bar.get_content_area()
        content.add(info_label)

        infobuttonnever = Gtk.Button.new_with_label(_("Never ask again"))
        Gtk.StyleContext.add_class(
            infobuttonnever.get_style_context(), Gtk.STYLE_CLASS_FLAT
        )

        info_bar.add_action_widget(infobuttonnever, Gtk.ResponseType.REJECT)
        info_bar.add_button(_("Set as Default"), Gtk.ResponseType.ACCEPT)

        if (
            app.settings.get_boolean("ask-default") == True
            and Gio.AppInfo.get_default_for_type(app.content_types[1], True).get_id()
            != Gio.Application.get_application_id(app) + ".desktop"
        ):
            outer_box.add(info_bar)

        # Get all apps which are registered as browsers
        browsers = Gio.AppInfo.get_all_for_type(app.content_types[1])

        # The Gio.AppInfo.launch_uris method takes a list object, so let's make a list and put our url in there
        uris = []
        uris.append(self.entry.get_text())

        # create an empty dict to use later
        appslist = {}

        self.check_url_mappings(app, self.entry.get_text(), browsers)

        # Remove Browz from the list of browsers
        self.browsers = list(
            filter(
                lambda b: Gio.Application.get_application_id(app) not in b.get_id(),
                browsers,
            )
        )

        # Loop over the apps in the list of browsers
        for index, browser in enumerate(self.browsers):
            # Get the icon and label, and put them in a button
            try:
                icon = Gtk.Image.new_from_gicon(browser.get_icon(), Gtk.IconSize.DIALOG)
            except:
                icon = Gtk.Image.new_from_icon_name(
                    "applications-internet", Gtk.IconSize.DIALOG
                )

            icon.set_name("browsericon")
            label = Gtk.Label.new(browser.get_display_name())
            label.set_max_width_chars(10)
            label.set_width_chars(10)
            label.set_line_wrap(True)
            label.set_ellipsize(Pango.EllipsizeMode.END)
            label.set_justify(Gtk.Justification.LEFT)

            # Every button has a vertical Gtk.Box inside
            browser_button = Gtk.Button()
            browserBtnBox = Gtk.Box()
            browserBtnBox.set_name("browser-btn")
            browserBtnBox.set_orientation(Gtk.Orientation.VERTICAL)
            browserBtnBox.set_spacing(0)
            browserBtnBox.pack_start(icon, True, True, 0)
            browserBtnBox.pack_start(label, True, True, 0)

            browser_button.add(browserBtnBox)
            # Connect the click signal, passing on all relevant data(browser and url)
            browser_button.connect("clicked", self.browser_click_handle, index, app)

            # Browser entry box
            browser_entry_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            browser_entry_box.pack_start(browser_button, True, True, 0)

            # Hotkey recorder/indicator
            if index < 10:
                hotkey_button = Gtk.Label(label=str(index + 1))
                hotkey_button.set_name("hotkey-btn")
                hotkey_button.set_hexpand(False)
                hotkey_button.set_halign(Gtk.Align.CENTER)
                browser_entry_box.pack_end(hotkey_button, True, True, 0)

            # Add our button to the horizontal box we made earlier
            hbox.pack_start(browser_entry_box, True, True, 0)

    def check_url_mappings(self, app, url, browsers):
        browser = app.browser_mappings.determine_browser(url, browsers)
        if browser:
            uris = [url]
            browser.launch_uris(uris)
            self.quit_app(self, app)

    def keyboard_handle(self, widget, event, app):
        index = int(Gdk.keyval_name(event.keyval)) - 1
        self.launch_browser(index, app)

    # Function to actually launch the browser
    def browser_click_handle(self, target, index, app):
        self.launch_browser(index, app)

    def launch_browser(self, index, app):
        # The Gio.AppInfo.launch_uris method takes a list object, so let's make a list and put our url in there
        uris = [self.entry.get_text()]
        browser = self.browsers[index]
        browser.launch_uris(uris)
        print("Opening " + browser.get_display_name())
        self.quit_app(self, app)

    # Quit app action
    def quit_app(self, *args):
        app = args[1]
        print("Bye…")
        app.quit()

    def on_about(self, action, param):
        about_dialog = Gtk.AboutDialog(transient_for=self, modal=True)
        about_dialog.present()

    def on_infobar_response(self, infobar, response_id, app):
        infobar.hide()
        appinfo = Gio.DesktopAppInfo.new(
            Gio.Application.get_application_id(app) + ".desktop"
        )

        if response_id == Gtk.ResponseType.ACCEPT:
            # set as default
            try:
                # loop through content types, and set Browz as default for those
                for content_type in app.content_types:
                    appinfo.set_as_default_for_type(content_type)

            except GLib.Error:
                print("error")

        elif response_id == Gtk.ResponseType.REJECT:
            # don't ask again
            app.settings.set_boolean("ask-default", False)
