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

# 載入圖片(記得要寫在初始化後面，初始化後才能載入圖片，要不然會出錯)
background_img = pygame.image.load(os.path.join("img","background.png")).convert()
# load(圖片路徑) 
# 路徑寫法以os函數表示，os.path代表目前python檔案所在位置(太空生存戰 資料夾)  
# .join("圖片所在資料夾名稱(太空生存戰 資料夾底下的資料夾)","圖片檔案名")
# .convert()將圖片轉換成pygame較容易讀取的格式，畫到畫面上的速度會比較快
player_img = pygame.image.load(os.path.join("img","player.png")).convert()
rock_imgs = [] # 用rock_imgs存放列表
for i in range(7): # 將7張不一樣的石頭圖片 存放至rock_imgs列表中 # 跑此迴圈7次(0 1 2 3 4 5 6(不含7))
    rock_imgs.append(pygame.image.load(os.path.join("img",f"rock{i}.png")).convert())
    # 傳入rock0~rock6圖片 # 字串與變數串接的方法:變數外加大括弧，字串前面加f
# rock_img = pygame.image.load(os.path.join("img","rock.png")).convert()
bullet_img = pygame.image.load(os.path.join("img","bullet.png")).convert()


# Sprite:pygame中的類別，可以創建視窗中的畫面物件
# 玩家操縱的飛船(Sprite類別)
class Player(pygame.sprite.Sprite): # 表示創建Player物件類別(玩家操縱的飛船) self物件 #Player物件 繼承 內建的Sripte這個類別(pygame.sprite.Sprite為Sprite類別的位置)
    # 初始函式
    def __init__(self): #_init_表示初始函式 self表示物件本身
        pygame.sprite.Sprite.__init__(self) # 先CALL內建的Sprite的初始函式(Sprite初始函式的固定寫法)
        # 此初始函式有兩個屬性:image(顯示圖片)及rect(定位圖片)
        self.image = pygame.transform.scale(player_img, (50,38)) # pygame.transform.scale(要重新定義大小的圖片, (寬,高))
        self.image.set_colorkey(BLACK) # 把圖片的甚麼顏色(黑色)變成透明
        # self.image = pygame.Surface((50,40)) #物件有一個屬性叫image，而這個屬性被傳入pygame.Surface((50,40))這個值 #pygame.Surface((50,40))為寬度50高度40的平面
        # self.image.fill(GREEN)
        self.rect = self.image.get_rect() # 將本類別image屬性，用get_rect() 框起來(框起來後可以設定一些屬性(中間、上下左右、右上右下左上(xy座標)左下...)，設定image要在框框中的甚麼位置)後，指定給 屬性rect
        # 將image(玩家飛船)碰撞邊界畫成圓
        self.radius = 20 # 圓形碰撞判斷下，需要知道半徑(以圖片中心點為圓心，畫出半徑20的圓形碰撞邊界)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius) # 畫圓形(測試觀看用):pygame.draw.circle(要畫在哪, 顏色, 圓心位置, 半徑)
        # 讓image的左上角 對齊 框框座標(200,200)的位置(注意:框框 座標體系 原點 在 左上角，座標往右下增加):
        # self.rect.x = 200
        # self.rect.y = 200
        # 讓image左右置中:
        self.rect.centerx = WIDTH/2 # centerx為image在x軸方向的中間點
        # 讓image置底:
        self.rect.bottom = HEIGHT-10 # image底部邊界座標 等於視窗高度-10(等同底部留10單位空間)
        # 讓image置中:
        # self.rect.center = (WIDTH/2, HEIGHT/2) # centerx為image在x軸及y軸方向的中間點
        self.speedx = 8 # 屬性speedx x軸的移動速度

    # 方向控制
    def update(self):
        key_pressed = pygame.key.get_pressed() # pygame.key.get_pressed() 會回傳一整串布林值(代表鍵盤上每個按鍵是否被按下去的狀態)，將此一整串布林值 指定給 變數 key_pressed
        if key_pressed[pygame.K_d]: # 判斷d鍵是否被按下
            self.rect.x += self.speedx # 按下的話 image就往右移speedx單位 #把原先的x座標值+speedx後的值 指定給 x座標值 #這個類別本身的屬性 要加self.
        if key_pressed[pygame.K_a]:
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
        # 創建bullet子彈sprite物件後，於 all_sprites及bullets Sprite群組 加入 該子彈物件
        bullet = Bullet(self.rect.centerx, self.rect.top) 
        # 使用Bullet類別(Sprite類別) 創建一個bullet物件(子彈)(Sprite物件)，初始函式要求傳入子彈初始位置(此處傳入玩家飛船位置)
        # centerx為 image(玩家飛船)x軸的中間座標，top為image(玩家飛船)的頂部邊界(子彈 初始位置為 玩家飛船 的 頂部中央)
        all_sprites.add(bullet)
        bullets.add(bullet) 

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
        self.radius = self.rect.width * 0.85 / 2 # 設定半徑 # self.rect.width為image(石頭)寬度
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

# Sprite群組
all_sprites = pygame.sprite.Group() # 將 變數all_sprites 指定為 一個sprite群組，群組中可放很多 sprite物件
rocks = pygame.sprite.Group() # 專放石頭sprite物件的sprite群組
bullets = pygame.sprite.Group() # 專放子彈sprite物件的sprite群組 (石頭和子彈放在不一樣的sprite群組，才能用pygame內建的函式判斷 石頭與子彈是否碰撞)

# 創建player玩家飛船sprite物件後，於 all_sprites Sprite群組加入 該玩家飛船物件
player = Player() # 使用Player類別(Sprite類別) 創建一個player物件(玩家飛船)(Sprite物件) # 括弧裡不用寫self
all_sprites.add(player) # player物件(Sprite物件) 加入 sprite群組
# 創建r石頭sprite物件後，於 all_sprites及rocks Sprite群組 加入 該石頭物件
for i in range(8): # 執行以下程式碼8次(創建石頭物件 於 all_sprites及rocks Sprite群組)
    r = Rock()
    all_sprites.add(r)
    rocks.add(r)


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
        elif event.type == pygame.KEYDOWN: # .KEYDOWN表示按下鍵盤 
            if event.key == pygame.K_SPACE: # 如果按下空白鍵盤
                player.shoot() # 就呼叫飛船物件的shoot函式

    # 更新遊戲
    all_sprites.update() # 執行all_sprites Sprite群組中 每個Sprite物件的 update函式(記得，目前一秒鐘會跑60次這個函式)
    # 以pygame內建的函式判斷 石頭與子彈(各自位於不同sprite群組)是否碰撞，會回傳一個 「字典」，裡面裝著 被碰撞到的石頭與子彈，將此字典 指定給 變數hits
    hits = pygame.sprite.groupcollide(rocks, bullets, True, True) # groupcollide(裏頭物件被碰撞的群組1, 裏頭物件被碰撞的群組2, 被碰撞到的群組1內的物件是否要被刪除, 被碰撞到的群組2內的物件是否要被刪除)
    for hit in hits: # 對在字典hits中的每個資料(被碰撞到所以消失的物件)，進行以下程式碼(重新建回消失的物件)
        r = Rock() # 創建石頭Sprite物件
        all_sprites.add(r) # 將石頭Sprite物件 加入 all_sprites Sprite群組(物件才會被更新 並呈現於畫面)
        rocks.add(r) # 將石頭Sprite物件 加入 rocks Sprite群組(物件才能繼續被判斷是否與子彈碰撞)
        # 子彈本來就可無限發射(按空白鍵就會執行shoot函式，生成子彈物件) 所以不用做如石頭的碰撞消失重生處理
    # 判斷 玩家飛船與石頭兩類Sprite物件 是否碰撞，此函式回傳 「列表」，存放所有 碰撞到 玩家飛船 的 石頭
    hits = pygame.sprite.spritecollide(player, rocks, False, pygame.sprite.collide_circle) #spritecollide(裏頭物件被碰撞的群組1, 裏頭物件被碰撞的群組2, 被碰撞到的群組2內的物件是否要被刪除) #撞到就要關閉遊戲了 所以要不要刪除物件意義不大 #python中比較特別，變數名稱相同時，後指定的值，不會影響前面指定給同名變數的值
    # spritecollide預設為矩形碰撞判斷 
    # pygame.sprite.collide_circle讓其改為圓形碰撞判斷，但player, rocks就要加上radius屬性(用以設定圓形半徑大小)
    if hits: # 如果玩家飛船有撞到石頭(True)
        running = False # 就跳出回圈，關閉遊戲

    # 畫面顯示
    screen.fill(BLACK) # screen是前面創建的視窗變數 # full函式裡面要放代表顏色的元組(RGB)，會用該顏色填滿畫面
    screen.blit(background_img, (0,0)) # blit為畫的意思 #blit(要畫的圖片, 畫的位置:(0,0)表示 圖片左上角 對齊座標0,0位置)
    all_sprites.draw(screen) # 把all_sprites群組裡的東西(各個Sprite物件)都畫到screen(畫面)上
    pygame.display.update() # 更新畫面 (記得，目前一秒鐘會跑60次這個函式=更新60次畫面)

pygame.quit() # 既然跳出迴圈，表示遊戲進行狀態running為false，故進行關閉視窗函數