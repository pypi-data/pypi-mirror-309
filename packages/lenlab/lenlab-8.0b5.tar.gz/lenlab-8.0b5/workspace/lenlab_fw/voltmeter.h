#ifndef VOLTMETER_H
#define VOLTMETER_H

#include "packet.h"

struct VoltmeterPoint {
    uint32_t time;
    uint16_t ch1;
    uint16_t ch2;
};

struct VoltmeterReply {
    struct Packet packet;
    struct VoltmeterPoint points[8];
};

struct Voltmeter {
    volatile bool flag0;
    volatile bool flag1;
    volatile uint32_t time;
    struct VoltmeterReply reply[2];
    volatile bool running;
    volatile bool reply_requested;
    volatile bool stop_requested;
    volatile uint8_t reply_write;
    volatile uint8_t point_write;
};

void voltmeter_start(void);

void voltmeter_next(void);

void voltmeter_stop(void);

void voltmeter_init(void);

#endif
