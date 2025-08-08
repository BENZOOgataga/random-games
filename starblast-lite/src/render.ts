import { TAU } from './math';
import type { World, Asteroid, Drone, Bullet, Particle } from './types';

export const resize = (cv:HTMLCanvasElement)=>{ cv.width = innerWidth; cv.height = innerHeight; };

export const render = (cv:HTMLCanvasElement, ctx:CanvasRenderingContext2D, w:World, cam:{x:number;y:number;z:number})=>{
  ctx.clearRect(0,0,cv.width,cv.height);
  // bg stars
  ctx.fillStyle = '#070a12'; ctx.fillRect(0,0,cv.width,cv.height);
  ctx.save();
  ctx.translate(cv.width/2, cv.height/2); ctx.scale(cam.z, cam.z); ctx.translate(-cam.x, -cam.y);

  // draw ents
  for(const e of w.ents){
    if(e.type==='ast') drawAst(ctx,e as Asteroid);
    else drawDrone(ctx,e as Drone);
  }
  // bullets
  ctx.fillStyle = '#cfe4ff';
  for(const b of w.bullets){ ctx.beginPath(); ctx.arc(b.x,b.y,b.r,0,TAU); ctx.fill(); }
  // player
  drawShip(ctx, w.player.x, w.player.y, w.player.a);

  // particles
  for(const p of w.particles){ drawParticle(ctx,p); }

  ctx.restore();
};

function drawShip(ctx:CanvasRenderingContext2D, x:number,y:number,a:number){
  ctx.save(); ctx.translate(x,y); ctx.rotate(a);
  ctx.strokeStyle = '#66d1ff'; ctx.lineWidth = 2; ctx.beginPath();
  ctx.moveTo(16,0); ctx.lineTo(-12,10); ctx.lineTo(-8,0); ctx.lineTo(-12,-10); ctx.closePath();
  ctx.stroke();
  ctx.restore();
}

function drawAst(ctx:CanvasRenderingContext2D, e:Asteroid){
  ctx.save(); ctx.translate(e.x,e.y); ctx.rotate(e.a);
  ctx.strokeStyle = '#8aa0b8'; ctx.beginPath();
  for(let i=0;i<e.pts.length;i++){
    const p=e.pts[i]; const x=Math.cos(p.ang)*p.rad, y=Math.sin(p.ang)*p.rad;
    if(i===0) ctx.moveTo(x,y); else ctx.lineTo(x,y);
  }
  ctx.closePath(); ctx.stroke(); ctx.restore();
}

function drawDrone(ctx:CanvasRenderingContext2D, e:Drone){
  ctx.save(); ctx.translate(e.x,e.y); ctx.rotate(e.a);
  ctx.strokeStyle = '#ff6a6a'; ctx.lineWidth=2; ctx.beginPath();
  ctx.arc(0,0,e.r,0,TAU); ctx.moveTo(-6,0); ctx.lineTo(6,0); ctx.stroke();
  ctx.restore();
}

function drawParticle(ctx:CanvasRenderingContext2D, p:Particle){
  ctx.save(); ctx.translate(p.x,p.y); ctx.globalAlpha = Math.max(0, Math.min(1, p.life));
  if(p.type==='spark'){ ctx.fillStyle='#cfe4ff'; ctx.fillRect(-p.r/2,-p.r/2,p.r,p.r); }
  else { ctx.fillStyle='#4bb6ff'; ctx.beginPath(); ctx.arc(0,0,p.r,0,TAU); ctx.fill(); }
  ctx.restore();
}