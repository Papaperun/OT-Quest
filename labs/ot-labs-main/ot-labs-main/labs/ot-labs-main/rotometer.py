import pygame, sys
from pygame.locals import *


while True:
    flow = float(input("Enter flow 0-24 MGD: ")) # use this flow range for set up for 4-20 mA signal, 0-24 MGD is the range for the rotometer
    if 0 <= flow <= 24:
        break
    print("Invalid entry, try again")

while True:
    dosage = float(input("Enter the doseage in mg/L: ")) # in most case there is no limit to the dosage, but for the sake of this practice we will say 0-10 mg/L
    if 0 <= dosage <= 10:
        break   
    print("Invalid entry, try again")


flow_up = 1   # this is the amount it wil increas in flow by 1 MGD ( millions of gallons per day) when the W key is pressed, and decrease by 1 MGD when the S key is pressed
dosage_up = 1 # this is the amount it will increase in dosage by 1 mg/L when the D key is pressed, and decrease by 1 mg/L when the A key is pressed




def calculate_dose(flow, dosage):
    calculate_dose= (flow * 8.34 * dosage) # this is the formula to calculate the dose in pounds per day, where flow is in MGD, 8.34 is the conversion factor from gallons to pounds, and dosage is in mg/L
    return calculate_dose   


def main():
    global flow, dosage
    pygame.init()

    DISPLAY = pygame.display.set_mode((500,400),0,32)
    
    WHITE = (255,255,255)
    GREEN = (0,255,0)
    BLUE = (0,0,255)

    result = calculate_dose(flow, dosage)
    
    ball_x = 250
    
    ball_speed = -1.5  # this needs to be fed by the dosaged claulation 

    tube_top = 50
    tube_bottom = 350  # dosage calculation determines tube bottom, scaled 0-800 where 800 is top
    radius = 15
   
    ball_y = tube_bottom - ((result / 800) * (tube_bottom - tube_top))  # start near bottom
    if ball_y < tube_top + radius:
        ball_y = tube_top
    if ball_y > tube_bottom - radius:
        ball_y = tube_bottom
    while True:
        DISPLAY.fill(WHITE)
        pygame.draw.rect(DISPLAY, GREEN, (225, tube_top, 50, 300))
        pygame.draw.circle(DISPLAY, BLUE, (ball_x, int(ball_y)), radius)
        
        font = pygame.font.SysFont(None, 36)

# show the numbers
        flow_label = font.render(f"Flow: {flow} MGD", True, (0,0,0))
        dose_label = font.render(f"Dosage: {dosage} mg/L", True, (0,0,0))
        result_label = font.render(f"Lbs/day: {round(result, 2)}", True, (0,0,0))
        # will put a 4-@0mA  later 
        DISPLAY.blit(flow_label, (10, 10))
        DISPLAY.blit(dose_label, (10, 50))
        DISPLAY.blit(result_label, (10, 90))

       


        

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == pygame.K_w:
                    flow = flow + flow_up
                    print(f"Flow: {flow}")
                if event.key == pygame.K_s:
                    flow = flow - flow_up
                    print(f"Flow: {flow}")

                if event.key == pygame.K_d:
                    dosage = dosage + dosage_up
                    print(f"Dosage: {dosage}")
                if event.key == pygame.K_a:
                    dosage = dosage - dosage_up
                    print(f"Dosage: {dosage}")

                result = calculate_dose(flow, dosage)
                ball_y = tube_bottom - ((result / 800) * (tube_bottom - tube_top))  
                if ball_y < tube_top + radius:
                    ball_y = tube_top
                if ball_y > tube_bottom - radius:
                    ball_y = tube_bottom


        pygame.display.update()

main()
