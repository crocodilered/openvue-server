__all__ = ['FolderModel']


class FolderModel:

    STATUS_NONE = 0
    STATUS_PERFORMING = 1
    STATUS_REVIEW = 2
    STATUS_DONE = 3

    def __init__(self, id, title, creator_id, performer_id, created, updated, status, creator_name='', performer_name=''):
        self.id = id
        self.title = title
        self.creator_id = creator_id
        self.performer_id = performer_id
        self.created = created
        self.updated = updated
        self.status = status
        self.formulars = []
        self.photos = []
        # TODO: Refactor it to use UserModel
        self.creator_name = creator_name
        self.performer_name = performer_name

    @property
    def json(self):
        r = {
            'id': self.id,
            'title': self.title,
            'creator_id': self.creator_id,
            'performer_id': self.performer_id,
            'creator_name': self.creator_name,
            'performer_name': self.performer_name,
            'status': self.status
        }

        if self.updated:
            r['updated'] = self.updated.timestamp()

        if self.created:
            r['updated'] = self.created.timestamp()

        if self.photos:
            r['photos'] = self.photos

        if self.formulars:
            r['formulars'] = [f.json for f in self.formulars]

        return r

    @staticmethod
    def from_row(row):
        # TODO: Check it out
        if len(row) > 7:
            return FolderModel(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
        else:
            return FolderModel(row[0], row[1], row[2], row[3], row[4], row[5], row[6])

    @staticmethod
    def from_json(data):
        return FolderModel(
            data['id'],
            data['title'],
            data['creator_id'],
            data['performer_id'],
            None,
            None,
            data['status']
        )
