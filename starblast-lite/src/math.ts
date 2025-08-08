export const TAU = Math.PI * 2;
export const clamp = (v:number,a:number,b:number)=>Math.max(a, Math.min(b, v));
export const lerp = (a:number,b:number,t:number)=>a+(b-a)*t;