import { newPlayer } from './entities';
import type { World } from './types';

export const newWorld = (seed:number):World=>({
  width:6000, height:4000, seed, time:0, tick:0,
  player:newPlayer(), ents:[], bullets:[], particles:[],
  gems:0, kills:0, level:1, nextWaveAt:10,
});