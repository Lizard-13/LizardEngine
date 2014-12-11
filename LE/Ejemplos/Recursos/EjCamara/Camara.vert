#version 120

varying vec4 p;

void main(){
	gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
	gl_TexCoord[0] = gl_MultiTexCoord0;

	p = gl_ModelViewProjectionMatrix * gl_Vertex;
}
