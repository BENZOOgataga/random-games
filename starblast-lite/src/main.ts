import { bindInput } from './input';
import { bindUI, updateHUD, ui } from './ui';
import { createGame, startGame, hardReset, frame } from './game';
import { resize } from "./render";

const cv = document.getElementById('game') as HTMLCanvasElement;
const g = createGame(cv);

bindInput(cv);
bindUI(()=>{ startGame(g); requestAnimationFrame(t=>frame(g,t)); }, ()=>{ hardReset(g); updateHUD(g.world); });
addEventListener('resize', ()=>resize(cv));

// simple pause/help
addEventListener('keydown', e=>{
  if(e.code==='KeyP') g.paused = !g.paused;
  if(e.code==='KeyH') ui.overlay.classList.toggle('show');
});

// HUD tick
setInterval(()=>updateHUD(g.world), 100);