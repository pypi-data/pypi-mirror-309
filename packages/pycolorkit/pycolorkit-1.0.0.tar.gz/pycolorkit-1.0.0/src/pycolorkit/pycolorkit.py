# ColorKit

class ColorConverter:
    @staticmethod
    def format_hex(s):
        # Remove hashtages
        s = s.replace('#','')
        if len(s) == 3: # convert 3-char to 6-char
            s = [s[i] * 2 for i in range(3)] # duplicate each char in order
        return ''.join(s)
    
    @staticmethod
    def hex_to_rgb(h):
        # hexadecimal to decimal
        return (int(h[i:i+2], 16) for i in (0, 2, 4))
    
    @staticmethod
    def rgb_to_hsl(rgb):
        # Change range from 0-255 to 0-100%
        r = rgb[0] / 255
        g = rgb[1] / 255
        b = rgb[2] / 255

        # Determine Chroma component values 
        cmax = max(r, g, b)
        cmin = min(r, g, b)
        delta = cmax - cmin

        # Calculate Hue: Distance from white (0-350 degrees)
        if delta == 0:
            h = 0
        elif cmax == r:                # more red
            h = (g - b) / delta % 6
        elif cmax == g:
            h = (b - r) / delta + 2.0   # more green
        else:                       # more blue
            h = (r - g) / delta + 4.0

        # Calulate Lightness: Midrange of RGB (0-100%)
        l = (cmax + cmin) / 2

        # Calulate Saturation: Gray to Pure (0-100%)
        if delta == 0:
            s = 0
        else:
            s = delta / (1 - abs(2 * l - 1))

        h = round(h * 60)
        s = round(s * 100)
        l = round(l * 100)
        return (h, s, l)
    
    @staticmethod
    def hsl_to_rgb(hsl):
        h = hsl[0]
        s = hsl[1]/100
        l = hsl[2]/100

        # Find chroma
        chroma = (1 - abs(2*l - 1)) * s

        # Find point (r,g,b) of RGB cube
        X = chroma * (1 - abs((h/60) % 2 - 1))

        if      0 <= h < 1: rgb = [chroma, X, 0]
        elif    1 <= h < 2: rgb = [X, chroma, 0]
        elif    2 <= h < 3: rgb = [0, chroma, X]
        elif    3 <= h < 4: rgb = [0, X, chroma]
        elif    4 <= h < 5: rgb = [X, 0, chroma]
        else:   rgb = [chroma, 0, X]

        # Match the lightness
        m = l - chroma/2
        return tuple(int((i+m) * 255) for i in rgb)
    
    @staticmethod
    def rgb_to_hex(rgb):
        hexcode = [hex(i)[2:] for i in rgb]

        # six digit format
        for i in range(len(hexcode)):
            if len(hexcode[i]) != 2:
                hexcode[i] *= 2 
        
        return ''.join(hexcode)

class ColorGenerator:
    @staticmethod
    def sequence(hsl, ncolors=10, min_l=10, max_l=90): # Set range of lightness values
        h = round(hsl[0])
        s = round(hsl[1])
        l = round(hsl[2])
        
        if abs(l - max_l) <= 10: # only shades
            max_l = l
            shade_diff = int((l - min_l) / (ncolors))
            shades = [i for i in range(min_l, l, shade_diff)]
            sequence = shades
        elif abs(l - min_l) <=10: # only tints
            min_l = l
            tint_diff = int((max_l - l) / (ncolors))
            tints = [i for i in range(l, max_l, tint_diff)]
            sequence = tints
        else:
            shade_diff = int((l - min_l) / (ncolors/2))
            shades = [i for i in range(min_l, l, shade_diff)]

            tint_diff = int((max_l - l) / (ncolors/2))
            tints = [i for i in range(l, max_l, tint_diff)]
            sequence = shades+tints

            return [(h,s,l) for l in sequence]
    
    @staticmethod
    def compliment(hsl):
        h = hsl[0]
        s = hsl[1]
        l = hsl[2]

        if (h + 180) > 360:
            return (h-180, s, l)
        else:
            return (h+180, s, l)