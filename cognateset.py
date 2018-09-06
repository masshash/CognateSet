# Copyright (c) 2018 Masashi Takahashi
# This software is released under the MIT License.

# cognateset.py version 1.0.0

__all__ = ['CognateSet']

from _collections_abc import KeysView as _KeysView

def _transfer_error(error):
    transfer = error.__class__(*error.args)
    transfer.__suppress_context__ = True
    return transfer

class _ElementError(Exception):
    def __init__(self, *args):
        self.__suppress_context__ = True

class _ElementsView(_KeysView):
    def __repr__(self):
        return '_ElementsView(%r)' % list(self._mapping.keys())
    
class _CognatesView():
    def __init__(self, cognates, protect):
        self.__cognates = cognates
        self.__protect = protect

    def __iter__(self):
        if self.__protect:
            for cognate in self.__cognates:
                yield cognate.copy()
        else:
            yield from self.__cognates

    def __repr__(self):
        if self:
            return '_CognatesView([' + ', '.join(repr(cognate)[9:-1]
                    for cognate in self.__cognates) + '])'
        return '_CognatesView([])'

    def __len__(self):
        return len(self.__cognates)

    def __contains__(self, iterable):
        elems = set(iterable)
        for cognate in self.__cognates:
            if elems == cognate:
                return True
        return False
        
    def __eq__(self, other):
        if not isinstance(other, _CognatesView):
            return False
        if self.__len__() != other.__len__():
            return False
        return (set(map(tuple, self.__cognates)) ==
                set(map(tuple, other.__cognates)))
                
    def __ne__(self, other):
        return not self.__eq__(other)

    def __bool__(self):
        if self.__cognates:
            return True
        return False

class _Cognate(set):
    __slots__ = ()
    __hash__ = object.__hash__
    def _copy(self):
        c = _Cognate()
        c.update(self)
        return c

class CognateSet():
    def __init__(self, *args):
        if len(args) > 1:
            raise TypeError('expected at most 1 arguments, got %d' % len(args))
        self.__mapping = {}
        self.__sets = set()
        if args:
            try:
                self.expand(args[0])
            except Exception as e:
                raise _transfer_error(e)

    def join(self, iterable):
        mapping, sets = self.__mapping, self.__sets
        sub_cognates = set()
        new_cognate = _Cognate()

        for elem in set(iterable):
            if elem in mapping:
                sub_cognates.add(mapping[elem])
            else:
                new_cognate.add(elem)

        if not new_cognate and len(sub_cognates) < 2:
            return

        max_size = 0
        for cognate in sub_cognates:
            size = len(cognate)
            if size > max_size:
                max_size, super_cognate = size, cognate

        if new_cognate:
            if len(new_cognate) > max_size:
                for elem in new_cognate:
                    mapping[elem] = new_cognate
                sets.add(new_cognate)
                if not sub_cognates:
                    return
                super_cognate = new_cognate
            else:
                sub_cognates.add(new_cognate)
                sub_cognates.remove(super_cognate)
        else:
            sub_cognates.remove(super_cognate)

        for sub_cognate in sub_cognates:
            for elem in sub_cognate:
                mapping[elem] = super_cognate
            super_cognate |= sub_cognate
            sets.discard(sub_cognate)

    def expand(self, other):
        other = other.__sets if isinstance(other, CognateSet) else other
        try:
            for iterable in other:
                self.join(iterable)
        except Exception as e:
            raise _transfer_error(e)

    def reorg(self, iterable):
        mapping, sets = self.__mapping, self.__sets
        new_cognate = _Cognate()
        new_cognate.update(iterable)
        for elem in new_cognate:
            if elem in mapping:
                cognate = mapping[elem]
                cognate.remove(elem)
                if not cognate:
                    sets.remove(cognate)
            mapping[elem] = new_cognate
        sets.add(new_cognate)

    def cognate(self, elem, protect=True):
        mapping = self.__mapping
        if elem in mapping:
            if protect:
                return mapping[elem].copy()
            return mapping[elem]
        return set()

    __default = object()

    def pop(self, elem=__default, default=__default):
        if elem is self.__default:
            try:
                cognate = self.__sets.pop()
            except KeyError:
                raise _ElementError('CognateSet is empty')
        else:
            if elem not in self:
                if default is self.__default:
                    raise  _ElementError('%r is not a element' % (elem))
                return default
            cognate = self.__mapping[elem]
            self.__sets.remove(cognate)
        mapping = self.__mapping
        for e in cognate:
            del mapping[e]
        return cognate

    def delelem(self, elem):
        try:
            cognate = self.__mapping[elem]
        except KeyError:
            raise _ElementError('%r is not a element' % (elem))
        cognate.remove(elem)
        if not cognate:
            self.__sets.remove(cognate)
        del self.__mapping[elem]

    def delcog(self, elem):
        try:
            cognate = self.__mapping[elem]
        except KeyError:
            raise _ElementError('%r is not a element' % (elem))
        mapping = self.__mapping
        for e in cognate:
            del mapping[e]
        self.__sets.remove(cognate)

    def elements(self):
        return _ElementsView(self.__mapping)

    def cognates(self, protect=True):
        return _CognatesView(self.__sets, protect)

    def copy(self):
        cs = CognateSet()
        cs.__sets = set(cognate._copy() for cognate in self.__sets)
        cs.__mapping = {elem: cognate for cognate in cs.__sets for elem in cognate}
        return cs

    def clear(self):
        self.__mapping.clear()
        self.__sets.clear()

    def __iter__(self):
        yield from self.__mapping

    def __repr__(self):
        if self:
            return 'CognateSet(' + ', '.join(repr(cognate)[9:-1]
                    for cognate in self.__sets) + ')'
        return 'CognateSet()'

    def __len__(self):
        return len(self.__mapping)

    def __contains__(self, item):
        return item in self.__mapping

    def __eq__(self, other):
        if not isinstance(other, CognateSet):
            return False
        if self.ncogs != other.ncogs:
            return False
        if self.__mapping.keys() == other.__mapping.keys():
            return set(map(tuple, self.__sets)) == set(map(tuple, other.__sets))
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __bool__(self):
        if self.__sets:
            return True
        return False

    def __copy__(self):
        return self.copy()
        
    @property
    def ncogs(self):
        return len(self.__sets)
