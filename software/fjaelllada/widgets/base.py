import functools
import os
import traceback


SVG_PATH = os.path.join(__file__, '..', 'layout.svg')


def exc(fn):

    @functools.wraps(fn)
    def _fn(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except BaseException:
            traceback.print_exc()
            raise

    return _fn
