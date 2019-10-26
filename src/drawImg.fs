
precision lowp float;

varying vec2 v_texcoord;

uniform sampler2D u_texture;

void main() {

    float distortion = 0.95;
    vec2 center=vec2(.5,.5);

   //gl_FragColor = texture2D(u_texture, v_texcoord);
   vec2 offset = v_texcoord - center;
   float stretch = distortion + (pow(offset.x,2.0)+ pow(offset.y,2.0))/5.0;
   gl_FragColor = texture2D(u_texture, center + offset * stretch);
}
