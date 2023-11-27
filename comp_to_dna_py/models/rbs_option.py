class RBSOption:
    def __init__(self, name, description, rbs, cds, first6aas):
        self.name = name
        self.description = description
        self.rbs = rbs
        self.cds = cds
        self.first6aas = first6aas

    def __str__(self):
        return f'{self.name}\n{self.rbs}\n{self.cds}\n{self.first6aas}'
