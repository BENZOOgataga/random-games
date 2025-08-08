import type { World } from './types';

export const ui = {
  hp: document.getElementById('hpbar') as HTMLSpanElement,
  gems: document.getElementById('gems') as HTMLElement,
  lvl: document.getElementById('lvl') as HTMLElement,
  kills: document.getElementById('kills') as HTMLElement,
  overlay: document.getElementById('overlay') as HTMLDivElement,
  startBtn: document.getElementById('startBtn') as HTMLButtonElement,
  resetBtn: document.getElementById('resetBtn') as HTMLButtonElement,
};

export const bindUI = (start:()=>void, reset:()=>void)=>{
  ui.startBtn.onclick = ()=>{ ui.overlay.classList.remove('show'); start(); };
  ui.resetBtn.onclick = ()=>{ reset(); };
};

export const updateHUD = (w:World)=>{
  ui.gems.textContent = String(w.gems);
  ui.lvl.textContent = String(w.level);
  ui.kills.textContent = String(w.kills);
  ui.hp.style.width = `${Math.max(0, Math.min(1, w.player.hp/w.player.hpMax))*100}%`;
};