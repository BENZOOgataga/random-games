import { TAU } from './math';
import type { Asteroid, Drone, Player } from './types';

let nextId = 1;
export const newId = ()=>nextId++;

export const newPlayer = ():Player=>({
  x:0,y:0,vx:0,vy:0,a:0,r:16,
  hp:100,hpMax:100,accel:180,drag:0.985,turn:12,
  boost:0,boostMax:1.8,boostRegen:0.25,
  fireCd:0,fireRate:10,dmg:12,bulletSpeed:540,
  upgrades:{ hp:0, gun:0, engine:0, cargo:0 }
});

export const newAsteroid = (rand:()=>number, x:number,y:number, size:number):Asteroid=>{
  const vx = (rand()-0.5)*80/Math.sqrt(size);
  const vy = (rand()-0.5)*80/Math.sqrt(size);
  const hp = 20 + size*12;
  const r = 10 + size*8;
  const n = 7 + (size|0);
  const pts = Array.from({length:n}, (_,i)=>{
    const ang = i/n*TAU + rand()*0.25; const rad = r * (0.75 + rand()*0.5); return { ang, rad };
  });
  return { id:newId(), type:'ast', x,y,vx,vy,a:rand()*TAU,av:(rand()-0.5)*0.6, r,hp,size, pts };
};

export const newDrone = (x:number,y:number):Drone=>({ id:newId(), type:'drone', x,y,vx:0,vy:0,a:0,r:14,hp:60,fireCd:0 });