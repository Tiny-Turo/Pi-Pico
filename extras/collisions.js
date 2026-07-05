// I made all of TS

import "./utilities/utilities.js";

let lastTime;
window.time = {
  deltaTime: 0,
  time: 0,
  timeSpeed: 1,
  maxFPS: 2000,
};

const SECTOR = { x: 200, y: 720, radius: 300, startAngle: 2, endAngle: 4 };
const RADIUS2 = 70;

function update(currentTime) {
  // Calculate delta time
  // time.deltaTime = ((currentTime - lastTime) / 1000) * time.timeSpeed;
  // lastTime = currentTime;
  // time.time = currentTime / 1000;

  // ctx.clearRect(0, 0, canvas.width, canvas.height);
  // ctx.fillStyle = "white";
  // ctx.fillRect(0, 0, canvas.width, canvas.height);

  // ctx.fillStyle = "black";
  // ctx.beginPath();
  // ctx.arc(
  //   SECTOR.x,
  //   SECTOR.y,
  //   SECTOR.radius,
  //   SECTOR.startAngle + Math.PI,
  //   SECTOR.endAngle + Math.PI,
  // );
  // ctx.lineTo(SECTOR.x, SECTOR.y);
  // ctx.fill();

  let dx = SECTOR.x - mouse.x;
  let dy = SECTOR.y - mouse.y;
  let distance = Math.sqrt(dx * dx + dy * dy);

  let angleNorm = (Math.atan2(dy, dx) + Math.PI * 2) % (Math.PI * 2);

  // ctx.fillStyle = "rgba(0, 0, 0, 0.2)";
  // ctx.beginPath();
  // ctx.moveTo(SECTOR.x, SECTOR.y);
  // ctx.lineTo(
  //   mouse.x + Math.cos(angleNorm + Math.PI / 2) * RADIUS2,
  //   mouse.y + Math.sin(angleNorm + Math.PI / 2) * RADIUS2,
  // );
  // ctx.lineTo(
  //   mouse.x + Math.cos(angleNorm - Math.PI / 2) * RADIUS2,
  //   mouse.y + Math.sin(angleNorm - Math.PI / 2) * RADIUS2,
  // );
  // ctx.fill();

  let dx1 = SECTOR.x - (mouse.x + Math.cos(angleNorm + Math.PI / 2) * RADIUS2);
  let dy1 = SECTOR.y - (mouse.y + Math.sin(angleNorm + Math.PI / 2) * RADIUS2);
  let ang1 = (Math.atan2(dy1, dx1) + Math.PI * 2) % (Math.PI * 2);

  let dx2 = SECTOR.x - (mouse.x + Math.cos(angleNorm - Math.PI / 2) * RADIUS2);
  let dy2 = SECTOR.y - (mouse.y + Math.sin(angleNorm - Math.PI / 2) * RADIUS2);
  let ang2 = (Math.atan2(dy2, dx2) + Math.PI * 2) % (Math.PI * 2);

  const COLLISION =
    (((ang1 < SECTOR.endAngle && ang1 > SECTOR.startAngle) ||
      (ang2 < SECTOR.endAngle && ang2 > SECTOR.startAngle)) &&
      distance < RADIUS2 + SECTOR.radius) ||
    distance < RADIUS2;
  console.log(COLLISION);

  // ctx.fillStyle = COLLISION ? "green" : "red";
  // ctx.beginPath();
  // ctx.arc(mouse.x, mouse.y, RADIUS2, 0, 2 * Math.PI);
  // ctx.fill();

  // if (time.deltaTime < 1 / time.maxFPS) {
  //   setTimeout(
  //     () => {
  //       requestAnimationFrame(update);
  //     },
  //     (1 / time.maxFPS - time.deltaTime) * 1000,
  //   );
  // } else {
  //   requestAnimationFrame(update);
  // }
}

requestAnimationFrame(function (currentTime) {
  lastTime = currentTime;
  update(currentTime);
});
