

class Warframe:

    def __init__(self, warframe_data_ref):
        self.warframe_data = warframe_data_ref

    def get_build(self, build_name):
        if build_name in self.warframe_data['builds']:
            return Build(self.warframe_data['builds'][build_name])
        return None

    def add_build(self, build_name, build):
        if build_name not in self.warframe_data['builds']:
            self.warframe_data['builds'][build_name] = build
            return True
        return False


    def del_build(self, build_name):
        if build_name in self.warframe_data['builds']:
            del  self.warframe_data['builds'][build_name]
            return True
        return False

    def create_build(self, build_name, description, link, category):

        if build_name not in self.warframe_data['builds']:
            self.warframe_data['builds'][build_name] = {
                "desc": description,
                "link": link,
                "categ": category
            }
            return True
        return False


class Build:

    def __init__(self, build_data_ref):
        self.build_data = build_data_ref


    def description(self):
        return self.build_data['desc']

    def link(self):
        return self.build_data['link']

    def category(self):
        return self.build_data['categ']


    def set_description(self, desc):
        self.build_data['desc'] = desc

    def set_link(self, lnk):
        self.build_data['link'] = lnk

    def set_category(self, categ):
        self.build_data['categ'] = categ

