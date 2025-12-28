import pygame
import random
import math
import sys
from datetime import datetime, timedelta

# 初始化pygame
pygame.init()

# 设置窗口
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2026跨年倒计时 - 新年快乐！")

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# 全局用于测试/模拟：如果不为None，则倒计时目标设置为当前时间加上该秒数
SIMULATE_SECONDS = None

# 烟花粒子类
class Particle:
    def __init__(self, x, y, vx, vy, color, life=1.0, size=3):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.life = life  # 生命值，1.0为完全可见，0.0为完全透明
        self.max_life = life
        self.size = size
        self.gravity = 0.15  # 重力加速度
        
    def update(self):
        # 更新位置
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity  # 重力影响
        # 速度衰减
        self.vx *= 0.98
        self.vy *= 0.98
        # 生命值衰减
        self.life -= 0.015
        
    def draw(self, surface):
        if self.life > 0:
            alpha = int(255 * self.life)
            color_with_alpha = (*self.color, alpha)
            # 创建一个临时surface用于绘制带透明度的粒子
            particle_surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
            pygame.draw.circle(particle_surface, color_with_alpha, (self.size, self.size), self.size)
            surface.blit(particle_surface, (self.x - self.size, self.y - self.size))
    
    def is_alive(self):
        return self.life > 0

# 烟花类
class Firework:
    def __init__(self, x, y_target):
        self.x = x
        self.y = HEIGHT
        self.y_target = y_target  # 爆炸目标高度
        self.vy = -random.uniform(8, 12)  # 上升速度
        self.exploded = False
        self.particles = []
        self.trail = []  # 上升轨迹
        
        # 随机选择鲜艳的颜色
        color_schemes = [
            [(255, 0, 0), (255, 165, 0), (255, 255, 0)],  # 红橙黄
            [(0, 255, 0), (0, 255, 255), (0, 150, 255)],  # 绿青蓝
            [(255, 0, 255), (255, 20, 147), (255, 105, 180)],  # 紫粉红
            [(255, 140, 0), (255, 215, 0), (255, 255, 0)],  # 金橙黄
            [(138, 43, 226), (75, 0, 130), (148, 0, 211)],  # 紫色系
            [(255, 0, 127), (255, 20, 147), (255, 105, 180)],  # 粉红系
        ]
        self.colors = random.choice(color_schemes)
        self.main_color = random.choice(self.colors)
        
    def update(self):
        if not self.exploded:
            # 上升阶段
            self.y += self.vy
            self.vy *= 0.98  # 轻微减速
            
            # 添加轨迹
            self.trail.append((self.x, self.y))
            if len(self.trail) > 5:
                self.trail.pop(0)
            
            # 检查是否到达目标高度
            if self.y <= self.y_target:
                self.explode()
        else:
            # 更新粒子
            for particle in self.particles[:]:
                particle.update()
                if not particle.is_alive():
                    self.particles.remove(particle)
    
    def explode(self):
        self.exploded = True
        num_particles = random.randint(80, 150)
        
        for _ in range(num_particles):
            # 随机角度和速度
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 8)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed - random.uniform(1, 3)  # 向上偏一点
            
            # 随机选择颜色
            color = random.choice(self.colors)
            # 添加一些颜色变化
            color = tuple(min(255, max(0, c + random.randint(-30, 30))) for c in color)
            
            # 随机大小和生命值
            size = random.randint(2, 5)
            life = random.uniform(0.7, 1.0)
            
            self.particles.append(Particle(self.x, self.y, vx, vy, color, life, size))
    
    def draw(self, surface):
        if not self.exploded:
            # 绘制上升轨迹
            for i, (tx, ty) in enumerate(self.trail):
                if len(self.trail) > 0:
                    alpha = int(255 * ((i + 1) / len(self.trail)))
                    trail_surface = pygame.Surface((4, 4), pygame.SRCALPHA)
                    color_with_alpha = (*self.main_color, alpha)
                    pygame.draw.circle(trail_surface, color_with_alpha, (2, 2), 2)
                    surface.blit(trail_surface, (tx - 2, ty - 2))
            
            # 绘制主体
            pygame.draw.circle(surface, self.main_color, (int(self.x), int(self.y)), 4)
            pygame.draw.circle(surface, WHITE, (int(self.x), int(self.y)), 2)
        else:
            # 绘制粒子
            for particle in self.particles:
                particle.draw(surface)
    
    def is_alive(self):
        if not self.exploded:
            return True
        return len(self.particles) > 0

# 获取倒计时
def get_countdown():
    now = datetime.now()
    # 目标：2026年1月1日 00:00:00
    # 如果启用了模拟，则将目标设为当前时间加上模拟秒数（用于演示最后几秒）
    if SIMULATE_SECONDS is not None:
        target = now + timedelta(seconds=SIMULATE_SECONDS)
    else:
        target = datetime(2026, 1, 1, 0, 0, 0)
    
    # 如果已经过了2026年1月1日，显示新年状态
    if now >= target:
        return "00:00:00", True
    
    delta = target - now
    total_seconds = int(delta.total_seconds())
    
    if total_seconds <= 0:
        return "00:00:00", True
    
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}", False

# 绘制带发光阴影的文字
def draw_text_with_glow(surface, text, font, x, y, color, glow_color=(255, 255, 100), glow_size=3):
    # 绘制多层阴影创造发光效果
    for i in range(glow_size, 0, -1):
        alpha = 150 // (i + 1)
        glow_text = font.render(text, True, glow_color)
        glow_text.set_alpha(alpha)
        for dx in range(-i, i+1):
            for dy in range(-i, i+1):
                if dx*dx + dy*dy <= i*i:
                    text_rect = glow_text.get_rect(center=(x + dx, y + dy))
                    surface.blit(glow_text, text_rect)
    
    # 绘制主文字
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    surface.blit(text_surface, text_rect)
    
    return text_rect

# 绘制带渐变边框的文字
def draw_text_with_gradient_border(surface, text, font, x, y, text_color, border_width=3):
    # 创建渐变颜色
    colors = [
        (255, 0, 0),    # 红
        (255, 165, 0),  # 橙
        (255, 255, 0),  # 黄
        (0, 255, 0),    # 绿
        (0, 255, 255),  # 青
        (0, 0, 255),    # 蓝
        (138, 43, 226), # 紫
    ]
    
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=(x, y))
    
    # 绘制渐变边框（多层）
    for i in range(border_width):
        color_idx = int((pygame.time.get_ticks() / 50 + i * 2) % len(colors))
        border_color = colors[color_idx]
        
        # 绘制边框文字（通过多次偏移绘制）
        for dx in [-i-1, 0, i+1]:
            for dy in [-i-1, 0, i+1]:
                if dx != 0 or dy != 0:
                    border_surface = font.render(text, True, border_color)
                    surface.blit(border_surface, text_rect.move(dx, dy))
    
    # 绘制主文字
    surface.blit(text_surface, text_rect)
    
    return text_rect

# 主函数
def main():
    clock = pygame.time.Clock()
    fireworks = []
    font_large = pygame.font.Font(None, 120)
    font_huge = pygame.font.Font(None, 150)
    font_title = pygame.font.Font(None, 100)
    
    last_firework_time = 0
    firework_interval = 800  # 每800毫秒发射一个烟花
    
    running = True
    new_year = False
    
    while running:
        current_time = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # 填充背景
        screen.fill(BLACK)
        
        # 获取倒计时
        countdown_text, is_new_year = get_countdown()
        new_year = is_new_year
        
        # 随机发射烟花
        if current_time - last_firework_time > firework_interval and not new_year:
            x = random.randint(100, WIDTH - 100)
            y_target = random.randint(HEIGHT // 4, HEIGHT // 2)
            fireworks.append(Firework(x, y_target))
            last_firework_time = current_time
        
        # 新年时发射更多烟花
        if new_year:
            if random.random() < 0.3:  # 30%概率每帧发射
                for _ in range(2):
                    x = random.randint(100, WIDTH - 100)
                    y_target = random.randint(HEIGHT // 4, HEIGHT // 2)
                    fireworks.append(Firework(x, y_target))
        
        # 更新和绘制烟花
        for firework in fireworks[:]:
            firework.update()
            firework.draw(screen)
            if not firework.is_alive():
                fireworks.remove(firework)
        
        # 绘制倒计时
        if not new_year:
            # 绘制"距离2026年还有"
            title_text = "距离2026年还有"
            title_surface = font_title.render(title_text, True, (200, 200, 255))
            title_rect = title_surface.get_rect(center=(WIDTH // 2, 150))
            screen.blit(title_surface, title_rect)
            
            # 绘制倒计时数字（带发光效果）
            draw_text_with_glow(
                screen, 
                countdown_text, 
                font_huge, 
                WIDTH // 2, 
                HEIGHT // 2 - 50,
                (255, 255, 255),
                glow_color=(100, 200, 255),
                glow_size=5
            )
        else:
            # 新年快乐！
            draw_text_with_gradient_border(
                screen,
                "xin nian kuai le！",
                font_huge,
                WIDTH // 2,
                HEIGHT // 2 - 100,
                WHITE,
                border_width=5
            )
            
            draw_text_with_gradient_border(
                screen,
                "Happy New Year 2026!",
                font_large,
                WIDTH // 2,
                HEIGHT // 2 + 50,
                WHITE,
                border_width=4
            )
        
        # 绘制底部提示
        if not new_year:
            hint_text = "按ESC退出"
            hint_surface = pygame.font.Font(None, 36).render(hint_text, True, (150, 150, 150))
            hint_rect = hint_surface.get_rect(center=(WIDTH // 2, HEIGHT - 50))
            screen.blit(hint_surface, hint_rect)
        
        pygame.display.flip()
        clock.tick(60)  # 60 FPS
    
    pygame.quit()

if __name__ == "__main__":
    main()

