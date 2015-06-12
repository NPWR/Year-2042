LEVELS_XP = [] #Necessary XP to go the next level
for i in range(100):
    LEVELS_XP.append(int(100 * (1.2 ** i)))

TURRET_COOLDOWN = []
for i in range(100):
    TURRET_COOLDOWN.append(int(20./(i+1.)))
    
HEALTH = [100, 125, 150, 200]
SPEED = [1.0, 1.5, 2.0, 2.5]

BOX_TO_UPG = {0:'turret',
              1:'health',
              2:'speed'}
