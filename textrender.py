from PIL import Image, ImageDraw, ImageFont
import random

font1="CustomFont3.ttf"  #Path to your output font file from finalfont.py
#font1 = "/home/sus/Downloads/font3.ttf"  # Regular text font
#font2 = "/home/sus/Downloads/font2.ttf"  # Additional text font
#font_err = "/home/sus/Downloads/error.ttf"  # Error font
#symbols = '/home/sus/Downloads/symbol.ttf'  # Symbol font


def apply_text_shadow(draw, text, position, font, shadow_offset=(2, 2), shadow_color='gray'):
    shadow_x, shadow_y = position[0] + shadow_offset[0], position[1] + shadow_offset[1]
    draw.text((shadow_x, shadow_y), text, font=font, fill=shadow_color)


def render_text(input_text, output_path):
    width, height = 2680, 3508
    x=50
    y=50
    pages = []
    line_spacing = 75
    paragraph_spacing = 50

    def create_new_page():
        page = Image.new("RGB", (width, height), "white")
        pages.append(page)
        return page, ImageDraw.Draw(page)

    def generate_error():
        nonlocal x,y
        err = str(random.randint(0, 10))
        font_err_size = random.randint(150, 160)
        fontt = ImageFont.truetype(font_err, size=font_err_size)
        bbox = draw.textbbox((0, 0), err, font=fontt)
        err_width, err_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text((x, y), err, font=fontt, fill='blue')
        x += err_width + random.randint(-2, 0)
        if x > 2630:
            x = 50 + random.randint(10, 30)
            y += err_height + random.randint(10, 20)

    
    image, draw = create_new_page()
    paragraphs = input_text.split("\n")

    for paragraph in paragraphs:
        words = paragraph.split(" ")

        for word in words:
            font_size = random.randint(100, 100)
            font = ImageFont.truetype(font1, size=font_size)
            bbox = draw.textbbox((0, 0), word, font=font)
            word_width, word_height = bbox[2] - bbox[0], bbox[3] - bbox[1]

            
            word_width -= 10 * len(word)

            if x + word_width > 2630:
                x = 50 + random.randint(0, 50)
                #y += word_height + line_spacing
                y += line_spacing


            if y + word_height > 3400:
                image, draw = create_new_page()
                x, y = 50, 50

            for char in word:
                #y_offset = random.randint(-3, 3)
                bbox = draw.textbbox((0, 0), char, font=font)
                char_width = bbox[2] - bbox[0]
                apply_text_shadow(draw, char, (x, y ), font)
                draw.text((x, y ), char, font=font, fill='blue')
                x += char_width - 10

            space_bbox = draw.textbbox((0, 0), " ", font=font)
            space_width = space_bbox[2] - space_bbox[0]
            x += space_width + random.randint(1, 90)

            if random.randint(0, 500) == 11:
                #generate_error()

        x = 50
        y += word_height + paragraph_spacing

    if len(pages) == 1:
        pages[0].save(output_path)
        print(f"Output saved to {output_path}")
    else:
        pdf_output = output_path.replace(".png", ".pdf")
        pages[0].save(pdf_output, save_all=True, append_images=pages[1:])
        print(f"Output saved as multi-page PDF to {pdf_output}")


# Test input 
input_text = '''apple ideal for shorter multiline strings that are directly embedded in your codebackslashes suitable for specific scenarios where you need more control over line breaks and formatting reading from a file best for extremely large strings or when you want to separate the string from the code for better readability and maintainability
the rapid advancement of technology has transformed neary every aspect of modern life from how we connect to how we work learn and entertain ourselves in just a few decades innovations like smartphones artificial intelligence and highspeed internet have reshaped the global landscape creating opportunities and challenges for example the rise of remote work has allowed individuals to collaborate across continents breaking geographical barriers and fostering cultural exchange however it has also blurred the boundaries between personal and professional life raising concerns about burnout and worklife balance
education has similarly evolved with online platforms providing access to vast resources and learning tools yet this digital shift has highlighted disparities in access to technology leaving some communities behind social media once a tool for connection now influences public opinion and even elections underscoring the need for ethical considerations in its use the digital divide and the power of technology to shape societal narratives emphasize the importance of equitable access and responsible usage
as these technologies continue to evolve society must address questions about privacy data security and ethical responsibility the future holds immense potential for breakthroughs in areas like medicine renewable energy and space exploration however harnessing this potential requires a collective effort to ensure that progress benefits all of humanity while mitigating unintended consequences balancing innovation with responsibility remains one of the defining challenges of our time
certainly heres a text separated into three paragraphs the importance of mental health awareness has grown significantly in recent years as society becomes more open to discussing emotional wellbeing individuals are encouraged to prioritize their mental health just as they would their physical health this shift in perspective is crucial as mental health issues affect millions globally often leading to debilitating conditions if left unaddressed by fostering an environment where mental health conversations are normalized we can reduce stigma and encourage those struggling to seek help
education plays a vital role in promoting mental health awareness schools and workplaces are increasingly integrating mental health education into their programs providing resources and support systems for individuals to understand and manage their mental wellbeing workshops seminars and counseling services are essential components of this educational approach equipping people with the tools they need to cope with stress anxiety and other mental health challenges
ultimately the goal is to create a supportive community that values mental health as an integral part of overall wellbeing by prioritizing mental health awareness and education we can empower individuals to take charge of their emotional health this proactive approach not only benefits individuals but also fosters healthier relationships and communities paving the way for a brighter future for everyone feel free to ask if you need any modifications or additional content'''
render_text(input_text, "Output.png")
