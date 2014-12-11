#version 120

uniform sampler2D textura;
uniform float blurV;

varying vec4 p;

void main(){
	//Blur gaussiano vertical
	vec4 sum = vec4(0.0);
	sum += texture2D(textura, vec2(gl_TexCoord[0].x, gl_TexCoord[0].y - 4.0*blurV)) * 0.05;
	sum += texture2D(textura, vec2(gl_TexCoord[0].x, gl_TexCoord[0].y - 3.0*blurV)) * 0.09;
	sum += texture2D(textura, vec2(gl_TexCoord[0].x, gl_TexCoord[0].y - 2.0*blurV)) * 0.12;
	sum += texture2D(textura, vec2(gl_TexCoord[0].x, gl_TexCoord[0].y - blurV)) * 0.15;
	sum += texture2D(textura, vec2(gl_TexCoord[0].x, gl_TexCoord[0].y)) * 0.16;
	sum += texture2D(textura, vec2(gl_TexCoord[0].x, gl_TexCoord[0].y + blurV)) * 0.15;
	sum += texture2D(textura, vec2(gl_TexCoord[0].x, gl_TexCoord[0].y + 2.0*blurV)) * 0.12;
	sum += texture2D(textura, vec2(gl_TexCoord[0].x, gl_TexCoord[0].y + 3.0*blurV)) * 0.09;
	sum += texture2D(textura, vec2(gl_TexCoord[0].x, gl_TexCoord[0].y + 4.0*blurV)) * 0.05;
	
	gl_FragColor = sum;
	
	
	/*
	//Escala de grises
	float gray = dot(sum.rgb, vec3(0.299, 0.587, 0.114));
	gl_FragColor = vec4(gray, gray, gray, gl_Color.a);
	*/
	
	
	//gl_FragColor = texture2D(textura, vec2(gl_TexCoord[0].x + cos(10*p.y)/20.0, gl_TexCoord[0].y));
}
