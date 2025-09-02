const learnBtn = document.getElementById('learnBtn');
const foodBtn = document.getElementById('foodBtn');
const wellBtn = document.getElementById('wellBtn');
const learnPanel = document.getElementById('learnPanel');
const foodPanel = document.getElementById('foodPanel');
const wellPanel = document.getElementById('wellPanel');

function hideAll(){learnPanel.classList.add('hidden');foodPanel.classList.add('hidden');wellPanel.classList.add('hidden')}
learnBtn.onclick = ()=>{hideAll();learnPanel.classList.remove('hidden')}
foodBtn.onclick = ()=>{hideAll();foodPanel.classList.remove('hidden')}
wellBtn.onclick = ()=>{hideAll();wellPanel.classList.remove('hidden')}
