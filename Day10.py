from PIL import Image, ImageDraw, ImageFont
from pytesseract import pytesseract

from Day import Day


class CPU:
    def __init__(self):
        self.cycle = 0
        self.x = 1
        self.checkpoint = [20, 60, 100, 140, 180, 220]
        self.res = 0
        self.crt = []
        self.current_line = ""

    def process_instruction(self, instruction):
        self.process_cycle()
        if instruction != "noop":
            self.process_cycle()
            self.x += int(instruction[5:])

    def process_cycle(self):
        # print("Current cycle {} - {}".format(self.cycle, self.x))
        self.cycle += 1
        if 20 <= self.cycle <= 220 and (self.cycle - 20) % 40 == 0:
            self.res += self.cycle * self.x
        self.current_line += (
            "#" if self.x - 1 <= ((self.cycle - 1) % 40) <= self.x + 1 else " "
        )
        if len(self.current_line) == 40:
            self.crt.append(self.current_line)
            self.current_line = ""


class Day10(Day):
    def __init__(self):
        super().__init__(self)

    @staticmethod
    def solve(input_value):
        cpu = CPU()
        for instruction in input_value:
            cpu.process_instruction(instruction)
        return cpu.res

    @staticmethod
    def solve_2(input_value):
        cpu = CPU()
        for instruction in input_value:
            cpu.process_instruction(instruction)
        text_to_print = "\n".join(cpu.crt)
        print(text_to_print)
        path_to_tesseract = "/opt/homebrew/Cellar/tesseract/5.2.0/bin/tesseract"
        path_to_image = "output/day-10.png"
        pytesseract.tesseract_cmd = path_to_tesseract
        img = Image.new("L", (255, 125), color=255)
        draw = ImageDraw.ImageDraw(img)
        draw.text((0, 0), text_to_print)
        img.save(path_to_image)
        # Extract text from image
        text = pytesseract.image_to_string(path_to_image)
        return text

    def solution_first_star(self, input_value):
        return self.solve(input_value)

    def solution_second_star(self, input_value):
        return self.solve_2(input_value)
