from data.objectcache import ObjectCache


def test_objectCacheIsSingleton():
    cache1 = ObjectCache()
    cache1.clear()
    cache1.add('1', 'Some string object')
    cache2 = ObjectCache()
    assert cache1 == cache2
    assert cache2.nrObjects() == 1
    assert cache2.get('1') == 'Some string object'
    cache2.clear()
    cache1.clear()