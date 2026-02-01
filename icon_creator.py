from PIL import Image, ImageDraw, ImageFont

def create_snake_icon(size):
    # Gradient arka plan
    img = Image.new('RGB', (size, size), color='#667eea')
    draw = ImageDraw.Draw(img)
    
    # Yılan emojisi veya şekil çiz
    center = size // 2
    
    # Basit yılan çiz (yeşil kareler)
    square_size = size // 5
    positions = [
        (center - square_size, center - square_size),
        (center, center - square_size),
        (center, center),
        (center - square_size, center),
    ]
    
    for pos in positions:
        draw.rectangle([pos[0], pos[1], pos[0] + square_size, pos[1] + square_size], 
                      fill='#16C79A', outline='white', width=3)
    
    # Elma çiz (kırmızı daire)
    apple_pos = (center + square_size, center + square_size)
    draw.ellipse([apple_pos[0], apple_pos[1], 
                  apple_pos[0] + square_size, apple_pos[1] + square_size],
                 fill='#F94C66')
    
    return img

# 192x192 ve 512x512 boyutlarında oluştur
icon_192 = create_snake_icon(192)
icon_512 = create_snake_icon(512)

# Kaydet
icon_192.save('icon-192.png')
icon_512.save('icon-512.png')

print("✅ Icon'lar oluşturuldu: icon-192.png ve icon-512.png")