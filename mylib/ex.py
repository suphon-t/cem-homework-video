import math
from manim import *

SINGULAR_COLORS = [GREEN, RED, BLUE, MAROON, PURPLE]

A = np.matrix([[1, 8, 5, 4],
               # [9, 6, 1, 7],
               [4, 0, 7, 5],
               [6, 3, 2, 8]])

U, sigmas, Vt = np.linalg.svd(A, full_matrices=True)
E = np.zeros(A.shape)
E[:len(sigmas), :len(sigmas)] = np.diag(sigmas)


def matrix_a():
    return Matrix(A)


def matrix_u():
    mat = DecimalMatrix(U)
    mat.set_column_colors(*SINGULAR_COLORS[:len(sigmas)])
    return mat


def matrix_e():
    mat = DecimalMatrix(E)
    for idx in range(len(sigmas)):
        mat.mob_matrix[idx, idx].set_color(SINGULAR_COLORS[idx])
    return mat


def matrix_vt():
    mat = DecimalMatrix(Vt)
    mat.set_row_colors(*SINGULAR_COLORS[:len(sigmas)])
    return mat


def col_box(mat, col):
    return SurroundingRectangle(mat.get_columns()[col])


def row_box(mat, row):
    return SurroundingRectangle(mat.get_rows()[row])


def diag_box(mat, diag):
    return SurroundingRectangle(mat.mob_matrix[diag, diag])


def calc_piece(idx):
    return [E[idx, idx], U[:, idx], Vt[idx]]


def get_pieces():
    pieces = []
    for idx in range(len(sigmas)):
        [si, ui, vti] = calc_piece(idx)
        si_mobj = DecimalNumber(si, num_decimal_places=1)
        ui_mobj = DecimalMatrix(ui).next_to(si_mobj, RIGHT)
        vti_mobj = DecimalMatrix(vti).next_to(ui_mobj, RIGHT)
        clr = SINGULAR_COLORS[idx]
        si_mobj.set_color(clr)
        ui_mobj.set_column_colors(clr)
        vti_mobj.set_row_colors(clr)
        pieces.append(Group(si_mobj, ui_mobj, vti_mobj))
    return pieces


def pieces_sum_equation(pieces):
    symbols = [MathTex("=")]
    for idx in range(len(sigmas)):
        if idx != 0:
            symbols.append(MathTex("+").next_to(pieces[idx - 1], direction=RIGHT))
        pieces[idx].next_to(symbols[idx], direction=RIGHT)
    return symbols


def transform_piece_from(pieces, idx, mat_u, mat_e, mat_vt):
    [si, ui, vti] = pieces[idx]
    return AnimationGroup(
        FadeIn(ui.get_brackets()),
        FadeIn(vti.get_brackets()),
        TransformFromCopy(mat_e.mob_matrix[idx, idx], si),
        TransformFromCopy(mat_u.get_columns()[idx], ui.get_columns()[0]),
        TransformFromCopy(mat_vt.get_rows()[idx], vti.get_rows()[0]),
    )


def pieces_box(pieces, to_idx):
    return SurroundingRectangle(Group(pieces[0], pieces[to_idx]))


def calc_piece_product(idx):
    [si, ui, vti] = calc_piece(idx)
    return si * np.outer(ui, vti)


def new_fade(mobject):
    fade = FullScreenFadeRectangle()
    fade.set_fill(BLACK, 0.75)
    fade.replace(mobject, stretch=True)
    return fade


def result_sum_steps():
    current = np.zeros(A.shape)
    steps = []
    for idx in range(len(sigmas)):
        current = current + calc_piece_product(idx)
        steps.append(current)
    return steps


def steps_matrix(steps):
    step_tracker = ValueTracker(0)
    shape = steps[0].shape
    size = shape[0] * shape[1]
    matrix = DecimalMatrix(steps[0])
    steps = [step.reshape(size) for step in steps]
    mobs = matrix.mob_matrix.reshape(size)
    for idx in range(size):
        mobs[idx].add_updater(lambda d, tmp=idx: d.set_value(interp_step(steps, tmp, step_tracker.get_value())))
    return [matrix, step_tracker]


def interp_step(steps, idx, value):
    ps = steps[math.floor(value)][idx]
    ns = steps[math.ceil(value)][idx]
    alpha = value - math.floor(value)
    return interpolate(ps, ns, alpha)
