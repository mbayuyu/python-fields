from __future__ import print_function

from fields import Fields

from pytest import fixture
from pytest import raises


def test_factory():
    class T1(Fields.a.b.c(1).d(2)):
        pass

    t = T1(1, 2)
    assert repr(t) == "<T1(a=1, b=2, c=1, d=2)>"


def test_factory_all_defaults():
    class T2(Fields.a(0).b(1).c(2).d(3)):
        pass

    t = T2()
    assert repr(t) == "<T2(a=0, b=1, c=2, d=3)>"


def test_factory_no_required_after_defaults():
    raises(TypeError, getattr, Fields.a(0).b, 'c')


def test_factory_no_required_after_defaults_2():
    raises(TypeError, type, 'Broken', (Fields.a(0).b,), {})


def test_factory_t3():
    class T3(Fields.a):
        pass

    t = T3(1)
    assert repr(t) == "<T3(a=1)>"


def test_factory_empty_raise():
    raises(TypeError, type, "T5", (Fields,), {})


@fixture(scope="module")
def CmpC(request):
    class CmpC(Fields.a.b):
        pass

    return CmpC


def test_equal(CmpC):
    """
    Equal objects are detected as equal.
    """
    assert CmpC(1, 2) == CmpC(1, 2)
    assert not (CmpC(1, 2) != CmpC(1, 2))


def test_unequal_same_class(CmpC):
    """
    Unequal objects of correct type are detected as unequal.
    """
    assert CmpC(1, 2) != CmpC(2, 1)
    assert not (CmpC(1, 2) == CmpC(2, 1))


def test_unequal_different_class(CmpC):
    """
    Unequal objects of differnt type are detected even if their attributes
    match.
    """
    class NotCmpC(object):
        a = 1
        b = 2
    assert CmpC(1, 2) != NotCmpC()
    assert not (CmpC(1, 2) == NotCmpC())


def test_lt(CmpC):
    """
    __lt__ compares objects as tuples of attribute values.
    """
    for a, b in [
        ((1, 2),  (2, 1)),
        ((1, 2),  (1, 3)),
        (("a", "b"), ("b", "a")),
    ]:
        assert CmpC(*a) < CmpC(*b)


def test_lt_unordable(CmpC):
    """
    __lt__ returns NotImplemented if classes differ.
    """
    assert NotImplemented == (CmpC(1, 2).__lt__(42))


def test_le(CmpC):
    """
    __le__ compares objects as tuples of attribute values.
    """
    for a, b in [
        ((1, 2),  (2, 1)),
        ((1, 2),  (1, 3)),
        ((1, 1),  (1, 1)),
        (("a", "b"), ("b", "a")),
        (("a", "b"), ("a", "b")),
    ]:
        assert CmpC(*a) <= CmpC(*b)


def test_le_unordable(CmpC):
    """
    __le__ returns NotImplemented if classes differ.
    """
    assert NotImplemented == (CmpC(1, 2).__le__(42))


def test_gt(CmpC):
    """
    __gt__ compares objects as tuples of attribute values.
    """
    for a, b in [
        ((2, 1), (1, 2)),
        ((1, 3), (1, 2)),
        (("b", "a"), ("a", "b")),
    ]:
        assert CmpC(*a) > CmpC(*b)


def test_gt_unordable(CmpC):
    """
    __gt__ returns NotImplemented if classes differ.
    """
    assert NotImplemented == (CmpC(1, 2).__gt__(42))


def test_ge(CmpC):
    """
    __ge__ compares objects as tuples of attribute values.
    """
    for a, b in [
        ((2, 1), (1, 2)),
        ((1, 3), (1, 2)),
        ((1, 1), (1, 1)),
        (("b", "a"), ("a", "b")),
        (("a", "b"), ("a", "b")),
    ]:
        assert CmpC(*a) >= CmpC(*b)


def test_ge_unordable(CmpC):
    """
    __ge__ returns NotImplemented if classes differ.
    """
    assert NotImplemented == (CmpC(1, 2).__ge__(42))


def test_hash(CmpC):
    """
    __hash__ returns different hashes for different values.
    """
    assert hash(CmpC(1, 2)) != hash(CmpC(1, 1))


@fixture(scope="module")
def InitC(request):
    class InitC(Fields.a.b):
        def __init__(self, *args, **kwargs):
            super(InitC, self).__init__(*args, **kwargs)
            if self.a == self.b:
                raise ValueError

    return InitC


def test_sets_attributes(InitC):
    """
    The attributes are initialized using the passed keywords.
    """
    obj = InitC(a=1, b=2)
    assert 1 == obj.a
    assert 2 == obj.b


def test_custom_init(InitC):
    """
    The class initializer is called too.
    """
    with raises(ValueError):
        InitC(a=1, b=1)


def test_passes_args(InitC):
    """
    All positional parameters are passed to the original initializer.
    """
    class InitWithArg(Fields.a):
        def __init__(self, arg, **kwargs):
            super(InitWithArg, self).__init__(**kwargs)
            self.arg = arg

    obj = InitWithArg(42, a=1)
    assert 42 == obj.arg
    assert 1 == obj.a


def test_missing_arg(InitC):
    """
    Raises `ValueError` if a value isn't passed.
    """
    with raises(TypeError):
        InitC(a=1)