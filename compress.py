import subprocess
import os

def compress_video(input_path, output_path, method='h264'):
    """
    压缩视频文件，提供多种压缩方法
    
    Args:
        input_path (str): 输入视频路径
        output_path (str): 输出视频路径
        method (str): 压缩方法 ('h264', 'h265', 'crf', 'bitrate', 'resolution')
    """
    try:
        if method == 'h264':
            # 使用H.264编码，平衡压缩率和质量
            cmd = [
                'ffmpeg', '-i', input_path,
                '-c:v', 'libx264',
                '-preset', 'slow',  # 压缩速度：slower/slow/medium/fast/faster
                '-crf', '23',       # 质量控制：18-28，越小质量越好
                '-c:a', 'aac',      # 音频编码
                '-b:a', '128k',     # 音频比特率
                output_path
            ]
            
        elif method == 'h265':
            # 使用H.265编码，更高压缩率
            cmd = [
                'ffmpeg', '-i', input_path,
                '-c:v', 'libx265',
                '-preset', 'medium',
                '-crf', '28',       # H.265的CRF值比H.264高约6
                '-c:a', 'aac',
                '-b:a', '128k',
                output_path
            ]
            
        elif method == 'crf':
            # 使用CRF（恒定速率因子）方法
            cmd = [
                'ffmpeg', '-i', input_path,
                '-c:v', 'libx264',
                '-preset', 'veryslow',  # 最慢但最好的压缩
                '-crf', '20',           # 较高质量
                '-c:a', 'copy',         # 复制音频流
                output_path
            ]
            
        elif method == 'bitrate':
            # 控制比特率
            cmd = [
                'ffmpeg', '-i', input_path,
                '-c:v', 'libx264',
                '-b:v', '2000k',    # 视频比特率
                '-bufsize', '2000k', # 缓冲区大小
                '-maxrate', '2500k', # 最大比特率
                '-c:a', 'aac',
                '-b:a', '128k',
                output_path
            ]
            
        elif method == 'resolution':
            # 降低分辨率
            cmd = [
                'ffmpeg', '-i', input_path,
                '-vf', 'scale=-2:720',  # 保持宽高比，高度设为720p
                '-c:v', 'libx264',
                '-crf', '23',
                '-c:a', 'aac',
                '-b:a', '128k',
                output_path
            ]
            
        # 执行命令
        subprocess.run(cmd, check=True)
        print(f"Successfully compressed video to {output_path}")
        
        # 显示压缩前后的文件大小
        original_size = os.path.getsize(input_path) / (1024 * 1024)  # MB
        compressed_size = os.path.getsize(output_path) / (1024 * 1024)  # MB
        print(f"Original size: {original_size:.2f}MB")
        print(f"Compressed size: {compressed_size:.2f}MB")
        print(f"Compression ratio: {compressed_size/original_size:.2%}")
        
    except Exception as e:
        print(f"Error compressing video: {e}")

# 高级压缩设置
def advanced_compress_video(input_path, output_path):
    """
    使用更高级的压缩设置
    """
    try:
        cmd = [
            'ffmpeg', '-i', input_path,
            # 视频设置
            '-c:v', 'libx264',
            '-preset', 'veryslow',
            '-crf', '22',
            # 高级视频设置
            '-profile:v', 'high',
            '-level', '4.1',
            '-movflags', '+faststart',  # Web播放优化
            '-tune', 'film',            # 内容类型优化
            # 视频过滤器
            '-vf', 'format=yuv420p',    # 确保兼容性
            # 音频设置
            '-c:a', 'aac',
            '-b:a', '128k',
            '-ar', '44100',             # 音频采样率
            # 输出
            output_path
        ]
        subprocess.run(cmd, check=True)
        
    except Exception as e:
        print(f"Error in advanced compression: {e}")

# 批量处理视频
def batch_compress_videos(input_dir, output_dir, method='h264'):
    """
    批量处理目录中的所有MP4文件
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    for filename in os.listdir(input_dir):
        if filename.endswith('.mp4'):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, f'compressed_{filename}')
            compress_video(input_path, output_path, method)

# 使用示例
# input_video = "/home/admin01/project/ExDex/website/ExDex/static/videos/wall_lipton.mp4"
# output_video = "output.mp4"

# # 基本压缩
# compress_video(input_video, output_video, method='h264')

# # 高级压缩
# advanced_compress_video(input_video, "output_advanced.mp4")

# 批量处理
batch_compress_videos("/home/admin01/ExDex-main/ExDex-main/static/videos_ori", "/home/admin01/ExDex-main/ExDex-main/static/videos", method='h264')
