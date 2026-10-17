# 简体中文 README

项目主页已迁移至 [README.md](README.md)。此文件保留，兼容既有的 `README.zh.md` 链接。

> 为 [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness)（dsh）网页版重组《明日方舟》莱茵生命界面：以档案终端为核心视觉，并加入克制的机构 HUD 标识。

![莱茵生命浅色总部档案模式](screenshots/light.png)
![莱茵生命深色夜间行动模式](screenshots/dark.png)

## 视觉系统

这次重组把 Harness 呈现为内部研究档案，而不是叠加装饰：

- **浅色总部档案模式**使用暖纸、浓墨、方正文件边缘与研究橙授权强调。
- **深色夜间行动模式**在炭黑底色上保留同一套记录结构；青色只表示实时数据，红色只表示失败。
- **克制的直接品牌标识**仅包含不可交互的档案文字和莱茵生命 shell 标记，不会新增控件或改变 Harness 工作流。
- **可访问性与响应式行为**保留正常交互，尊重 `prefers-reduced-motion`，并只在窄屏时减少非必要题注和留白。

本包不会重新分发任何本地参考站点媒体。它只包含自身源码、编译产物、文档，以及上方的发布截图。

## 兼容性与安全降级

兼容目标是 Web 端的 **DeepSeek Harness 0.1.0-rc.5**（`dsh --profile web`）。样式只作用于稳定的 Harness data attribute。若未来或更早版本缺少某个锚点，对应装饰会自然不生效；宿主的控件、布局轨道、滚动、代码区域和设置仍由宿主自己管理，这就是安全降级。

原有的 **设置 → 通用** 开关仍是唯一控制入口。它继续读写持久化的 `ui-theme-rhine-lab.enabled` 偏好；不迁移、也不替换设置命名空间。浅色、深色和跟随系统仍在重组界面之下决定基础模式。

## 安装

从已发布包或本地 tarball 安装：

```sh
dsh plugin --profile web add dsh-theme-rhine-lab
pnpm pack
dsh plugin --profile web add ./dsh-theme-rhine-lab-0.2.1.tgz
```

从源码安装前先构建：

```sh
git clone https://github.com/ReLuckyLucy/dsh_Rhine_Lab_theme.git
cd dsh_Rhine_Lab_theme
pnpm install
pnpm build
dsh plugin --profile web add .
```

安装插件集合后重启 `dsh web`，再刷新浏览器。Git 安装会直接使用已提交的 `lib/` 产物，不需要在目标 profile 中放行生命周期脚本；生成 tarball 前，`prepack` 会重新构建这些产物。

## 工作原理

- [`cordis.patch.yml`](cordis.patch.yml) 将本组合包接入 dsh。
- [`src/index.ts`](src/index.ts) 注册持久化的 `ui-theme-rhine-lab` 设置。
- [`src/client/index.ts`](src/client/index.ts) 把 enabled 设置投射为令牌覆盖、作用域内的档案终端样式、不可交互 HUD 和通用设置行。
- [`lib/`](lib) 已提交，因此 registry/tarball 安装能直接使用预构建产物。

## 开发与发布

```sh
pnpm test
pnpm build
npm pack --dry-run
```

发布 tarball 会包含 `lib`、`src`、`cordis.patch.yml`、两份 README、`LICENSE`，以及发布截图存在时的 `screenshots`。它不会包含测试、本地笔记或任何参考站点素材。

## 许可证

[MIT](LICENSE)。本项目为粉丝自制皮肤；《明日方舟》与莱茵生命版权归鹰角网络 / Yostar 所有。
