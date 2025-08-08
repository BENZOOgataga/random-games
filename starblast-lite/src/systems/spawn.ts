import { newAsteroid, newDrone } from '../entities';
import type { World } from '../types';

export const spawnWave = (w:World, rand:()=>number)=>{
  const nAst = 10 + w.level*3;
  const W=w.width, H=w.height;
  for(let i=0;i<nAst;i++){
    const x = (rand()*W - W/2)|0; const y = (rand()*H - H/2)|0; const size = 1 + (rand()*2)|0;
    w.ents.push(newAsteroid(rand,x,y,size));
  }
  const nDrone = Math.min(2 + (w.level/2)|0, 6);
  for(let i=0;i<nDrone;i++){
    const x = (rand()*W - W/2)|0; const y = (rand()*H - H/2)|0;
    w.ents.push(newDrone(x,y));
  }
  w.level++;
  w.nextWaveAt += 20;
};