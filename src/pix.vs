
precision lowp float;

attribute vec3 a_position;
attribute vec4 a_shading;

uniform mat4 u_matrix;
uniform float u_glyphByRow;
uniform float u_glyphByCol;

uniform float u_inLetterWidth;
uniform float u_inLetterHeight;
uniform float u_pixelSize;
uniform float u_times;

varying vec2 v_texcoord;

varying vec4 u_shades;

varying vec2 v_shadecoord;
varying float v_glyphId;
varying float v_glyphX;
varying float v_glyphY;



#define GET_X(x) (mod((x),1.0))
#define GET_Y(y,rem,mod) GET_X((((y)-(rem))/ (mod)))

float osci(float period , float phase){
//return [0,1]
    return abs(mod(u_times+(phase*period),period)/period  - 0.5)*2.0 ;
}

vec4 shade(vec4 invec){
        
    float p =  GET_X(invec.x);
    float i1 =  GET_Y(invec.x,p,10.0);
    float j1 =  GET_Y(invec.x,i1,100.0);
    float k1 =  GET_Y(invec.x,j1,1000.0);

    float phase =  GET_X(invec.y);
    float i2 =  GET_Y(invec.y,phase,10.0);
    float j2 =  GET_Y(invec.y,i2,100.0);
    float k2 =  GET_Y(invec.y,j2,1000.0);
    
    float ph =  GET_X(invec.z);
    float i3 =  GET_Y(invec.z,phase,10.0);
    float j3 =  GET_Y(invec.z,i3,100.0);
    float k3 =  GET_Y(invec.z,j3,1000.0);
    
    
    float pd =  GET_X(invec.w);
    float i4 =  GET_Y(invec.w,phase,10.0);
    float j4 =  GET_Y(invec.w,i4,100.0);
    float k4 =  GET_Y(invec.w,j4,1000.0);
        
    return mix(  vec4(i1,j1,k1,0.9)*1.1,
                vec4(i2,j2,k2,0.9)*1.1,
                osci(p*11.0,phase*11.0) );
     
}

void main() {
  //direct in clip space :d 
  gl_Position =  vec4(a_position.xy,1.0,1.0);
  

  // getting glyphId 
  v_glyphId = a_position.z;
  
  v_glyphX= ( mod(v_glyphId,u_glyphByRow )  );
  v_glyphY= ((v_glyphId - v_glyphX) / u_glyphByCol ) / u_inLetterHeight;

  v_glyphX = v_glyphX / u_inLetterWidth;
    

  //vec3 color1 = mix(vec3(1.0, 0.0, 0.0), vec3(0.0, 1.0, 0.0), float(v_glyphX < 3.0 && v_glyphX>2.0));


    u_shades = shade(a_shading);

    //j =  i |  3;
  //u_shades.z = vec4(float(GET_X(a_shading.x)),0.0,0.0,1.0)






  gl_PointSize=u_pixelSize;
}


