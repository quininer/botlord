# http://stackoverflow.com/questions/4984647/accessing-dict-keys-like-an-attribute-in-python#answer-14620633

class AttrDict(dict):
    '''
    >>> ad = AttrDict({'x':1})
    >>> ad['x']
    1
    >>> ad.x
    1
    >>> ad['y'] = 2
    >>> ad.z = 3
    >>> ad.y
    2
    >>> ad['z']
    3
    >>> type([i for i in ad])
    <class 'list'>
    '''
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self
