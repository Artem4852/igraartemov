import pygame, os, time, textwrap
from PIL import Image

pygame.init()

class cursorSprite(pygame.sprite.Sprite):
  def __init__(self, x, y, imagePath):
    super().__init__()
    # self.image = pygame.image.load(imagePath).convert_alpha()
    self.image = imagePath
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y
    self.cursorX = 0
    self.cursorY = 0

    self.step = 500/currentLevelSize
    self.upPressed = False
    self.downPressed = False
    self.rightPressed = False
    self.leftPressed = False
    self.returnPressed = False

    self.playerScore = 0

  def update(self):
    global menu, _credits, paused, currentTutorialMessage, firstMistake, firstMistakeSeen
    keys = pygame.key.get_pressed()
    if not paused:
      if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        if not self.leftPressed:
          if self.cursorX == 0:
            self.cursorX = currentLevelSize - 1
          else:
            self.cursorX -= 1
          self.leftPressed = True
      else:
        self.leftPressed = False
      if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        if not self.rightPressed:
          if self.cursorX == currentLevelSize - 1:
            self.cursorX = 0
          else:
            self.cursorX += 1
          self.rightPressed = True
      else:
        self.rightPressed = False
      if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        if not self.downPressed:
          if self.cursorY == currentLevelSize - 1:
            self.cursorY = 0
          else:
            self.cursorY += 1
          self.downPressed = True
      else:
        self.downPressed = False
      if keys[pygame.K_UP] or keys[pygame.K_w]:
        if not self.upPressed:
          if self.cursorY == 0:
            self.cursorY = currentLevelSize - 1
          else:
            self.cursorY -= 1
          self.upPressed = True
      else:
        self.upPressed = False
      
    self.rect.x = self.step * self.cursorX
    self.rect.y = self.step * self.cursorY + 150 + gap

    if keys[pygame.K_SPACE]:
      if patterns[currentLevel][self.cursorY][self.cursorX] == 0 and filledPattern[self.cursorY][self.cursorX] == 2:
        filledPattern[self.cursorY][self.cursorX] = 0
        self.playerScore += 1
        pygame.draw.rect(blocksCrossesSufrace, colors["FG"], (self.rect.x, self.rect.y, self.step, self.step))
      elif patterns[currentLevel][self.cursorY][self.cursorX] == 1 and filledPattern[self.cursorY][self.cursorX] == 2:
        filledPattern[self.cursorY][self.cursorX] = 1
        blocksCrossesSufrace.blit(crossSprite, (self.rect.x, self.rect.y))
        if tutorial and not firstMistake:
          firstMistake = True
          print(firstMistake, 2)
    elif keys[pygame.K_c]:
      if patterns[currentLevel][self.cursorY][self.cursorX] == 1 and filledPattern[self.cursorY][self.cursorX] == 2:
        filledPattern[self.cursorY][self.cursorX] = 1
        self.playerScore += 1
        blocksCrossesSufrace.blit(crossSprite, (self.rect.x, self.rect.y))
      elif patterns[currentLevel][self.cursorY][self.cursorX] == 0 and filledPattern[self.cursorY][self.cursorX] == 2:
        filledPattern[self.cursorY][self.cursorX] = 0
        pygame.draw.rect(blocksCrossesSufrace, colors["FG"], (self.rect.x, self.rect.y, self.step, self.step))
        if tutorial and not firstMistake:
          firstMistake = True
    elif keys[pygame.K_RETURN]:
      if len(tutorialMessages) - 1 != currentTutorialMessage and not self.returnPressed and not currentTutorialMessage in unskippableMessages and (not firstMistake or firstMistakeSeen):
        currentTutorialMessage += 1
      elif not firstMistakeSeen and firstMistake:
        firstMistakeSeen = True
      self.returnPressed = True
    else:
      self.returnPressed = False

    if keys[pygame.K_ESCAPE]:
      paused = True
      _credits = False

WIDTH, HEIGHT = 600, 650
colors = {
  "BG": (239, 239, 239),
  "FG": (148, 126, 176),
  "Accent": (45, 48, 71),
  "Cross": (146, 20, 12),
  "Spare": (194, 197, 187),
  "Black": (0, 0, 0)
}
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill(colors["BG"])
pygame.display.set_caption("igra Artema")
cursorWidth = [4, 5, 7.5]
currentCursorWidth = 0

running = True
menu = True
_credits = False
levelsMenu = False
paused = False
levelPassed = False
tutorial = True
firstMistake = False
firstMistakeSeen = False
tutorialMessages = [
  "Welcome! In this tutorial you will learn to play the game. Movement is performed with arrow keys or WASD keys. Press them to move cursor up, down, left and right.", # 0
  "Numbers on the top and right sides of the field indicate which parts of the field should be filled, and which not.", # 1
  "For instance, this number 5 means that all 5 parts of the row should be filled, as the size of this level is 5x5.", # 2
  "To fill a space on the field press Space. If you see that the area should remain unfilled, put the cross there by pressing C.", # 3
  "Now use cursor movement and Space to go over the marked areas and fill them.", # 4
  "Nice! Now let's take these 1's. If the numbers are not added, it means that they should go separately.", # 5
  "This means that there should be one spot filled, at least one skipped, one filled, at least one skipped, and so on...", # 6
  "If we take a look at the field, it will look something like this. 1st, 3rd and 5th blocks will be filled.", # 7
  "Now it's your turn. Fill those three spots.", # 8
  "Amazing job! Now you can fill those two remaining empty blocks with crosses by pressing C.", # 9
  "Correct! This will especially help you in the future when solving harder puzzles.", # 10
  "Look at this column. The numbers 2 and 1 are a bit more complicating to solve. The 2 before the 1 means that 2x1 rectangle should go first - above.", # 11
  "First, this square is already filled and that means it is a part of 2x1 rectangle, because this is the only way we can fill this column.", # 12
  "This means that the first spot in the column will remain empty anyways. Put a cross there!", # 13
  "Now there are four spots left. As said before, rectangles 2x1 and 1x1 should go separately.", # 14
  "If we assume that this spot is filled - as another part of 2x1 rectangle, then it will be imposible for us to fit one more rectangle as we need some space between.", # 15
  "Then, the only option for our 2x1 rectangle is to fill this spot. Fill it!", # 16
  "Now, if we take in count that there should be space left between rectangles, then there is only one option left for our 1x1 rectangle.", # 17
  "Fill this spot and put a cross at the last spot of the column, at the place of the empty space.", # 18
  "Perfect! One more column filled and we are closer to the win. Now try to use your knowledge to fill these two columns.", # 19
  "You are learning so fast! Now, the only column left is the middle one. Considering that we filled all the other columns, it won't be that hard.", # 20
  "Take a look at both, the column numbers and the rows numbers. For instance, these two 1's mean that there should be only two spots filled in this row.", # 21
  "They should have a space between. We already have two spots filled, so you can put a cross between and continue with other numbers.",  # 22
  "Let's take these 1's. We solved similar thing already. Not only those three, but also this 1 at the top shows us that this spot should definitely be filled. Fill it.", # 23
  "The level is almost solved at this point! Let's take a look at this 1. All the spots in this row are with crosses, so the only spot left should be filled. Fill it.", # 24
  "Now look at these 2's. We already have two 2x1 rectangles so the only space left should be filled with a cross. Complete the level by putting it in place.", # 25
  ]
tips = [
  "Tip: if a block or the cross is put in a wrong spot, the spot will be filled with a correct object, but the score will not increase."
]
unskippableMessages = [4, 8, 9, 13, 16, 18, 19, 22, 23, 24, 25]
currentTutorialMessage = 0

totalLevels = 10
currentLevel = 0
currentLevelSize = 5
filledPattern = [[2, 2, 2, 2, 2] for _ in range(5)]
gap = 0
page = 0
firstFilledPatternTime = 0
creditsTime = 0
messageSlidingTime = 0

sprites = pygame.sprite.Group()
cursorImage = pygame.Surface((100, 100)).convert_alpha()
cursor = cursorSprite(0, 150, cursorImage)
sprites.add(cursor)

mainMenuSurface = pygame.Surface((WIDTH, HEIGHT)).convert_alpha()
levelsMenuSurface = pygame.Surface((WIDTH, HEIGHT)).convert_alpha()
creditsSurface = pygame.Surface((WIDTH, HEIGHT)).convert_alpha()
levelSurface = pygame.Surface((WIDTH, HEIGHT)).convert_alpha()
blocksCrossesSufrace = pygame.Surface((WIDTH, HEIGHT)).convert_alpha()
textSurface = pygame.Surface((WIDTH, HEIGHT)).convert_alpha()
pausedSurface = pygame.Surface((WIDTH, HEIGHT)).convert_alpha()
levelPassedSurface = pygame.Surface((WIDTH, HEIGHT)).convert_alpha()
tutorialSurface = pygame.Surface((WIDTH, HEIGHT)).convert_alpha()

def loadImages():
  global mainMenuBG, mainMenuLevelsButton, mainMenuCreditsButton, creditsBG, levelsMenuBG, levelsMenuControlForward, levelsMenuControlBackward, crossSprite, buttonsX, buttonsY, numberFont, scoreFont, levelNumbersFont, pausedBG, pausedButtonMenu, pausedButtonContinue, pausedButtonRestart, pausedButtonsCoordinates, levelPassedButtonMainMenu, levelPassedButtonNextLevel, levelPassedButtonRestart, levelPassedButtonsCoordinates, creditsText, levelPassedButtonCredits, tutorialMessageSurface, tutorialFontMain, tutorialFontSecondary, tutorialOverlays, widthDiff
  
  widthDiff = (WIDTH - 560)//2

  numberFont = pygame.font.Font("assets/Fonts/Main/static/SofiaSans-SemiBold.ttf", 16)
  scoreFont = pygame.font.Font("assets/Fonts/PressStart2P-Regular.ttf", 20)
  levelNumbersFont = pygame.font.Font("assets/Fonts/PressStart2P-Regular.ttf", 24)
  menuFont = pygame.font.Font("assets/Fonts/PressStart2P-Regular.ttf", 26)
  tutorialFontMain = pygame.font.Font("assets/Fonts/merriweather/Merriweather-Regular.otf", 14)
  tutorialFontSecondary = pygame.font.Font("assets/Fonts/PressStart2P-Regular.ttf", 8)

  cursorImage.fill((0, 0, 0, 0))
  pygame.draw.rect(cursorImage, colors["Accent"], (0, 0, cursorImage.get_size()[0]//2, cursorWidth[currentCursorWidth]))
  pygame.draw.rect(cursorImage, colors["Accent"], (0, 0, cursorWidth[currentCursorWidth], cursorImage.get_size()[1]//2))
  pygame.draw.rect(cursorImage, colors["Accent"], (cursorImage.get_size()[0]//2, cursorImage.get_size()[1] - cursorWidth[currentCursorWidth], cursorImage.get_size()[0], cursorImage.get_size()[1]))
  pygame.draw.rect(cursorImage, colors["Accent"], (cursorImage.get_size()[0] - cursorWidth[currentCursorWidth], cursorImage.get_size()[1]//2, cursorImage.get_size()[0], cursorImage.get_size()[1]))
  
  crossSprite = pygame.image.load("assets/sprites/cross.png").convert_alpha()
  crossPixels = pygame.PixelArray(crossSprite)
  crossPixels.replace((0, 0, 0, 255), colors["FG"])
  del crossPixels

  mainMenuBG = pygame.image.load("assets/sprites/mainMenuBG.png")
  mainMenuBG = pygame.transform.smoothscale(mainMenuBG, (WIDTH, HEIGHT))
  mainMenuLevelsButton = pygame.image.load("assets/sprites/mainMenuLevelsButton.png")
  mainMenuLevelsButton = pygame.transform.smoothscale(mainMenuLevelsButton, (mainMenuLevelsButton.get_size()[0]/2, mainMenuLevelsButton.get_size()[1]/2))
  mainMenuCreditsButton = pygame.image.load("assets/sprites/mainMenuCreditsButton.png")
  mainMenuCreditsButton = pygame.transform.smoothscale(mainMenuCreditsButton, (mainMenuCreditsButton.get_size()[0]/2, mainMenuCreditsButton.get_size()[1]/2))
  creditsBG = pygame.image.load("assets/sprites/credits.png")
  creditsBG = pygame.transform.smoothscale(creditsBG, (WIDTH, HEIGHT))
  creditsText = pygame.image.load("assets/sprites/creditsText.png")
  levelsMenuBG = pygame.image.load("assets/sprites/levels.png")
  levelsMenuBG = pygame.transform.smoothscale(levelsMenuBG, (WIDTH, HEIGHT))
  levelsMenuControlForward = pygame.image.load("assets/sprites/levelsPageControlForward.png")
  levelsMenuControlForward = pygame.transform.smoothscale(levelsMenuControlForward, (levelsMenuControlForward.get_size()[0] // 2, levelsMenuControlForward.get_size()[1] // 2))
  levelsMenuControlBackward = pygame.image.load("assets/sprites/levelsPageControlBackwards.png")
  levelsMenuControlBackward = pygame.transform.smoothscale(levelsMenuControlBackward, (levelsMenuControlBackward.get_size()[0] // 2, levelsMenuControlBackward.get_size()[1] // 2))
  pausedButtonContinue = pygame.image.load("assets/sprites/pauseButtonContinue.png").convert_alpha()
  pausedButtonMenu = pygame.image.load("assets/sprites/pauseButtonMenu.png").convert_alpha()
  pausedButtonRestart = pygame.image.load("assets/sprites/pauseButtonRestart.png").convert_alpha()
  pausedButtonsCoordinates = [(86 + widthDiff, 187), (86 + widthDiff, 287), (86 + widthDiff, 387)]
  levelPassedButtonNextLevel = pygame.image.load("assets/sprites/levelPassedButtonNextLevel.png").convert_alpha()
  levelPassedButtonMainMenu = pygame.image.load("assets/sprites/levelPassedButtonMainMenu.png").convert_alpha()
  levelPassedButtonRestart = pygame.image.load("assets/sprites/levelPassedButtonRestart.png").convert_alpha()
  levelPassedButtonCredits = pygame.image.load("assets/sprites/levelPassedButtonCredits.png").convert_alpha()
  levelPassedButtonsCoordinates = [(86 + widthDiff, 212), (86 + widthDiff, 312), (86 + widthDiff, 412)]

  mainMenuSurface.fill(colors["BG"])
  mainMenuSurface.blit(mainMenuBG, (0, 0))
  buttonsX = WIDTH/2 - mainMenuLevelsButton.get_size()[0]/2
  buttonsY = 270
  mainMenuSurface.blit(mainMenuLevelsButton, (buttonsX, buttonsY))
  mainMenuSurface.blit(mainMenuCreditsButton, (buttonsX, buttonsY + mainMenuCreditsButton.get_size()[1] + 20))
  creditsSurface.fill(colors["BG"])
  creditsSurface.blit(creditsBG, (0, 0))
  levelsMenuSurface.blit(levelsMenuBG, (0, 0))

  pygame.draw.rect(pausedSurface, (colors["Accent"][0], colors["Accent"][1], colors["Accent"][2], 127), (0, 0, WIDTH, HEIGHT))
  pygame.draw.rect(pausedSurface, (198, 198, 198, 229), (47 + widthDiff, 152, 462, 341), 0, 15)
  pygame.draw.rect(pausedSurface, (colors["Accent"][0], colors["Accent"][1], colors["Accent"][2], 229), (47 + widthDiff, 152, 462, 341), 5, 15)
  pausedSurface.blit(pausedButtonContinue, pausedButtonsCoordinates[0])
  pausedSurface.blit(pausedButtonMenu, pausedButtonsCoordinates[1])
  pausedSurface.blit(pausedButtonRestart, pausedButtonsCoordinates[2])

  pygame.draw.rect(levelPassedSurface, (colors["Accent"][0], colors["Accent"][1], colors["Accent"][2], 127), (0, 0, WIDTH, HEIGHT))
  pygame.draw.rect(levelPassedSurface, (198, 198, 198, 229), (23 + widthDiff, 95, 510, 421), 0, 15)
  pygame.draw.rect(levelPassedSurface, (colors["Accent"][0], colors["Accent"][1], colors["Accent"][2], 229), (23 + widthDiff, 95, 510, 421), 5, 15)
  levelPassedText = menuFont.render("Congratulations!", True, colors["Accent"])
  levelPassedTextCoords = (WIDTH//2-levelPassedText.get_size()[0]//2, 120)
  levelPassedSurface.blit(levelPassedText, (levelPassedTextCoords[0], levelPassedTextCoords[1]))
  levelPassedText = menuFont.render("Level passed", True, colors["Accent"])
  levelPassedTextCoords = (WIDTH//2-levelPassedText.get_size()[0]//2, 120)
  levelPassedSurface.blit(levelPassedText, (levelPassedTextCoords[0], levelPassedTextCoords[1] + levelPassedText.get_size()[1] + 15))

  tutorialMessageSurface = pygame.Surface((280, 150)).convert_alpha()
  pygame.draw.rect(tutorialMessageSurface, (198, 198, 198, 229), (0, 0, tutorialMessageSurface.get_size()[0], tutorialMessageSurface.get_size()[1]), 0, 15)
  pygame.draw.rect(tutorialMessageSurface, (colors["Accent"][0], colors["Accent"][1], colors["Accent"][2], 229), (0, 0, tutorialMessageSurface.get_size()[0], tutorialMessageSurface.get_size()[1]), 5, 15)
  skipText = tutorialFontSecondary.render("Press enter to continue", True, colors["Accent"])
  tutorialMessageSurface.blit(skipText, (tutorialMessageSurface.get_size()[0]//2 - skipText.get_size()[0]//2, tutorialMessageSurface.get_size()[1] - skipText.get_size()[1] - 15))

  tutorialOverlays = []
  for i in range(18):
    tutorialOverlays.append("")
    tutorialOverlays[i] = pygame.Surface((WIDTH, HEIGHT)).convert_alpha()
    tutorialOverlays[i].fill((0, 0, 0, 0))
  pygame.draw.rect(tutorialOverlays[0], colors["Cross"], (505, HEIGHT-475, 45, HEIGHT-(HEIGHT-450)), 3)
  pygame.draw.rect(tutorialOverlays[0], colors["Cross"], (25, HEIGHT-565, WIDTH-(WIDTH-450), 60), 3)
  pygame.draw.rect(tutorialOverlays[1], colors["Cross"], (505, HEIGHT-265, 20, 30), 3)
  pygame.draw.rect(tutorialOverlays[1], colors["Cross"], (0, HEIGHT-300, 500, 100), 3)
  pygame.draw.rect(tutorialOverlays[2], colors["Cross"], (440, HEIGHT-565, 20, 60), 3)
  pygame.draw.rect(tutorialOverlays[3], colors["Cross"], (400, HEIGHT-500, 100, 100), 3)
  pygame.draw.rect(tutorialOverlays[3], colors["Cross"], (400, HEIGHT-300, 100, 100), 3)
  pygame.draw.rect(tutorialOverlays[3], colors["Cross"], (400, HEIGHT-100, 100, 100), 3)
  pygame.draw.rect(tutorialOverlays[4], colors["Cross"], (400, HEIGHT-200, 100, 100), 3)
  pygame.draw.rect(tutorialOverlays[4], colors["Cross"], (400, HEIGHT-400, 100, 100), 3)
  pygame.draw.rect(tutorialOverlays[5], colors["Cross"], (300, HEIGHT-500, 100, 500), 3)
  pygame.draw.rect(tutorialOverlays[6], colors["Cross"], (300, HEIGHT-300, 100, 100), 3)
  pygame.draw.rect(tutorialOverlays[7], colors["Cross"], (300, HEIGHT-500, 100, 100), 3)
  pygame.draw.rect(tutorialOverlays[8], colors["Cross"], (300, HEIGHT-400, 100, 400), 3)
  pygame.draw.rect(tutorialOverlays[9], colors["Cross"], (300, HEIGHT-200, 100, 100), 3)
  pygame.draw.rect(tutorialOverlays[10], colors["Cross"], (300, HEIGHT-400, 100, 100), 3)
  pygame.draw.rect(tutorialOverlays[11], colors["Cross"], (300, HEIGHT-100, 100, 100), 3)
  pygame.draw.rect(tutorialOverlays[12], colors["Cross"], (0, HEIGHT-500, 100, 500), 3)
  pygame.draw.rect(tutorialOverlays[12], colors["Cross"], (100, HEIGHT-500, 100, 500), 3)
  pygame.draw.rect(tutorialOverlays[13], colors["Cross"], (505, HEIGHT-365, 35, 30), 3)
  pygame.draw.rect(tutorialOverlays[14], colors["Cross"], (200, HEIGHT-400, 100, 100), 3)
  pygame.draw.rect(tutorialOverlays[15], colors["Cross"], (200, HEIGHT-500, 100, 100), 3)
  pygame.draw.rect(tutorialOverlays[15], colors["Cross"], (505, HEIGHT-465, 45, 30), 3)
  pygame.draw.rect(tutorialOverlays[15], colors["Cross"], (240, HEIGHT-545, 20, 20), 3)
  pygame.draw.rect(tutorialOverlays[16], colors["Cross"], (505, HEIGHT-165, 20, 30), 3)
  pygame.draw.rect(tutorialOverlays[16], colors["Cross"], (200, HEIGHT-200, 100, 100), 3)
  pygame.draw.rect(tutorialOverlays[17], colors["Cross"], (505, HEIGHT-65, 35, 30), 3)
  pygame.draw.rect(tutorialOverlays[17], colors["Cross"], (200, HEIGHT-100, 100, 100), 3)

def loadPatterns():
  patterns = []
  patternFiles = os.listdir("assets/Patterns")
  patternFiles = [filename for filename in patternFiles if filename != ".DS_Store"]
  patternFiles.sort(key=lambda x: int(x.split("_")[1][:-4]))
  for patternFile in patternFiles:
    pattern = Image.open("assets/Patterns/" + patternFile).convert("RGB")
    pixels = pattern.getdata()
    pattern_pixels = []
    for x in range(pattern.height):
      pattern_pixels.append([])
      for y in range(pattern.width):
        pattern_pixels[x].append(0 if pixels[x*pattern.width+y][0] < 100 else 1)
    patterns.append(pattern_pixels)
  return patterns

def generateLevelsMenu():
  global levelButtons
  pages = []
  for i in range(len(patterns)):
    if i % 10 == 0:
      pages.append([])
    pages[-1].append(i)
  buttonSize = 75
  levelButtons = []
  for page in pages:
    levelButtons.append([])
    for instance in page:
      buttonSurface = pygame.Surface((buttonSize, buttonSize))
      pygame.draw.rect(buttonSurface, colors["Black"], (0, 0, buttonSize, buttonSize), border_radius=10)
      boxN = levelNumbersFont.render(str(instance+1), True, colors["BG"], colors["Black"])
      buttonSurface.blit(boxN, ((buttonSize-boxN.get_size()[0])//2, (buttonSize-boxN.get_size()[1])//2))
      levelButtons[-1].append([buttonSurface, instance])

def updateParams():
  global currentLevelSize, crossSprite, filledPattern, patterns, cursor, gap, firstFilledPatternTime, currentTutorialMessage
  currentLevelSize = len(patterns[currentLevel])
  cursor.step = int(500/currentLevelSize)
  cursor.image = pygame.transform.smoothscale(cursor.image, (cursor.step, cursor.step))
  cursor.cursorX = 0
  cursor.cursorY = 0
  crossSprite = pygame.transform.smoothscale(crossSprite, (cursor.step, cursor.step))
  filledPattern = [[2 for _ in range(currentLevelSize)] for _ in range(currentLevelSize)]
  cursor.playerScore = 0
  gap = 500 - cursor.step * currentLevelSize
  firstFilledPatternTime = 0

  currentCursorWidth = 0 if currentLevelSize <=6 else 2
  cursorImage.fill((0, 0, 0, 0))
  pygame.draw.rect(cursorImage, colors["Accent"], (0, 0, cursorImage.get_size()[0]//2, cursorWidth[currentCursorWidth]))
  pygame.draw.rect(cursorImage, colors["Accent"], (0, 0, cursorWidth[currentCursorWidth], cursorImage.get_size()[1]//2))
  pygame.draw.rect(cursorImage, colors["Accent"], (cursorImage.get_size()[0]//2, cursorImage.get_size()[1] - cursorWidth[currentCursorWidth], cursorImage.get_size()[0], cursorImage.get_size()[1]))
  pygame.draw.rect(cursorImage, colors["Accent"], (cursorImage.get_size()[0] - cursorWidth[currentCursorWidth], cursorImage.get_size()[1]//2, cursorImage.get_size()[0], cursorImage.get_size()[1]))

  currentTutorialMessage = 0

def drawGrid():
  levelSurface.fill((0, 0, 0, 0))
  pygame.draw.rect(levelSurface, colors["Accent"], (0, 150+gap, cursor.step*currentLevelSize, cursor.step*currentLevelSize), 2)
  for x in range(currentLevelSize):
    for y in range(currentLevelSize):
      pygame.draw.rect(levelSurface, colors["Accent"], (x*cursor.step, y*cursor.step+150+gap, cursor.step, cursor.step), 1)
  drawNumbers()

def drawNumbers():
  currentPattern = patterns[currentLevel]
  numbers = []
  distanceBetweenNumbers = 20
  distanceFromGrid = 15
  for x in range(currentLevelSize):
    currentSequence = [0]
    for y in range(currentLevelSize):
      if currentPattern[y][x] == 0:
        currentSequence[-1] += 1
      else:
        currentSequence.append(0)
    currentSequence = [num for num in currentSequence if num != 0]
    numbers.append(currentSequence)

  for x in range(currentLevelSize):
    currentSequence = [0]
    for y in range(currentLevelSize):
      if currentPattern[x][y] == 0:
        currentSequence[-1] += 1
      else:
        currentSequence.append(0)
    currentSequence = [num for num in currentSequence if num != 0]
    numbers.append(currentSequence)

  for sequenceN in range(len(numbers)):
    horizontal = sequenceN <= len(numbers)/2-1
    sequence = numbers[sequenceN]
    if horizontal:
      sequence = sequence[::-1]
    for number in range(len(sequence)):
      numberText = numberFont.render(str(sequence[number]), True, colors["Accent"])
      textWidth, textHeight = numberText.get_size()
      if horizontal:
        xCoord = sequenceN * cursor.step + cursor.step//2 - textWidth//2
        yCoord = 150 - distanceFromGrid - textHeight//2 - number * distanceBetweenNumbers
      else:
        xCoord = 550 - (50 - distanceFromGrid) - textWidth//2 + number * distanceBetweenNumbers//1.5
        yCoord = (sequenceN - currentLevelSize) * cursor.step + 150 + cursor.step//2 - textHeight//2 + gap
      levelSurface.blit(numberText, (xCoord, yCoord))

def clickedOn(rect, mousePos, isRect = False):
  mouseX, mouseY = mousePos
  if not isRect:
    rect = rect.get_rect()
  if rect.collidepoint(mouseX, mouseY):
    return True
  return False

def updateScreen():
  global running, menu, _credits, currentLevel, filledPattern, levelsMenu, levelButtons, page, paused, firstFilledPatternTime, levelPassed, creditsTime, currentTutorialMessage, messageSlidingTime, tutorial

  levelButtonsX = [200, 280]
  levelButtonsY = 440

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

    elif event.type == pygame.MOUSEBUTTONDOWN:
      mouseX, mouseY = event.pos
      if menu and not _credits and not levelsMenu and not paused:
        if mainMenuLevelsButton.get_rect(topleft=(buttonsX, buttonsY)).collidepoint(mouseX, mouseY):
          levelsMenu = True
          page = 0
        elif mainMenuCreditsButton.get_rect(topleft=(buttonsX, buttonsY + mainMenuCreditsButton.get_size()[1] + 20)).collidepoint(mouseX, mouseY):
          _credits = True
      elif levelsMenu:
        for button in levelButtons[page]:
          buttonRect = pygame.Rect(button[2][0], button[2][1], 75, 75)
          if clickedOn(buttonRect, (mouseX, mouseY), True):
            currentLevel = button[1]
            updateParams()
            drawGrid()
            blocksCrossesSufrace.fill((0, 0, 0, 0))
            menu = False
            levelsMenu = False
        if levelsMenuControlForward.get_rect(topleft=(levelButtonsX[1], levelButtonsY)).collidepoint(mouseX, mouseY):
          page += 1
        elif levelsMenuControlBackward.get_rect(topleft=(levelButtonsX[0], levelButtonsY)).collidepoint(mouseX, mouseY):
          page -= 1
      elif paused:
        if pausedButtonContinue.get_rect(topleft=pausedButtonsCoordinates[0]).collidepoint(mouseX, mouseY):
          paused = False
        elif pausedButtonMenu.get_rect(topleft=pausedButtonsCoordinates[1]).collidepoint(mouseX, mouseY):
          paused = False
          menu = True
        elif pausedButtonRestart.get_rect(topleft=pausedButtonsCoordinates[2]).collidepoint(mouseX, mouseY):
          paused = False
          updateParams()
          drawGrid()
          blocksCrossesSufrace.fill((0, 0, 0, 0))
      elif levelPassed:
        if len(patterns) - 1 != currentLevel:
          if levelPassedButtonNextLevel.get_rect(topleft=levelPassedButtonsCoordinates[0]).collidepoint(mouseX, mouseY):
            currentLevel += 1
            updateParams()
            drawGrid()
            blocksCrossesSufrace.fill((0, 0, 0, 0))
            levelPassed = False
          elif levelPassedButtonMainMenu.get_rect(topleft=levelPassedButtonsCoordinates[1]).collidepoint(mouseX, mouseY):
            levelPassed = False
            menu = True
        else:
          if levelPassedButtonMainMenu.get_rect(topleft=levelPassedButtonsCoordinates[0]).collidepoint(mouseX, mouseY):
            levelPassed = False
            menu = True
          elif levelPassedButtonCredits.get_rect(topleft=levelPassedButtonsCoordinates[1]).collidepoint(mouseX, mouseY):
            levelPassed = False
            menu = True
            _credits = True
        if levelPassedButtonRestart.get_rect(topleft=levelPassedButtonsCoordinates[2]).collidepoint(mouseX, mouseY):
          updateParams()
          drawGrid()
          blocksCrossesSufrace.fill((0, 0, 0, 0))
          levelPassed = False

    elif pygame.key.get_pressed()[pygame.K_ESCAPE]:
      if levelsMenu:
        levelsMenu = False
        page = 0
      elif not menu and not paused:
        paused = True

  screen.fill(colors["BG"])

  if not menu:
    textSurface.fill((255, 255, 255, 0))
    playerScore = scoreFont.render("Score: " + str(cursor.playerScore), True, colors["Accent"])
    textSurface.blit(playerScore, (WIDTH - playerScore.get_size()[0] - 20, 20))
    level = scoreFont.render("Level " + str(currentLevel+1), True, colors["Accent"])
    textSurface.blit(level, (20, 20))

    screen.blit(blocksCrossesSufrace, (0, 0))
    screen.blit(levelSurface, (0, 0))
    screen.blit(textSurface, (0, 0))

    sprites.update()
    sprites.draw(screen)

    if currentLevel == 0 and tutorial:
      tutorialMessageSurfaceX = 0
      tutorialMessageSurfaceY = tutorialSurface.get_size()[1] - tutorialMessageSurface.get_size()[1]
      tutorialSurface.fill((0, 0, 0, 0))
      tutorialMessageSurface.fill((0, 0, 0, 0))
      pygame.draw.rect(tutorialMessageSurface, (198, 198, 198, 229), (0, 0, tutorialMessageSurface.get_size()[0], tutorialMessageSurface.get_size()[1]), 0, 15)
      pygame.draw.rect(tutorialMessageSurface, (colors["Accent"][0], colors["Accent"][1], colors["Accent"][2], 229), (0, 0, tutorialMessageSurface.get_size()[0], tutorialMessageSurface.get_size()[1]), 5, 15)
      if currentTutorialMessage not in unskippableMessages:
        skipText = tutorialFontSecondary.render("Press enter to continue", True, colors["Accent"])
      else:
        skipText = tutorialFontSecondary.render("Complete the task to continue", True, colors["Accent"])
      tutorialMessageSurface.blit(skipText, (tutorialMessageSurface.get_size()[0]//2 - skipText.get_size()[0]//2, tutorialMessageSurface.get_size()[1] - skipText.get_size()[1] - 15))
      if currentTutorialMessage == 1:
        tutorialSurface.blit(tutorialOverlays[0], (0, 0))
      elif currentTutorialMessage in [2, 4]:
        tutorialSurface.blit(tutorialOverlays[1], (0, 0))
      elif currentTutorialMessage in [5, 6]:
        tutorialSurface.blit(tutorialOverlays[2], (0, 0))
      elif currentTutorialMessage in [7, 8]:
        tutorialSurface.blit(tutorialOverlays[3], (0, 0))
      elif currentTutorialMessage == 9:
        tutorialSurface.blit(tutorialOverlays[4], (0, 0))
      elif currentTutorialMessage == 11:
        tutorialSurface.blit(tutorialOverlays[5], (0, 0))
      elif currentTutorialMessage == 12:
        tutorialSurface.blit(tutorialOverlays[6], (0, 0))
      elif currentTutorialMessage == 13:
        tutorialSurface.blit(tutorialOverlays[7], (0, 0))
      elif currentTutorialMessage == 14:
        tutorialSurface.blit(tutorialOverlays[8], (0, 0))
      elif currentTutorialMessage == 15:
        tutorialSurface.blit(tutorialOverlays[9], (0, 0))
      elif currentTutorialMessage == 16:
        tutorialSurface.blit(tutorialOverlays[10], (0, 0))
      elif currentTutorialMessage in [17, 18]:
        tutorialSurface.blit(tutorialOverlays[11], (0, 0))
      elif currentTutorialMessage == 19:
        if messageSlidingTime == 0:
          messageSlidingTime = time.time()
        elif time.time() - messageSlidingTime <= .5:
          tutorialMessageSurfaceX = (time.time() - messageSlidingTime) / .5 * (500 - tutorialMessageSurface.get_width())
        else:
          tutorialMessageSurfaceX = 500 - tutorialMessageSurface.get_width()
        tutorialSurface.blit(tutorialOverlays[12], (0, 0))
      elif currentTutorialMessage == 20:
        if messageSlidingTime == 0:
          messageSlidingTime = time.time()
        elif time.time() - messageSlidingTime <= .5:
          tutorialMessageSurfaceX = 500 - tutorialMessageSurface.get_width() - (time.time() - messageSlidingTime) / .5 * (500 - tutorialMessageSurface.get_width())
        else: tutorialMessageSurfaceX = 0
      elif currentTutorialMessage == 21:
        messageSlidingTime = 0
        tutorialSurface.blit(tutorialOverlays[13], (0, 0))
      elif currentTutorialMessage == 22:
        tutorialSurface.blit(tutorialOverlays[14], (0, 0))
      elif currentTutorialMessage == 23:
        tutorialSurface.blit(tutorialOverlays[15], (0, 0))
      elif currentTutorialMessage == 24:
        if messageSlidingTime == 0:
          messageSlidingTime = time.time()
        elif time.time() - messageSlidingTime <= .5:
          tutorialMessageSurfaceY = (HEIGHT - tutorialMessageSurface.get_size()[1]) - ((time.time() - messageSlidingTime) / .5 * (500 - tutorialMessageSurface.get_size()[1]))
        else:
          tutorialMessageSurfaceY = HEIGHT - 500
        tutorialSurface.blit(tutorialOverlays[16], (0, 0))
      elif currentTutorialMessage == 25:
        tutorialMessageSurfaceY = HEIGHT - 500
        tutorialSurface.blit(tutorialOverlays[17], (0, 0))

      if currentTutorialMessage == 4 and 2 not in filledPattern[2]:
        currentTutorialMessage += 1
      elif currentTutorialMessage == 8 and 2 not in [filledPattern[0][4], filledPattern[2][4], filledPattern[4][4]]:
        currentTutorialMessage += 1
      elif currentTutorialMessage == 9 and 2 not in [filledPattern[1][4], filledPattern[3][4]]:
        currentTutorialMessage += 1
      elif currentTutorialMessage == 13 and filledPattern[0][3] != 2:
        currentTutorialMessage += 1
      elif currentTutorialMessage == 16 and filledPattern[1][3] != 2:
        currentTutorialMessage += 1
      elif currentTutorialMessage == 18 and 2 not in [filledPattern[3][3], filledPattern[4][3]]:
        currentTutorialMessage += 1
      elif currentTutorialMessage == 19 and (2 not in [filledPattern[i][0] for i in range(5)]) and (2 not in [filledPattern[i][1] for i in range(5)]):
        currentTutorialMessage += 1
        messageSlidingTime = 0
      elif currentTutorialMessage == 22 and filledPattern[1][2] != 2:
        currentTutorialMessage += 1
      elif currentTutorialMessage == 23 and filledPattern[0][2] != 2:
        currentTutorialMessage += 1
      elif currentTutorialMessage == 24 and filledPattern[3][2] != 2:
        currentTutorialMessage += 1
      elif currentTutorialMessage == 25 and filledPattern[4][2] != 2:
        tutorial = False
      tutorialText = [""]
      currentTutorialMessageText = tutorialMessages[currentTutorialMessage] if not firstMistake or firstMistakeSeen else tips[0]
      for word in currentTutorialMessageText.split(" "):
        if tutorialFontMain.render(tutorialText[-1], True, colors["Accent"]).get_width() + 40 >= tutorialMessageSurface.get_width() - 40:
          tutorialText[-1] = tutorialText[-1][:-1]
          tutorialText.append("")
        tutorialText[-1] += word + " "
      textY = 15
      for line in tutorialText:
        messageLine = tutorialFontMain.render(line, True, colors["Accent"])
        tutorialMessageSurface.blit(messageLine, (tutorialMessageSurface.get_width()//2 - messageLine.get_width()//2, textY))
        textY += messageLine.get_height() + 3
      tutorialSurface.blit(tutorialMessageSurface, (tutorialMessageSurfaceX, tutorialMessageSurfaceY))
      screen.blit(tutorialSurface, (0, 0))

    if paused:
      screen.blit(pausedSurface, (0, 0))
    
    if sum(1 for row in filledPattern for item in row if item == 2) == 0:
      if firstFilledPatternTime == 0:
        firstFilledPatternTime = time.time()
      elif time.time() - firstFilledPatternTime >= 1:
        levelPassed = True
        if len(patterns) - 1 != currentLevel:
          levelPassedSurface.blit(levelPassedButtonNextLevel, levelPassedButtonsCoordinates[0])
          levelPassedSurface.blit(levelPassedButtonMainMenu, levelPassedButtonsCoordinates[1])
          levelPassedSurface.blit(levelPassedButtonRestart, levelPassedButtonsCoordinates[2])
        else:
          levelPassedSurface.blit(levelPassedButtonMainMenu, levelPassedButtonsCoordinates[0])
          levelPassedSurface.blit(levelPassedButtonCredits, levelPassedButtonsCoordinates[1])
          levelPassedSurface.blit(levelPassedButtonRestart, levelPassedButtonsCoordinates[2])

        screen.blit(levelPassedSurface, (0, 0))
    else:
      levelPassed = False
  
  else:
    if not _credits and not levelsMenu:
      screen.blit(mainMenuSurface, (0, 0))
    elif _credits:
      movementDuration = 15
      delay = .5
      creditsSurface.fill(colors["BG"])
      textPos = (WIDTH//2 - creditsText.get_size()[0]//2, 300)
      if creditsTime == 0:
        creditsTime = time.time()
      elif time.time() - creditsTime >= delay:
        textPos = (textPos[0], textPos[1] - (time.time() - creditsTime - delay) / movementDuration * (creditsText.get_size()[1] + textPos[1]))
      creditsSurface.blit(creditsText, textPos)
      creditsSurface.blit(creditsBG, (0, 0))
      screen.blit(creditsSurface, (0, 0))
      if time.time() - creditsTime >= movementDuration + delay:
        _credits = False
        creditsTime = 0
    elif levelsMenu:
      levelsMenuSurface.fill(colors["BG"])
      levelsMenuSurface.blit(levelsMenuBG, (0, 0))
      for surface in range(len(levelButtons[page])):
        instance = levelButtons[page][surface][1] - (levelButtons[page][surface][1] // 10 * 10)
        if len(levelButtons[page][surface]) == 2: levelButtons[page][surface].append([]) 
        levelButtons[page][surface][2] = (42 + 100 * instance, 240) if instance <= 4 else (42 + 100 * (instance - 5), 340)
        levelsMenuSurface.blit(levelButtons[page][surface][0], levelButtons[page][surface][2])

      if len(levelButtons) - 1 > page:
        levelsMenuSurface.blit(levelsMenuControlForward, (levelButtonsX[1], levelButtonsY))
      if page > 0:
        levelsMenuSurface.blit(levelsMenuControlBackward, (levelButtonsX[0], levelButtonsY))

      screen.blit(levelsMenuSurface, (0, 0))

  pygame.display.update()

def main():
  global patterns, totalLevels
  loadImages()
  patterns = loadPatterns()
  generateLevelsMenu()
  totalLevels = len(patterns)
  updateParams()
  drawGrid()

  while running:
    updateScreen()

main()

os.system("clear")

pygame.quit()