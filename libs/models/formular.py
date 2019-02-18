__all__ = ['FormularModel']


class FormularModel:

    def __init__(self, id, folder_id, title, created=None, updated=None):
        self.id = id
        self.folder_id = folder_id
        self.title = title
        self.created = created
        self.updated = updated

    @property
    def json(self):
        r = {
            'id': self.id,
            'folder_id': self.folder_id,
            'title': self.title
        }
        if self.created:
            r['created'] = self.created.timestamp()
        if self.updated:
            r['created'] = self.updated.timestamp()
        return r

    @staticmethod
    def from_row(row):
        return FormularModel(row[0], row[1], row[2], row[3], row[4])
