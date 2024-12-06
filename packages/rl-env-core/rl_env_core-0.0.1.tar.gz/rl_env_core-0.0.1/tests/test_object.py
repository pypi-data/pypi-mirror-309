import math

from core import Vec3, Triangle, BBox, PlainObject, angleAxis, Mat4x4, World


def test_fill():
    obj = PlainObject()
    obj.fill(BBox(Vec3(0.2, 0.1, 0.15), 0.7))

    assert obj.is_filled(Vec3(0.3, 0.4, 0.5))
    assert not obj.is_filled(Vec3(0.1, 0.1, 0.1))

    obj.carve(BBox(Vec3(0.3, 0.4, 0.5), Vec3(0.1, 0.2, 0.1)))

    assert not obj.is_filled(Vec3(0.35, 0.55, 0.55))


def test_generate_mesh():
    obj = PlainObject()
    obj.fill(BBox(Vec3(0.0, 0.0, 0.0), 0.5))
    assert obj.generate_mesh() == [Triangle(Vec3(0, 0, 0), Vec3(0, 0, 0.5), Vec3(0, 0.5, 0)),
                                   Triangle(Vec3(0, 0, 0.5), Vec3(0, 0.5, 0.5), Vec3(0, 0.5, 0)),
                                   Triangle(Vec3(0.5, 0, 0), Vec3(0.5, 0.5, 0), Vec3(0.5, 0, 0.5)),
                                   Triangle(Vec3(0.5, 0.5, 0), Vec3(0.5, 0.5, 0.5), Vec3(0.5, 0, 0.5)),
                                   Triangle(Vec3(0, 0, 0), Vec3(0, 0, 0.5), Vec3(0.5, 0, 0)),
                                   Triangle(Vec3(0, 0, 0.5), Vec3(0.5, 0, 0.5), Vec3(0.5, 0, 0)),
                                   Triangle(Vec3(0, 0.5, 0), Vec3(0.5, 0.5, 0), Vec3(0, 0.5, 0.5)),
                                   Triangle(Vec3(0.5, 0.5, 0), Vec3(0.5, 0.5, 0.5), Vec3(0, 0.5, 0.5)),
                                   Triangle(Vec3(0, 0, 0), Vec3(0, 0.5, 0), Vec3(0.5, 0, 0)),
                                   Triangle(Vec3(0, 0.5, 0), Vec3(0.5, 0.5, 0), Vec3(0.5, 0, 0)),
                                   Triangle(Vec3(0, 0, 0.5), Vec3(0.5, 0, 0.5), Vec3(0, 0.5, 0.5)),
                                   Triangle(Vec3(0.5, 0, 0.5), Vec3(0.5, 0.5, 0.5), Vec3(0, 0.5, 0.5))]


def tesh_have_changed():
    obj = PlainObject()
    assert not obj.changed

    obj.fill(BBox(Vec3(0.2, 0.1, 0.15), 0.7))

    assert obj.changed

    obj.clear_changed()
    assert not obj.changed

    obj.carve(BBox(Vec3(0.3, 0.4, 0.5), Vec3(0.1, 0.2, 0.1)))
    assert obj.changed


def test_transform():
    obj = PlainObject()
    obj.position = Vec3(1, 2, 3)
    obj.scale = 2
    obj.rotation = angleAxis(math.pi / 2, Vec3(0, 0, 1))

    assert obj.position == Vec3(1, 2, 3)
    assert obj.scale == 2
    assert obj.rotation == angleAxis(math.pi / 2, Vec3(0, 0, 1))

    assert obj.transform.nearly_equal(Mat4x4(
        0, 2, 0, 0,
        -2, 0, 0, 0,
        0, 0, 2, 0,
        1, 2, 3, 1,
    ), 1.e-10)


def test_transform_is_filled():
    obj = PlainObject()
    obj.fill(BBox(Vec3(0, 0, 0), 1))

    obj.position = Vec3(1, 2, 3)
    obj.scale = 2
    obj.rotation = angleAxis(math.pi / 2, Vec3(0, 0, 1))

    assert obj.is_filled(Vec3(0, 3, 4))


def test_transform_origin():
    obj = PlainObject()
    obj.position = Vec3(1, 1, 1)
    obj.scale = 2
    obj.rotation = angleAxis(math.pi / 2, Vec3(0, 0, 1))
    obj.origin = Vec3(0.5, 0.5, 0.5)

    assert obj.origin == Vec3(0.5, 0.5, 0.5)

    assert obj.transform.nearly_equal(Mat4x4(
        0, 2, 0, 0,
        -2, 0, 0, 0,
        0, 0, 2, 0,
        2, 0, 0, 1,
    ), 1.e-10)


def test_world():
    world = World()
    assert world.objects == []

    obj = PlainObject()
    obj.position = Vec3(1, 2, 3)
    world.add(obj)
    assert [obj.position for obj in world.objects] == [Vec3(1, 2, 3)]

    world.objects[0].position = Vec3(2, 3, 4)
    assert [obj.position for obj in world.objects] == [Vec3(2, 3, 4)]
