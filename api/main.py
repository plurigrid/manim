File name: example_scenes.py
```python
   from flask import Flask, request, jsonify
   from manimlib import *

   app = Flask(__name__)

   @app.route('/create_scene', methods=['POST'])
   def create_scene():
       # ... existing code from example_scenes.py ...
       from manimlib import *
       import numpy as np

       class OpeningManimExample(Scene):
           def construct(self):
               intro_words = Text("""
                   The original motivation for manim was to
                   better illustrate mathematical functions
                   as transformations.
               """)
               intro_words.to_edge(UP)

               self.play(Write(intro_words))
               self.wait(2)

               # Linear transform
               grid = NumberPlane((-10, 10), (-5, 5))
               matrix = [[1, 1], [0, 1]]
               linear_transform_words = VGroup(
                   Text("This is what the matrix"),
                   IntegerMatrix(matrix, include_background_rectangle=True),
                   Text("looks like")
               )
               linear_transform_words.arrange(RIGHT)
               linear_transform_words.to_edge(UP)
               linear_transform_words.set_backstroke(width=5)

               self.play(
                   ShowCreation(grid),
                   FadeTransform(intro_words, linear_transform_words)
               )
               self.wait()
               self.play(grid.animate.apply_matrix(matrix), run_time=3)
               self.wait()

               # Complex map
               c_grid = ComplexPlane()
               moving_c_grid = c_grid.copy()
               moving_c_grid.prepare_for_nonlinear_transform()
               c_grid.set_stroke(BLUE_E, 1)
               c_grid.add_coordinate_labels(font_size=24)
               complex_map_words = TexText("""
                   Or thinking of the plane as $\\mathds{C}$,\\\\
                   this is the map $z \\rightarrow z^2$
               """)
               complex_map_words.to_corner(UR)
               complex_map_words.set_backstroke(width=5)

               self.play(
                   FadeOut(grid),
                   Write(c_grid, run_time=3),
                   FadeIn(moving_c_grid),
                   FadeTransform(linear_transform_words, complex_map_words),
               )
               self.wait()
               self.play(
                   moving_c_grid.animate.apply_complex_function(lambda z: z**2),
                   run_time=6,
               )
               self.wait(2)
       return jsonify({'message': 'Scene created successfully'})

   @app.route('/add_object', methods=['POST'])
   def add_object():
       # ... existing code from example_scenes.py ...
       from manimlib import *
       import numpy as np

       class AnimatingMethods(Scene):
           def construct(self):
               grid = Tex(R"\pi").get_grid(10, 10, height=4)
               self.add(grid)

               # You can animate the application of mobject methods with the
               # ".animate" syntax:
               self.play(grid.animate.shift(LEFT))

               # Both of those will interpolate between the mobject's initial
               # state and whatever happens when you apply that method.
               # For this example, calling grid.shift(LEFT) would shift the
               # grid one unit to the left, but both of the previous calls to
               # "self.play" animate that motion.

               # The same applies for any method, including those setting colors.
               self.play(grid.animate.set_color(YELLOW))
               self.wait()
               self.play(grid.animate.set_submobject_colors_by_gradient(BLUE, GREEN))
               self.wait()
               self.play(grid.animate.set_height(TAU - MED_SMALL_BUFF))
               self.wait()

               # The method Mobject.apply_complex_function lets you apply arbitrary
               # complex functions, treating the points defining the mobject as
               # complex numbers.
               self.play(grid.animate.apply_complex_function(np.exp), run_time=5)
               self.wait()

               # Even more generally, you could apply Mobject.apply_function,
               # which takes in functions form R^3 to R^3
               self.play(
                   grid.animate.apply_function(
                       lambda p: [
                           p[0] + 0.5 * math.sin(p[1]),
                           p[1] + 0.5 * math.sin(p[0]),
                           p[2]
                       ]
                   ),
                   run_time=5,
               )
               self.wait()
       return jsonify({'message': 'Object added successfully'})

   @app.route('/apply_transformation', methods=['POST'])
   def apply_transformation():
       # ... existing code from example_scenes.py ...
       from manimlib import *
       import numpy as np

       class TexTransformExample(Scene):
           def construct(self):
               # Tex to color map
               t2c = {
                   "A": BLUE,
                   "B": TEAL,
                   "C": GREEN,
               }
               # Configuration to pass along to each Tex mobject
               kw = dict(font_size=72, t2c=t2c)
               lines = VGroup(
                   Tex("A^2 + B^2 = C^2", **kw),
                   Tex("A^2 = C^2 - B^2", **kw),
                   Tex("A^2 = (C + B)(C - B)", **kw),
                   Tex(R"A = \sqrt{(C + B)(C - B)}", **kw),
               )
               lines.arrange(DOWN, buff=LARGE_BUFF)

               self.add(lines[0])
               # The animation TransformMatchingStrings will line up parts
               # of the source and target which have matching substring strings.
               # Here, giving it a little path_arc makes each part rotate into
               # their final positions, which feels appropriate for the idea of
               # rearranging an equation
               self.play(
                   TransformMatchingStrings(
                       lines[0].copy(), lines[1],
                       # matched_keys specifies which substring should
                       # line up. If it's not specified, the animation
                       # will align the longest matching substrings.
                       # In this case, the substring "^2 = C^2" would
                       # trip it up
                       matched_keys=["A^2", "B^2", "C^2"],
                       # When you want a substring from the source
                       # to go to a non-equal substring from the target,
                       # use the key map.
                       key_map={"+": "-"},
                       path_arc=90 * DEGREES,
                   ),
               )
               self.wait()
               self.play(TransformMatchingStrings(
                   lines[1].copy(), lines[2],
                   matched_keys=["A^2"]
               ))
               self.wait()
               self.play(
                   TransformMatchingStrings(
                       lines[2].copy(), lines[3],
                       key_map={"2": R"\sqrt"},
                       path_arc=-30 * DEGREES,
                   ),
               )
               self.wait(2)
               self.play(LaggedStartMap(FadeOut, lines, shift=2 * RIGHT))
       return jsonify({'message': 'Transformation applied successfully'})

   if __name__ == "__main__":
       app.run(debug=True)
   ```
</new_file>