# ============================================
# 💕 新年表白特效 - 2026快乐！💕
# 百万特效设计师出品
# ============================================

# 安装必要的包（如果还没有安装）
if (!require("ggplot2")) install.packages("ggplot2")
if (!require("gganimate")) install.packages("gganimate")
if (!require("dplyr")) install.packages("dplyr")
if (!require("magick")) install.packages("magick")

library(ggplot2)
library(gganimate)
library(dplyr)
library(magick)

# ============================================
# 1. 创建爱心形状数据
# ============================================
create_heart <- function(n = 100) {
  t <- seq(0, 2*pi, length.out = n)
  x <- 16 * sin(t)^3
  y <- 13 * cos(t) - 5 * cos(2*t) - 2 * cos(3*t) - cos(4*t)
  return(data.frame(x = x, y = y))
}

# ============================================
# 2. 创建烟花粒子效果
# ============================================
create_fireworks <- function(n_fireworks = 5, n_particles = 50) {
  fireworks <- data.frame()
  for (i in 1:n_fireworks) {
    center_x <- runif(1, -20, 20)
    center_y <- runif(1, 5, 15)
    angle <- seq(0, 2*pi, length.out = n_particles)
    radius <- runif(n_particles, 0, 8)
    x <- center_x + radius * cos(angle)
    y <- center_y + radius * sin(angle)
    fireworks <- rbind(fireworks, 
                      data.frame(x = x, y = y, 
                                firework_id = i,
                                color = rainbow(n_fireworks)[i]))
  }
  return(fireworks)
}

# ============================================
# 3. 创建动画帧数据
# ============================================
n_frames <- 100
heart_data <- create_heart(200)

# 创建多帧数据用于动画
animation_data <- data.frame()
for (frame in 1:n_frames) {
  # 爱心数据
  heart_frame <- heart_data %>%
    mutate(frame = frame,
           type = "heart",
           alpha = 0.8 + 0.2 * sin(frame * 0.1))
  
  # 烟花数据（每10帧更新一次）
  if (frame %% 10 == 1) {
    fireworks_data <- create_fireworks(3, 30) %>%
      mutate(frame = frame,
             type = "firework",
             alpha = 1 - (frame %% 10) / 10)
  } else {
    fireworks_data <- data.frame()
  }
  
  animation_data <- rbind(animation_data, heart_frame, fireworks_data)
}

# ============================================
# 4. 绘制静态爱心图（基础版）
# ============================================
create_static_heart <- function() {
  heart <- create_heart(200)
  
  p <- ggplot(heart, aes(x = x, y = y)) +
    geom_polygon(fill = "#FF69B4", color = "#FF1493", size = 2, alpha = 0.8) +
    coord_fixed() +
    theme_void() +
    theme(plot.background = element_rect(fill = "#000000"),
          plot.title = element_text(color = "#FFD700", size = 24, hjust = 0.5, face = "bold"),
          plot.subtitle = element_text(color = "#FFFFFF", size = 18, hjust = 0.5)) +
    labs(title = "💕 新年快乐 2026 💕",
         subtitle = "愿我们的爱情如烟花般绚烂\n愿新的一年充满幸福与美好")
  
  return(p)
}

# ============================================
# 5. 创建动态爱心动画
# ============================================
create_animated_heart <- function() {
  # 创建多帧爱心数据
  frames_data <- data.frame()
  for (frame in 1:60) {
    heart <- create_heart(200)
    scale <- 1 + 0.1 * sin(frame * 0.2)
    heart <- heart %>%
      mutate(x = x * scale,
             y = y * scale,
             frame = frame)
    frames_data <- rbind(frames_data, heart)
  }
  
  p <- ggplot(frames_data, aes(x = x, y = y, group = frame)) +
    geom_polygon(fill = "#FF69B4", color = "#FF1493", size = 2, alpha = 0.8) +
    coord_fixed(xlim = c(-25, 25), ylim = c(-20, 20)) +
    theme_void() +
    theme(plot.background = element_rect(fill = "#000000"),
          plot.title = element_text(color = "#FFD700", size = 20, hjust = 0.5, face = "bold"),
          plot.subtitle = element_text(color = "#FFFFFF", size = 16, hjust = 0.5)) +
    labs(title = "💕 新年快乐 2026 💕",
         subtitle = "愿我们的爱情如烟花般绚烂") +
    transition_states(frame, transition_length = 2, state_length = 1) +
    ease_aes('sine-in-out')
  
  return(p)
}

# ============================================
# 6. 创建文字特效图
# ============================================
create_text_effect <- function() {
  # 创建背景
  bg <- data.frame(x = 0, y = 0)
  
  p <- ggplot(bg, aes(x = x, y = y)) +
    geom_blank() +
    xlim(-10, 10) +
    ylim(-5, 5) +
    theme_void() +
    theme(plot.background = element_rect(fill = "#1a1a2e"),
          plot.title = element_text(color = "#FFD700", size = 32, hjust = 0.5, 
                                    face = "bold", margin = margin(b = 20)),
          plot.subtitle = element_text(color = "#FF69B4", size = 24, hjust = 0.5,
                                       margin = margin(t = 10, b = 10)),
          plot.caption = element_text(color = "#FFFFFF", size = 18, hjust = 0.5,
                                     margin = margin(t = 20))) +
    labs(title = "🎉 2026 新年快乐 🎉",
         subtitle = "💕 愿我们的爱情永远甜蜜 💕",
         caption = "愿新的一年\n充满幸福、快乐与美好\n\n💖 爱你到永远 💖")
  
  return(p)
}

# ============================================
# 7. 创建烟花爱心组合特效
# ============================================
create_firework_heart_combo <- function() {
  # 创建多个爱心
  hearts <- data.frame()
  colors <- c("#FF69B4", "#FF1493", "#FF6347", "#FF4500", "#FFD700")
  
  for (i in 1:5) {
    heart <- create_heart(100)
    offset_x <- (i - 3) * 15
    offset_y <- (i %% 2) * 5
    heart <- heart %>%
      mutate(x = x * 0.5 + offset_x,
             y = y * 0.5 + offset_y,
             heart_id = i,
             color = colors[i])
    hearts <- rbind(hearts, heart)
  }
  
  # 创建烟花
  fireworks <- create_fireworks(8, 40)
  
  p <- ggplot() +
    # 绘制烟花
    geom_point(data = fireworks, aes(x = x, y = y, color = color), 
               size = 2, alpha = 0.7) +
    # 绘制爱心
    geom_polygon(data = hearts, aes(x = x, y = y, fill = color, group = heart_id),
                 color = "white", size = 1, alpha = 0.8) +
    scale_color_identity() +
    scale_fill_identity() +
    coord_fixed(xlim = c(-30, 30), ylim = c(-10, 20)) +
    theme_void() +
    theme(plot.background = element_rect(fill = "#000033"),
          plot.title = element_text(color = "#FFD700", size = 28, hjust = 0.5, 
                                    face = "bold", margin = margin(b = 15)),
          plot.subtitle = element_text(color = "#FF69B4", size = 20, hjust = 0.5)) +
    labs(title = "🎆 2026 新年快乐 🎆",
         subtitle = "💕 愿我们的爱情如烟花般绚烂夺目 💕")
  
  return(p)
}

# ============================================
# 8. 主函数 - 生成所有特效
# ============================================
generate_all_effects <- function() {
  cat("🎨 开始生成表白特效...\n\n")
  
  # 1. 静态爱心
  cat("💕 生成静态爱心图...\n")
  p1 <- create_static_heart()
  ggsave("表白特效_静态爱心.png", p1, width = 12, height = 10, dpi = 300)
  cat("✅ 静态爱心图已保存！\n\n")
  
  # 2. 文字特效
  cat("📝 生成文字特效图...\n")
  p2 <- create_text_effect()
  ggsave("表白特效_文字.png", p2, width = 12, height = 10, dpi = 300)
  cat("✅ 文字特效图已保存！\n\n")
  
  # 3. 烟花爱心组合
  cat("🎆 生成烟花爱心组合特效...\n")
  p3 <- create_firework_heart_combo()
  ggsave("表白特效_烟花爱心.png", p3, width = 14, height = 10, dpi = 300)
  cat("✅ 烟花爱心特效已保存！\n\n")
  
  # 4. 尝试创建动画（如果gganimate可用）
  cat("🎬 尝试生成动画...\n")
  tryCatch({
    p4 <- create_animated_heart()
    anim_save("表白特效_动画.gif", p4, width = 800, height = 600, fps = 10)
    cat("✅ 动画已保存为 GIF 文件！\n\n")
  }, error = function(e) {
    cat("⚠️  动画生成失败（可能需要额外配置），但静态图片已成功生成！\n\n")
  })
  
  cat("🎉 所有特效生成完成！\n")
  cat("📁 请查看当前目录下的图片文件：\n")
  cat("   - 表白特效_静态爱心.png\n")
  cat("   - 表白特效_文字.png\n")
  cat("   - 表白特效_烟花爱心.png\n")
  if (file.exists("表白特效_动画.gif")) {
    cat("   - 表白特效_动画.gif\n")
  }
  cat("\n💕 祝你和女朋友新年快乐，2026年幸福美满！💕\n")
}

# ============================================
# 9. 快速预览函数
# ============================================
quick_preview <- function() {
  cat("🎨 快速预览模式...\n\n")
  
  # 显示文字特效
  p <- create_text_effect()
  print(p)
  
  # 显示烟花爱心
  p2 <- create_firework_heart_combo()
  print(p2)
  
  cat("\n💕 预览完成！运行 generate_all_effects() 生成高清图片！\n")
}

# ============================================
# 使用说明
# ============================================
cat("
╔═══════════════════════════════════════════════════════╗
║        💕 新年表白特效 R语言版 - 2026快乐 💕          ║
╚═══════════════════════════════════════════════════════╝

📖 使用方法：

1️⃣  快速预览（在RStudio中查看）：
   quick_preview()

2️⃣  生成所有高清特效图片：
   generate_all_effects()

3️⃣  单独生成某个特效：
   - create_static_heart()      # 静态爱心
   - create_text_effect()       # 文字特效
   - create_firework_heart_combo()  # 烟花爱心组合

💡 提示：
   - 所有图片会保存在当前工作目录
   - 建议使用高分辨率显示器查看效果
   - 可以自定义文字和颜色

🎉 祝你和女朋友新年快乐，2026年幸福美满！🎉

")

# 自动运行快速预览（可选）
# quick_preview()

# 或者直接生成所有特效
# generate_all_effects()

