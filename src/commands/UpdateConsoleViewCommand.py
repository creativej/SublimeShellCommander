import sublime_plugin

class UpdateConsoleViewCommand(sublime_plugin.TextCommand):
    def run(self, edit, text, jump = False):
        regions = self.view.find_all('$')

        if len(regions):
            last_region = regions[len(regions) - 1]
            if jump:
                eof = self.view.layout_extent()[1]
                self.view.set_viewport_position((0, eof))
            self.view.insert(edit, last_region.end(), text)
