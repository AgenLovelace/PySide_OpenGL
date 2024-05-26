#version 330 core

layout (location = 0) in vec3 position;
//layout (location = 1) in vec3 color;
//layout (location = 2) in vec2 tex_coord;

//out vec4 out_color;
//out vec2 out_text_coord;

void main()
{
   gl_Position = vec4(position, 1.0);
//   out_color = vec4(1.0, 0.5, 0.5, 1.0);
}