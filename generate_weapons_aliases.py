from pathlib import Path

WORKDIR = 'weapons'

weapons = {
    'pistol': {
        "weapon_usp_silencer": "weapon_hkp2000",
        "weapon_deagle": "weapon_deagle",
        "weapon_elite": "weapon_elite",
        "weapon_fiveseven": "weapon_fiveseven",
        "weapon_glock": "weapon_glock",
        "weapon_hkp2000": "weapon_hkp2000",
        "weapon_p250": "weapon_p250",
        "weapon_tec9": "weapon_tec9",
        "weapon_cz75a": "weapon_p250",
        "weapon_revolver": "weapon_deagle"
    },
    'rifle': {
        "weapon_m4a1": "weapon_m4a1",
        "weapon_m4a1_silencer": "weapon_m4a1",
        "weapon_ak47": "weapon_ak47",
        "weapon_aug": "weapon_aug",
        "weapon_famas": "weapon_famas",
        "weapon_galilar": "weapon_galilar",
        "weapon_sg556": "weapon_sg556"
    },
    'smg': {
        "weapon_bizon": "weapon_bizon",
        "weapon_mac10": "weapon_mac10",
        "weapon_mp7": "weapon_mp7",
        "weapon_mp9": "weapon_mp9",
        "weapon_p90": "weapon_p90",
        "weapon_ump45": "weapon_ump45",
        "weapon_mp5sd": "weapon_mp7",
    },
    'shotgun': {
        "weapon_nova": "weapon_nova",
        "weapon_sawedoff": "weapon_sawedoff",
        "weapon_xm1014": "weapon_xm1014",
        "weapon_mag7": "weapon_mag7",
    },
    'sniper': {
        "weapon_awp": "weapon_awp",
        "weapon_g3sg1": "weapon_g3sg1",
        "weapon_scar20": "weapon_scar20",
        "weapon_ssg08": "weapon_ssg08",
    },
    'minigun': {
        "weapon_m249": "weapon_m249",
        "weapon_negev": "weapon_negev",
    },
    'knife': {
        "weapon_knife_css": "weapon_knife",
        "weapon_knife_ghost": "weapon_knife",
        "weapon_bayonet": "weapon_knife",
        "weapon_knife_flip": "weapon_knife",
        "weapon_knife_gut": "weapon_knife",
        "weapon_knife_karambit": "weapon_knife",
        "weapon_knife_m9_bayonet": "weapon_knife",
        "weapon_knife_tactical": "weapon_knife",
        "weapon_knife_butterfly": "weapon_knife",
        "weapon_knife_falchion": "weapon_knife",
        "weapon_knifegg": "weapon_knife",
        "weapon_knife_survival_bowie": "weapon_knife",
        "weapon_knife_ursus": "weapon_knife",
        "weapon_knife_gypsy_jackknife": "weapon_knife",
        "weapon_knife_stiletto": "weapon_knife",
        "weapon_knife_widowmaker": "weapon_knife",
        "weapon_knife_push": "weapon_knife"
    }
}

PRESS_KEY_TMP = """ent_remove_all {classname};
ent_fire {weapon} addoutput "classname backup";
ent_fire {weapon} addoutput "targetname backup";
"""

RELEASE_KEY_TMP = """give {weapon};
ent_fire {weapon_classname} addoutput "classname {classname}";
ent_fire {weapon_classname} addoutput "targetname {classname}";
"""

CHANGE_WEAPONS_ALIASE = """alias +{weapon_type}_{bind_number} "exec {path}\\+{weapon}.cmd; alias -{weapon_type}_toggle -{weapon_type}_{bind_number};"
alias -{weapon_type}_{bind_number} "exec {path}\\-{weapon}.cmd; alias +{weapon_type}_toggle +{weapon_type}_{next_bind_number};"
"""


def get_aliases_list(weapon_type, bind_number, path, weapon):
    next_bind_number = 1 if bind_number == len(weapons[weapon_type]) else bind_number + 1
    return CHANGE_WEAPONS_ALIASE.format(weapon_type=weapon_type, bind_number=bind_number, path=path, weapon=weapon,
                                        next_bind_number=next_bind_number)


def make_weapon_generator(weapon_type):
    path = '{}\\{}'.format(WORKDIR, weapon_type)
    slot = 3 if weapon_type == 'knife' else 1 if weapon_type == 'pistol' else 2
    bind_number = 0
    is_knife = weapon_type == 'knife'
    Path(path).mkdir(exist_ok=True, parents=True)
    changing_aliases = ''
    for weapon in weapons[weapon_type]:
        bind_number += 1
        new_classname = 'prev_weapon_' + str(slot) if not is_knife else 'weapon_knifegg'
        #
        weapon_classname = weapons[weapon_type][weapon]
        press_aliases = PRESS_KEY_TMP.format(classname=new_classname, weapon=weapons[weapon_type][weapon] if not is_knife else 'weapon_knife')
        release_aliases = RELEASE_KEY_TMP.format(classname=new_classname, weapon=weapon, weapon_classname=weapon_classname)
        open('{}\\+{}.cmd'.format(path, weapon), 'w').write(press_aliases)
        open('{}\\-{}.cmd'.format(path, weapon), 'w').write(release_aliases)
        #
        changing_aliases += get_aliases_list(weapon_type, bind_number, path, weapon)
    open('{}\\aliases.cmd'.format(path), 'w').write(changing_aliases)
    return 'exec {}\\aliases.cmd;\n'.format(path)


def main():
    startup_aliase, startup_aliase_text = open(WORKDIR + '\\' + "aliases.cmd", 'w'), ''
    for weapon in weapons.keys():
        startup_aliase_text += make_weapon_generator(weapon)
    startup_aliase.write(startup_aliase_text)


if __name__ == '__main__':
    main()
