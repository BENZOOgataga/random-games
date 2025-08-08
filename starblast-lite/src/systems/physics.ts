import { clamp } from '../math';
import type { World, Bullet } from '../types';

export const integrate = (w:World, dt:number)=>{
  // player
  const p = w.player; p.x += p.vx*dt; p.y += p.vy*dt; p.vx *= p.drag; p.vy *= p.drag;
  // bullets
  for(const b of w.bullets){ b.x += b.vx*dt; b.y += b.vy*dt; b.life -= dt; }
  w.bullets = w.bullets.filter(b=>b.life>0);
  // ents
  for(const e of w.ents){
    e.x += e.vx*dt; e.y += e.vy*dt; // wrap
    const W=w.width/2,H=w.height/2;
    if(e.x<-W) e.x+=w.width; if(e.x>W) e.x-=w.width;
    if(e.y<-H) e.y+=w.height; if(e.y>H) e.y-=w.height;
    // simple rot
    // @ts-ignore
    if('av' in e) e.a += (e as any).av*dt;
  }
};

export const wrapPoint = (w:World, x:number, y:number)=>{
  const W=w.width/2,H=w.height/2;
  if(x<-W) x+=w.width; if(x>W) x-=w.width;
  if(y<-H) y+=w.height; if(y>H) y-=w.height;
  return {x,y};
};