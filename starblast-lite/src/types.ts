export type Vec = { x:number; y:number };
export type Bullet = { id:number; x:number; y:number; vx:number; vy:number; life:number; dmg:number; r:number; friendly:boolean };
export type Asteroid = { id:number; type:'ast'; x:number; y:number; vx:number; vy:number; a:number; av:number; r:number; hp:number; size:number; pts:{ang:number; rad:number}[] };
export type Drone = { id:number; type:'drone'; x:number; y:number; vx:number; vy:number; a:number; r:number; hp:number; fireCd:number };
export type Entity = Asteroid | Drone;
export type Player = { x:number; y:number; vx:number; vy:number; a:number; r:number; hp:number; hpMax:number; accel:number; drag:number; turn:number; boost:number; boostMax:number; boostRegen:number; fireCd:number; fireRate:number; dmg:number; bulletSpeed:number; upgrades: Record<string,number> };
export type World = { width:number; height:number; seed:number; time:number; tick:number; player:Player; ents:Entity[]; bullets:Bullet[]; particles:Particle[]; gems:number; kills:number; level:number; nextWaveAt:number };
export type Particle = { type:'spark'|'gem'; x:number; y:number; vx:number; vy:number; r:number; life:number };