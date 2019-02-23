import os

import moderngl.experimental as mgl
import numpy as np
from PIL import Image

import data
from example_window import Example, run_example


class Fractal(Example):
    def __init__(self):
        self.ctx = mgl.create_context()

        self.prog = self.ctx.program(
            vertex_shader='''
                #version 330

                in vec2 in_vert;
                out vec2 v_text;

                void main() {
                    gl_Position = vec4(in_vert, 0.0, 1.0);
                    v_text = in_vert;
                }
            ''',
            fragment_shader='''
                #version 330

                in vec2 v_text;
                out vec4 f_color;

                uniform sampler2D Texture;
                uniform vec2 Seed;
                uniform int Iter;

                void main() {
                    vec2 c = Seed;
                    int i;

                    vec2 z = vec2(3.0 * v_text.x, 2.0 * v_text.y);

                    for (i = 0; i < Iter; i++) {
                        float x = (z.x * z.x - z.y * z.y) + c.x;
                        float y = (z.y * z.x + z.x * z.y) + c.y;

                        if ((x * x + y * y) > 4.0) {
                            break;
                        }

                        z.x = x;
                        z.y = y;
                    }

                    f_color = texture(Texture, vec2((i == Iter ? 0.0 : float(i)) / 100.0, 0.0));
                }
            ''',
        )

        img = Image.open(data.find('pal.png')).convert('RGB')
        self.texture = self.ctx.texture(img.size, 3, img.tobytes())
        self.sampler = self.ctx.sampler(self.texture)
        self.sampler.use()

        vertices = np.array([-1.0, -1.0, -1.0, 1.0, 1.0, -1.0, 1.0, 1.0])

        self.vbo = self.ctx.buffer(vertices.astype('f4').tobytes())
        self.vao = self.ctx.simple_vertex_array(self.prog, self.vbo, 'in_vert')

    def render(self):
        self.ctx.screen.viewport = self.wnd.viewport
        self.ctx.clear(1.0, 1.0, 1.0)

        self.prog['Seed'] = (-0.8, 0.156)
        self.prog['Iter'] = 100

        self.vao.render(mgl.TRIANGLE_STRIP)


run_example(Fractal)