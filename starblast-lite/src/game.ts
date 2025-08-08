import { createRng } from './rng';
import { lerp } from './math';
import { input } from './input';
import { newWorld } from './world';
import { render, resize } from "./render";
import { spawnWave } from './systems/spawn';
import { integrate } from './systems/physics';
import { resolveCombat } from './systems/combat';
import type { World } from './types';

export type Game = { cv:HTMLCanvasElement; ctx:CanvasRenderingContext2D; cam:{x:number;y:number;z:number}; running:boolean; paused:boolean; dt:number; tacc:number; rand:()=>number; world:World };

export const createGame = (cv:HTMLCanvasElement):Game=>{
  const ctx = cv.getContext('2d')!; resize(cv);
  const seed = (Date.now()|0) ^ 0xBADF00D;
  const rand = createRng(seed);
  const world = newWorld(seed);
  const cam = { x:0, y:0, z:1 };
  return { cv, ctx, cam, running:false, paused:false, dt:1/120, tacc:0, rand, world };
};

export const startGame = (g:Game)=>{ g.running = true; };
export const hardReset = (g:Game)=>{ const seed=(Date.now()|0)^0xBADC0DE; g.rand=createRng(seed); g.world=newWorld(seed); };

export const update = (g:Game)=>{
  const w = g.world; w.time += g.dt; w.tick++;
  // controls -> physics
  const p = w.player;
  const dx = input.mx - g.cv.width/2; const dy = input.my - g.cv.height/2; // screen space aim
  const targetA = Math.atan2(dy, dx);
  const da = ((targetA - p.a + Math.PI) % (Math.PI*2)) - Math.PI; // shortest
  p.a += da * 0.2; // soft turn
  const thrust = (input.up?1:0) + (input.down?-0.6:0);
  const strafe = (input.left?-1:0) + (input.right?1:0);
  const spd = p.accel * (1 + (input.boost?0.7:0));
  if(input.boost) p.boost = Math.min(p.boostMax, p.boost + p.boostRegen*g.dt);
  p.vx += Math.cos(p.a)*thrust*spd*g.dt + Math.cos(p.a+Math.PI/2)*strafe*spd*0.7*g.dt;
  p.vy += Math.sin(p.a)*thrust*spd*g.dt + Math.sin(p.a+Math.PI/2)*strafe*spd*0.7*g.dt;

  // shooting
  p.fireCd -= g.dt;
  if(input.shoot && p.fireCd<=0){
    p.fireCd = 1/Math.max(2, p.fireRate);
    const bs = p.bulletSpeed;
    const bx = p.x + Math.cos(p.a)*18; const by = p.y + Math.sin(p.a)*18;
    w.bullets.push({ id:Date.now()+Math.random(), x:bx,y:by, vx:Math.cos(p.a)*bs, vy:Math.sin(p.a)*bs, life:1.2, dmg:p.dmg, r:3, friendly:true });
  }

  // waves
  if(w.time >= w.nextWaveAt) spawnWave(w, g.rand);

  integrate(w, g.dt);
  resolveCombat(w);

  // cam follow
  g.cam.x = lerp(g.cam.x, p.x, 0.08); g.cam.y = lerp(g.cam.y, p.y, 0.08);
};

export const frame = (g:Game, t:number)=>{
  if(!g.running) return;
  if(!g.paused){
    // fixed step
    g.tacc += Math.min(0.05, (t - (frame as any).lt || 0)/1000);
    (frame as any).lt = t;
    while(g.tacc >= g.dt){ update(g); g.tacc -= g.dt; }
  }
  render(g.cv, g.ctx, g.world, g.cam);
  requestAnimationFrame(t2=>frame(g,t2));
};