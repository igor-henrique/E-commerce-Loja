import os
from PIL import Image, ImageDraw, ImageFont
import random

def criar_imagens_placeholder():
    """Cria imagens placeholder para os produtos"""
    
    # Cria pasta de uploads se não existir
    upload_dir = os.path.join('static', 'uploads')
    os.makedirs(upload_dir, exist_ok=True)
    
    # Lista de imagens para criar (baseada nos produtos)
    imagens = [
        ('notebook-dell.jpg', 'Notebook Dell', '#1a73e8'),
        ('samsung-a54.jpg', 'Samsung A54', '#1f1f1f'),
        ('tv-lg-50.jpg', 'Smart TV LG', '#a50034'),
        ('jbl-tune.jpg', 'JBL Tune', '#ff6b00'),
        ('ipad-9.jpg', 'iPad 9', '#555555'),
        ('mouse-g403.jpg', 'Mouse Gamer', '#00d4ff'),
        ('teclado-redragon.jpg', 'Teclado', '#ff0000'),
        ('ssd-kingston.jpg', 'SSD Kingston', '#0055a5'),
        ('webcam-c920.jpg', 'Webcam', '#00a650'),
        ('monitor-aoc.jpg', 'Monitor AOC', '#ed1c24'),
        ('ventilador-torre.jpg', 'Ventilador', '#4a90e2'),
        ('luminaria-led.jpg', 'Luminária', '#ffd700'),
        ('umidificador.jpg', 'Umidificador', '#87ceeb'),
        ('tenis-nike.jpg', 'Tênis Nike', '#111111'),
        ('bola-penalty.jpg', 'Bola Penalty', '#ff4500'),
        ('halteres.jpg', 'Kit Halteres', '#696969'),
        ('livro-python.jpg', 'Python', '#3776ab'),
        ('programador-pragmatico.jpg', 'Livro', '#2c3e50'),
        ('clean-code.jpg', 'Clean Code', '#27ae60'),
        ('ps5.jpg', 'PlayStation 5', '#003791'),
        ('controle-xbox.jpg', 'Controle Xbox', '#107c10'),
        ('headset-hyperx.jpg', 'Headset', '#e31837')
    ]
    
    # Tamanho das imagens
    width, height = 600, 600
    
    print("🖼️  Criando imagens placeholder...\n")
    
    for filename, text, color in imagens:
        try:
            # Cria nova imagem
            img = Image.new('RGB', (width, height), color='white')
            draw = ImageDraw.Draw(img)
            
            # Desenha fundo colorido
            draw.rectangle([0, 0, width, height], fill=color)
            
            # Adiciona borda
            border_width = 20
            draw.rectangle([border_width, border_width, width-border_width, height-border_width], 
                         outline='white', width=3)
            
            # Tenta usar uma fonte maior, senão usa padrão
            try:
                font = ImageFont.truetype("arial.ttf", 40)
                small_font = ImageFont.truetype("arial.ttf", 20)
            except:
                font = ImageFont.load_default()
                small_font = font
            
            # Adiciona texto do produto
            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            
            text_x = (width - text_width) // 2
            text_y = (height - text_height) // 2 - 20
            
            draw.text((text_x, text_y), text, fill='white', font=font)
            
            # Adiciona "IMAGEM EXEMPLO"
            exemplo_text = "IMAGEM EXEMPLO"
            exemplo_bbox = draw.textbbox((0, 0), exemplo_text, font=small_font)
            exemplo_width = exemplo_bbox[2] - exemplo_bbox[0]
            
            exemplo_x = (width - exemplo_width) // 2
            exemplo_y = text_y + text_height + 20
            
            draw.text((exemplo_x, exemplo_y), exemplo_text, fill='white', font=small_font)
            
            # Salva a imagem
            filepath = os.path.join(upload_dir, filename)
            img.save(filepath, quality=85)
            print(f"✅ {filename} criada")
            
        except Exception as e:
            print(f"❌ Erro ao criar {filename}: {e}")
    
    print(f"\n✅ Imagens salvas em: {upload_dir}")
    print("\n💡 Dica: Substitua essas imagens por fotos reais dos produtos!")

if __name__ == "__main__":
    print("="*50)
    print("🖼️  GERADOR DE IMAGENS PLACEHOLDER")
    print("="*50)
    
    # Verifica se PIL está instalado
    try:
        import PIL
        criar_imagens_placeholder()
    except ImportError:
        print("\n❌ Biblioteca PIL não encontrada!")
        print("\nInstale com: pip install Pillow")
        print("\nOu use placeholders online:")
        print("- https://placehold.co/600x600")
        print("- https://via.placeholder.com/600")
