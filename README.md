## 簡介
- 本專案為一個太空生存戰遊戲，玩家需操控太空船，透過閃避並射擊外太空的石頭，以獲取分數
- 為跟著「[【python】pygame 3小時製作一個遊戲](https://www.youtube.com/watch?v=61eX0bFAsYs)」製作之遊戲，圖片、聲音、字型等檔案皆自此下載
- 以Python撰寫
- 主要使用Pygame套件中的函式撰寫

## 功能
- 於遊戲初始畫面按下鍵盤任一鍵，即開始遊戲
- 透過方向鍵左右鍵移動飛船，空白鍵發射子彈
- 飛船被石頭撞到時，根據石頭大小，扣除玩家血量(血量顯示於視窗左上角)
- 血量歸零時，扣一條命，總共有三條命(生命數顯示於視窗右上角)
- 三條命皆用畢時，回到遊戲初始畫面
- 子彈打到石頭時，根據石頭大小，獲得分數(分數顯示於視窗中間上方)
- 射擊石頭後，爆炸之石頭有一定機率出現道具
- 吃到閃電道具可讓子彈暫時由一次射擊1發，變成一次射擊2發
- 吃到盾牌道具，可增加部分血量
- 遊戲音樂:
  - 背景音樂
  - 爆炸聲
  - 吃道具聲

## 畫面
### 初始畫面
![螢幕擷取畫面 2024-05-22 初始畫面](https://github.com/TamyTsai/space-survival-game/assets/97825677/7ce04971-78e7-467d-90cf-0affcbb2d882)

### 遊戲開始
![螢幕擷取畫面 2024-05-22 遊戲畫面](https://github.com/TamyTsai/space-survival-game/assets/97825677/1b6d20fe-188d-4ba2-9169-e07014bbdbac)

### 單子彈
![螢幕擷取畫面 2024-05-22 單子彈](https://github.com/TamyTsai/space-survival-game/assets/97825677/18e00ce9-dfac-4a68-be2a-5f6f918059ae)

### 雙子彈
![螢幕擷取畫面 2024-05-22 雙子彈](https://github.com/TamyTsai/space-survival-game/assets/97825677/b2484805-35e8-4bc2-896f-a59285070a09)


## 安裝
以下皆為於windows環境運行

### 檢查是否有安裝Python，若無，則至官網下載安裝
```bash
py --version
```

### 安裝Python延伸套件

### 檢查是否有安裝pip
```bash
py -m pip --version
```

### 安裝Pygame套件
```bash
py -m pip install pygame
```

### 取得專案
```bash
git clone https://github.com/TamyTsai/space-survival-game.git
```
### 移動到專案內
```bash
cd space-survival-game
```

## 資料夾及檔案說明
- img - 遊戲圖片放置處
- sound - 遊戲音效放置處
- font.ttf - 遊戲使用字體
- main.exe - 打包後的遊戲主程式執行檔
- main.py - 遊戲Python檔
- player.ico - 遊戲圖示

## 專案技術
- Python v3.12.3
  - pygame v2.5.2
