// Generate PWA icons for Flavify
const { createCanvas } = require('canvas');
const fs = require('fs');

function generateIcon(size, outputPath) {
  const canvas = createCanvas(size, size);
  const ctx = canvas.getContext('2d');
  const s = size;

  // Background with rounded corners
  const r = s * 0.2;
  ctx.beginPath();
  ctx.moveTo(r, 0);
  ctx.lineTo(s - r, 0);
  ctx.quadraticCurveTo(s, 0, s, r);
  ctx.lineTo(s, s - r);
  ctx.quadraticCurveTo(s, s, s - r, s);
  ctx.lineTo(r, s);
  ctx.quadraticCurveTo(0, s, 0, s - r);
  ctx.lineTo(0, r);
  ctx.quadraticCurveTo(0, 0, r, 0);
  ctx.closePath();
  
  // Gradient background
  const grad = ctx.createLinearGradient(0, 0, s, s);
  grad.addColorStop(0, '#1a0a10');
  grad.addColorStop(1, '#0a0a12');
  ctx.fillStyle = grad;
  ctx.fill();

  // Accent circle glow
  const glowGrad = ctx.createRadialGradient(s*0.5, s*0.5, 0, s*0.5, s*0.5, s*0.45);
  glowGrad.addColorStop(0, 'rgba(230, 57, 70, 0.25)');
  glowGrad.addColorStop(1, 'rgba(230, 57, 70, 0)');
  ctx.fillStyle = glowGrad;
  ctx.fillRect(0, 0, s, s);

  // "F" letter
  ctx.fillStyle = '#ffffff';
  ctx.font = `bold ${s * 0.5}px sans-serif`;
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillText('F', s * 0.42, s * 0.48);

  // "y" in accent color
  ctx.fillStyle = '#e63946';
  ctx.font = `bold ${s * 0.35}px sans-serif`;
  ctx.fillText('y', s * 0.68, s * 0.52);

  const buffer = canvas.toBuffer('image/png');
  fs.writeFileSync(outputPath, buffer);
  console.log(`Generated ${outputPath} (${size}x${size})`);
}

generateIcon(192, './icons/icon-192.png');
generateIcon(512, './icons/icon-512.png');
console.log('Done!');
