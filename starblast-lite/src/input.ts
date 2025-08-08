export type Input = { up:number; down:number; left:number; right:number; shoot:number; boost:number; mx:number; my:number; mdown:number };
export const input: Input = { up:0, down:0, left:0, right:0, shoot:0, boost:0, mx:0, my:0, mdown:0 };
export const bindInput = (canvas:HTMLCanvasElement)=>{
  addEventListener('keydown', e=>{
    if(e.code==='KeyW'||e.code==='ArrowUp') input.up=1;
    if(e.code==='KeyS'||e.code==='ArrowDown') input.down=1;
    if(e.code==='KeyA'||e.code==='ArrowLeft') input.left=1;
    if(e.code==='KeyD'||e.code==='ArrowRight') input.right=1;
    if(e.code==='Space') input.boost=1;
  });
  addEventListener('keyup', e=>{
    if(e.code==='KeyW'||e.code==='ArrowUp') input.up=0;
    if(e.code==='KeyS'||e.code==='ArrowDown') input.down=0;
    if(e.code==='KeyA'||e.code==='ArrowLeft') input.left=0;
    if(e.code==='KeyD'||e.code==='ArrowRight') input.right=0;
    if(e.code==='Space') input.boost=0;
  });
  canvas.addEventListener('mousemove', e=>{ input.mx=e.clientX; input.my=e.clientY; });
  canvas.addEventListener('mousedown', ()=>{ input.mdown=1; input.shoot=1; });
  addEventListener('mouseup', ()=>{ input.mdown=0; input.shoot=0; });
};