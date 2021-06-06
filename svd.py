from mylib.ex import *


class SVDScene(MovingCameraScene):
    def construct(self):
        # initialize object
        a_eq_u_e_vt = MathTex("A", "=", "U", "\\Sigma", "V^T")
        a = a_eq_u_e_vt[0]
        eq = a_eq_u_e_vt[1]
        u = a_eq_u_e_vt[2]
        e = a_eq_u_e_vt[3]
        vt = a_eq_u_e_vt[4]
        obj_a = matrix_a().next_to(eq, LEFT)
        obj_u = matrix_u().next_to(eq, RIGHT)
        obj_e = matrix_e().next_to(obj_u, RIGHT)
        obj_vt = matrix_vt().next_to(obj_e, RIGHT)
        ba = Brace(obj_a, direction=UP)
        ba_text = ba.get_tex("A")
        bu = Brace(obj_u, direction=UP)
        bu_text = bu.get_tex("U")
        be = Brace(obj_e, direction=UP)
        be_text = be.get_tex("\\Sigma")
        bvt = Brace(obj_vt, direction=UP)
        bvt_text = bvt.get_tex("V^T")
        group = Group(obj_a, a_eq_u_e_vt, obj_u, obj_e, obj_vt)
        group_a_eq_u_e_vt = Group(obj_a, eq, obj_u, obj_e, obj_vt)

        # start from A
        self.wait()
        self.camera.frame.move_to(a)
        self.play(Write(a))

        # reveal = U \Sigma V^T
        self.wait()
        self.play(AnimationGroup(
            self.camera.frame.animate.move_to(a_eq_u_e_vt),
            Write(a_eq_u_e_vt[1:]),
        ))

        # reveal the matrices
        self.wait()
        self.play(AnimationGroup(
            self.camera.frame.animate.scale(1.75).move_to(group),
            Transform(a, ba_text),
            Transform(u, bu_text),
            Transform(e, be_text),
            Transform(vt, bvt_text),
            FadeIn(Group(obj_a, ba)),
            FadeIn(Group(obj_u, bu)),
            FadeIn(Group(obj_e, be)),
            FadeIn(Group(obj_vt, bvt)),
        ))

        # focus each singular value and its corresponding row and column
        u_box = col_box(obj_u, 0)
        e_box = diag_box(obj_e, 0)
        vt_box = row_box(obj_vt, 0)
        self.wait()
        self.play(FadeIn(Group(u_box, e_box, vt_box)))
        for idx in range(1, len(sigmas)):
            self.wait()
            self.play(AnimationGroup(
                Transform(u_box, col_box(obj_u, idx)),
                Transform(e_box, diag_box(obj_e, idx)),
                Transform(vt_box, row_box(obj_vt, idx)),
            ))
        self.wait()
        self.play(FadeOut(Group(u_box, e_box, vt_box)))

        # prepare pieces
        pieces = get_pieces()
        symbols = pieces_sum_equation(pieces)
        pieces_eq = Group(*(pieces + symbols[1:]))
        pieces_eq.next_to(group_a_eq_u_e_vt, direction=DOWN)
        pieces_eq.shift(DOWN)

        # pieces product
        [sum_result, step_tracker] = steps_matrix()
        sum_result.next_to(pieces_eq, direction=DOWN)
        sum_result.shift(DOWN)

        # position the camera and hide annotations
        all_group = Group(group_a_eq_u_e_vt, pieces_eq, sum_result)
        self.wait()
        self.play(AnimationGroup(
            self.camera.frame.animate.scale(2/1.75).move_to(all_group),
            FadeOut(Group(ba, a)),
            FadeOut(Group(bu, u)),
            FadeOut(Group(be, e)),
            FadeOut(Group(bvt, vt)),
        ))

        # start revealing pieces
        self.wait()
        self.play(transform_piece_from(pieces, 0, obj_u, obj_e, obj_vt))
        for idx in range(1, len(sigmas)):
            self.wait()
            self.play(AnimationGroup(
                FadeIn(symbols[idx]),
                transform_piece_from(pieces, idx, obj_u, obj_e, obj_vt),
            ))

        # Fade out everything but the first clause, and fade in sum result
        top_fade = new_fade(group_a_eq_u_e_vt)
        eq_fades = [new_fade(Group(symbols[idx], pieces[idx])) for idx in range(len(sigmas))]
        self.wait()
        self.play(FadeIn(Group(top_fade, *eq_fades[1:])))
        self.wait()
        self.play(FadeIn(sum_result))

        # Gradually reveal the clauses and animate the sum result
        for idx in range(1, len(sigmas)):
            self.wait()
            self.play(AnimationGroup(
                FadeOut(eq_fades[idx]),
                step_tracker.animate.set_value(idx)
            ))

        self.play(FadeOut(top_fade))
