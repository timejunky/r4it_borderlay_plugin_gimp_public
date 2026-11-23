# Copyright (c) 2025 - dato Nejat Philip Eryiğit. All rights reserved.
class CircularSelectionHelper:

    @staticmethod
    def select_ellipse_box(*_args, **_kwargs):
        return None

    @staticmethod
    def normalize_box(x1, y1, x2, y2, force_circle: bool=False):
        return (float(x1), float(y1), max(1.0, float(x2 - x1)), max(1.0, float(y2 - y1)))
from shapes.common.shape_transform import ShapeTransformHelper
from shapes.freeform.freeform_selection import FreeformSelectionHelper
__all__ = ('CircularSelectionHelper', 'FreeformSelectionHelper', 'ShapeTransformHelper', 'VALID_SHAPE_MODES', 'get_active_rotation', 'get_active_shape_mode', 'is_circular_mode', 'is_curved_or_freeform_mode', 'is_forced_circle_1_1', 'is_freeform_mode', 'is_leaf_mode', 'is_rotated_selection', 'set_active_rotation', 'set_active_shape_mode')
VALID_SHAPE_MODES = ('rectangular',)
_ACTIVE_SHAPE_MODE = 'rectangular'
_ACTIVE_ROTATION_DEG = 0
_ACTIVE_PIVOT_MODE = 'center'

def set_active_shape_mode(shape_mode: str):
    global _ACTIVE_SHAPE_MODE
    clean = str(shape_mode or 'rectangular').strip().lower()
    _ACTIVE_SHAPE_MODE = 'rectangular'

def get_active_shape_mode() -> str:
    return _ACTIVE_SHAPE_MODE

def set_active_rotation(angle_deg: int=0, pivot_mode: str='center'):
    global _ACTIVE_ROTATION_DEG, _ACTIVE_PIVOT_MODE
    _ACTIVE_ROTATION_DEG = int(round(float(angle_deg or 0)))
    _ACTIVE_PIVOT_MODE = str(pivot_mode or 'center').strip().lower()

def get_active_rotation() -> tuple:
    return (_ACTIVE_ROTATION_DEG, _ACTIVE_PIVOT_MODE)

def is_rotated_selection() -> bool:
    return abs(_ACTIVE_ROTATION_DEG) > 0

def is_circular_mode(shape_mode: str='') -> bool:
    mode = (shape_mode or _ACTIVE_SHAPE_MODE).strip().lower()
    return mode in ('circular', 'circle_1_1')

def is_forced_circle_1_1(shape_mode: str='') -> bool:
    mode = (shape_mode or _ACTIVE_SHAPE_MODE).strip().lower()
    return mode == 'circle_1_1'

def is_leaf_mode(shape_mode: str='') -> bool:
    mode = (shape_mode or _ACTIVE_SHAPE_MODE).strip().lower()
    return mode == 'leaf'

def is_freeform_mode(shape_mode: str='') -> bool:
    mode = (shape_mode or _ACTIVE_SHAPE_MODE).strip().lower()
    return mode in ('freeform', 'leaf') or is_rotated_selection()

def is_curved_or_freeform_mode(shape_mode: str='') -> bool:
    mode = (shape_mode or _ACTIVE_SHAPE_MODE).strip().lower()
    return mode in ('circular', 'circle_1_1', 'freeform', 'leaf') or is_rotated_selection()
