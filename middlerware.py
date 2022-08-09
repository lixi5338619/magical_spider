# -*- coding: utf-8 -*-
import os,requests
from urllib.parse import urlparse
try:
    import cv2, numpy as np
except:
    ...

class Slide(object):
    def __init__(self, gap, bg, gap_size=None, bg_size=None, out=None):
        """
        :param bg: 带缺口的图片链接或者url
        :param gap: 缺口图片链接或者url
        """
        self.img_dir = os.path.join(os.getcwd(), 'img')
        if not os.path.exists(self.img_dir):
            os.makedirs(self.img_dir)

        bg_resize = bg_size if bg_size else (340, 212)
        gap_size = gap_size if gap_size else (68, 68)
        self.bg = self.check_is_img_path(bg, 'bg', resize=bg_resize)
        self.gap = self.check_is_img_path(gap, 'gap', resize=gap_size)
        self.out = out if out else os.path.join(self.img_dir, 'out.jpg')


    @staticmethod
    def check_is_img_path(img, img_type, resize):
        if img.startswith('http'):
            headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;"
                          "q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "zh-CN,zh;q=0.9,en-GB;q=0.8,en;q=0.7,ja;q=0.6",
                "Cache-Control": "max-age=0",
                "Connection": "keep-alive",
                "Host": urlparse(img).hostname,
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/91.0.4472.164 Safari/537.36",
            }
            img_res = requests.get(img, headers=headers)
            if img_res.status_code == 200:
                img_path = f'./img/{img_type}.jpg'
                image = np.asarray(bytearray(img_res.content), dtype="uint8")
                image = cv2.imdecode(image, cv2.IMREAD_COLOR)
                if resize:
                    image = cv2.resize(image, dsize=resize)
                cv2.imwrite(img_path, image)
                return img_path
            else:
                raise Exception(f"保存{img_type}图片失败")
        else:
            return img


    @staticmethod
    def clear_white(img):
        """清除图片的空白区域，这里主要清除滑块的空白"""
        img = cv2.imread(img)
        rows, cols, channel = img.shape
        min_x = 255
        min_y = 255
        max_x = 0
        max_y = 0
        for x in range(1, rows):
            for y in range(1, cols):
                t = set(img[x, y])
                if len(t) >= 2:
                    if x <= min_x:
                        min_x = x
                    elif x >= max_x:
                        max_x = x

                    if y <= min_y:
                        min_y = y
                    elif y >= max_y:
                        max_y = y
        img1 = img[min_x:max_x, min_y: max_y]
        return img1


    def template_match(self, tpl, target):
        th, tw = tpl.shape[:2]
        result = cv2.matchTemplate(target, tpl, cv2.TM_CCOEFF_NORMED)
        # 寻找矩阵(一维数组当作向量,用Mat定义) 中最小值和最大值的位置
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        tl = max_loc
        br = (tl[0] + tw, tl[1] + th)
        # 绘制矩形边框，将匹配区域标注出来
        # target：目标图像
        # tl：矩形定点
        # br：矩形的宽高
        # (0,0,255)：矩形边框颜色
        # 1：矩形边框大小
        cv2.rectangle(target, tl, br, (0, 0, 255), 2)
        cv2.imwrite(self.out, target)
        return tl[0]


    @staticmethod
    def image_edge_detection(img):
        edges = cv2.Canny(img, 100, 200)
        return edges


    def discern(self):
        img1 = self.clear_white(self.gap)
        img1 = cv2.cvtColor(img1, cv2.COLOR_RGB2GRAY)
        slide = self.image_edge_detection(img1)

        back = cv2.imread(self.bg, 0)
        back = self.image_edge_detection(back)

        slide_pic = cv2.cvtColor(slide, cv2.COLOR_GRAY2RGB)
        back_pic = cv2.cvtColor(back, cv2.COLOR_GRAY2RGB)
        x = self.template_match(slide_pic, back_pic)
        # 输出横坐标, 即 滑块在图片上的位置
        return x


    @staticmethod
    def get_tracks(distance, rate=0.6, t=0.2, v=0):
        """
        将distance分割成小段的距离
        :param distance: 总距离
        :param rate: 加速减速的临界比例
        :param a1: 加速度
        :param a2: 减速度
        :param t: 单位时间
        :param t: 初始速度
        :return: 小段的距离集合
        """
        tracks = []
        # 加速减速的临界值
        mid = rate * distance
        # 当前位移
        s = 0
        # 循环
        while s < distance:
            # 初始速度
            v0 = v
            if s < mid:
                a = 20
            else:
                a = -3
            # 计算当前t时间段走的距离
            s0 = v0 * t + 0.5 * a * t * t
            # 计算当前速度
            v = v0 + a * t
            # 四舍五入距离，因为像素没有小数
            tracks.append(round(s0))
            # 计算当前距离
            s += s0
        return tracks
