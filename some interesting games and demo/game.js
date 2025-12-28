// 游戏画布和上下文
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
canvas.width = 800;
canvas.height = 600;

// 游戏状态
let gameState = 'menu'; // menu, playing, paused, gameOver
let score = 0;
let lives = 3;
let level = 1;
let enemiesKilled = 0;
let enemiesToKill = 5;

// 游戏对象数组
let player = null;
let enemies = [];
let bullets = [];
let enemyBullets = [];
let walls = [];
let explosions = [];

// 键盘状态
const keys = {};

// 坦克类
class Tank {
    constructor(x, y, color, isPlayer = false) {
        this.x = x;
        this.y = y;
        this.width = 30;
        this.height = 30;
        this.color = color;
        this.angle = 0;
        this.speed = isPlayer ? 3 : 1.5;
        this.isPlayer = isPlayer;
        this.health = isPlayer ? 1 : 1;
        this.lastShot = 0;
        this.shootCooldown = isPlayer ? 300 : 1500;
        this.moveDirection = Math.random() * Math.PI * 2;
        this.moveTimer = 0;
        this.moveDuration = 2000 + Math.random() * 2000;
    }

    draw() {
        ctx.save();
        ctx.translate(this.x + this.width / 2, this.y + this.height / 2);
        ctx.rotate(this.angle);
        
        // 坦克主体
        ctx.fillStyle = this.color;
        ctx.fillRect(-this.width / 2, -this.height / 2, this.width, this.height);
        
        // 坦克边框
        ctx.strokeStyle = '#000';
        ctx.lineWidth = 2;
        ctx.strokeRect(-this.width / 2, -this.height / 2, this.width, this.height);
        
        // 炮管
        ctx.fillStyle = '#333';
        ctx.fillRect(this.width / 2 - 5, -3, 20, 6);
        
        // 坦克标识
        if (this.isPlayer) {
            ctx.fillStyle = '#fff';
            ctx.beginPath();
            ctx.arc(0, 0, 5, 0, Math.PI * 2);
            ctx.fill();
        }
        
        ctx.restore();
    }

    update() {
        if (this.isPlayer) {
            this.updatePlayer();
        } else {
            this.updateEnemy();
        }
        
        // 边界检测
        this.x = Math.max(0, Math.min(canvas.width - this.width, this.x));
        this.y = Math.max(0, Math.min(canvas.height - this.height, this.y));
    }

    updatePlayer() {
        let moved = false;
        
        if (keys['w'] || keys['W'] || keys['ArrowUp']) {
            this.y -= this.speed;
            this.angle = -Math.PI / 2;
            moved = true;
        }
        if (keys['s'] || keys['S'] || keys['ArrowDown']) {
            this.y += this.speed;
            this.angle = Math.PI / 2;
            moved = true;
        }
        if (keys['a'] || keys['A'] || keys['ArrowLeft']) {
            this.x -= this.speed;
            this.angle = Math.PI;
            moved = true;
        }
        if (keys['d'] || keys['D'] || keys['ArrowRight']) {
            this.x += this.speed;
            this.angle = 0;
            moved = true;
        }
        
        // 检查与墙壁的碰撞
        if (moved) {
            this.checkWallCollision();
        }
    }

    updateEnemy() {
        this.moveTimer += 16;
        
        // 定期改变移动方向
        if (this.moveTimer > this.moveDuration) {
            this.moveDirection = Math.random() * Math.PI * 2;
            this.moveTimer = 0;
            this.moveDuration = 2000 + Math.random() * 2000;
        }
        
        // 朝向玩家
        if (player) {
            const dx = player.x - this.x;
            const dy = player.y - this.y;
            this.angle = Math.atan2(dy, dx);
        }
        
        // 移动
        const newX = this.x + Math.cos(this.moveDirection) * this.speed;
        const newY = this.y + Math.sin(this.moveDirection) * this.speed;
        
        // 边界检测
        if (newX >= 0 && newX <= canvas.width - this.width) {
            this.x = newX;
        } else {
            this.moveDirection = Math.PI - this.moveDirection;
        }
        
        if (newY >= 0 && newY <= canvas.height - this.height) {
            this.y = newY;
        } else {
            this.moveDirection = -this.moveDirection;
        }
        
        // 检查与墙壁的碰撞
        this.checkWallCollision();
        
        // 随机射击
        if (Math.random() < 0.01 && Date.now() - this.lastShot > this.shootCooldown) {
            this.shoot(false);
        }
    }

    checkWallCollision() {
        for (let wall of walls) {
            if (this.isColliding(wall)) {
                // 回退位置
                if (this.isPlayer) {
                    if (keys['w'] || keys['W'] || keys['ArrowUp']) this.y += this.speed;
                    if (keys['s'] || keys['S'] || keys['ArrowDown']) this.y -= this.speed;
                    if (keys['a'] || keys['A'] || keys['ArrowLeft']) this.x += this.speed;
                    if (keys['d'] || keys['D'] || keys['ArrowRight']) this.x -= this.speed;
                } else {
                    this.moveDirection = Math.random() * Math.PI * 2;
                }
                break;
            }
        }
    }

    shoot(isPlayerBullet) {
        const now = Date.now();
        if (now - this.lastShot < this.shootCooldown) return;
        
        this.lastShot = now;
        
        const bulletX = this.x + this.width / 2 + Math.cos(this.angle) * (this.width / 2 + 10);
        const bulletY = this.y + this.height / 2 + Math.sin(this.angle) * (this.height / 2 + 10);
        
        if (isPlayerBullet) {
            bullets.push(new Bullet(bulletX, bulletY, this.angle, '#ffeb3b', true));
        } else {
            enemyBullets.push(new Bullet(bulletX, bulletY, this.angle, '#f44336', false));
        }
    }

    isColliding(other) {
        return this.x < other.x + other.width &&
               this.x + this.width > other.x &&
               this.y < other.y + other.height &&
               this.y + this.height > other.y;
    }

    takeDamage() {
        this.health--;
        return this.health <= 0;
    }
}

// 子弹类
class Bullet {
    constructor(x, y, angle, color, isPlayerBullet) {
        this.x = x;
        this.y = y;
        this.angle = angle;
        this.speed = 8;
        this.radius = 4;
        this.color = color;
        this.isPlayerBullet = isPlayerBullet;
    }

    draw() {
        ctx.fillStyle = this.color;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        ctx.fill();
        ctx.strokeStyle = '#fff';
        ctx.lineWidth = 1;
        ctx.stroke();
    }

    update() {
        this.x += Math.cos(this.angle) * this.speed;
        this.y += Math.sin(this.angle) * this.speed;
    }

    isOutOfBounds() {
        return this.x < 0 || this.x > canvas.width || 
               this.y < 0 || this.y > canvas.height;
    }
}

// 墙壁类
class Wall {
    constructor(x, y, width, height) {
        this.x = x;
        this.y = y;
        this.width = width;
        this.height = height;
    }

    draw() {
        ctx.fillStyle = '#7f8c8d';
        ctx.fillRect(this.x, this.y, this.width, this.height);
        ctx.strokeStyle = '#34495e';
        ctx.lineWidth = 2;
        ctx.strokeRect(this.x, this.y, this.width, this.height);
    }
}

// 爆炸效果类
class Explosion {
    constructor(x, y) {
        this.x = x;
        this.y = y;
        this.radius = 5;
        this.maxRadius = 40;
        this.life = 0;
        this.maxLife = 20;
    }

    draw() {
        const alpha = 1 - (this.life / this.maxLife);
        ctx.save();
        ctx.globalAlpha = alpha;
        ctx.fillStyle = '#ff9800';
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        ctx.fill();
        ctx.fillStyle = '#f44336';
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius * 0.6, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
    }

    update() {
        this.life++;
        this.radius = (this.life / this.maxLife) * this.maxRadius;
        return this.life < this.maxLife;
    }
}

// 初始化游戏
function initGame() {
    // 创建玩家坦克
    player = new Tank(canvas.width / 2, canvas.height - 100, '#4caf50', true);
    
    // 创建敌人
    enemies = [];
    enemiesToKill = 5 + level * 2;
    for (let i = 0; i < enemiesToKill; i++) {
        const x = Math.random() * (canvas.width - 100) + 50;
        const y = Math.random() * (canvas.height / 2) + 50;
        enemies.push(new Tank(x, y, '#f44336', false));
    }
    
    // 创建墙壁
    walls = [];
    // 随机生成一些墙壁
    for (let i = 0; i < 8 + level; i++) {
        const x = Math.random() * (canvas.width - 100);
        const y = Math.random() * (canvas.height - 100);
        const width = 40 + Math.random() * 40;
        const height = 40 + Math.random() * 40;
        walls.push(new Wall(x, y, width, height));
    }
    
    bullets = [];
    enemyBullets = [];
    explosions = [];
}

// 碰撞检测
function checkCollisions() {
    // 玩家子弹与敌人
    for (let i = bullets.length - 1; i >= 0; i--) {
        const bullet = bullets[i];
        
        // 与墙壁碰撞
        let hitWall = false;
        for (let wall of walls) {
            if (bullet.x > wall.x && bullet.x < wall.x + wall.width &&
                bullet.y > wall.y && bullet.y < wall.y + wall.height) {
                bullets.splice(i, 1);
                hitWall = true;
                break;
            }
        }
        if (hitWall) continue;
        
        // 与敌人碰撞
        for (let j = enemies.length - 1; j >= 0; j--) {
            const enemy = enemies[j];
            const dx = bullet.x - (enemy.x + enemy.width / 2);
            const dy = bullet.y - (enemy.y + enemy.height / 2);
            const distance = Math.sqrt(dx * dx + dy * dy);
            
            if (distance < enemy.width / 2 + bullet.radius) {
                bullets.splice(i, 1);
                if (enemy.takeDamage()) {
                    enemies.splice(j, 1);
                    explosions.push(new Explosion(enemy.x + enemy.width / 2, enemy.y + enemy.height / 2));
                    score += 100;
                    enemiesKilled++;
                    updateUI();
                    
                    // 检查是否完成关卡
                    if (enemies.length === 0) {
                        levelUp();
                    }
                }
                break;
            }
        }
        
        // 边界检测
        if (bullet.isOutOfBounds()) {
            bullets.splice(i, 1);
        }
    }
    
    // 敌人子弹与玩家
    for (let i = enemyBullets.length - 1; i >= 0; i--) {
        const bullet = enemyBullets[i];
        
        // 与墙壁碰撞
        let hitWall = false;
        for (let wall of walls) {
            if (bullet.x > wall.x && bullet.x < wall.x + wall.width &&
                bullet.y > wall.y && bullet.y < wall.y + wall.height) {
                enemyBullets.splice(i, 1);
                hitWall = true;
                break;
            }
        }
        if (hitWall) continue;
        
        // 与玩家碰撞
        if (player) {
            const dx = bullet.x - (player.x + player.width / 2);
            const dy = bullet.y - (player.y + player.height / 2);
            const distance = Math.sqrt(dx * dx + dy * dy);
            
            if (distance < player.width / 2 + bullet.radius) {
                enemyBullets.splice(i, 1);
                if (player.takeDamage()) {
                    lives--;
                    updateUI();
                    if (lives <= 0) {
                        gameOver(false);
                    } else {
                        // 重置玩家位置
                        player = new Tank(canvas.width / 2, canvas.height - 100, '#4caf50', true);
                    }
                }
                break;
            }
        }
        
        // 边界检测
        if (bullet.isOutOfBounds()) {
            enemyBullets.splice(i, 1);
        }
    }
    
    // 玩家与敌人碰撞
    if (player) {
        for (let enemy of enemies) {
            if (player.isColliding(enemy)) {
                // 推开玩家
                const dx = player.x - enemy.x;
                const dy = player.y - enemy.y;
                const distance = Math.sqrt(dx * dx + dy * dy);
                if (distance > 0) {
                    player.x += (dx / distance) * 5;
                    player.y += (dy / distance) * 5;
                }
            }
        }
    }
}

// 升级关卡
function levelUp() {
    level++;
    enemiesKilled = 0;
    updateUI();
    
    // 创建新一波敌人
    enemiesToKill = 5 + level * 2;
    for (let i = 0; i < enemiesToKill; i++) {
        const x = Math.random() * (canvas.width - 100) + 50;
        const y = Math.random() * (canvas.height / 2) + 50;
        enemies.push(new Tank(x, y, '#f44336', false));
    }
    
    // 重置玩家位置
    player = new Tank(canvas.width / 2, canvas.height - 100, '#4caf50', true);
    
    // 添加更多墙壁
    for (let i = 0; i < 3; i++) {
        const x = Math.random() * (canvas.width - 100);
        const y = Math.random() * (canvas.height - 100);
        const width = 40 + Math.random() * 40;
        const height = 40 + Math.random() * 40;
        walls.push(new Wall(x, y, width, height));
    }
}

// 更新UI
function updateUI() {
    document.getElementById('score').textContent = score;
    document.getElementById('lives').textContent = lives;
    document.getElementById('level').textContent = level;
}

// 游戏结束
function gameOver(won) {
    gameState = 'gameOver';
    const modal = document.getElementById('gameOverModal');
    const title = document.getElementById('gameOverTitle');
    const message = document.getElementById('gameOverMessage');
    const finalScore = document.getElementById('finalScore');
    
    if (won) {
        title.textContent = '🎉 恭喜通关！';
        message.textContent = `你成功通过了 ${level} 关！`;
    } else {
        title.textContent = '💥 游戏结束';
        message.textContent = '你的坦克被摧毁了！';
    }
    
    finalScore.textContent = score;
    modal.classList.add('show');
}

// 游戏主循环
function gameLoop() {
    if (gameState !== 'playing') return;
    
    // 清空画布
    ctx.fillStyle = '#2c3e50';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    // 绘制网格背景
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.1)';
    ctx.lineWidth = 1;
    for (let i = 0; i < canvas.width; i += 40) {
        ctx.beginPath();
        ctx.moveTo(i, 0);
        ctx.lineTo(i, canvas.height);
        ctx.stroke();
    }
    for (let i = 0; i < canvas.height; i += 40) {
        ctx.beginPath();
        ctx.moveTo(0, i);
        ctx.lineTo(canvas.width, i);
        ctx.stroke();
    }
    
    // 绘制墙壁
    for (let wall of walls) {
        wall.draw();
    }
    
    // 更新和绘制玩家
    if (player) {
        player.update();
        player.draw();
    }
    
    // 更新和绘制敌人
    for (let enemy of enemies) {
        enemy.update();
        enemy.draw();
    }
    
    // 更新和绘制子弹
    for (let bullet of bullets) {
        bullet.update();
        bullet.draw();
    }
    
    for (let bullet of enemyBullets) {
        bullet.update();
        bullet.draw();
    }
    
    // 更新和绘制爆炸效果
    for (let i = explosions.length - 1; i >= 0; i--) {
        const explosion = explosions[i];
        explosion.draw();
        if (!explosion.update()) {
            explosions.splice(i, 1);
        }
    }
    
    // 碰撞检测
    checkCollisions();
    
    requestAnimationFrame(gameLoop);
}

// 事件监听
document.addEventListener('keydown', (e) => {
    keys[e.key] = true;
    
    if (e.key === ' ' && gameState === 'playing') {
        e.preventDefault();
        if (player) {
            player.shoot(true);
        }
    }
});

document.addEventListener('keyup', (e) => {
    keys[e.key] = false;
});

// 按钮事件
document.getElementById('startBtn').addEventListener('click', () => {
    gameState = 'playing';
    score = 0;
    lives = 3;
    level = 1;
    enemiesKilled = 0;
    initGame();
    updateUI();
    document.getElementById('startBtn').disabled = true;
    document.getElementById('pauseBtn').disabled = false;
    document.getElementById('restartBtn').disabled = false;
    gameLoop();
});

document.getElementById('pauseBtn').addEventListener('click', () => {
    if (gameState === 'playing') {
        gameState = 'paused';
        document.getElementById('pauseBtn').textContent = '继续';
    } else if (gameState === 'paused') {
        gameState = 'playing';
        document.getElementById('pauseBtn').textContent = '暂停';
        gameLoop();
    }
});

document.getElementById('restartBtn').addEventListener('click', () => {
    gameState = 'playing';
    score = 0;
    lives = 3;
    level = 1;
    enemiesKilled = 0;
    initGame();
    updateUI();
    document.getElementById('pauseBtn').textContent = '暂停';
    document.getElementById('gameOverModal').classList.remove('show');
    gameLoop();
});

document.getElementById('playAgainBtn').addEventListener('click', () => {
    document.getElementById('restartBtn').click();
});

// 初始化
updateUI();

