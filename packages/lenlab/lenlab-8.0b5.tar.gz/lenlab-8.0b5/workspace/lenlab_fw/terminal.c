#include "terminal.h"

#include "memory.h"
#include "version.h"
#include "voltmeter.h"

#include "ti_msp_dl_config.h"

// knock
static const struct Packet knock = { .label = 'L', .code = 'k', .length = 0, .arg = ARG(nock) }; // knock
// memory
static const struct Packet mi28K = { .label = 'L', .code = 'm', .length = 0, .arg = ARG(i28K) }; // init 28K
static const struct Packet mg28K = { .label = 'L', .code = 'm', .length = 0, .arg = ARG(g28K) }; // get 28K
// voltmeter
static const struct Packet vstrt = { .label = 'L', .code = 'v', .length = 0, .arg = ARG(strt) }; // start
static const struct Packet vnext = { .label = 'L', .code = 'v', .length = 0, .arg = ARG(next) }; // next
static const struct Packet vstop = { .label = 'L', .code = 'v', .length = 0, .arg = ARG(stop) }; // stop
// oscilloscope

struct Terminal terminal = { .rx_flag = false, .tx_flag = false, .rx_stalled = false };

static void terminal_receive(uint32_t address, uint32_t size)
{
    while (terminal.rx_flag) { }
    terminal.rx_flag = true;
    terminal.rx_stalled = false;

    DL_DMA_setDestAddr(DMA, DMA_CH_RX_CHAN_ID, address);
    DL_DMA_setTransferSize(DMA, DMA_CH_RX_CHAN_ID, size);
    DL_DMA_enableChannel(DMA, DMA_CH_RX_CHAN_ID);
}

static void terminal_receivePacket(struct Packet* packet)
{
    terminal_receive((uint32_t)packet, sizeof(*packet));
}

void terminal_receiveCommand(void)
{
    terminal_receivePacket(&terminal.cmd);
}

static void terminal_transmit(uint32_t address, uint32_t size)
{
    while (terminal.tx_flag) { }
    terminal.tx_flag = true;

    DL_DMA_setSrcAddr(DMA, DMA_CH_TX_CHAN_ID, address);
    DL_DMA_setTransferSize(DMA, DMA_CH_TX_CHAN_ID, size);
    DL_DMA_enableChannel(DMA, DMA_CH_TX_CHAN_ID);
}

void terminal_transmitPacket(const struct Packet* packet)
{
    terminal_transmit((uint32_t)packet, packet->length + 8);
}

void terminal_transmitReply(void)
{
    terminal_transmitPacket(&terminal.rpl);
}

void terminal_init(void)
{
    NVIC_EnableIRQ(TERMINAL_UART_INST_INT_IRQN);

    DL_DMA_setSrcAddr(DMA, DMA_CH_RX_CHAN_ID, (uint32_t)&TERMINAL_UART_INST->RXDATA);
    DL_DMA_setDestAddr(DMA, DMA_CH_TX_CHAN_ID, (uint32_t)&TERMINAL_UART_INST->TXDATA);

    terminal_receiveCommand();
}

void terminal_tick(void)
{
    if (DL_DMA_isChannelEnabled(DMA, DMA_CH_RX_CHAN_ID)) { // RX active
        if (DL_DMA_getTransferSize(DMA, DMA_CH_RX_CHAN_ID) < sizeof(struct Packet)) { // some bytes have arrived
            if (terminal.rx_stalled) { // reset RX
                DL_DMA_disableChannel(DMA, DMA_CH_RX_CHAN_ID);
                terminal.rx_flag = false;
                terminal_receiveCommand();
            } else {
                terminal.rx_stalled = true;
            }
        }
    }
}

static void terminal_init28K(void)
{
    uint32_t* restrict payload = (uint32_t*)&memory.payload;

    memory.packet.label = 'L';
    memory.packet.code = 'm';
    memory.packet.length = sizeof(memory.payload);
    memory.packet.arg = mg28K.arg; // get 28K

    DL_CRC_setSeed32(CRC, CRC_SEED);
    for (uint32_t i = 0; i < sizeof(memory.payload) / sizeof(*payload); i++) {
        DL_CRC_feedData32(CRC, 0);
        payload[i] = DL_CRC_getResult32(CRC);
    }
}

static void terminal_version(void)
{
    const char version[] = VERSION;
    uint8_t i = 0;
    uint8_t *buffer = (uint8_t *) &terminal.rpl.arg;

    terminal.rpl.label = 'L';
    terminal.rpl.code = 'k';
    terminal.rpl.length = 0;

    if (version[i]) i++;
    if (version[i]) i++;

    buffer[0] = version[i];
    if (version[i]) i++;
    buffer[1] = version[i];
    if (version[i]) i++;
    buffer[2] = version[i];
    if (version[i]) i++;
    buffer[3] = version[i];

    terminal_transmitReply();
}

void terminal_main(void)
{
    if (!terminal.rx_flag) {
        if (terminal.cmd.label == 'L' && terminal.cmd.length == 0) {
            switch (terminal.cmd.code) {
            case 'k':
                if (terminal.cmd.arg == knock.arg) {
                    terminal_version();
                }
                break;
            case 'm':
                if (terminal.cmd.arg == mi28K.arg) { // init 28K
                    terminal_init28K();
                    terminal_transmitPacket(&mi28K);
                } else if (terminal.cmd.arg ==  mg28K.arg) { // get 28K
                    terminal_transmitPacket(&memory.packet);
                }
                break;
            case 'v':
                if (terminal.cmd.arg == vstrt.arg) {
                    voltmeter_start();
                } else if (terminal.cmd.arg == vnext.arg) {
                    voltmeter_next();
                } else if (terminal.cmd.arg == vstop.arg) {
                    voltmeter_stop();
                }
                break;
            }
        }
        terminal_receiveCommand();
    }
}

void TERMINAL_UART_INST_IRQHandler(void)
{
    switch (DL_UART_Main_getPendingInterrupt(TERMINAL_UART_INST)) {
    case DL_UART_MAIN_IIDX_DMA_DONE_TX:
        terminal.tx_flag = false;
        break;
    case DL_UART_MAIN_IIDX_DMA_DONE_RX:
        terminal.rx_flag = false;
        break;
    default:
        break;
    }
}
