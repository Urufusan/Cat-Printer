from matplotlib import font_manager

fontmap = {font.name: font for font in font_manager.fontManager.ttflist}


def findfont(fontname:str):
    for family in sorted(fontmap.keys()):
        font = fontmap[family]
        if fontname.lower() in family.lower():
            if font.fname.lower().endswith(("ttf")):
                return font.fname
    raise Exception(f"No font found with name {fontname}!")
        #print(f'{family:<30}: {font.fname}')

if __name__ == "__main__":
    print(f'Total fonts: {len(fontmap.keys())}')

    for family in sorted(fontmap.keys()):
        font = fontmap[family]
        print(f'{family:<30}: {font.fname}')
