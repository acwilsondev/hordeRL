from horderl.engine.components.timed_actor import TimedActor


def run(scene, dt: float) -> None:
    for actor in get_actors(scene):
        actor.update(scene, dt)


def get_actors(scene):
    return [actor for actor in scene.cm.get(TimedActor)]
