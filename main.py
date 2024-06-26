import pygame # 引入pygame 以使用其函式
import random # 引入random 以使用其函式 讓石頭隨機出現
import os # 為了統一不同電腦、作業系統的路徑寫法 而引入

# 慣例上會把設定好就不會在遊戲中變動的值的變數名稱 以大寫命名
FPS = 60 # 一秒鐘更新60次畫面
WIDTH = 500 # 視窗寬度
HEIGHT = 600 # 視窗高度

WHITE = (255, 255, 255) # 白色
BLACK = (0, 0, 0) # 黑色
GREEN = (0, 255, 0) # 綠色
RED = (255, 0, 0) # 紅色
YELLOW = (255, 255, 0) # 黃色

# 遊戲初始化 及 創建視窗
pygame.init() #pygame函式，將遊戲初始化
pygame.mixer.init() # 初始化音效模組，這樣才能引入音效
screen = pygame.display.set_mode((WIDTH,HEIGHT)) 
# pygame函式，創建視窗 
# 會傳入一元組(以小括弧包住) 
# 元組中第一個資料為寬度，第二個為高度 
# 元組與列表之差異--元組一旦創建，不能做新增、修改或刪除--防止資料被意外修改
# python宣告變數不用寫var
# 遊戲迴圈:取得輸入->更新遊戲->渲染畫面，迴圈結束後，經過一段時間，再跑下一次迴圈，此處尚未寫迴圈(底下的其他程式碼)，所以程式運行時，視窗會出現後馬上關掉(後面沒有程式碼要執行了)
pygame.display.set_caption("太空生存戰!") # 視窗標題
clock = pygame.time.Clock() # 創建物件，此物件可對時間做管理與操縱
# 每個人電腦效能不同，故遊戲迴圈結束後要等待下一次迴圈的時間不同，故要做時間管理

# 載入圖片(記得要寫在初始化後面，初始化後才能載入圖片，要不然會出錯)
background_img = pygame.image.load(os.path.join("img","background.png")).convert()
# load(圖片路徑) 
# 路徑寫法以os函數表示，os.path代表目前python檔案所在位置(太空生存戰 資料夾)  
# .join("圖片所在資料夾名稱(太空生存戰 資料夾底下的資料夾)","圖片檔案名")
# .convert()將圖片轉換成pygame較容易讀取的格式，畫到畫面上的速度會比較快
player_img = pygame.image.load(os.path.join("img","player.png")).convert() # 玩家飛船
player_mini_img = pygame.transform.scale(player_img, (25,19)) # 生命數圖片(玩家飛船圖片縮小)
player_mini_img.set_colorkey(BLACK)
pygame.display.set_icon(player_mini_img) # 設定視窗左上角圖示 # 不能寫在引入player_mini_img圖片路徑前 會找不到
rock_imgs = [] # 用rock_imgs存放列表
for i in range(7): # 將7張不一樣的石頭圖片 存放至rock_imgs列表中 # 跑此迴圈7次(0 1 2 3 4 5 6(不含7))
    rock_imgs.append(pygame.image.load(os.path.join("img",f"rock{i}.png")).convert())
    # 傳入rock0~rock6圖片 # 字串與變數串接的方法:變數外加大括弧，字串前面加f
# rock_img = pygame.image.load(os.path.join("img","rock.png")).convert()
bullet_img = pygame.image.load(os.path.join("img","bullet.png")).convert()
# 載入爆炸動畫圖片
expl_anim = {} # 創建 用來 放置 三種大小爆炸動畫 所需圖片 的 字典(類似js ruby中的物件) # 其中 子彈撞石頭、石頭撞飛船(一般) 兩種爆炸圖片一樣，只是大小不同
expl_anim['lg'] = [] # 創建expl_anim字典中 用來 裝大爆炸(子彈打到石頭)圖片(value) 的key(列表型態) # 字典[想在字典裡取得的value 所對應的key]
expl_anim['sm'] = [] # 創建expl_anim字典中 用來 裝小爆炸(石頭撞到玩家飛船)圖片(value) 的key(列表型態)
expl_anim['player'] = [] # 玩家飛船被石頭撞到生命歸零 的 爆炸
for i in range(9):
    # 子彈撞石頭、石頭撞飛船(一般) 
    expl_img = pygame.image.load(os.path.join("img",f"expl{i}.png")).convert()
    expl_img.set_colorkey(BLACK) # 把圖片的甚麼顏色(黑色)變成透明
    expl_anim['lg'].append(pygame.transform.scale(expl_img, (75, 75))) # pygame.transform.scale(要重新定義大小的圖片, (寬,高))
    expl_anim['sm'].append(pygame.transform.scale(expl_img, (30, 30)))
    # 玩家飛船被石頭撞到生命歸零 的 爆炸
    player_expl_img = pygame.image.load(os.path.join("img",f"player_expl{i}.png")).convert()
    player_expl_img.set_colorkey(BLACK)
    expl_anim['player'].append(player_expl_img)
# 載入道具圖片
power_imgs = {} # 創建用來裝道具圖片的字典
power_imgs['shield'] = pygame.image.load(os.path.join("img","shield.png")).convert() # 創建power_imgs字典中 用來裝 盾牌圖片(value) 的key
power_imgs['gun'] = pygame.image.load(os.path.join("img","gun.png")).convert()

# 載入音樂
shoot_sound = pygame.mixer.Sound(os.path.join("sound","shoot.wav")) # 射擊音效
gun_sound = pygame.mixer.Sound(os.path.join("sound","pow1.wav")) # 吃到gun音效
shield_sound = pygame.mixer.Sound(os.path.join("sound","pow0.wav")) # 吃到盾牌音效
die_sound = pygame.mixer.Sound(os.path.join("sound","rumble.ogg")) # 玩家飛船被石頭撞到生命歸零 的 爆炸音效
expl_sounds = [
    pygame.mixer.Sound(os.path.join("sound","expl0.wav")),
    pygame.mixer.Sound(os.path.join("sound","expl1.wav")) 
] # 用列表裝兩種石頭爆炸聲(子彈撞石頭)
pygame.mixer.music.load(os.path.join("sound","background.ogg")) # 要持續播放的背景音效，所以寫法不一樣
# 不用放進變數中，之後用pygame.mixer.music.play(-1)就可以讓其被播放
pygame.mixer.music.set_volume(0.4) # 設定pygame.mixer.music.load()所載入音樂的聲音大小(0~1)

# 載入分數字
font_name = os.path.join("font.ttf") # 要引入的字體的路徑(跟py檔同一個路徑的話，不用寫資料夾名稱)
# font_name = pygame.font.match_font('arial') # pygame.font.match_font('字體名稱')會去 執行此程式的電腦 找 要引入的字體，盡量選通用一點的字體，別人開啟的時候字體才不會不一致 # arial不支援中文
# 定義 用來在畫面呈現文字 的函式
def draw_text(surf, text, size, x, y): #(要顯示文字的平面(在哪個平面顯示文字), 文字內容, 文字大小, 文字x座標, 文字y座標)
    font = pygame.font.Font(font_name, size) # 創建文字物件 (字體名稱, 文字大小)
    text_surface = font.render(text, True, WHITE) # 將上一行建立的 文字物件 渲染出來 #渲染函式:.render(文字內容, 字體是否反鋸齒, 文字顏色)
    text_rect = text_surface.get_rect() # 定位文字位置 #把text_rect變成一個被框起來的變數，後面就可以用各種方法定位其
    text_rect.centerx = x # text_rect的x軸中心位置 定位在 本函式傳進來的x值
    text_rect.top = y  # text_rect的頂部邊界 定位在 本函式傳進來的y值
    surf.blit(text_surface, text_rect) # blit為畫的意思 # 要被畫的平面.blit(要畫的圖片(渲染後的文字物件), 畫的位置:(0,0)表示 圖片左上角 對齊座標0,0位置)

# 用以 畫出生命條及剩餘生命條 之 函式
def draw_health(surf, hp, x, y): # (要顯示HP值的平面, HP值, 顯示出來的生命條x座標, 顯示出來的生命條y座標)
    if hp < 0: # 如果HP被扣到變成負數
        hp = 0 # 就變成0 (畫不出負值的剩餘血條長度)
    BAR_LENGTH = 100 # 血條長度
    BAR_HEIGHT = 10 # 血條高度
    fill = (hp/100)*BAR_LENGTH # 現存的hp(剩餘血量條)佔整個血條槽多少百分比的長度
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT) # 血槽的框框(矩形) #pygame.Rect(矩形x座標, 矩形y座標, 矩形寬度, 矩形高度)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT) # 血槽中的剩餘血量條
    pygame.draw.rect(surf, GREEN, fill_rect) # 畫出矩形(血槽中的剩餘血量條):pygame.draw.rect(要畫在哪, 顏色, 位置)
    pygame.draw.rect(surf, WHITE, outline_rect, 2) # 畫出矩形(血槽框框):pygame.draw.rect(要畫在哪, 框框顏色, 位置, 外框粗細) # 有第四個參數的話，就會辨別為要畫矩形框框，框框內透明

# 用以 畫出生命數(小飛船) 之 函式
def draw_lives(surf, lives, img, x, y): # (要顯示生命數的平面, 生命數, 代表生命的圖片, 生命們的x座標, 生命們的y座標)
    for i in range(lives): # 先看現在還剩幾條命
        # 定位 代表 生命數的圖片(img，到時於「畫面顯示」呼叫此函數時，會傳入小飛船)
        img_rect = img.get_rect()
        img_rect.x = x + 32*i 
        # 根據剩餘生命數，決定位於x軸的何位置，如果還剩2條命，新畫的生命圖片 就要在左邊留 兩個 生命圖片位置
        # 一個生命圖片寬度25 每個圖片間隔5
        img_rect.y = y # 圖片y座標就定義在傳進來的參數y即可
        surf.blit(img, img_rect) # 要被畫的平面.blit(要畫的圖片, 畫的位置)

# 用以 畫出遊戲初始畫面並判斷是否進入遊戲 的 函式
def draw_init():
    screen.blit(background_img, (0,0)) # 畫出背景畫面
    draw_text(screen, '太空生存戰!', 64, WIDTH/2, HEIGHT/4) # draw_text(surf, text, size, x, y)
    draw_text(screen, '按下← →移動飛船，空白鍵發射子彈', 22, WIDTH/2, HEIGHT/2)
    draw_text(screen, '按下任意鍵開始遊戲!(請先將輸入法切換為英文)', 18, WIDTH/2, HEIGHT*3/4)
    pygame.display.update() # 更新畫面
    waiting = True # 是否為處於等待鍵盤被按下的狀態
    while waiting: # 當處於等待鍵盤被按下的狀態
        clock.tick(FPS) # 如果沒寫這行，一秒鐘執行迴圈的速度就會非常多
        for event in pygame.event.get(): 
        # pygame.event.get()會回傳現在發生的所有事件(列表)(如:滑鼠移動到哪、輸入甚麼按鍵)
        # for迴圈會到 此事件陣列中 對每個資料執行以下程式碼
            if event.type == pygame.QUIT: # 檢查 事件陣列中 事件內容 是否為 將遊戲關閉(.QUIT使用者點擊視窗右上角叉叉)
                pygame.quit() # 關閉遊戲視窗 # 但沒有真正跳出遊戲迴圈
                return True
            elif event.type == pygame.KEYUP: # .KEYUP表示按下鍵盤後鬆開鍵盤的狀態 
                waiting = False # 就跳出迴圈 離開初始畫面顯示狀態
                return False

# 創建石頭(以副程式的寫法 達到程式碼的再用(有回傳值的副程式稱 函數，沒回傳值的副程式稱 程序))
def new_rock():
    r = Rock() # 創建石頭Sprite物件
    all_sprites.add(r) # 將石頭Sprite物件 加入 all_sprites Sprite群組(物件才會被更新 並呈現於畫面)
    rocks.add(r) # 將石頭Sprite物件 加入 rocks Sprite群組(物件才能繼續被判斷是否與子彈碰撞) 

# Sprite:pygame中的類別，可以創建視窗中的畫面物件
# 玩家操縱的飛船(Sprite類別)
class Player(pygame.sprite.Sprite): # 表示創建Player物件類別(玩家操縱的飛船) self物件 #Player物件 繼承 內建的Sripte這個類別(pygame.sprite.Sprite為Sprite類別的位置)
    # 初始函式
    def __init__(self): #_init_表示初始函式 self表示物件本身
        pygame.sprite.Sprite.__init__(self) # 先CALL內建的Sprite的初始函式(Sprite初始函式的固定寫法)
        # 此初始函式有兩個屬性:image(顯示圖片)及rect(以矩形rectangle定位圖片)
        self.image = pygame.transform.scale(player_img, (50,38)) # pygame.transform.scale(要重新定義大小的圖片, (寬,高))
        self.image.set_colorkey(BLACK) # 把圖片的甚麼顏色(黑色)變成透明
        # self.image = pygame.Surface((50,40)) #物件有一個屬性叫image，而這個屬性被傳入pygame.Surface((50,40))這個值 #pygame.Surface((50,40))為寬度50高度40的平面
        # self.image.fill(GREEN)
        self.rect = self.image.get_rect() # 將本類別image屬性，用get_rect() (定位用函式)矩形框起來(框起來後可以設定一些屬性(中間、上下左右、右上右下左上(xy座標)左下...)，設定image要在框框中的甚麼位置)後，指定給 屬性rect
        # 將image(玩家飛船)碰撞邊界畫成圓
        self.radius = 20 # 圓形碰撞判斷下，需要知道半徑(以圖片中心點為圓心，畫出半徑20的圓形碰撞邊界)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius) # 畫圓形(測試觀看用):pygame.draw.circle(要畫在哪, 顏色, 圓心位置, 半徑)
        # 讓image的左上角 對齊 框框座標(200,200)的位置(注意:框框 座標體系 原點 在 左上角，座標往右下增加):
        # self.rect.x = 200
        # self.rect.y = 200
        # 讓image(玩家飛船)左右置中:
        self.rect.centerx = WIDTH/2 # centerx為image在x軸方向的中間點
        # 讓image(玩家飛船)置底:
        self.rect.bottom = HEIGHT-10 # image底部邊界座標 等於視窗高度-10(等同底部留10單位空間)
        # 讓image(玩家飛船)置中:
        # self.rect.center = (WIDTH/2, HEIGHT/2) # centerx為image在x軸及y軸方向的中間點
        self.speedx = 8 # 屬性speedx x軸的移動速度
        self.health = 100 # 玩家飛船的初始HP
        self.lives = 3 # 玩家生命數 物件被創建時初始3條命
        self.hidden = False # 玩家飛船隱藏狀態，初始為不隱藏
        self.hide_time = 0 # 玩家飛船隱藏時間
        self.gun = 1 # 子彈等級 初始為1
        self.gun_time = 0 # 紀錄吃到gun的時間，初始為0

    # 更新畫面
    def update(self):
        now = pygame.time.get_ticks()

        # 讓gun道具效果在吃到後5秒消失
        if self.gun > 1 and now - self.gun_time > 5000:
            self.gun -= 1 # 因為不是設定為self.gun = 1，所以如果一直吃到gun，gun等級就會被一直往上加，每過5秒等級只會-1，-1後還是>=2的話，就還是有兩發子彈的效果
            self.gun_time = now # now - self.gun_time變0，就不會符合now - self.gun_time > 5000的條件，self.gun不會再減1

        # 讓死亡冷卻消失的飛船1秒後重新出現
        if self.hidden and now - self.hide_time > 1000 : # 當 處於死亡隱藏狀態 且 目前時間 距離 開始隱藏的時間 超過1秒 時
            self.hidden = False # 取消隱藏
            # 重新定位回原位
            self.rect.centerx = WIDTH/2
            self.rect.bottom = HEIGHT-10

        # 方向控制
        key_pressed = pygame.key.get_pressed() # pygame.key.get_pressed() 會回傳一整串布林值(代表鍵盤上每個按鍵是否被按下去的狀態)，將此一整串布林值 指定給 變數 key_pressed
        if key_pressed[pygame.K_RIGHT]: # 判斷方向鍵右鍵是否被按下
            self.rect.x += self.speedx # 按下的話 image就往右移speedx單位 #把原先的x座標值+speedx後的值 指定給 x座標值 #這個類別本身的屬性 要加self.
        if key_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speedx

        # 讓image不要超出左右邊界
        if self.rect.right > WIDTH: # image的右邊邊界 大於 視窗寬度
            self.rect.right = WIDTH
        if self.rect.left < 0: # image的左邊邊界 小於 座標0
            self.rect.left = 0

        # 讓image往右動2單位
        # self.rect.x += 2
        # # 讓image往右移動超出視窗時，再從左邊重新出現
        # if self.rect.left > WIDTH: # 判斷image的左邊座標是否已經大於畫面寬度
        #     self.rect.right = 0 # 將image的右邊座標設為0
    
    # 發射子彈
    def shoot(self):
        # 非 處於死亡冷卻隱藏效果時 才能發射子彈
        if not(self.hidden):
            if self.gun == 1: # 如果gun等級為1(初始等級)
                # 創建bullet子彈sprite物件後，於 all_sprites及bullets Sprite群組 加入 該子彈物件
                bullet = Bullet(self.rect.centerx, self.rect.top) 
                # 使用Bullet類別(Sprite類別) 創建一個bullet物件(子彈)(Sprite物件)，初始函式要求傳入子彈初始位置(此處傳入玩家飛船位置)
                # centerx為 image(玩家飛船)x軸的中間座標，top為image(玩家飛船)的頂部邊界(子彈 初始位置為 玩家飛船 的 頂部中央)
                all_sprites.add(bullet)
                bullets.add(bullet) 
                shoot_sound.play() # 播放射擊音效
            elif self.gun >= 2: # 如果gun等級超過2 就可以發射2顆子彈
                bullet1 = Bullet(self.rect.left, self.rect.centery) # 子彈1由玩家飛船左側邊界(船身中間)發射
                bullet2 = Bullet(self.rect.right, self.rect.centery) # 子彈2由玩家飛船右側邊界(船身中間)發射
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1) 
                bullets.add(bullet2) 
                shoot_sound.play()

    # 死亡冷卻隱藏飛船效果
    def hide(self):
        self.hidden = True
        self.hide_time = pygame.time.get_ticks() # 抓目前時間 # 紀錄隱藏的起始時間點
        self.rect.center = (WIDTH/2, HEIGHT+500) # 把玩家飛船定位在視窗外，達隱藏效果 # 將玩家飛船之矩形框框中心點 x軸位置定位在 視窗寬度除以2，y軸位置定義在 視窗高度+500(離視窗底部邊界500px的位置)

    # 玩家飛船吃到gun道具的效果
    def gunup(self):
        self.gun += 1 # 子彈等級+1
        self.gun_time = pygame.time.get_ticks() # 吃到gun的時間，設定為當前時間


# 石頭(Sprite類別)
class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_ori = random.choice(rock_imgs) # 轉動前未失真之圖片 # rock_imgs為存有7張石頭圖片的列表 # random.choice(rock_imgs)可從rock_imgs列表中隨機取資料
        self.image_ori.set_colorkey(BLACK)
        self.image = self.image_ori.copy() # 複製一份 self.image_ori 指定給self.image
        # self.image = pygame.Surface((30,40))
        # self.image.fill(RED)
        self.rect = self.image.get_rect()
        # 將image(石頭)碰撞邊界畫成圓
        self.radius = int(self.rect.width * 0.85 / 2) # 設定半徑 # self.rect.width為image(石頭)寬度 #因為分數是照打到的石頭半徑計算的，為了不讓分數有小數點，所以將半徑轉為整數
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius) 
        # 讓image(石頭)於在左右方向隨機出現:
        self.rect.x = random.randrange(0, WIDTH - self.rect.width) # 使用random中的randrage函式，函式中的數字表示數字隨機產生的範圍 # 最左邊:石頭的左邊界靠著X軸座標0的位置；最右邊:石頭的左邊界 靠著畫面寬度-石頭本身寬度 的位置
        # 讓image(石頭)於視窗上方外上下隨機出現:
        self.rect.y = random.randrange(-180, -100) # -180與-100為視窗上方外
        # 讓image(石頭)落下速度隨機
        self.speedy = random.randrange(2, 10)
        # 讓image(石頭)左右移動速度隨機
        self.speedx = random.randrange(-3, 3) # 負數表示往左跑(X座標減少)
        self.total_degree = 0 # 初始旋轉總角度
        self.rot_degree = random.randrange(-3, 3) # 設定圖片旋轉角度(作為pygame.transform.rotate函式的參數使用)

    def rotate(self):
        self.total_degree += self.rot_degree # 每次執行rotate函式 就旋轉self.rot_degree度 # 把旋轉總角度的值加上self.rot_degree度後 指定回給 旋轉總角度
        self.total_degree = self.total_degree % 360 # 防止轉超過一圈 # 旋轉總角度 = 旋轉總角度 除以 360 所剩下的餘數，即表示 旋轉總角度 會介於0~359
        self.image = pygame.transform.rotate(self.image_ori, self.total_degree)
        # pygame內建的轉動圖片的函式 pygame.transform.rotate(要旋轉的圖片, 旋轉的角度) # self.total_degree每次更新畫面都隨機旋轉-3~3度，總旋轉角度介於0~359之間
        # 每次旋轉都會失真一些，一秒鐘更新60次畫面的話，失真就會因疊加而變嚴重，所以要旋轉的圖片不能用self.image，而要用self.image_ori，不過這樣每次都是對原始圖片做轉動，而非旋轉角度疊加，所以圖片會靜止，故要再寫total_degree來裝旋轉總角度
        # 替轉動後的圖片重新做定位(轉動後沒有重新定位的話，中心點就不會隨轉動後的圖片做調整，圖片會出現旋轉抖動效果)
        center = self.rect.center # 將變數center指定為 image(石頭)的中心點(原始中心點)
        self.rect = self.image.get_rect()
        self.rect.center = center # 把image(石頭)的中心點 定位到 變數center存放的值(self.rect.center原先的中心點)的位置

    def update(self):
        # image(石頭)動畫
        self.rotate()
        # image(石頭)落下效果
        self.rect.y += self.speedy # 把原先的y座標值+speedy後的值 指定給 y座標值
        self.rect.x += self.speedx
        # 如果image(石頭)掉到畫面外(下、左、右)，就重新生成
        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0: #  self.rect.top > HEIGHT:image(石頭)的頂部邊界座標 大於 視窗高度
            # 讓image(石頭)於在左右方向隨機出現:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width) # 使用random中的randrage函式，函式中的數字表示數字隨機產生的範圍 # 最左邊:石頭的左邊界靠著X軸座標0的位置；最右邊:石頭的左邊界 靠著畫面寬度-石頭本身寬度 的位置
            # 讓image(石頭)於視窗上方外上下隨機出現:
            self.rect.y = random.randrange(-100, -40) # -100與-40為視窗上方外
            # 讓image(石頭)落下速度隨機
            self.speedy = random.randrange(2, 10)
            # 讓image(石頭)左右移動速度隨機
            self.speedx = random.randrange(-3, 3) # 負數表示往左跑(X座標減少)

# 子彈(Sprite類別)
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y): # 子彈位置是根據玩家飛船位置變動的，故以此類別創建物件實體時，需要傳入x,y座標位置(使用此類別創建子彈物件時(在 玩家飛船類別 中創建)，xy參數要帶入玩家飛船位置)
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        # self.image = pygame.Surface((10,20))
        # self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        # 讓image(子彈)x軸方向的中間座標 位於 x:
        self.rect.centerx = x
        # 讓image(子彈)底部邊界座標 位於 y:
        self.rect.bottom = y
        # image(子彈)向上發射速度
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy # 把原先的y座標值+speedy後的值 指定給 y座標值
        # 讓image(子彈)底部邊界出視窗上方後，刪除子彈
        if self.rect.bottom < 0:
            self.kill() # kill為Sprite類別的內建函式，作用是會將 該Sprite 自所有存有該Sprite的Sprite群組中 刪除

# 爆炸動畫腳本(Sprite類別)
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size): # 爆炸動畫呈現位置，及是大爆炸還是小爆炸動畫(使用此類別創建物件時，要傳入爆炸動畫要呈現在哪，及欲使用大還是小爆炸動畫)
        pygame.sprite.Sprite.__init__(self)
        self.size = size # 物件的size屬性 存放 物件創建時傳入的size參數
        self.image = expl_anim[self.size][0] # 初始爆炸圖片 # expl_anim為字典(存有兩個列表，key值分別為lg及sm)，[self.size]為列表(裝有一系列圖片的大爆炸或小爆炸列表)，[0]為列表中的資料索引值(列表中的某一張圖片)
        self.rect = self.image.get_rect() # 對爆炸圖片做定位(以矩形框住，以利後續做定位操縱)
        self.rect.center = center # 框住 爆炸圖片 的矩形 中心點 設定為 物件創建時傳入的center參數
        self.frame = 0 # 更新到第0張圖片
        # 直接用update更新圖片的話，因為FPS設定為60，所以爆炸動畫會變太快，所以要 紀錄圖片最後更新的時間，並設定至少經過多少毫秒，再更新到下一張圖片
        self.last_update = pygame.time.get_ticks() # 用以 紀錄「最後」更新的時間 # pygame.time.get_ticks() 函式回傳初始化至今經過的毫秒數?
        self.frame_rate = 50 # 經過至少50毫秒 再更新到下一張圖片(用以 判斷上次最後更新圖片之時間，與目前時間是否已過至少50毫秒)

    def update(self):
        now = pygame.time.get_ticks() # 「目前」圖片被更新的時間
        if now - self.last_update > self.frame_rate: # 當 現在時間 與 上次最後更新圖片的時間 相距 超過 self.frame_rate毫秒
            self.last_update = now # 就把 讓 最後更新圖片的時間 變成 現在時間
            self.frame += 1 # 並更新下一張圖片
            if self.frame == len(expl_anim[self.size]): # 如果已經更新到最後一張圖片(最後一張圖片的序號(8) 會 等於存放圖片們列表的長度(9張圖片)??)
                self.kill() # 就把用此類別建立的物件(爆炸動畫) 刪除
            else: # 若 還沒更新到最後一張
                self.image = expl_anim[self.size][self.frame] # 就把圖片更新到下一張
                # 更新圖片後要重新定位
                center = self.rect.center # 將變數center指定為 爆炸圖片的中心點(原始中心點) # 先記錄原始中心點 # 初始函式中的參數 只能用在 初始函式中 的 程式碼區塊
                self.rect = self.image.get_rect()
                self.rect.center = center # 把 爆炸圖片 的中心點 定位到 變數center存放的值(self.rect.center原先的中心點)的位置

# 道具
class Power(pygame.sprite.Sprite):
    def __init__(self, center): # 使用此類別創建道具物件時，要傳入道具中心點要定位在哪
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun']) # 於存放盾牌及槍的列表中，隨機選取一筆資料
        self.image = power_imgs[self.type] # power_imgs字典中存有兩個key(shield及gun)，以[key]取得key所對應的value(盾牌和槍的圖片)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center # 道具的中心點定位在 以此類別創建物件時傳入的center參數
        self.speedy = 3 # 道具向下掉落的速度

    def update(self):
        self.rect.y += self.speedy # 把原先的y座標值+speedy後的值 指定給 y座標值
        # 讓image(道具)頂部邊界出視窗下方後，刪除道具
        if self.rect.top > HEIGHT:
            self.kill()

# 播放遊戲背景音效
pygame.mixer.music.play(-1) # pygame.mixer.music.play(要重複播放的次數，-1表示無限播放):播放 用pygame.mixer.music.load()函式 載入的音樂


# 遊戲迴圈
show_init = True # 初始畫面顯示狀態
running = True # 遊戲是否進行中(以running變數存放此狀態)
while running: # 條件為真時，執行以下程式碼 #若遊戲進行中:
    if show_init: # 如果要顯示初始畫面
        close = draw_init() # 畫出初始畫面 # 玩家若按下右上角叉叉 則此函式會回傳True
        if close: # 若玩家按下右上角叉叉
            break # 直接跳出迴圈，不執行下面的程式碼
        show_init = False # 初始畫面顯示完後就關掉
        # Sprite群組
        all_sprites = pygame.sprite.Group() # 將 變數all_sprites 指定為 一個sprite群組，群組中可放很多 sprite物件 # 專放要被呈現在畫面的物件
        rocks = pygame.sprite.Group() # 專放石頭sprite物件的sprite群組
        bullets = pygame.sprite.Group() # 專放子彈sprite物件的sprite群組 (石頭和子彈放在不一樣的sprite群組，才能用pygame內建的函式判斷 石頭與子彈是否碰撞)
        powers = pygame.sprite.Group() # 專放道具sprite物件的sprite群組

        # 創建player玩家飛船sprite物件後，於 all_sprites Sprite群組加入 該玩家飛船物件
        player = Player() # 使用Player類別(Sprite類別) 創建一個player物件(玩家飛船)(Sprite物件) # 括弧裡不用寫self
        all_sprites.add(player) # player物件(Sprite物件) 加入 sprite群組
        # 創建r石頭sprite物件後，於 all_sprites及rocks Sprite群組 加入 該石頭物件
        for i in range(8): # 執行以下程式碼8次(創建石頭物件 於 all_sprites及rocks Sprite群組)
            new_rock()
        # 遊戲分數
        score = 0

    clock.tick(FPS) # 一秒鐘之內最多只會執行FPS次，這樣即使有人電腦跑超快，最多也只能在一秒鐘內跑FPS次(一秒鐘更新FPS次畫面)
    # 取得輸入
    for event in pygame.event.get(): 
        # pygame.event.get()會回傳現在發生的所有事件(列表)(如:滑鼠移動到哪、輸入甚麼按鍵)
        # for迴圈會到 此事件陣列中 對每個資料執行以下程式碼
        # Python for迴圈寫法類似Ruby，都與js不同
        if event.type == pygame.QUIT: # 檢查 事件陣列中 事件內容 是否為 將遊戲關閉(使用者點擊視窗右上角叉叉)
            running = False # 跳出迴圈(迴圈執行條件為runnung為true)
        elif event.type == pygame.KEYDOWN: # .KEYDOWN表示按下鍵盤 
            if event.key == pygame.K_SPACE: # 如果按下空白鍵盤
                player.shoot() # 就呼叫飛船物件的shoot函式

    # 更新遊戲
    all_sprites.update() # 執行all_sprites Sprite群組中 每個Sprite物件的 update函式(記得，目前一秒鐘會跑60次這個函式)
    # 以pygame內建的函式判斷 石頭與子彈(各自位於不同sprite群組)是否碰撞，會回傳一個 「字典」，裡面裝著 被碰撞到的石頭與子彈(key是石頭 value是子彈)，將此字典 指定給 變數hits
    hits = pygame.sprite.groupcollide(rocks, bullets, True, True) # groupcollide(裏頭物件被碰撞的群組1, 裏頭物件被碰撞的群組2, 被碰撞到的群組1內的物件是否要被刪除, 被碰撞到的群組2內的物件是否要被刪除)
    for hit in hits: # 對在字典hits中的每個資料(被碰撞到所以消失的物件)，進行以下程式碼(重新建回消失的物件)
        random.choice(expl_sounds).play() # 於存放石頭爆炸聲響的列表中，隨機選取一筆資料 #.play()可播放音效
        # 每個hit是被碰撞到的石頭(hits字典存放的每個資料) # 所以hit.radius是被碰撞到的石頭的半徑
        score += hit.radius # 根據 子彈 打到的 石頭半徑大小 
        expl = Explosion(hit.rect.center, 'lg') #創建 名為expl的 爆炸動畫Sprite物件 Explosion(center, size) # 爆炸動畫的圖片中心點為 被子彈撞到的石頭圖片的中心點 #子彈石頭相撞為大爆炸
        all_sprites.add(expl) # 要把expl sprite物件加入all_sprites Sprite群組，才會被畫到畫面上 # 因為後面有寫all_sprites.draw(screen)讓群組裡的物件都被畫到screen上
        # 道具
        if random.random() > 0.9: # random.random()會回傳隨機0~1的值 #只要隨機回傳的值>0.9 # random.random() > 0.9 表示掉寶率1成(只有10%的機會回傳的數字會>0.9)
            pow = Power(hit.rect.center) # 就以Power道具類別 創建 道具物件pow # 道具出現的位置，是被子彈打掉的石頭的位置
            all_sprites.add(pow)
            powers.add(pow) # 將道具pow Sprite物件 加入 powers Sprite群組(物件才能 被判斷 是否與 玩家飛船 碰撞) 
        # 把與子彈碰撞後消失的石頭創建回來
        new_rock()
        # 子彈本來就可無限發射(按空白鍵就會執行shoot函式，生成子彈物件) 所以不用做如石頭的碰撞消失重生處理
    # 判斷 玩家飛船與石頭兩類Sprite物件 是否碰撞，此函式回傳 「列表」，存放 所有 碰撞到 玩家飛船 的 石頭
    hits = pygame.sprite.spritecollide(player, rocks, True, pygame.sprite.collide_circle)
    #spritecollide(裏頭物件被碰撞的群組1, 裏頭物件被碰撞的群組2, 被碰撞到的群組2內的物件是否要被刪除)
    # 撞到玩家飛船的石頭要被刪掉 
    # python中比較特別，變數名稱相同時，後指定的值，不會影響前面指定給同名變數的值
    # spritecollide預設為矩形碰撞判斷 
    # pygame.sprite.collide_circle讓其改為圓形碰撞判斷，但player, rocks就要加上radius屬性(用以設定圓形半徑大小)
    for hit in hits:
        # 把每顆撞到飛船而消失的 石頭 加回來
        new_rock()
        # 按照被多大的石頭撞到，來決定扣血量
        player.health -= hit.radius # 每個hit是被碰撞到的石頭(hits列表存放的每個資料)，所以hit.radius是被碰撞到的石頭的半徑
        expl = Explosion(hit.rect.center, 'sm') # 創建 名為expl的 爆炸動畫Sprite物件 Explosion(center, size) # 爆炸動畫的圖片中心點為 撞到 玩家飛船 的 石頭圖片 的 中心點 #玩家飛船與石頭相撞為 小爆炸
        all_sprites.add(expl)
        # 血量沒了才關閉遊戲
        if player.health <= 0: 
            death_expl = Explosion(player.rect.center, 'player') # 創建 名為die的 爆炸動畫Sprite物件 Explosion(center, size) # 爆炸動畫的圖片中心點為 撞到 玩家飛船sprite物件圖片 的 中心點 #玩家飛船與石頭相撞為 玩家爆炸
            all_sprites.add(death_expl)
            die_sound.play()
            player.lives -= 1 # 血量<=0時，玩家飛船生命數扣1
            player.health = 100 # 並且把血量加滿(回復到初始值100)
            player.hide() # 玩家飛船死亡後冷卻一陣子(隱藏一陣子)

    # 判斷 玩家飛船 與 道具 兩類Sprite物件 是否碰撞，此函式回傳 「列表」，存放 所有 碰撞到 玩家飛船 的 道具
    hits = pygame.sprite.spritecollide(player, powers, True)
    #spritecollide(裏頭物件被碰撞的群組1, 裏頭物件被碰撞的群組2, 被碰撞到的群組2內的物件是否要被刪除)
    for hit in hits:
        if hit.type == 'shield':  # 每個hit是被碰撞到的道具(hits列表存放的每個資料)，所以hit.type是被碰撞到的道具的類型
            player.health += 20 # 玩家生命值+20
            if player.health > 100: # 如果玩家生命值滿了
                player.health = 100 # 就不再增加
            shield_sound.play()
        if hit.type == 'gun':
            player.gunup()
            gun_sound.play()

    # 玩家飛船生命數歸零時，遊戲結束，跳出迴圈，回到初始畫面
    if player.lives  == 0 and not(death_expl.alive()):
        # and not(die.alive()):且當die物件不存在時(.alive()函式用以判斷物件是否存在)，才結束遊戲(要不然最後一次死掉的爆炸聲不會被執行，動畫也不會跑完)
        show_init = True

    # if hits: # 如果玩家飛船有撞到石頭(True)
    #     running = False # 就跳出回圈，關閉遊戲

    # 畫面顯示
    screen.fill(BLACK) # screen是前面創建的視窗變數 # full函式裡面要放代表顏色的元組(RGB)，會用該顏色填滿畫面
    screen.blit(background_img, (0,0)) # blit為畫的意思 # 要被畫的平面.blit(要畫的圖片, 畫的位置:(0,0)表示 圖片左上角 對齊座標0,0位置)
    all_sprites.draw(screen) # 把all_sprites群組裡的東西(各個Sprite物件)都畫到screen(畫面)上
    draw_text(screen, str(score), 18, WIDTH/2, 10)  # 呈現 分數 於畫面上 # str(score):把分數轉為字串
    draw_health(screen, player.health, 5, 15) # 呈現 血槽與剩餘血條 於畫面上
    draw_lives(screen, player.lives, player_mini_img, WIDTH-100, 15) # 呈現生命數 # draw_lives(surf, lives, img, x, y): # (要顯示生命數的平面, 生命數, 代表生命的圖片,生命們的x座標, 生命們的y座標) # 高度設定跟血條一樣高
    pygame.display.update() # 更新畫面 (記得，目前一秒鐘會跑60次這個函式=更新60次畫面)

pygame.quit() # 既然跳出迴圈，表示遊戲進行狀態running為false，故進行關閉視窗函式