# 🚀 在Cursor中运行表白特效 - 详细步骤

## 方法1：使用终端运行（最简单）

### 步骤1：打开终端
- 按快捷键：`Ctrl + \`` (Windows/Linux) 或 `Cmd + \`` (Mac)
- 或者点击顶部菜单：**Terminal** → **New Terminal**
- 终端会在底部打开

### 步骤2：安装依赖库
在终端中输入以下命令，然后按回车：

```bash
pip3 install matplotlib numpy pillow
```

**如果提示权限错误，尝试：**
```bash
pip3 install --user matplotlib numpy pillow
```

**或者使用conda（如果你有）：**
```bash
conda install matplotlib numpy pillow
```

### 步骤3：运行脚本
在终端中输入：

```bash
cd ~/Desktop
python3 表白特效.py
```

或者直接：
```bash
python3 ~/Desktop/表白特效.py
```

### 步骤4：查看结果
运行完成后，在桌面上会生成以下文件：
- ✅ `表白特效_静态爱心.png`
- ✅ `表白特效_文字.png`
- ✅ `表白特效_烟花爱心.png`
- ✅ `表白特效_旋转爱心.png`
- ✅ `表白特效_动画.gif`

---

## 方法2：使用Cursor的运行按钮

### 步骤1：打开文件
- 在Cursor左侧文件列表中，点击 `表白特效.py` 打开

### 步骤2：安装依赖（如果还没安装）
- 先按照方法1的步骤2安装依赖库

### 步骤3：运行脚本
- 点击文件右上角的 **▶️ 运行** 按钮
- 或者按快捷键 `F5`
- 或者右键点击文件 → **Run Python File in Terminal**

---

## 方法3：使用命令面板

1. 按 `Cmd+Shift+P` (Mac) 或 `Ctrl+Shift+P` (Windows)
2. 输入 "Python: Run Python File"
3. 选择该选项
4. 脚本会在终端中运行

---

## ⚠️ 常见问题解决

### 问题1：提示 "No module named 'matplotlib'"
**解决方法：**
```bash
pip3 install matplotlib numpy pillow
```

### 问题2：提示权限错误
**解决方法：**
```bash
pip3 install --user matplotlib numpy pillow
```

### 问题3：提示找不到python3
**解决方法：**
- Mac/Linux: 使用 `python3`
- Windows: 使用 `python` 或 `py`

### 问题4：中文显示为方块
**解决方法：**
脚本已自动处理，如果还是有问题，可以忽略（图片中的emoji和英文会正常显示）

### 问题5：动画生成失败
**解决方法：**
确保安装了pillow：
```bash
pip3 install pillow
```

---

## 🎯 快速命令（复制粘贴即可）

```bash
# 1. 安装依赖
pip3 install matplotlib numpy pillow

# 2. 运行脚本
cd ~/Desktop && python3 表白特效.py
```

---

## 💡 提示

- 如果安装依赖时很慢，可以使用国内镜像：
  ```bash
  pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple matplotlib numpy pillow
  ```

- 运行脚本时，终端会显示进度信息
- 所有图片会保存在桌面（当前工作目录）
- 图片都是高清PNG格式（300 DPI），可以直接打印或分享

---

## 🎉 完成！

运行成功后，你就可以看到精美的表白特效图片了！

祝你和女朋友新年快乐，2026年幸福美满！💕

