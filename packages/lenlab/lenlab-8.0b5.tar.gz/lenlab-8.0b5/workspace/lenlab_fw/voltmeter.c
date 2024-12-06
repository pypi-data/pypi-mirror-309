#include "voltmeter.h"

#include "terminal.h"

#include "ti_msp_dl_config.h"

struct Voltmeter voltmeter = {
    .flag0 = false,
    .flag1 = false,
    .time = 0,
    .reply = {
        {
            .packet = {
                .label = 'L',
                .code = 'v',
                .length = 0,
            },
        },
        {
            .packet = {
                .label = 'L',
                .code = 'v',
                .length = 0,
            },
        },
    },
    .running = false,
    .reply_requested = false,
    .stop_requested = false,
    .reply_write = 0,
    .point_write = 0,
};

void voltmeter_reply(void)
{
    struct Voltmeter* const self = &voltmeter;
    struct VoltmeterReply* const reply = &self->reply[self->reply_write];

    if (!self->reply_requested)
        return;
    if (self->point_write == 0)
        return;

    reply->packet.length = self->point_write * sizeof(*reply->points);
    terminal_transmitPacket(&reply->packet);

    self->reply_requested = false;
    self->reply_write = (self->reply_write + 1) & 1;
    self->point_write = 0;

    if (self->stop_requested) {
        DL_TimerG_stopCounter(VOLT_TIMER_INST);
        self->running = false;
    }
}

void voltmeter_start(void)
{
    struct Voltmeter* const self = &voltmeter;

    if (self->running) return;

    self->reply_write = 0;
    self->point_write = 0;
    self->time = 0;

    self->reply[0].packet.arg = ARG(next);
    self->reply[1].packet.arg = ARG(next);

    self->running = true;
    self->stop_requested = false;
    DL_TimerG_startCounter(VOLT_TIMER_INST);

    self->reply_requested = true;

}

void voltmeter_next(void)
{
    struct Voltmeter* const self = &voltmeter;

    if (!self->running) return;

    self->reply_requested = true;
    voltmeter_reply();
}

void voltmeter_stop(void)
{
    struct Voltmeter* const self = &voltmeter;

    if (!self->running)
        return;

    self->reply[0].packet.arg = ARG(last);
    self->reply[1].packet.arg = ARG(last);

    self->reply_requested = true;
    self->stop_requested = true;
    voltmeter_reply();
}

void voltmeter_init(void)
{
    NVIC_EnableIRQ(ADC12_0_INST_INT_IRQN);
    NVIC_EnableIRQ(ADC12_1_INST_INT_IRQN);
}

void voltmeter_main(void)
{
    struct Voltmeter* const self = &voltmeter;
    struct VoltmeterReply* const reply = &self->reply[self->reply_write];
    struct VoltmeterPoint* const point = &reply->points[self->point_write];

    if (!self->flag0)
        return;
    if (!self->flag1)
        return;

    self->point_write = self->point_write == 7 ? 7 : (self->point_write + 1);
    // while (self->point_write == LENGTH(reply->points)) {}

    point->time = self->time;
    self->time += 1;
    point->ch1 = DL_ADC12_getMemResult(ADC12_0_INST, DL_ADC12_MEM_IDX_0);
    point->ch2 = DL_ADC12_getMemResult(ADC12_1_INST, DL_ADC12_MEM_IDX_0);

    self->flag0 = false;
    self->flag1 = false;

    voltmeter_reply();
}

void ADC12_0_INST_IRQHandler(void)
{
    switch (DL_ADC12_getPendingInterrupt(ADC12_0_INST)) {
    case DL_ADC12_IIDX_MEM0_RESULT_LOADED:
        voltmeter.flag0 = true;
        DL_GPIO_togglePins(GPIO_LEDS_USER_LED_2_PORT, GPIO_LEDS_USER_LED_2_PIN);
        voltmeter_main();
        break;
    default:
        break;
    }
}

void ADC12_1_INST_IRQHandler(void)
{
    switch (DL_ADC12_getPendingInterrupt(ADC12_1_INST)) {
    case DL_ADC12_IIDX_MEM0_RESULT_LOADED:
        voltmeter.flag1 = true;
        voltmeter_main();
        break;
    default:
        break;
    }
}
