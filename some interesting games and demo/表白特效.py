# ============================================
# 💕 新年表白特效 - 2026快乐！💕
# 百万特效设计师出品 - Python版
# ============================================

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle
import matplotlib.patches as mpatches
import random
import math

# 设置中文字体（如果系统支持）
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# ============================================
# 1. 创建爱心形状
# ============================================
def create_heart(t):
    """使用参数方程创建爱心形状"""
    x = 16 * np.sin(t)**3
    y = 13 * np.cos(t) - 5 * np.cos(2*t) - 2 * np.cos(3*t) - np.cos(4*t)
    return x, y

# ============================================
# 2. 创建静态爱心图
# ============================================
def create_static_heart():
    """创建静态爱心表白图"""
    fig, ax = plt.subplots(figsize=(12, 10), facecolor='black')
    ax.set_facecolor('black')
    
    # 绘制爱心
    t = np.linspace(0, 2*np.pi, 1000)
    x, y = create_heart(t)
    
    # 绘制多个爱心层叠效果
    colors = ['#FF69B4', '#FF1493', '#FF6347', '#FFD700']
    sizes = [1.0, 0.9, 0.8, 0.7]
    
    for i, (color, size) in enumerate(zip(colors, sizes)):
        x_scaled = x * size
        y_scaled = y * size
        ax.fill(x_scaled, y_scaled, color=color, alpha=0.7-i*0.15, 
                edgecolor='white', linewidth=2)
    
    # 添加文字
    ax.text(0, 15, '💕 新年快乐 2026 💕', 
            fontsize=32, ha='center', color='#FFD700', 
            weight='bold', family='sans-serif')
    ax.text(0, -18, '愿我们的爱情如烟花般绚烂\n愿新的一年充满幸福与美好', 
            fontsize=20, ha='center', color='white', 
            family='sans-serif', linespacing=1.5)
    
    ax.set_xlim(-25, 25)
    ax.set_ylim(-25, 20)
    ax.axis('off')
    ax.set_aspect('equal')
    
    plt.tight_layout()
    plt.savefig('表白特效_静态爱心.png', dpi=300, facecolor='black', 
                bbox_inches='tight', pad_inches=0.2)
    print("✅ 静态爱心图已保存：表白特效_静态爱心.png")
    plt.close()

# ============================================
# 3. 创建文字特效图
# ============================================
def create_text_effect():
    """创建文字特效图"""
    fig, ax = plt.subplots(figsize=(14, 10), facecolor='#1a1a2e')
    ax.set_facecolor('#1a1a2e')
    
    # 添加背景装饰星星
    for _ in range(100):
        x = random.uniform(-10, 10)
        y = random.uniform(-5, 5)
        size = random.uniform(0.5, 2)
        ax.scatter(x, y, s=size*50, c='white', alpha=0.6, marker='*')
    
    # 主标题
    ax.text(0, 3, '🎉 2026 新年快乐 🎉', 
            fontsize=40, ha='center', color='#FFD700', 
            weight='bold', family='sans-serif')
    
    # 副标题
    ax.text(0, 1, '💕 愿我们的爱情永远甜蜜 💕', 
            fontsize=28, ha='center', color='#FF69B4', 
            weight='bold', family='sans-serif')
    
    # 祝福文字
    ax.text(0, -1, '愿新的一年\n充满幸福、快乐与美好', 
            fontsize=22, ha='center', color='white', 
            family='sans-serif', linespacing=1.8)
    
    # 结尾
    ax.text(0, -3.5, '💖 爱你到永远 💖', 
            fontsize=24, ha='center', color='#FF1493', 
            weight='bold', family='sans-serif')
    
    ax.set_xlim(-10, 10)
    ax.set_ylim(-5, 5)
    ax.axis('off')
    
    plt.tight_layout()
    plt.savefig('表白特效_文字.png', dpi=300, facecolor='#1a1a2e', 
                bbox_inches='tight', pad_inches=0.3)
    print("✅ 文字特效图已保存：表白特效_文字.png")
    plt.close()

# ============================================
# 4. 创建烟花爱心组合特效
# ============================================
def create_firework_heart_combo():
    """创建烟花和爱心组合特效"""
    fig, ax = plt.subplots(figsize=(14, 10), facecolor='#000033')
    ax.set_facecolor('#000033')
    
    # 创建多个爱心
    colors = ['#FF69B4', '#FF1493', '#FF6347', '#FF4500', '#FFD700']
    positions = [(-20, 5), (-10, 8), (0, 5), (10, 8), (20, 5)]
    
    for i, ((px, py), color) in enumerate(zip(positions, colors)):
        t = np.linspace(0, 2*np.pi, 200)
        x, y = create_heart(t)
        x = x * 0.4 + px
        y = y * 0.4 + py
        ax.fill(x, y, color=color, alpha=0.8, 
                edgecolor='white', linewidth=1.5)
    
    # 创建烟花效果
    firework_colors = ['#FFD700', '#FF69B4', '#00FFFF', '#FF1493', 
                      '#FF6347', '#00FF00', '#FF4500', '#9370DB']
    
    for center_x in [-25, -15, -5, 5, 15, 25]:
        for center_y in [10, 15]:
            color = random.choice(firework_colors)
            n_particles = 30
            for angle in np.linspace(0, 2*np.pi, n_particles):
                radius = random.uniform(2, 6)
                x = center_x + radius * np.cos(angle)
                y = center_y + radius * np.sin(angle)
                size = random.uniform(20, 80)
                ax.scatter(x, y, s=size, c=color, alpha=0.7, 
                          edgecolors='white', linewidths=0.5)
    
    # 添加文字
    ax.text(0, -12, '🎆 2026 新年快乐 🎆', 
            fontsize=36, ha='center', color='#FFD700', 
            weight='bold', family='sans-serif')
    ax.text(0, -16, '💕 愿我们的爱情如烟花般绚烂夺目 💕', 
            fontsize=24, ha='center', color='#FF69B4', 
            weight='bold', family='sans-serif')
    
    ax.set_xlim(-30, 30)
    ax.set_ylim(-20, 20)
    ax.axis('off')
    ax.set_aspect('equal')
    
    plt.tight_layout()
    plt.savefig('表白特效_烟花爱心.png', dpi=300, facecolor='#000033', 
                bbox_inches='tight', pad_inches=0.2)
    print("✅ 烟花爱心特效已保存：表白特效_烟花爱心.png")
    plt.close()

# ============================================
# 5. 创建动画效果
# ============================================
def create_animation():
    """创建跳动的爱心动画"""
    fig, ax = plt.subplots(figsize=(10, 8), facecolor='black')
    ax.set_facecolor('black')
    
    def animate(frame):
        ax.clear()
        ax.set_facecolor('black')
        
        # 计算缩放和颜色变化
        scale = 1 + 0.15 * np.sin(frame * 0.2)
        alpha = 0.7 + 0.3 * np.sin(frame * 0.15)
        
        # 绘制爱心
        t = np.linspace(0, 2*np.pi, 500)
        x, y = create_heart(t)
        x = x * scale
        y = y * scale
        
        # 渐变颜色
        colors_list = ['#FF69B4', '#FF1493', '#FF6347']
        color = colors_list[frame % len(colors_list)]
        
        ax.fill(x, y, color=color, alpha=alpha, 
                edgecolor='white', linewidth=2)
        
        # 添加文字
        ax.text(0, 15, '💕 新年快乐 2026 💕', 
                fontsize=28, ha='center', color='#FFD700', 
                weight='bold', family='sans-serif')
        ax.text(0, -18, '愿我们的爱情永远甜蜜', 
                fontsize=18, ha='center', color='white', 
                family='sans-serif')
        
        ax.set_xlim(-25, 25)
        ax.set_ylim(-25, 20)
        ax.axis('off')
        ax.set_aspect('equal')
    
    anim = FuncAnimation(fig, animate, frames=100, interval=50, repeat=True)
    anim.save('表白特效_动画.gif', writer='pillow', fps=20, dpi=100)
    print("✅ 动画已保存：表白特效_动画.gif")
    plt.close()

# ============================================
# 6. 创建超炫酷特效（多个爱心旋转）
# ============================================
def create_rotating_hearts():
    """创建旋转爱心特效"""
    fig, ax = plt.subplots(figsize=(14, 10), facecolor='#000033')
    ax.set_facecolor('#000033')
    
    # 创建多个旋转的爱心
    n_hearts = 8
    colors = plt.cm.rainbow(np.linspace(0, 1, n_hearts))
    
    for i in range(n_hearts):
        angle = i * 2 * np.pi / n_hearts
        radius = 12
        center_x = radius * np.cos(angle)
        center_y = radius * np.sin(angle)
        
        t = np.linspace(0, 2*np.pi, 200)
        x, y = create_heart(t)
        x = x * 0.3 + center_x
        y = y * 0.3 + center_y
        
        ax.fill(x, y, color=colors[i], alpha=0.7, 
                edgecolor='white', linewidth=1.5)
    
    # 中心大爱心
    t = np.linspace(0, 2*np.pi, 500)
    x, y = create_heart(t)
    ax.fill(x, y, color='#FFD700', alpha=0.9, 
            edgecolor='white', linewidth=3)
    
    # 添加文字
    ax.text(0, -20, '🎉 2026 新年快乐 🎉', 
            fontsize=32, ha='center', color='#FFD700', 
            weight='bold', family='sans-serif')
    ax.text(0, -24, '💕 愿我们的爱情如星辰般永恒 💕', 
            fontsize=22, ha='center', color='#FF69B4', 
            weight='bold', family='sans-serif')
    
    ax.set_xlim(-25, 25)
    ax.set_ylim(-28, 20)
    ax.axis('off')
    ax.set_aspect('equal')
    
    plt.tight_layout()
    plt.savefig('表白特效_旋转爱心.png', dpi=300, facecolor='#000033', 
                bbox_inches='tight', pad_inches=0.2)
    print("✅ 旋转爱心特效已保存：表白特效_旋转爱心.png")
    plt.close()

# ============================================
# 主函数 - 生成所有特效
# ============================================
def generate_all_effects():
    """生成所有特效"""
    print("🎨 开始生成表白特效...\n")
    
    try:
        print("💕 生成静态爱心图...")
        create_static_heart()
        
        print("\n📝 生成文字特效图...")
        create_text_effect()
        
        print("\n🎆 生成烟花爱心组合特效...")
        create_firework_heart_combo()
        
        print("\n💫 生成旋转爱心特效...")
        create_rotating_hearts()
        
        print("\n🎬 生成动画...")
        try:
            create_animation()
        except Exception as e:
            print(f"⚠️  动画生成失败（可能需要安装pillow）：{e}")
            print("   但静态图片已成功生成！")
        
        print("\n" + "="*50)
        print("🎉 所有特效生成完成！")
        print("="*50)
        print("\n📁 生成的文件：")
        print("   ✅ 表白特效_静态爱心.png")
        print("   ✅ 表白特效_文字.png")
        print("   ✅ 表白特效_烟花爱心.png")
        print("   ✅ 表白特效_旋转爱心.png")
        print("   ✅ 表白特效_动画.gif（如果成功）")
        print("\n💕 祝你和女朋友新年快乐，2026年幸福美满！💕\n")
        
    except Exception as e:
        print(f"\n❌ 生成过程中出现错误：{e}")
        print("\n💡 提示：请确保已安装必要的Python库：")
        print("   pip install matplotlib numpy pillow")

# ============================================
# 运行主函数
# ============================================
if __name__ == "__main__":
    print("""
╔═══════════════════════════════════════════════════════╗
║     💕 新年表白特效 Python版 - 2026快乐 💕            ║
╚═══════════════════════════════════════════════════════╝
    """)
    
    # 检查依赖
    try:
        import matplotlib
        import numpy
        print("✅ 依赖库检查通过！\n")
    except ImportError as e:
        print("❌ 缺少必要的库，请先安装：")
        print("   pip install matplotlib numpy pillow")
        print("\n然后在VS Code/Cursor中运行此脚本即可！")
        exit(1)
    
    # 生成所有特效
    generate_all_effects()

