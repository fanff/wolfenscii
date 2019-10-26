
precision lowp float;

// Passed in from the vertex shader.
varying vec2 v_texcoord;
varying vec4 u_shades;

varying float v_glyphId;
varying float v_glyphX;
varying float v_glyphY;

uniform sampler2D u_texture;
uniform float u_glyphByRow;
uniform float u_glyphByCol;

void main() {
   
   gl_FragColor = texture2D(u_texture, vec2(v_glyphX+(gl_PointCoord.x/u_glyphByRow ),
                                            v_glyphY+gl_PointCoord.y/u_glyphByCol) ) ;
   
   gl_FragColor *= u_shades;

}


