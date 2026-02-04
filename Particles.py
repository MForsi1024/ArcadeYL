import random
import arcade
from arcade.particles import Emitter, EmitBurst, FadeParticle


def smoke_mutator(p):  # Дым раздувается и плавно исчезает
    p.scale_x *= 1.02
    p.scale_y *= 1.02
    p.alpha = max(0, p.alpha - 2)


def make_smoke_puff(x, y):
    SMOKE_TEX = arcade.make_soft_circle_texture(20, arcade.color.LIGHT_GRAY, 255, 80)
    # Короткий «пых» дыма: медленно плывёт и распухает
    return Emitter(
        center_xy=(x, y),
        emit_controller=EmitBurst(12),
        particle_factory=lambda e: FadeParticle(
            filename_or_texture=SMOKE_TEX,
            change_xy=arcade.math.rand_in_circle((0.0, 0.0), 0.6),
            lifetime=random.uniform(1.5, 2.5),
            start_alpha=200, end_alpha=0,
            scale=random.uniform(0.6, 0.9),
            mutation_callback=smoke_mutator,
        ),
    )
