# PyOpenGL

Toy OpenGL setup using python for the driver code.


## OpenGL concepts


**Vertex**: a point in the world, used to define a boundary / to join surfaces. (We can technically also just render point clouds directly but that is an exceptional scenario).

**Triangle**: most common geometric primitive we deal with in graphics. It is defined by 3 poitns and a normal vector (indicate the front face of the triangle / it is **perpendicular to the surface**).

---

<details>
  <summary> <strong>Question.</strong> Why don't we use rectangles instead of triangles?</summary>

  ```
  Versatility. Geometry class: the three points of a triangle always exist in a single plane. 
  ```
</details>

---

**Frame Buffer** The Frame Buffer is a portion of graphics memory that holds the scene data. This buffer contains details such as the width and height of the surface (in pixels), color of each pixel, and depth and stencil buffers. Once all the fragments are processed, a 2D image is formed and displayed on the screen. The frame buffer is the final destination of the rendering pipeline


### Rendering pipeline

The graphics / rendering pipelien is the sequence of steps the GPU must follow in order to render a 3D scene to the screen.

There are 3 major steps involved: **application**, **gemoetry** and **rasterization**.

![3-steps](https://i.stack.imgur.com/osX19.png)

- **application**: this is executed by the CPU before sending data to the GPU.  Here we handle scene changes, e.g. a chacter animation or user input. It involves tasks such as collission detection, optimizing data in RAM, calculating animations, etc...
    - for our purposes we can ignore the details -- this would be handled for e.g. by a game engine before off-loading data to the graphics hardware
- **geometry**: the "work horse" of the graphics process. Most operations invovlving polygons and vertices are performed here. At the end of this step we end with a (2D) "description" of what actually has to be shown on the screen
    - so it handles **per-vertex** operations
- **rasterization**: think of it as the "painter" stage. at this point we have continous (geometric) primitives that will be turned into descrete fragments (fragment here means pixel or point on the grid).
    - at this step we basically start filling the colors (and illumination) pixel by pixel. we also apply any textures on the objects 
    - here we also determine which fragment is visible (in case polygons are overlapping). We usually use a Z-buffer to hidden surface determination
    - ***question***: *how do we prevent the user from seing partial images?* 
        - **double buffering** - The rasterization is carried out in a special memory area. Once the image has been *completely rasterized*, it is copied to the visible area of the image memory. 
        - ![Example](http://n64devkit.square7.ch/kantan/step2/2/img00008.gif)


So, in summary:

![3-step-2](https://i.stack.imgur.com/G34Py.png)

### The Geometry step
The geometry step, which is responsible for the majority of operations with polygons and their
vertices, can be divided into 5 tasks.

For each, it might be useful to think of an analogy - you are the director of a theatre play (congrats 🎉) and here is how each of the steps would go. (technical details in the dropdown)

**1. Model / Camera transformaton**

<details>
  <summary> <strong>Analogy:</strong> Think of this as the stage setup. Before the play begins, the actors (3D models) are positioned on the stage (world space) according to the script (model transformation). The camera (view transformation) is then moved to its position to capture the scene from a specific perspective, similar to how the view transformation moves the camera in the 3D scene.</summary>

  <hr> 
  <strong>Technical:</strong> 
  Besides the objects, the scene defines a virtual camera / viewer (from where are we looking at the objects). This camera indicates the position and the viewing angle from which to render the scene. 
  In order to simplify later projection and clipping, the scene is transformed so that the camera is at its origin, facing along the Z axis. The resulting coordinate system is called the camera coordinate system and the transformation is called the view transformation.
</details>


**2. Illumination (Lighting / Shading)**
<details>
  <summary> <strong>Analogy: </strong> This is akin to the lighting design in a theater. Just as a lighting designer decides where to place lights to highlight different parts of the stage and create shadows, the illumination step in the graphics pipeline determines how light affects the objects in the scene. It calculates how light bounces off surfaces, creating shadows and highlights that make the scene look realistic.</summary>

  <hr> 
  <strong>Technical: </strong> A scene often contains light sources placed at different positions to make the
lighting of the objects appear more realistic. This step calculates a texture enhancement factor <strong>for each vertex</strong> based on the light sources and the material properties associated with the corresponding triangle. 

General lighting (<strong>ambient light</strong>) is applied to all surfaces. It is the diffuse and thus <strong>direction-independent</strong> brightness of the scene. The sun is a <strong>directional light source</strong> that can be assumed to be infinitely distant. The lighting effect of the sun on a surface is determined by the formation of the scalar product of the directional vector from the sun and the normal vector of the surface. If the value is negative, the surface is facing the sun.
  
</details>

**3. Viewing transforamtion (Perspective / Orthographic)**
<details>
  <summary> <strong>Analogy:</strong> Imagine the camera lens changing from a wide-angle lens to a telephoto lens. A perspective projection is like using a wide-angle lens, where objects farther away appear smaller, mimicking how our eyes perceive the world. An orthographic projection, on the other hand, is like using a telephoto lens, where objects maintain their size regardless of distance, which is useful for technical or architectural drawings.</summary>

  <hr> 
  <strong>Technical:</strong> This step transforms the visible volume (the 3d scene) into a cube with corner point coordinates (-1, -1, -1, -1) and (1,1,1,1). <em>This transformation is called projection, <strong>although it transforms a volume into another volume</strong></em>. A central projection is used for a perspective image, and two additional clipping planes are used to limit the number of displayed objects, creating a visible volume that is a pyramid stump (Frustum). Parallel or orthogonal projection is used for technical representations, as it maintains the size and parallelism of objects regardless of their distance from the viewer.

  <hr> <strong>Even more details</strong>
  For efficiency reasons, the camera and projection matrix are usually combined in a transformation matrix, so that the camera coordinate system is ignored. The resulting matrix is usually consistent for a single image, while the world matrix looks different for each object. In practice, therefore, view and projection are pre-calculated, so that only the World-Matrix has to be adjusted during display. However, more complex transformations (e.g. vertex blending) are possible.  In the actual rendering step, the model matrix * camera (view) matrix * projection matrix is then calculated and finally applied to each individual point.

![image](https://i.imgur.com/rVyhq2G.png)
  
</details>

**4. Clipping**
<details>
  <summary> <strong>Analogy:</strong> This is like a director deciding which parts of the play to keep and which to cut out (or hide behind the stage walls) because the audience will not be able to see them. In the graphics pipeline, clipping removes objects that are outside the camera's view (the view frustum), ensuring that only the relevant parts of the scene are processed further.</summary>

  <hr> 
  <strong>Technical:</strong> Only the primitives that are located within the visible volume must actually be rasterized. Primitives that are completely out of sight are discarded, a process known as frustum culling. Primitives that are only partially inside the cube must be clipped against the cube. The advantage of the previous projection step is that clipping always takes place against the same cube, ensuring that only the possibly clipped primitives that are within the visible volume are forwarded to the next step. <strong>
  The advantage of the previous projection step is that clipping always takes place against the same cube. Only the - possibly clipped - primitives that are within the visible volume are forwarded to the next step.</strong>
</details>

**5. Projection (to Screen Space)**
<details>
  <summary> <strong>Analogy:</strong> Finally, this is like projecting the stage onto a screen. The final transformation takes the 3D scene and projects it onto a 2D screen, similar to how a projector displays the stage on a screen. This step ensures that the final image is correctly displayed on the computer screen.</summary>

  <hr> 
  <strong>Technical:</strong> To output the image to any viewport on the screen, a further transformation, the Window Viewport Transformation, must be applied. This is a shift, followed by scaling, resulting in the device coordinates of the output device. The viewport contains values for the height and width of the window in pixels, the lower left-hand corner of the window in window coordinates, and the minimum and maximum values for Z. This step ensures that the final image is correctly projected onto the 2D screen.
  
</details>

---

NB. The order of these stages is not gospel. While some clearly depend on others, diffrent graphics APIs can execute them in diffrent order. This is how OpenGL does it though.

---

### What the F are shaders?

A program fo the GPU
- that is **user-defined**
- and allows to take control of certain programable stages of the [rendering pipeline](#rendering-pipeline)
- each stage has a separate set of inputs and outputs, as well as built-in variables -- so a shader can only control **one stage** (e.g. cannot use a shader which alters geometry to raster the image)

The most common ones are the [**Vertex Shader**](#vertex-shader) and the [**Fragment Shader**](#fragment-shader), though more exists (e.g. you can do general computations with a Compute Shader -- **way way out of scope**).

For OpenGL, shaderes **MUST** be written in [OpenGL Shading Language (GLSL)](https://www.khronos.org/opengl/wiki/OpenGL_Shading_Language). (well, there are extension to allow for other programs but it is **out of scope**). 

The language is similar to C but of course the compute model is more restricted (e.g. no pointers, no recusrion).

> In GLSL-based pipelines, all processing steps of the graphics card can be programmed directly, with the exception of rasterization.

### Typical Shader
This is a dummy shader to show how GLSL works:

```glsl
#version 330 core // defines the version of the version of GLSL being used 

// Variables defined with the in keyword stay and (user-defined) inputs we get from
// a previous step in the graphics pipeline
// e.g. a vertex shader can output data that a fragment shader can recieve as in
// (the variables must have the same name in both programs for this to work!!!)
in vec3 info;
// output data (in for the next step(s))
out vec3 vertexColor;

// Values that stay constant for the whole mesh.
uniform mat4 MVP;
uniform vec3 triangleColor;

// Here we do the compute ... We do not return any value directly
// but we need to set/update the values we pass as `out`.

// There might also be default outputs we need to have. E.g a 
// vertex shader must output a gl_Position (vec4)
void main() {

    // Output position of the vertex, same as the input position.
    gl_Position = MVP * vec4(vertexPosition_modelspace, 1);

    // Pass the color to the fragment shader.
    vertexColor = triangleColor;
}
```

### Vertex Shader

- The most common kind of 3D shader
- Run once for each vertex given to the graphics processor
- purpose: transform each vertex's 3D position in virtual space to the 2D coordinate at which it appears on the screen (as well as a depth value for the Z-buffer)
    - crucial for determining which vertices are visible to the camera and should be rendered. By doing so, it simplifies the subsequent stages of the graphics pipeline, as the GPU has less data to process
- The shader only has access to the vertex (including its texture coordinates, normal and other transferred data), but not to neighbouring vertices, the topology or similar.


Vertex shaders can manipulate properties such as position, color and texture coordinates, but **CANNOT create new vertices**. The output of the vertex shader goes to the next stage in the pipeline, which is either a geometry shader if present, or the rasterizer. Vertex shaders can enable powerful control over the details of position, movement, lighting, and color in any scene involving 3D models. 


The vertex shader receives a single vertex from the list of vertices as input. It then performs a series of matrix multiplications to determine the vertex's final position in clip-space (**vec4**). This process involves three key matrices: the model matrix, the view matrix, and the projection matrix. The model matrix transforms the vertex's position relative to the model's origin. The view matrix then positions the model in the world, and finally, the projection matrix projects the 3D scene onto the 2D screen. The result of these operations is the vertex's position in clip-space, which is stored in the special variable.


### Fragment Shader
The fragment shader is executed **once for every fragment** (pixels before they are displayed on the display device). The colour for the corresponding fragment is calculated here. 

- operates on fragments generated by the rasterization stage. For each pixel covered by a primitive, a fragment is created. The fragment shader processes these fragments to determine their final color values
- here we apply lighting, shadows, texture mapping, etc...
- (advanced): Fragment shaders can define multiple output variables, which can be used to write data to different buffers in the framebuffer. This flexibility allows for advanced rendering techniques, such as deferred shading and multi-pass rendering

