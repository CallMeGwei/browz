from gi.repository import GLib


class BrowserMappings:
    def __init__(self, settings):
        self.settings = settings

    def set_browser(self, url, browser):
        mappings_dict = self.load_url_mappings()
        mappings_dict[url] = browser

        mappings_array = []
        for url, browser in mappings_dict.items():
            mappings_array.append(url + " " + browser)

        tmp_variant = GLib.Variant("aas", mappings_array)
        self.settings.set_value("url-mapping", tmp_variant)

    def clear_browser_mappings(self):
        empty_variant = GLib.Variant("aas", [])
        self.settings.set_value("url-mapping", empty_variant)

    def load_url_mappings(self):
        url_mappings = self.settings.get_value("url-mapping")
        mappings_dict = {}

        for mapping in url_mappings:
            path_to_match = "".join(mapping).split(" ")
            mappings_dict[path_to_match[0]] = path_to_match[1]

        return mappings_dict

    def determine_browser(self, url, browsers):
        mappings_dict = self.load_url_mappings()

        for urlPattern, browserID in mappings_dict.items():
            if not url.startswith(urlPattern):
                continue

            for b in browsers:
                if b.get_id() != browserID:
                    continue
                return b
