import pygame # 引入pygame 以使用其函式
import random # 引入random 以使用其函式 讓石頭隨機出現

# 慣例上會把設定好就不會在遊戲中變動的值的變數名稱 以大寫命名
FPS = 60 # 一秒鐘更新60次畫面
WIDTH = 500 # 視窗寬度
HEIGHT = 600 # 視窗高度

WHITE = (255,255,255) # 視窗背景顏色
GREEN = (0,255,0) # 綠色
RED = (255,0,0) # 紅色

# 遊戲初始化 及 創建視窗
pygame.init() #pygame函式，將遊戲初始化
screen = pygame.display.set_mode((WIDTH,HEIGHT)) 
# pygame函式，創建視窗 
# 會傳入一元組(以小括弧包住) 
# 元組中第一個資料為寬度，第二個為高度 
# 元組與列表之差異--元組一旦創建，不能做新增、修改或刪除--防止資料被意外修改
# python宣告變數不用寫var
# 遊戲迴圈:取得輸入->更新遊戲->渲染畫面，迴圈結束後，經過一段時間，再跑下一次迴圈，此處尚未寫迴圈(底下的其他程式碼)，所以程式運行時，視窗會出現後馬上關掉(後面沒有程式碼要執行了)
pygame.display.set_caption("第一個遊戲") # 視窗標題
clock = pygame.time.Clock() # 創建物件，此物件可對時間做管理與操縱
# 每個人電腦效能不同，故遊戲迴圈結束後要等待下一次迴圈的時間不同，故要做時間管理


# Sprite:pygame中的類別，可以創建視窗中的畫面
# 玩家操縱的飛船 Sprite類別
class Player(pygame.sprite.Sprite): # 表示創建Player物件類別(玩家操縱的飛船) self物件 #Player物件 繼承 內建的Sripte這個類別(pygame.sprite.Sprite為Sprite類別的位置)
    def __init__(self): #_init_表示初始函式 self表示物件本身
        pygame.sprite.Sprite.__init__(self) # 先CALL內建的Sprite的初始函式(Sprite初始函式的固定寫法)
        # 此初始函式有兩個屬性:image(顯示圖片)及rect(定位圖片)
        self.image = pygame.Surface((50,40)) #物件有一個屬性叫image，而這個屬性被傳入pygame.Surface((50,40))這個值 #pygame.Surface((50,40))為寬度50高度40的平面
        self.image.fill(GREEN)
        self.rect = self.image.get_rect() # 將本類別image屬性，用get_rect() 框起來(框起來後可以設定一些屬性(中間、上下左右、右上右下左上(xy座標)左下...)，設定image要在框框中的甚麼位置)後，指定給 屬性rect
        # 讓image的左上角 對齊 框框座標(200,200)的位置(框框座標體系原點在左上角):
        # self.rect.x = 200
        # self.rect.y = 200
        # 讓image左右置中:
        self.rect.centerx = WIDTH/2
        # 讓image置底:
        self.rect.bottom = HEIGHT-10 # image底部邊界座標 等於視窗高度-10(等同底部留10單位空間)
        # 讓image置中:
        # self.rect.center = (WIDTH/2, HEIGHT/2)
        self.speedx = 8 # 屬性speedx x軸的移動速度

    def update(self):
        # 方向控制
        key_pressed = pygame.key.get_pressed() # pygame.key.get_pressed() 會回傳一整串布林值(代表鍵盤上每個按鍵是否被按下去的狀態)，將此一整串布林值 指定給 變數 key_pressed
        if key_pressed[pygame.K_d]: # 判斷d鍵是否被按下
            self.rect.x += self.speedx # 按下的話 image就往右移speedx單位 #把原先的x座標值+speedx後的值 指定給 x座標值 #這個類別本身的屬性 要加self.
        if key_pressed[pygame.K_a]:
            self.rect.x -= self.speedx

        # 讓image不要超出左右邊界
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

        # 讓image往右動2單位
        # self.rect.x += 2
        # # 讓image往右移動超出視窗時，再從左邊重新出現
        # if self.rect.left > WIDTH: # 判斷image的左邊座標是否已經大於畫面寬度
        #     self.rect.right = 0 # 將image的右邊座標設為0

# 石頭 Sprite類別
class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30,40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        # 讓image(石頭)於在左右方向隨機出現:
        self.rect.x = random.randrange(0, WIDTH - self.rect.width) # 使用random中的randrage函式，函式中的數字表示數字隨機產生的範圍 # 最左邊:石頭的左邊界靠著X軸座標0的位置；最右邊:石頭的左邊界 靠著畫面寬度-石頭本身寬度 的位置
        # 讓image(石頭)於視窗上方外上下隨機出現:
        self.rect.y = random.randrange(-100, -40) # -100與-40為視窗上方外
        # 讓image(石頭)落下速度隨機
        self.speedy = random.randrange(2, 10)
        # 讓image(石頭)左右移動速度隨機
        self.speedx = random.randrange(-3, 3) # 負數表示往左跑(X座標減少)

    def update(self):
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

all_sprites = pygame.sprite.Group() # 將 變數all_sprites 指定為 一個sprite群組，群組中可放很多 sprite物件
player = Player() # 創建一個player物件(玩家飛船)(Sprite物件)(使用Player類別(Sprite類別)新建)
all_sprites.add(player) # player物件(Sprite物件) 加入 sprite群組
for i in range(8): # 執行以下程式碼8次(創建石頭物件 加入sprite群組)
    r = Rock()
    all_sprites.add(r)


# 遊戲迴圈
running = True # 遊戲是否進行中(以running變數存放此狀態)
while running: #條件為真時，執行以下程式碼 #若遊戲進行中:
    clock.tick(FPS) # 一秒鐘之內最多只會執行FPS次，這樣即使有人電腦跑超快，最多也只能在一秒鐘內跑FPS次(一秒鐘更新FPS次畫面)
    # 取得輸入
    for event in pygame.event.get(): 
        # pygame.event.get()會回傳現在發生的所有事件(列表)(如:滑鼠移動到哪、輸入甚麼按鍵)
        # for迴圈會到 此事件陣列中 對每個資料執行以下程式碼
        # Python for迴圈寫法類似Ruby，都與js不同
        if event.type == pygame.QUIT: # 檢查 事件陣列中 事件內容 是否為 將遊戲關閉(使用者點擊視窗右上角叉叉)
            running = False # 跳出迴圈(迴圈執行條件為runnung為true)

    # 更新遊戲
    all_sprites.update() # 執行all_sprites Sprite群組中 每個Sprite物件的 update函式(記得，目前一秒鐘會跑60次這個函式)

    # 畫面顯示
    screen.fill(WHITE) # screen是前面創建的視窗變數 # full函式裡面要放代表顏色的元組(RGB)，會用該顏色填滿畫面
    all_sprites.draw(screen) # 把all_sprites群組裡的東西(各個Sprite物件)都畫到screen(畫面)上
    pygame.display.update() # 更新畫面 (記得，目前一秒鐘會跑60次這個函式=更新60次畫面)

pygame.quit() # 既然跳出迴圈，表示遊戲進行狀態running為false，故進行關閉視窗函數