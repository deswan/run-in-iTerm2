# run-in-iterm2

一键在iTerm2中跑齐命令的效率脚本

## 安装
需要自行安装python3

#### 先安装 python 依赖
```
pip3 instaill iterm2
```

#### 安装 run-in-iterm2
```
sudo npm i -g run-in-iterm2
```


## 使用

#### 配置
``` bash
$ cd ~
$ vim .run-in-iterm2.yaml
```

``` yaml
# ~/.run-in-iterm2.yaml

# 默认路径前缀
defaultPath: /Users/micky 
# 默认命令
defaultCommand: 
  - npm run webpack
  - npm run develop
# 项目列表，每次执行 run 命令选择其中一个项目，将会在你的 iTerm2 中新建一个 tab，执行 command
projects: 
  - project1 #仅指定项目名称
  - 
    name: project2     #项目名称
    title: my_project2 #iTerm2 Tab标题，不填默认为 name 的值
    path: /Users/micky/my_project2    #项目路径，command 将会在 path 下执行，不填默认为 defaultPath + name
    command:    #要执行的命令，每一项会 split panel 一次执行，如只需执行单个命令则可填为字符串，不填默认为 defaultCommand 的值
        - npm run webpack
        - npm run develop

```

#### 执行
``` bash
# 选择项目，即可在 iTerm2 中优雅执行相应命令
$ run
```
