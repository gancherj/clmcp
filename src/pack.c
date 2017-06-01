#include <stdint.h>
#include <stdbool.h>

inline void lmcp_pack_bool(bool b, uint8_t* head) {
    if (b == true)
        *head = (uint8_t)1;
    else
        *head = (uint8_t)0;
    head++;
}

inline void lmcp_pack_byte(uint8_t i, uint8_t* head) {
    *head = i;
    head++;
}

inline void lmcp_pack_char(char c, uint8_t* head) {
    *head = c;
    head++;
}

inline void lmcp_pack_int16(uint16_t i, uint8_t* head) {
    *(uint16_t

