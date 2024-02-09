# main.py
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

import sys
import gi

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk, Gio

from .browser_mappings import BrowserMappings
from .window import BrowzWindow


class Application(Gtk.Application):
    content_types = [
        "x-scheme-handler/http",
        "x-scheme-handler/https",
        "text/html",
        "application/x-extension-htm",
        "application/x-extension-html",
        "application/x-extension-shtml",
        "application/xhtml+xml",
        "application/x-extension-xht",
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            application_id="com.andrewanderson.browz",
            flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE
            | Gio.ApplicationFlags.NON_UNIQUE,
            **kwargs
        )

        self.settings = Gio.Settings.new("com.andrewanderson.browz")
        self.browser_mappings = BrowserMappings(self.settings)

    def do_activate(self):
        self.win = BrowzWindow(self)
        self.win.show_all()

    def do_command_line(self, command_line):
        args = command_line.get_arguments()
        if len(args) == 0:
            self.activate()

        try:
            if args[1] == "--set":
                url = args[2]
                browser = args[3]
                self.browser_mappings.set_browser(url, browser)
                return 0

            if args[1] == "--clear":
                self.browser_mappings.clear_browser_mappings()
                return 0

            if args[1] == "--get-mappings":
                mappings = self.browser_mappings.load_url_mappings()
                for url, browser in mappings.items():
                    print(url, ":", browser)
                return 0

        except IndexError:
            print("No arguments provided")

        self.activate()
        return 0

    def do_startup(self):
        Gtk.Application.do_startup(self)

    def on_about(self, action):
        about_dialog = Gtk.AboutDialog(transient_for=self.win, modal=True)

        about_dialog.set_title(_("About"))
        about_dialog.set_program_name(_("Browz"))
        about_dialog.set_comments(
            "A small app to choose a browser whenever you open links"
        )
        about_dialog.set_website("https://browz.andrewanderson.com")
        about_dialog.set_website_label("Browz website")
        about_dialog.set_authors(["Kavya Gokul", "Andrew D. Anderson"])
        about_dialog.connect("response", lambda dialog, data: dialog.destroy())
        about_dialog.set_logo_icon_name("applications-internet")
        about_dialog.present()


def main(version):
    app = Application()
    return app.run(sys.argv)
