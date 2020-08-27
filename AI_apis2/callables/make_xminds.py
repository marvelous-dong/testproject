import xmind
import os
from settings import XMINDS_DIR


def make_xmind(target_dict, point=None, name=None, method_title="", field_title="", img_name=""):
    w = xmind.load("testt.xmind")
    s1 = w.getPrimarySheet()
    s1.setTitle("first sheet")

    if not point:
        point = s1.getRootTopic()

    if not name:
        point.setTitle(f"{field_title}_{method_title}")
    else:
        point.setTitle(name)

    for i in target_dict:
        if type(target_dict[i]) in [str, int]:
            point_sub = point.addSubTopic()
            point_sub.setTitle(f"参数：{i}, 值：{target_dict[i]}")
        elif type(target_dict[i]) == list:
            point_sub = point.addSubTopic()
            try:
                make_xmind(target_dict[i][0], point=point_sub, name=i, method_title=method_title, field_title=field_title, img_name=img_name)
            except IndexError:
                pass
        elif type(target_dict[i]) == dict:
            point_sub = point.addSubTopic()
            make_xmind(target_dict[i], point=point_sub, name=i, method_title=method_title, field_title=field_title, img_name=img_name)

    if not os.path.exists(XMINDS_DIR):
        os.mkdir(XMINDS_DIR)

    xmind.save(w, os.path.join(XMINDS_DIR, f"{field_title}_{method_title}_{img_name}_returns.xmind"))

