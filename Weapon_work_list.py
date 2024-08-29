import pygame
from math import asin, degrees


class Stagnum_blade():
    def apply(self, x, y, side, rect, position, weapon, AoE, base_ats, timer, enemies, fps, base_dmg, size,
            is_attacking, sprite_images, s):
        cox1 = 154 * size ** 1.15
        cox2 = -65 * size ** 1.05
        coy = -121 * size ** 0.6
        formx = (-rect.w + cox1 if not side else rect.w + cox2)
        formy = rect.h + coy
        if not is_attacking:
            image = pygame.transform.scale_by(
                sprite_images['war_weapons'][position][weapon][1 if side else 0], size)
            rect.x = x - formx
            rect.y = y - formy
        elif timer < fps / base_ats:
            timer += 1
            image = pygame.transform.rotate(pygame.transform.scale_by(
                sprite_images["war_weapons"][position][weapon][1 if side else 0], size),
                AoE / (fps / base_ats) * timer * (1 if side else -1))
            rect.x = x - formx - 25
            rect.y = y - formy - 15
            ret = pygame.sprite.spritecollide(s, enemies, False)
            if ret:
                for i in ret:
                    i.get_damage(base_dmg, (fps // base_ats - timer) + 2, "warrior")
        else:
            timer = 0
            is_attacking = False
            position = "hold"
            image = pygame.transform.scale_by(
                sprite_images["war_weapons"][position][weapon][1 if side else 0], size)
            rect.x = x - formx
            rect.y = y - formy
        return {"side": side, "rect": rect, "pos": position, "timer": timer, "is_att": is_attacking,
                    "image": image}


class Handgun():
    def apply(self, x, y, side, rect, mpos, position, weapon, base_ats, alt_ats, timer, fps,
            is_attacking, sprite_images, CAT, c_timer, max_ch_time, ch_to):
        proj = None
        coy = 65
        cox1 = 60
        cox2 = 45
        rect.x = x - rect.w + (cox1 if not side else cox2)
        rect.y = y - rect.h + coy
        mpos_x, mpos_y = mpos
        angle = degrees(asin((mpos_y - rect.y - rect.h // 2) / ((mpos_x - rect.x - rect.w // 2)
                                                                ** 2 + (mpos_y - rect.y - rect.h // 2) ** 2) ** 0.5))
        real_angle = (angle if not side else -angle + 180)
        if not side:
            angle = -angle
        image = pygame.transform.rotate(sprite_images["ran_weapons"][position][weapon][1 if side else 0], angle)
        if is_attacking and timer == 0:
            proj = {"angle": real_angle, "pos": (rect.x + (rect.w // 2 if side else 0), rect.y + rect.h // 4)}
            timer += 1
        elif 0 < timer < fps / base_ats:
            timer += 1
        else:
            timer = 0
            is_attacking = False
            position = "hold"
        ret = {"side": side, "pos": position, "timer": timer, "image": image, "is_attacking": is_attacking}
        if proj:
            ret["base_proj"] = proj
        return ret


class Volcano():
    def apply(self, x, y, side, rect, mpos, position, weapon, base_ats, alt_ats, timer, fps,
            is_attacking, sprite_images, CAT, c_timer, max_ch_time, ch_to):
        proj = None
        coy = 65
        cox1 = 60
        cox2 = 45
        rect.x = x - rect.w + (cox1 if not side else cox2)
        rect.y = y - rect.h + coy
        mpos_x, mpos_y = mpos
        angle = degrees(asin((mpos_y - rect.y - rect.h // 2) / ((mpos_x - rect.x - rect.w // 2)
                                                                ** 2 + (mpos_y - rect.y - rect.h // 2) ** 2) ** 0.5))
        real_angle = (angle if not side else -angle + 180)
        if not side:
            angle = -angle
        image = pygame.transform.rotate(sprite_images["ran_weapons"][position][weapon][1 if side else 0], angle)
        if is_attacking and timer == 0:
            proj = {"angle": real_angle, "pos": (rect.x + (rect.w // 2 if side else 0), rect.y + rect.h // 4)}
            timer += 1
        elif 0 < timer < fps / base_ats:
            timer += 1
        else:
            timer = 0
            is_attacking = False
            position = "hold"
        ret = {"side": side, "pos": position, "timer": timer, "image": image, "is_attacking": is_attacking}
        if proj:
            ret["base_proj"] = proj
        return ret


class Moon_blessing():
    def apply(self, x, y, side, rect, mpos, position, weapon, base_ats, alt_ats, timer, fps,
            is_attacking, sprite_images, CAT, c_timer, max_ch_time, ch_to):
        proj = None
        coy = 75
        cox1 = 40
        cox2 = 25
        rect.x = x - rect.w + (cox1 if not side else cox2)
        rect.y = y - rect.h + coy
        mpos_x, mpos_y = mpos
        mpos_y += rect.h // 3
        angle = degrees(asin((mpos_y - rect.y - rect.h) / ((mpos_x - rect.x - rect.w // 2)
                                                                ** 2 + (mpos_y - rect.y - rect.h) ** 2) ** 0.5))
        real_angle = (angle if not side else -angle + 180)
        if not side:
            angle = -angle
        image = pygame.transform.rotate(sprite_images["ran_weapons"][position][weapon][1 if side else 0], angle)
        if CAT != "changing":
            if is_attacking and timer == 0:
                proj = {"angle": real_angle, "pos": (rect.x + (rect.w // 2 if side else 0), rect.y + rect.h // 4)}
                timer += 1
            elif 0 < timer < fps / (base_ats if CAT == "base" else alt_ats):
                timer += 1
            else:
                timer = 0
                is_attacking = False
                position = "hold"
        elif CAT == "changing" and c_timer < max_ch_time * fps:
            c_timer += 1
        else:
            if ch_to == "base":
                ch_to = "alt"
                CAT = "base"
            else:
                ch_to = "base"
                CAT = "alt"
            c_timer = 0
        ret = {"side": side, "pos": position, "timer": timer, "image": image, "is_attacking": is_attacking,
               "ch_timer": c_timer,
               "cur_atk_type": CAT, "changing_to": ch_to}
        if proj and CAT == "base":
            ret["base_proj"] = proj
        elif proj and CAT == "alt":
            ret["alt_proj"] = proj
        return ret


class Planetar_bomber():
    def apply(self, x, y, side, rect, mpos, position, weapon, base_ats, alt_ats, timer, fps,
            is_attacking, sprite_images, CAT, c_timer, max_ch_time, ch_to):
        proj = None
        coy = 60
        cox1 = 70
        cox2 = 120
        if ch_to == "alt":
            rect.x = x - rect.w + (cox1 if not side else cox2)
            rect.y = y - rect.h + coy
        else:
            rect.x = x - rect.w + (cox1 if side else cox2)
            rect.y = y - rect.h + coy
        mpos_x, mpos_y = mpos
        mpos_y += rect.h // 3
        angle = degrees(asin((mpos_y - rect.y - rect.h) / ((mpos_x - rect.x - rect.w // 2)
                                                                ** 2 + (mpos_y - rect.y - rect.h) ** 2) ** 0.5))
        real_angle = (angle if not side else -angle + 180)
        if not side:
            angle = -angle
        image = pygame.transform.rotate(sprite_images["ran_weapons"][position][weapon][1 if side else 0], angle)
        if CAT != "changing":
            if is_attacking and timer == 0:
                proj = {"angle": real_angle, "pos": (rect.x + (rect.w // 2 if side else 0), rect.y + rect.h // 4)}
                timer += 1
            elif 0 < timer < fps / (base_ats if CAT == "base" else alt_ats):
                timer += 1
            else:
                timer = 0
                is_attacking = False
                position = ("hold" if ch_to == "alt" else "alt_hold")
        elif CAT == "changing" and c_timer < max_ch_time * fps:
            c_timer += 1
        else:
            if ch_to == "base":
                ch_to = "alt"
                CAT = "base"
                position = "hold"
            else:
                ch_to = "base"
                CAT = "alt"
                position = "alt_hold"
            c_timer = 0
        ret = {"side": side, "pos": position, "timer": timer, "image": image, "is_attacking": is_attacking,
               "ch_timer": c_timer,
               "cur_atk_type": CAT, "changing_to": ch_to}
        if proj and CAT == "base":
            ret["base_proj"] = proj
        elif proj and CAT == "alt":
            ret["alt_proj"] = proj
        return ret