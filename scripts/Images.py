from PIL import ImageTk, Image

def gather_images(image_size=(20,20)):
    """ Imports all the Tile, bomb, flag images into a dictionary and returns it """
    img_dict = {}

    # Get the normal numbers
    null_img = Image.open('assets/null.png')
    null_img = ImageTk.PhotoImage(null_img.resize(image_size, Image.ANTIALIAS))

    one_img = Image.open('assets/1.png')
    one_img = ImageTk.PhotoImage(one_img.resize(image_size, Image.ANTIALIAS))

    two_img = Image.open('assets/2.png')
    two_img = ImageTk.PhotoImage(two_img.resize(image_size, Image.ANTIALIAS))

    three_img = Image.open('assets/3.png')
    three_img = ImageTk.PhotoImage(three_img.resize(image_size, Image.ANTIALIAS))

    four_img = Image.open('assets/4.png')
    four_img = ImageTk.PhotoImage(four_img.resize(image_size, Image.ANTIALIAS))

    five_img = Image.open('assets/5.png')
    five_img = ImageTk.PhotoImage(five_img.resize(image_size, Image.ANTIALIAS))

    six_img = Image.open('assets/6.png')
    six_img = ImageTk.PhotoImage(six_img.resize(image_size, Image.ANTIALIAS))

    seven_img = Image.open('assets/7.png')
    seven_img = ImageTk.PhotoImage(seven_img.resize(image_size, Image.ANTIALIAS))

    eight_img = Image.open('assets/8.png')
    eight_img = ImageTk.PhotoImage(eight_img.resize(image_size, Image.ANTIALIAS))

    mine_img = Image.open('assets/-1.png')
    mine_img = ImageTk.PhotoImage(mine_img.resize(image_size, Image.ANTIALIAS))

    flag_img = Image.open('assets/flag.png')
    flag_img = ImageTk.PhotoImage(flag_img.resize(image_size, Image.ANTIALIAS))

    # Get the golden numbers
    gold_one_img = Image.open('assets/1_gold.png')
    gold_one_img = ImageTk.PhotoImage(gold_one_img.resize(image_size, Image.ANTIALIAS))

    gold_two_img = Image.open('assets/2_gold.png')
    gold_two_img = ImageTk.PhotoImage(gold_two_img.resize(image_size, Image.ANTIALIAS))

    gold_three_img = Image.open('assets/3_gold.png')
    gold_three_img = ImageTk.PhotoImage(gold_three_img.resize(image_size, Image.ANTIALIAS))

    gold_four_img = Image.open('assets/4_gold.png')
    gold_four_img = ImageTk.PhotoImage(gold_four_img.resize(image_size, Image.ANTIALIAS))

    gold_five_img = Image.open('assets/5_gold.png')
    gold_five_img = ImageTk.PhotoImage(gold_five_img.resize(image_size, Image.ANTIALIAS))

    gold_six_img = Image.open('assets/6_gold.png')
    gold_six_img = ImageTk.PhotoImage(gold_six_img.resize(image_size, Image.ANTIALIAS))

    gold_seven_img = Image.open('assets/7_gold.png')
    gold_seven_img = ImageTk.PhotoImage(gold_seven_img.resize(image_size, Image.ANTIALIAS))

    gold_eight_img = Image.open('assets/8_gold.png')
    gold_eight_img = ImageTk.PhotoImage(gold_eight_img.resize(image_size, Image.ANTIALIAS))

    gold_img = Image.open('assets/mystery.png')
    gold_img = ImageTk.PhotoImage(gold_img.resize(image_size, Image.ANTIALIAS))

    img_dict[0] = null_img
    img_dict[1] = one_img
    img_dict[2] = two_img
    img_dict[3] = three_img
    img_dict[4] = four_img
    img_dict[5] = five_img
    img_dict[6] = six_img
    img_dict[7] = seven_img
    img_dict[8] = eight_img     
    img_dict[-1] = mine_img
    img_dict[9] = flag_img

    # Golden Numbers
    img_dict['1_gold'] = gold_one_img
    img_dict['2_gold'] = gold_two_img
    img_dict['3_gold'] = gold_three_img
    img_dict['4_gold'] = gold_four_img
    img_dict['5_gold'] = gold_five_img
    img_dict['6_gold'] = gold_six_img
    img_dict['7_gold'] = seven_img
    img_dict['8_gold'] = gold_eight_img 
    img_dict['mystery'] = gold_img    

    
    return img_dict

def get_smile_img(img_size=(30,25)):
    """ A function to get smiley image """
    img = Image.open('assets/smile.png')
    img = ImageTk.PhotoImage(img.resize(img_size, Image.ANTIALIAS))
    return img

def get_flag_img(img_size=(20,20)):
    """ A function to get smiley image """
    flag_img = Image.open('assets/flag.png')
    flag_img = ImageTk.PhotoImage(flag_img.resize(img_size, Image.ANTIALIAS))

    return flag_img