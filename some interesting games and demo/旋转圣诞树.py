# ============================================
# 🎄 旋转圣诞树动画 - 带粒子特效 🎄
# 百万特效设计师出品
# ============================================

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle, Polygon
import random
import math

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# ============================================
# 1. 创建圣诞树形状
# ============================================
def create_christmas_tree():
    """创建圣诞树的多层三角形"""
    tree_layers = []
    
    # 树的主体（多层三角形）
    layers = [
        {'width': 8, 'height': 4, 'y': 8},   # 顶层
        {'width': 12, 'height': 5, 'y': 4},  # 中层
        {'width': 16, 'height': 6, 'y': -1}, # 底层
    ]
    
    for layer in layers:
        x_coords = [-layer['width']/2, 0, layer['width']/2, -layer['width']/2]
        y_coords = [layer['y'], layer['y'] + layer['height'], layer['y'], layer['y']]
        tree_layers.append({
            'x': x_coords,
            'y': y_coords,
            'color': '#228B22'  # 森林绿
        })
    
    # 树干
    trunk = {
        'x': [-2, 2, 2, -2, -2],
        'y': [-6, -6, -1, -1, -6],
        'color': '#8B4513'  # 棕色
    }
    
    return tree_layers, trunk

# ============================================
# 2. 创建装饰品（星星、彩球等）
# ============================================
def create_decorations():
    """创建圣诞树装饰品"""
    decorations = []
    
    # 树顶星星
    decorations.append({
        'type': 'star',
        'x': 0,
        'y': 12,
        'size': 2,
        'color': '#FFD700'
    })
    
    # 彩球装饰
    ball_positions = [
        (-3, 9), (3, 9), (-4, 5), (4, 5),
        (-5, 1), (5, 1), (-2, 6), (2, 6)
    ]
    ball_colors = ['#FF0000', '#0000FF', '#FFD700', '#FF1493', 
                   '#00FF00', '#FF6347', '#9370DB', '#00CED1']
    
    for i, (x, y) in enumerate(ball_positions):
        decorations.append({
            'type': 'ball',
            'x': x,
            'y': y,
            'size': 0.8,
            'color': ball_colors[i % len(ball_colors)]
        })
    
    return decorations

# ============================================
# 3. 创建粒子系统（雪花、星星粒子）
# ============================================
class ParticleSystem:
    def __init__(self, n_particles=100):
        self.n_particles = n_particles
        self.particles = []
        self.reset_particles()
    
    def reset_particles(self):
        """重置所有粒子"""
        self.particles = []
        for _ in range(self.n_particles):
            self.particles.append({
                'x': random.uniform(-20, 20),
                'y': random.uniform(-10, 15),
                'vx': random.uniform(-0.3, 0.3),
                'vy': random.uniform(-0.5, -0.1),
                'size': random.uniform(0.3, 1.5),
                'color': random.choice(['white', '#E0E0E0', '#F0F0F0', '#FFD700']),
                'type': random.choice(['snow', 'star']),
                'rotation': random.uniform(0, 2*math.pi),
                'rot_speed': random.uniform(-0.1, 0.1)
            })
    
    def update(self):
        """更新粒子位置"""
        for p in self.particles:
            # 更新位置
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['rotation'] += p['rot_speed']
            
            # 边界处理 - 从底部重新出现
            if p['y'] < -12:
                p['y'] = 15
                p['x'] = random.uniform(-20, 20)
            
            # 左右边界
            if p['x'] < -20:
                p['x'] = 20
            elif p['x'] > 20:
                p['x'] = -20

# ============================================
# 4. 绘制装饰品
# ============================================
def draw_decoration(ax, dec, rotation=0):
    """绘制装饰品"""
    if dec['type'] == 'star':
        # 绘制星星
        star_points = []
        for i in range(10):
            angle = i * math.pi / 5 + rotation
            if i % 2 == 0:
                r = dec['size']
            else:
                r = dec['size'] * 0.5
            x = dec['x'] + r * math.cos(angle)
            y = dec['y'] + r * math.sin(angle)
            star_points.append([x, y])
        
        star = Polygon(star_points, closed=True, 
                      facecolor=dec['color'], 
                      edgecolor='white', linewidth=1)
        ax.add_patch(star)
    
    elif dec['type'] == 'ball':
        # 绘制彩球
        circle = Circle((dec['x'], dec['y']), dec['size'],
                       facecolor=dec['color'],
                       edgecolor='white', linewidth=1)
        ax.add_patch(circle)
        
        # 高光效果
        highlight = Circle((dec['x'] - dec['size']*0.3, dec['y'] + dec['size']*0.3), 
                          dec['size']*0.3,
                          facecolor='white', alpha=0.6)
        ax.add_patch(highlight)

# ============================================
# 5. 绘制粒子
# ============================================
def draw_particles(ax, particles):
    """绘制粒子"""
    for p in particles:
        if p['type'] == 'snow':
            # 雪花 - 简单的点
            ax.scatter(p['x'], p['y'], s=p['size']*50, 
                      c=p['color'], alpha=0.8, marker='o')
        elif p['type'] == 'star':
            # 星星粒子
            star_size = p['size']
            angles = np.linspace(0, 2*math.pi, 5, endpoint=False) + p['rotation']
            x_star = p['x'] + star_size * np.cos(angles)
            y_star = p['y'] + star_size * np.sin(angles)
            ax.fill(x_star, y_star, color=p['color'], alpha=0.7)

# ============================================
# 6. 创建旋转动画
# ============================================
def create_rotating_tree_animation():
    """创建旋转圣诞树动画"""
    fig, ax = plt.subplots(figsize=(12, 10), facecolor='#000033')
    ax.set_facecolor('#000033')
    
    # 初始化粒子系统（减少粒子数量以加快速度）
    particle_system = ParticleSystem(n_particles=80)
    
    # 创建装饰品
    decorations = create_decorations()
    
    def animate(frame):
        ax.clear()
        ax.set_facecolor('#000033')
        
        # 计算旋转角度
        rotation_angle = frame * 0.05  # 控制旋转速度
        
        # 更新粒子
        particle_system.update()
        
        # 绘制粒子（背景层）
        draw_particles(ax, particle_system.particles)
        
        # 获取圣诞树数据
        tree_layers, trunk = create_christmas_tree()
        
        # 绘制树干（不旋转）
        trunk_poly = Polygon(list(zip(trunk['x'], trunk['y'])), 
                           closed=True,
                           facecolor=trunk['color'],
                           edgecolor='#654321', linewidth=2)
        ax.add_patch(trunk_poly)
        
        # 绘制旋转的树层
        for layer in tree_layers:
            # 应用旋转
            x_rotated = []
            y_rotated = []
            for x, y in zip(layer['x'], layer['y']):
                # 绕原点旋转
                x_rot = x * math.cos(rotation_angle) - y * math.sin(rotation_angle)
                y_rot = x * math.sin(rotation_angle) + y * math.cos(rotation_angle)
                x_rotated.append(x_rot)
                y_rotated.append(y_rot)
            
            tree_poly = Polygon(list(zip(x_rotated, y_rotated)),
                              closed=True,
                              facecolor=layer['color'],
                              edgecolor='#32CD32', linewidth=2)
            ax.add_patch(tree_poly)
        
        # 绘制旋转的装饰品
        for dec in decorations:
            # 计算装饰品的旋转位置
            x_rot = dec['x'] * math.cos(rotation_angle) - dec['y'] * math.sin(rotation_angle)
            y_rot = dec['x'] * math.sin(rotation_angle) + dec['y'] * math.cos(rotation_angle)
            
            dec_rotated = dec.copy()
            dec_rotated['x'] = x_rot
            dec_rotated['y'] = y_rot
            
            # 星星自身也旋转
            if dec['type'] == 'star':
                star_rotation = rotation_angle * 2
            else:
                star_rotation = 0
            
            draw_decoration(ax, dec_rotated, rotation=star_rotation)
        
        # 添加文字
        ax.text(0, -9, '🎄 2026 新年快乐 🎄', 
                fontsize=24, ha='center', color='#FFD700', 
                weight='bold', family='sans-serif')
        ax.text(0, -10.5, '💕 愿我们的爱情如圣诞树般长青 💕', 
                fontsize=16, ha='center', color='#FF69B4', 
                weight='bold', family='sans-serif')
        
        # 设置坐标轴
        ax.set_xlim(-20, 20)
        ax.set_ylim(-12, 15)
        ax.set_aspect('equal')
        ax.axis('off')
    
    # 创建动画（减少帧数以加快生成速度）
    print("🎬 正在生成旋转圣诞树动画...")
    print("⏳ 这可能需要1-2分钟，请耐心等待...")
    anim = FuncAnimation(fig, animate, frames=120, interval=50, repeat=True, blit=False)
    
    # 保存动画
    try:
        anim.save('旋转圣诞树动画.gif', writer='pillow', fps=20, dpi=100)
    except Exception as e:
        print(f"⚠️  使用pillow保存失败，尝试其他方法: {e}")
        # 尝试使用imagemagick（如果可用）
        try:
            anim.save('旋转圣诞树动画.gif', writer='imagemagick', fps=20)
        except:
            print("❌ 动画保存失败，但预览图已生成")
            return
    print("✅ 动画已保存：旋转圣诞树动画.gif")
    plt.close()

# ============================================
# 7. 创建静态预览图
# ============================================
def create_static_preview():
    """创建静态预览图"""
    fig, ax = plt.subplots(figsize=(12, 10), facecolor='#000033')
    ax.set_facecolor('#000033')
    
    # 创建粒子系统
    particle_system = ParticleSystem(n_particles=60)
    
    # 绘制粒子
    draw_particles(ax, particle_system.particles)
    
    # 获取圣诞树数据
    tree_layers, trunk = create_christmas_tree()
    
    # 绘制树干
    trunk_poly = Polygon(list(zip(trunk['x'], trunk['y'])), 
                        closed=True,
                        facecolor=trunk['color'],
                        edgecolor='#654321', linewidth=2)
    ax.add_patch(trunk_poly)
    
    # 绘制树层
    for layer in tree_layers:
        tree_poly = Polygon(list(zip(layer['x'], layer['y'])),
                           closed=True,
                           facecolor=layer['color'],
                           edgecolor='#32CD32', linewidth=2)
        ax.add_patch(tree_poly)
    
    # 绘制装饰品
    decorations = create_decorations()
    for dec in decorations:
        draw_decoration(ax, dec)
    
    # 添加文字
    ax.text(0, -9, '🎄 2026 新年快乐 🎄', 
            fontsize=24, ha='center', color='#FFD700', 
            weight='bold', family='sans-serif')
    ax.text(0, -10.5, '💕 愿我们的爱情如圣诞树般长青 💕', 
            fontsize=16, ha='center', color='#FF69B4', 
            weight='bold', family='sans-serif')
    
    ax.set_xlim(-20, 20)
    ax.set_ylim(-12, 15)
    ax.set_aspect('equal')
    ax.axis('off')
    
    plt.tight_layout()
    plt.savefig('旋转圣诞树_预览.png', dpi=300, facecolor='#000033', 
                bbox_inches='tight', pad_inches=0.2)
    print("✅ 预览图已保存：旋转圣诞树_预览.png")
    plt.close()

# ============================================
# 主函数
# ============================================
def main():
    print("""
╔═══════════════════════════════════════════════════════╗
║     🎄 旋转圣诞树动画 - 带粒子特效 🎄                  ║
╚═══════════════════════════════════════════════════════╝
    """)
    
    try:
        # 先创建预览图
        print("📸 生成预览图...")
        create_static_preview()
        
        # 创建动画
        print("\n🎬 生成旋转动画...")
        create_rotating_tree_animation()
        
        print("\n" + "="*50)
        print("🎉 完成！")
        print("="*50)
        print("\n📁 生成的文件：")
        print("   ✅ 旋转圣诞树_预览.png")
        print("   ✅ 旋转圣诞树动画.gif")
        print("\n💕 祝你和女朋友新年快乐！💕\n")
        
    except Exception as e:
        print(f"\n❌ 生成过程中出现错误：{e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

