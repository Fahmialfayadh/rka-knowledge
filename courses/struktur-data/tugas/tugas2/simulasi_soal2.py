from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService
from collections import deque

# Color palette
BG_COLOR = "#1a1a2e"
BOUGHT_COLOR = GREEN
FREE_COLOR = YELLOW
HIGHLIGHT_COLOR = BLUE
DEQUE_COLOR = TEAL
POP_COLOR = RED
BEST_COLOR = GOLD

config.background_color = BG_COLOR


def create_array_row(values, label_text, y_pos, cell_size=0.9, font_size=28):
    """Create a row of squares with values and index labels."""
    squares = VGroup()
    texts = []
    for v in values:
        sq = Square(side_length=cell_size, color=WHITE, stroke_width=2)
        t = Text(str(v), font_size=font_size, color=WHITE)
        t.move_to(sq.get_center())
        squares.add(VGroup(sq, t))
        texts.append(t)
    squares.arrange(RIGHT, buff=0.15)
    squares.move_to(UP * y_pos)

    idx_labels = VGroup()
    for i, cell in enumerate(squares):
        lbl = Text(str(i), font_size=18, color=GRAY)
        lbl.next_to(cell, DOWN, buff=0.15)
        idx_labels.add(lbl)

    label = Text(label_text, font_size=24, color=GRAY)
    label.next_to(squares, LEFT, buff=0.4)

    return squares, texts, idx_labels, label


class DPMonotonicDeque(VoiceoverScene):
    def construct(self):
        self.set_speech_service(
            GTTSService(lang="id", tld="co.id")
        )

        prices = [1, 6, 1, 2, 4]
        n = len(prices)

        # ============ SECTION 1: INTRO ============
        title = Text("Minimum Coins to Buy Fruits", font_size=44, color=WHITE)
        subtitle = Text(
            "DP + Monotonic Deque Optimization", font_size=26, color=BLUE
        )
        subtitle.next_to(title, DOWN, buff=0.4)

        with self.voiceover(
            text="Kita akan menyelesaikan masalah Minimum Coins to Buy Fruits, "
            "menggunakan Dynamic Programming dengan optimasi Monotonic Deque."
        ) as tracker:
            self.play(Write(title), run_time=1.5)
            self.play(FadeIn(subtitle, shift=UP * 0.3), run_time=0.8)

        # Problem rules
        rules = VGroup(
            Text("Buy fruit i  →  pay prices[i]", font_size=24, color=WHITE),
            Text(
                "Get next (i+1) fruits for FREE (1-indexed)",
                font_size=24,
                color=YELLOW,
            ),
            Text("Goal: minimum total cost", font_size=24, color=GREEN),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        rules.next_to(subtitle, DOWN, buff=0.6)

        with self.voiceover(
            text="Aturannya sederhana. Jika kita membeli buah ke i, "
            "maka kita mendapatkan i plus 1 buah berikutnya secara gratis. "
            "Tujuan kita adalah meminimalkan total biaya."
        ) as tracker:
            for rule in rules:
                self.play(FadeIn(rule, shift=RIGHT * 0.3), run_time=0.6)
            self.wait(max(0, tracker.duration - 1.8))

        # Show input
        input_text = Text("prices = [1, 6, 1, 2, 4]", font_size=32, color=WHITE)
        input_text.move_to(ORIGIN)

        with self.voiceover(
            text="Input yang kita gunakan adalah prices sama dengan 1, 6, 1, 2, 4."
        ) as tracker:
            self.play(
                FadeOut(title), FadeOut(subtitle), FadeOut(rules),
                FadeIn(input_text),
                run_time=0.8,
            )
            self.wait(max(0, tracker.duration - 0.8))

        self.play(FadeOut(input_text), run_time=0.5)

        # ============ SECTION 2: SETUP ============
        explanation = Text("Setup: Initialize arrays", font_size=24, color=WHITE)
        explanation.to_edge(UP, buff=0.4)

        p_squares, p_texts, p_idx, p_label = create_array_row(
            prices, "prices[]", y_pos=1.8
        )
        dp_values = [0] * (n + 1)
        dp_squares, dp_texts, dp_idx, dp_label = create_array_row(
            dp_values, "dp[]", y_pos=0.0
        )

        deque_label = Text("Deque:", font_size=24, color=GRAY)
        deque_label.move_to(DOWN * 2.0 + LEFT * 5)
        front_label = Text("front ←", font_size=18, color=TEAL)
        back_label = Text("→ back", font_size=18, color=TEAL)
        deque_area_center = DOWN * 2.0

        pointer = Triangle(fill_opacity=1, color=HIGHLIGHT_COLOR).scale(0.15)
        pointer.next_to(p_squares[-1], UP, buff=0.2)

        with self.voiceover(
            text="Pertama, kita siapkan array prices berisi harga tiap buah, "
            "dan array dp berisi 6 sel yang diinisialisasi nol. "
            "dp i menyimpan biaya minimum dari index i sampai akhir."
        ) as tracker:
            self.play(FadeIn(explanation), run_time=0.5)
            self.play(
                FadeIn(p_squares), FadeIn(p_idx), FadeIn(p_label), run_time=1
            )
            self.play(
                FadeIn(dp_squares), FadeIn(dp_idx), FadeIn(dp_label), run_time=1
            )
            self.wait(max(0, tracker.duration - 2.5))

        with self.voiceover(
            text="Kita juga menyiapkan deque untuk menyimpan kandidat index terbaik secara efisien."
        ) as tracker:
            self.play(FadeIn(deque_label), run_time=0.5)
            self.wait(max(0, tracker.duration - 0.5))

        # ============ SECTIONS 3-7: ITERATIONS ============
        q = deque()
        deque_mobjects = VGroup()

        def build_deque_element(idx):
            rect = RoundedRectangle(
                height=0.7, width=0.9, corner_radius=0.1,
                color=DEQUE_COLOR, stroke_width=2,
            )
            idx_text = Text(str(idx), font_size=22, color=WHITE)
            dp_val_text = Text(f"dp={dp_values[idx]}", font_size=16, color=GRAY_B)
            content = VGroup(idx_text, dp_val_text).arrange(DOWN, buff=0.05)
            content.move_to(rect.get_center())
            return VGroup(rect, content)

        def reposition_deque():
            if len(deque_mobjects) > 0:
                deque_mobjects.arrange(RIGHT, buff=0.15)
                deque_mobjects.move_to(deque_area_center)

        def update_front_back_labels():
            anims = []
            if len(deque_mobjects) > 0:
                new_front = front_label.copy().next_to(deque_mobjects[0], LEFT, buff=0.2)
                new_back = back_label.copy().next_to(deque_mobjects[-1], RIGHT, buff=0.2)
                anims.append(front_label.animate.move_to(new_front.get_center()))
                anims.append(back_label.animate.move_to(new_back.get_center()))
            return anims

        front_back_shown = False

        # Narration per iteration
        narrations = {
            4: "Iterasi pertama, i sama dengan 4. Harga buah ke-4 adalah 4. "
               "Ini buah terakhir, tidak ada buah gratis setelahnya. "
               "Kita masukkan index 5 ke deque. "
               "dp 4 sama dengan 4 plus dp 5, yaitu 4.",
            3: "Sekarang i sama dengan 3, harga 2. "
               "Jika beli buah ini, buah ke-4 gratis. "
               "Masukkan index 4 ke deque. "
               "Depan deque adalah index 5 dengan dp 0, jadi dp 3 sama dengan 2 plus 0, yaitu 2.",
            2: "i sama dengan 2, harga 1. Jika beli, buah ke-3 sampai ke-4 gratis. "
               "Kita pop index 4 dari belakang deque karena dp 3 lebih kecil dari dp 4. "
               "Masukkan index 3. Depan deque tetap index 5, "
               "jadi dp 2 sama dengan 1 plus 0, yaitu 1.",
            1: "i sama dengan 1, harga 6. Jika beli, buah ke-2 gratis. "
               "Pop index 3 dari belakang karena dp 2 lebih kecil. "
               "Masukkan index 2. Lalu expire index 5 dari depan karena sudah di luar jangkauan. "
               "Depan deque sekarang index 2 dengan dp 1, "
               "jadi dp 1 sama dengan 6 plus 1, yaitu 7.",
            0: "Terakhir, i sama dengan 0, harga 1. Jika beli, buah ke-1 gratis. "
               "Masukkan index 1 ke deque. "
               "Depan deque adalah index 2 dengan dp 1, "
               "jadi dp 0 sama dengan 1 plus 1, yaitu 2.",
        }

        for i in range(n - 1, -1, -1):
            with self.voiceover(text=narrations[i]) as tracker:
                # -- Update explanation --
                new_exp = Text(
                    f"Iteration: i = {i},  prices[{i}] = {prices[i]}",
                    font_size=24, color=WHITE,
                )
                new_exp.to_edge(UP, buff=0.4)
                self.play(Transform(explanation, new_exp), run_time=0.5)

                # -- Move pointer --
                self.play(
                    pointer.animate.next_to(p_squares[i], UP, buff=0.2),
                    run_time=0.4,
                )
                self.play(
                    p_squares[i][0].animate.set_fill(HIGHLIGHT_COLOR, opacity=0.3),
                    run_time=0.3,
                )

                # -- Show free window --
                free_start = i + 1
                free_end = min(2 * i + 1, n - 1)
                free_bracket = None
                free_text = None
                if free_start <= free_end and free_start < n:
                    free_group = VGroup(
                        *[p_squares[j] for j in range(free_start, free_end + 1)]
                    )
                    free_bracket = Brace(free_group, DOWN, color=YELLOW)
                    free_text = Text("free", font_size=18, color=YELLOW)
                    free_text.next_to(free_bracket, DOWN, buff=0.1)
                    self.play(Create(free_bracket), FadeIn(free_text), run_time=0.5)

                # -- Step A: Pop from right --
                while q and dp_values[i + 1] <= dp_values[q[-1]]:
                    pop_idx = q[-1]
                    reason = Text(
                        f"Pop back: dp[{i+1}]={dp_values[i+1]} <= dp[{pop_idx}]={dp_values[pop_idx]}",
                        font_size=20, color=POP_COLOR,
                    )
                    reason.to_edge(DOWN, buff=0.3)
                    self.play(FadeIn(reason, shift=UP * 0.2), run_time=0.3)

                    pop_mob = deque_mobjects[-1]
                    pop_mob[0].set_color(POP_COLOR)
                    self.play(FadeOut(pop_mob, shift=RIGHT * 0.5), run_time=0.4)
                    deque_mobjects.remove(pop_mob)
                    q.pop()

                    self.play(FadeOut(reason), run_time=0.2)
                    if len(deque_mobjects) > 0:
                        reposition_deque()
                        anims = update_front_back_labels()
                        if anims and front_back_shown:
                            self.play(*anims, run_time=0.3)

                # -- Append i+1 to deque --
                q.append(i + 1)
                new_elem = build_deque_element(i + 1)
                deque_mobjects.add(new_elem)
                reposition_deque()

                if not front_back_shown:
                    front_label.next_to(deque_mobjects[0], LEFT, buff=0.2)
                    back_label.next_to(deque_mobjects[-1], RIGHT, buff=0.2)
                    self.play(
                        FadeIn(new_elem, shift=LEFT * 0.3),
                        FadeIn(front_label), FadeIn(back_label),
                        run_time=0.5,
                    )
                    front_back_shown = True
                else:
                    anims = update_front_back_labels()
                    self.play(
                        FadeIn(new_elem, shift=LEFT * 0.3), *anims, run_time=0.5
                    )

                # -- Step B: Expire from left --
                while q and q[0] > 2 * i + 2:
                    exp_idx = q[0]
                    reason = Text(
                        f"Expire front: q[0]={exp_idx} > {2*i+2}",
                        font_size=20, color=POP_COLOR,
                    )
                    reason.to_edge(DOWN, buff=0.3)
                    self.play(FadeIn(reason, shift=UP * 0.2), run_time=0.3)

                    exp_mob = deque_mobjects[0]
                    exp_mob[0].set_color(POP_COLOR)
                    self.play(FadeOut(exp_mob, shift=LEFT * 0.5), run_time=0.4)
                    deque_mobjects.remove(exp_mob)
                    q.popleft()

                    self.play(FadeOut(reason), run_time=0.2)
                    if len(deque_mobjects) > 0:
                        reposition_deque()
                        anims = update_front_back_labels()
                        if anims and front_back_shown:
                            self.play(*anims, run_time=0.3)

                # -- Step C: Compute dp[i] --
                best_idx = q[0]
                dp_values[i] = prices[i] + dp_values[best_idx]

                deque_mobjects[0][0].set_color(BEST_COLOR)
                self.play(Indicate(deque_mobjects[0], color=BEST_COLOR), run_time=0.5)

                formula = Text(
                    f"dp[{i}] = {prices[i]} + dp[{best_idx}]({dp_values[best_idx]}) = {dp_values[i]}",
                    font_size=22, color=BEST_COLOR,
                )
                formula.to_edge(DOWN, buff=0.3)
                self.play(FadeIn(formula), run_time=0.4)

                new_dp_text = Text(
                    str(dp_values[i]), font_size=28, color=BEST_COLOR
                )
                new_dp_text.move_to(dp_squares[i][0].get_center())
                self.play(
                    Transform(dp_texts[i], new_dp_text),
                    Flash(dp_squares[i][0], color=BEST_COLOR, flash_radius=0.5),
                    run_time=0.6,
                )

                # Reset deque front color
                deque_mobjects[0][0].set_color(DEQUE_COLOR)

                # Clean up
                fade_outs = [FadeOut(formula)]
                if free_bracket:
                    fade_outs.extend([FadeOut(free_bracket), FadeOut(free_text)])
                self.play(
                    *fade_outs,
                    p_squares[i][0].animate.set_fill(BLACK, opacity=0),
                    run_time=0.4,
                )

        # ============ SECTION 8: CONCLUSION ============
        with self.voiceover(
            text="Jawaban akhirnya adalah dp 0 sama dengan 2. "
            "Strategi optimalnya: beli buah ke-0 dengan harga 1, dapat buah ke-1 gratis. "
            "Lalu beli buah ke-2 dengan harga 1, dapat buah ke-3 dan ke-4 gratis. "
            "Total biaya hanya 2."
        ) as tracker:
            new_exp = Text(
                f"Answer: dp[0] = {dp_values[0]}", font_size=30, color=GREEN
            )
            new_exp.to_edge(UP, buff=0.4)
            self.play(Transform(explanation, new_exp), run_time=0.5)

            highlight_rect = SurroundingRectangle(
                dp_squares[0], color=GREEN, buff=0.1, stroke_width=3
            )
            self.play(Create(highlight_rect), run_time=0.5)

            self.play(
                FadeOut(deque_mobjects), FadeOut(deque_label),
                FadeOut(front_label), FadeOut(back_label), FadeOut(pointer),
                run_time=0.5,
            )

            bought = [0, 2]
            free = [1, 3, 4]
            buy_anims = []
            for idx in bought:
                buy_anims.append(
                    p_squares[idx][0].animate.set_fill(BOUGHT_COLOR, opacity=0.4)
                )
            for idx in free:
                buy_anims.append(
                    p_squares[idx][0].animate.set_fill(FREE_COLOR, opacity=0.4)
                )
            self.play(*buy_anims, run_time=0.8)

            legend = VGroup(
                VGroup(
                    Square(
                        side_length=0.3, fill_color=BOUGHT_COLOR,
                        fill_opacity=0.4, stroke_width=1,
                    ),
                    Text(" = Bought", font_size=20, color=WHITE),
                ).arrange(RIGHT, buff=0.1),
                VGroup(
                    Square(
                        side_length=0.3, fill_color=FREE_COLOR,
                        fill_opacity=0.4, stroke_width=1,
                    ),
                    Text(" = Free", font_size=20, color=WHITE),
                ).arrange(RIGHT, buff=0.1),
            ).arrange(RIGHT, buff=0.6)
            legend.move_to(DOWN * 2.0)
            self.play(FadeIn(legend), run_time=0.5)

            answer = Text(
                f"Minimum cost = {dp_values[0]}", font_size=36, color=GREEN
            )
            answer.move_to(DOWN * 3.0)
            self.play(Write(answer), run_time=1)
            self.wait(max(0, tracker.duration - 3.3))

        self.wait(2)
