import pygame
import cv2
import pygame.camera
import time
pygame.camera.init()

camlist = pygame.camera.list_cameras()
print(camlist)

if camlist:
    while True:
        cam = pygame.camera.Camera(camlist[0],(640, 480))
        # cam1 = pygame.camera.Camera(camlist[1],(640, 480))
        cam.start()
        # cam1.start()
        time.sleep(1)
        image = cam.get_image()
        # image1 = cam1.get_image()
        # pygame.image.save(image, "cam0.png")
        img0=cv2.imread(image,1)
        cv2.imshow("Img0",img0)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
    # pygame.image1.save(image1, "cam1.png")

else:
    print("Some error occurs here")
