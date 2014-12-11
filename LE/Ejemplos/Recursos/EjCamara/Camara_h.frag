#version 120

uniform sampler2D textura;
uniform float blurH;

void main(){
	//Blur gaussiano horizontal
	vec4 sum = vec4(0.0);
	sum += texture2D(textura, vec2(gl_TexCoord[0].x - 4.0*blurH, gl_TexCoord[0].y)) * 0.05;
	sum += texture2D(textura, vec2(gl_TexCoord[0].x - 3.0*blurH, gl_TexCoord[0].y)) * 0.09;
	sum += texture2D(textura, vec2(gl_TexCoord[0].x - 2.0*blurH, gl_TexCoord[0].y)) * 0.12;
	sum += texture2D(textura, vec2(gl_TexCoord[0].x - blurH, gl_TexCoord[0].y)) * 0.15;
	sum += texture2D(textura, vec2(gl_TexCoord[0].x, gl_TexCoord[0].y)) * 0.16;
	sum += texture2D(textura, vec2(gl_TexCoord[0].x + blurH, gl_TexCoord[0].y)) * 0.15;
	sum += texture2D(textura, vec2(gl_TexCoord[0].x + 2.0*blurH, gl_TexCoord[0].y)) * 0.12;
	sum += texture2D(textura, vec2(gl_TexCoord[0].x + 3.0*blurH, gl_TexCoord[0].y)) * 0.09;
	sum += texture2D(textura, vec2(gl_TexCoord[0].x + 4.0*blurH, gl_TexCoord[0].y)) * 0.05;
	gl_FragColor = sum;
}
