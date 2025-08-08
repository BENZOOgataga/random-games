import type { World } from '../types';

export const circleHit = (ax:number,ay:number, ar:number, bx:number,by:number, br:number)=>{
  const dx=ax-bx, dy=ay-by; return dx*dx+dy*dy <= (ar+br)*(ar+br);
};

export const resolveCombat = (w:World)=>{
  // bullets vs ents
  for(const b of w.bullets){
    for(const e of w.ents){
      if(!b.friendly) continue;
      if(circleHit(b.x,b.y,b.r, e.x,e.y,e.r)){
        // @ts-ignore
        e.hp -= b.dmg; b.life = 0;
      }
    }
  }
  // remove dead ents and reward
  const kept = [] as typeof w.ents;
  for(const e of w.ents){
    // @ts-ignore
    if(e.hp<=0){ w.kills++; w.gems += 3; }
    else kept.push(e);
  }
  w.ents = kept;
};