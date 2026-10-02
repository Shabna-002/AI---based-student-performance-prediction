import os
import math
import random
import numpy as np
from PIL import Image, ImageDraw

def create_seamless_15s_video():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    image_path = os.path.join(base_dir, "static", "images", "edupredict_hero_bg.jpg")
    output_dir = os.path.join(base_dir, "static", "videos")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "edupredict_hero_bg_15s.mp4")

    if not os.path.exists(image_path):
        print(f"Error: Base image not found at {image_path}")
        return

    import imageio

    print("Loading base image...")
    src_img = Image.open(image_path).convert("RGB")
    target_w, target_h = 1920, 1080
    src_img = src_img.resize((target_w, target_h), Image.Resampling.LANCZOS)

    fps = 30
    duration_sec = 15
    total_frames = fps * duration_sec  # 450 frames

    # Generate fixed particles with periodic cyclic motion so frame 0 matches frame 450
    random.seed(42)
    np.random.seed(42)
    num_particles = 35
    particles = []
    color_palette = [
        (56, 189, 248),   # Cyan neon
        (168, 85, 247),  # Purple neon
        (96, 165, 250),  # Royal blue
        (192, 132, 252)  # Violet
    ]
    for _ in range(num_particles):
        particles.append({
            'base_x': random.uniform(50, target_w - 50),
            'base_y': random.uniform(50, target_h - 50),
            'amp_x': random.uniform(15, 35),
            'amp_y': random.uniform(10, 25),
            'freq': random.choice([1, 2, 3]), # integer cycle per 15s ensures seamless loop
            'phase': random.uniform(0, 2 * math.pi),
            'radius': random.uniform(2, 5),
            'color': random.choice(color_palette)
        })

    print(f"Rendering {total_frames} frames (15s @ {fps}fps, 1080p)...")
    writer = imageio.get_writer(output_path, fps=fps, codec='libx264', quality=8, pixelformat='yuv420p')

    for frame_idx in range(total_frames):
        if frame_idx % 45 == 0:
            print(f"Progress: {frame_idx}/{total_frames} frames ({frame_idx/total_frames*100:.1f}%)")

        progress = frame_idx / total_frames # 0.0 to 1.0
        angle = progress * 2.0 * math.pi

        # Seamless Ken Burns motion:
        # scale oscillates from 1.00 to 1.04 and back to 1.00 at frame 450
        scale = 1.0 + 0.038 * (0.5 - 0.5 * math.cos(angle))
        pan_x = math.sin(angle) * 16.0
        pan_y = math.sin(angle * 2.0) * 8.0

        # Zoom & Pan using PIL transform
        w_scaled = int(target_w * scale)
        h_scaled = int(target_h * scale)
        
        # Crop boundaries
        crop_x = int((w_scaled - target_w) / 2.0 - pan_x)
        crop_y = int((h_scaled - target_h) / 2.0 - pan_y)
        crop_x = max(0, min(crop_x, w_scaled - target_w))
        crop_y = max(0, min(crop_y, h_scaled - target_h))

        frame_pil = src_img.resize((w_scaled, h_scaled), Image.Resampling.BILINEAR)
        frame_pil = frame_pil.crop((crop_x, crop_y, crop_x + target_w, crop_y + target_h))

        # Overlay particle canvas with transparency
        particle_layer = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(particle_layer)

        # Calculate current particle positions
        current_pts = []
        for p in particles:
            p_angle = angle * p['freq'] + p['phase']
            px = p['base_x'] + math.sin(p_angle) * p['amp_x']
            py = p['base_y'] + math.cos(p_angle) * p['amp_y']
            current_pts.append((px, py, p))

        # Draw glowing neural connection lines
        for i in range(len(current_pts)):
            x1, y1, p1 = current_pts[i]
            for j in range(i + 1, len(current_pts)):
                x2, y2, p2 = current_pts[j]
                dist = math.hypot(x2 - x1, y2 - y1)
                if dist < 160:
                    alpha_line = int(80 * (1.0 - dist / 160.0) * (0.7 + 0.3 * math.sin(angle * 4 + p1['phase'])))
                    if alpha_line > 5:
                        draw.line([(x1, y1), (x2, y2)], fill=(147, 197, 253, alpha_line), width=1)

        # Draw glowing particles
        for px, py, p in current_pts:
            pulse = 0.5 + 0.5 * math.sin(angle * 3 + p['phase'])
            r = p['radius'] * (0.8 + 0.4 * pulse)
            c = p['color']
            alpha = int(180 * (0.6 + 0.4 * pulse))
            draw.ellipse([px - r, py - r, px + r, py + r], fill=(c[0], c[1], c[2], alpha))

        # Merge layers
        frame_pil.paste(particle_layer, (0, 0), particle_layer)
        writer.append_data(np.array(frame_pil))

def create_professional_15s_video():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    image_path = os.path.join(base_dir, "static", "images", "edupredict_hero_bg.jpg")
    output_dir = os.path.join(base_dir, "static", "videos")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "edupredict_hero_bg_pro_15s.mp4")

    if not os.path.exists(image_path):
        print(f"Error: Base image not found at {image_path}")
        return

    import imageio

    print("Loading base image for Professional Mode...")
    src_img = Image.open(image_path).convert("RGB")
    target_w, target_h = 1920, 1080
    src_img = src_img.resize((target_w, target_h), Image.Resampling.LANCZOS)

    fps = 30
    duration_sec = 15
    total_frames = fps * duration_sec  # 450 frames

    random.seed(99)
    np.random.seed(99)
    num_particles = 48
    particles = []
    color_palette = [
        (56, 189, 248),   # Cyan neon
        (168, 85, 247),  # Purple neon
        (129, 140, 248), # Indigo
        (236, 72, 153),  # Magenta
        (96, 165, 250)   # Sky blue
    ]
    for _ in range(num_particles):
        particles.append({
            'base_x': random.uniform(40, target_w - 40),
            'base_y': random.uniform(40, target_h - 40),
            'amp_x': random.uniform(20, 45),
            'amp_y': random.uniform(15, 30),
            'freq': random.choice([1, 2]), 
            'phase': random.uniform(0, 2 * math.pi),
            'radius': random.uniform(2, 6),
            'color': random.choice(color_palette)
        })

    print(f"Rendering Professional Mode ({total_frames} frames, 15s @ {fps}fps, 1080p ProRes-like quality)...")
    writer = imageio.get_writer(output_path, fps=fps, codec='libx264', quality=9, pixelformat='yuv420p', ffmpeg_params=['-crf', '16'])

    for frame_idx in range(total_frames):
        if frame_idx % 45 == 0:
            print(f"Pro Render: {frame_idx}/{total_frames} frames ({frame_idx/total_frames*100:.1f}%)")

        progress = frame_idx / total_frames
        angle = progress * 2.0 * math.pi

        # Smooth Cinematic Drone Drift
        scale = 1.0 + 0.045 * (0.5 - 0.5 * math.cos(angle))
        pan_x = math.sin(angle) * 22.0
        pan_y = math.cos(angle) * 12.0

        w_scaled = int(target_w * scale)
        h_scaled = int(target_h * scale)
        
        crop_x = int((w_scaled - target_w) / 2.0 - pan_x)
        crop_y = int((h_scaled - target_h) / 2.0 - pan_y)
        crop_x = max(0, min(crop_x, w_scaled - target_w))
        crop_y = max(0, min(crop_y, h_scaled - target_h))

        frame_pil = src_img.resize((w_scaled, h_scaled), Image.Resampling.BILINEAR)
        frame_pil = frame_pil.crop((crop_x, crop_y, crop_x + target_w, crop_y + target_h))

        layer = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(layer)

        # Anamorphic horizontal laser sweep
        flare_y = int(target_h * 0.45 + math.sin(angle) * 35)
        flare_alpha = int(35 * (0.5 + 0.5 * math.sin(angle * 2)))
        draw.line([(0, flare_y), (target_w, flare_y)], fill=(56, 189, 248, flare_alpha), width=2)
        draw.line([(0, flare_y + 1), (target_w, flare_y + 1)], fill=(168, 85, 247, int(flare_alpha * 0.7)), width=1)

        # Corner Telemetry HUD Crosshairs (Professional aesthetic)
        hud_alpha = 90
        coords = [(60, 60), (target_w - 60, 60), (60, target_h - 60), (target_w - 60, target_h - 60)]
        for cx, cy in coords:
            draw.line([(cx - 12, cy), (cx + 12, cy)], fill=(147, 197, 253, hud_alpha), width=1)
            draw.line([(cx, cy - 12), (cx, cy + 12)], fill=(147, 197, 253, hud_alpha), width=1)

        # Calculate particle positions
        current_pts = []
        for p in particles:
            p_angle = angle * p['freq'] + p['phase']
            px = p['base_x'] + math.sin(p_angle) * p['amp_x']
            py = p['base_y'] + math.cos(p_angle) * p['amp_y']
            current_pts.append((px, py, p))

        # Neural synapse lines and traveling data packets
        for i in range(len(current_pts)):
            x1, y1, p1 = current_pts[i]
            for j in range(i + 1, len(current_pts)):
                x2, y2, p2 = current_pts[j]
                dist = math.hypot(x2 - x1, y2 - y1)
                if dist < 170:
                    alpha_line = int(95 * (1.0 - dist / 170.0) * (0.7 + 0.3 * math.sin(angle * 3 + p1['phase'])))
                    if alpha_line > 8:
                        draw.line([(x1, y1), (x2, y2)], fill=(147, 197, 253, alpha_line), width=1)
                        # Traveling data energy packet
                        packet_prog = (progress * 6.0 + (i + j) * 0.15) % 1.0
                        pk_x = x1 + (x2 - x1) * packet_prog
                        pk_y = y1 + (y2 - y1) * packet_prog
                        draw.ellipse([pk_x - 1.5, pk_y - 1.5, pk_x + 1.5, pk_y + 1.5], fill=(255, 255, 255, int(alpha_line * 1.5)))

        # Glowing particles with halo bloom
        for px, py, p in current_pts:
            pulse = 0.5 + 0.5 * math.sin(angle * 3 + p['phase'])
            r = p['radius'] * (0.85 + 0.4 * pulse)
            c = p['color']
            # Outer halo
            draw.ellipse([px - r * 2.2, py - r * 2.2, px + r * 2.2, py + r * 2.2], fill=(c[0], c[1], c[2], int(40 * pulse)))
            # Core
            draw.ellipse([px - r, py - r, px + r, py + r], fill=(c[0], c[1], c[2], int(210 * (0.7 + 0.3 * pulse))))

        frame_pil.paste(layer, (0, 0), layer)
        writer.append_data(np.array(frame_pil))

    writer.close()
    print(f"Success! Professional Mode background video saved to: {output_path}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and "pro" in sys.argv[1].lower():
        create_professional_15s_video()
    else:
        create_professional_15s_video()

