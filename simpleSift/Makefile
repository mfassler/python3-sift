
######
######   What are we building?
######

TARGET = main

# Objects that must be built in order to link
OBJECTS = SimpleSIFT.o



######
######   Binaries and flags
######

INCDIRS = -I/usr/local/include
CFLAGS = $(INCDIRS)

LD = g++
#LDFLAGS = -L/usr/local/lib
LDLIBS = -ldl  #-lsiftgpu



######
######   Targets and Rules
######

# Default target:
.PHONY: all
all: $(TARGET)


$(TARGET): $(OBJECTS)
	$(LD) $(LDFLAGS) $(OBJECTS) -o $@ $(LDLIBS)


.PHONY: clean
clean:
	rm -f $(OBJECTS)
	rm -f $(TARGET)
