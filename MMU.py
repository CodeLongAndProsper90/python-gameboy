class MMU:

  def __init__ (self, cpu):
    self.inBios = True

    self.bios = [
      0x31, 0xFE, 0xFF, 0xAF, 0x21, 0xFF, 0x9F, 0x32, 0xCB, 0x7C, 0x20, 0xFB, 0x21, 0x26, 0xFF, 0x0E,
      0x11, 0x3E, 0x80, 0x32, 0xE2, 0x0C, 0x3E, 0xF3, 0xE2, 0x32, 0x3E, 0x77, 0x77, 0x3E, 0xFC, 0xE0,
      0x47, 0x11, 0x04, 0x01, 0x21, 0x10, 0x80, 0x1A, 0xCD, 0x95, 0x00, 0xCD, 0x96, 0x00, 0x13, 0x7B,
      0xFE, 0x34, 0x20, 0xF3, 0x11, 0xD8, 0x00, 0x06, 0x08, 0x1A, 0x13, 0x22, 0x23, 0x05, 0x20, 0xF9,
      0x3E, 0x19, 0xEA, 0x10, 0x99, 0x21, 0x2F, 0x99, 0x0E, 0x0C, 0x3D, 0x28, 0x08, 0x32, 0x0D, 0x20,
      0xF9, 0x2E, 0x0F, 0x18, 0xF3, 0x67, 0x3E, 0x64, 0x57, 0xE0, 0x42, 0x3E, 0x91, 0xE0, 0x40, 0x04,
      0x1E, 0x02, 0x0E, 0x0C, 0xF0, 0x44, 0xFE, 0x90, 0x20, 0xFA, 0x0D, 0x20, 0xF7, 0x1D, 0x20, 0xF2,
      0x0E, 0x13, 0x24, 0x7C, 0x1E, 0x83, 0xFE, 0x62, 0x28, 0x06, 0x1E, 0xC1, 0xFE, 0x64, 0x20, 0x06,
      0x7B, 0xE2, 0x0C, 0x3E, 0x87, 0xF2, 0xF0, 0x42, 0x90, 0xE0, 0x42, 0x15, 0x20, 0xD2, 0x05, 0x20,
      0x4F, 0x16, 0x20, 0x18, 0xCB, 0x4F, 0x06, 0x04, 0xC5, 0xCB, 0x11, 0x17, 0xC1, 0xCB, 0x11, 0x17,
      0x05, 0x20, 0xF5, 0x22, 0x23, 0x22, 0x23, 0xC9, 0xCE, 0xED, 0x66, 0x66, 0xCC, 0x0D, 0x00, 0x0B,
      0x03, 0x73, 0x00, 0x83, 0x00, 0x0C, 0x00, 0x0D, 0x00, 0x08, 0x11, 0x1F, 0x88, 0x89, 0x00, 0x0E,
      0xDC, 0xCC, 0x6E, 0xE6, 0xDD, 0xDD, 0xD9, 0x99, 0xBB, 0xBB, 0x67, 0x63, 0x6E, 0x0E, 0xEC, 0xCC,
      0xDD, 0xDC, 0x99, 0x9F, 0xBB, 0xB9, 0x33, 0x3E, 0x3c, 0x42, 0xB9, 0xA5, 0xB9, 0xA5, 0x42, 0x4C,
      0x21, 0x04, 0x01, 0x11, 0xA8, 0x00, 0x1A, 0x13, 0xBE, 0x20, 0xFE, 0x23, 0x7D, 0xFE, 0x34, 0x20,
      0xF5, 0x06, 0x19, 0x78, 0x86, 0x23, 0x05, 0x20, 0xFB, 0x86, 0x20, 0xFE, 0x3E, 0x01, 0xE0, 0x50
    ]

    self.rom = []
    self.wram = []
    self.eram = []
    self.zram = []
    self.cpu = cpu

  def rb (self, addr):
    index = addr & 0xF000

    # BIOS (256b)/ROM0
    if (index == 0x0000):
      if (self.inBios):
        if (addr < 0x0100):
          return self.bios[addr]
        elif (self.cpu.pc == 0x0100):
          self.inBios = False
      return self.rom[addr]

    # ROM0 + ROM1 (unbanked, 16k)
    elif (index <= 0x7000):
      return self.rom[addr]

    # VRAM (8k)
    elif (index <= 0x9000):
      #TODO gpu stuff
      return

    # External RAM (8k)
    elif (index <= 0xB000):
      return self.eram[addr & 0x1FFF]

    # Working RAM (8k) and Shadow
    elif (index <= 0xE000):
      return self.wram[addr & 0x1FFF]

    # Shadow, I/O, zero-page
    else:
      sIndex = addr & 0x0F00

      # Working RAM shadow
      if (sIndex <= 0xD00):
        return self.wram[addr & 0x1FFF]

      # Graphics: Object Attribute Memory
      # 160b, rest is 0
      elif (sIndex <= 0xE00):
        if (addr < 0xFEA0):
          #TODO return gpu stuff
          return
        else:
          return 0

      # Zero-page
      else:
        if (addr >= 0xFF80):
          return self.zram[addr & 0x7F]
        else: #TODO I/O stuff
          return 0

  def rw (self, addr):
    return self.rb(addr) + (self.rb(addr+1) << 8)

  def wb (self, addr, val):
    #Write 8 bits
    print "wb"

  def ww (self, addr, val):
    #Write 16 bits
    print "ww"

  def load (self, romFile):
    f = open(romFile, 'rb')
    self.rom = f.read()
    print self.rom[0]
