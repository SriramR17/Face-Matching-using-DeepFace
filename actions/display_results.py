import cv2
import matplotlib.pyplot as plt

def display_images(images, title):
    """ Displays images using matplotlib """
    if len(images) == 0:
        print(f"🚫 No images to display for {title}.")
        return
    
    print(f"📸 Displaying {len(images)} {title} images...")
    for img in images:
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        plt.figure(figsize=(6, 6))
        plt.imshow(img_rgb)
        plt.axis("off")
        plt.title(title)
        plt.show()
