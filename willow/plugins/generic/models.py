from willow.models import db, mixins

class TraitType(db.Model, mixins.WLWMixin):
    """
    Example constraint table for traits.
    Usage case: you want to categorize traits in addition to 
    their standard table.
    """
    pass

class GenericTrait(db.Model, mixins.TraitMixin):
    """
    Example GenericTrait.
    TraitMixin should be used as a base for any Mixins created
    for custom traits and trait types.
    """
    base_cost = 2
    type_id = db.Column(db.Integer, db.ForeignKey('traittype.id'), nullable=False)
    type = db.relationship('TraitType',
            primaryjoin="GenericTrait.type_id == TraitType.id",
            uselist=False,
            cascade=False,
            backref=db.backref('generic_traits', uselist=True))

class Profile(db.Model):
    __tablename__ = 'profile'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', 
            primaryjoin="foreign(Profile.user_id) == User.id",
            uselist=False,
            cascade=False,
            lazy='joined',
            backref=db.backref('wlw_profile', uselist=False, lazy='joined'))
    name = db.Column(db.String)
    primary_chapter_id = db.Column(db.Integer, nullable=True)
    primary_chapter = db.relationship('Chapter',
            primaryjoin='foreign(Profile.primary_chapter_id) == Chapter.id',
            uselist=False,
            cascade=False,
            lazy='joined')

    def is_active(self):
        return self.user.is_active()

    def is_admin(self):
        return self.user.has_role('Admin')
