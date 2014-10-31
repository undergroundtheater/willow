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

